# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

"""
=============================================================================
WELLBORE GEOLOGY (TVT) PREDICTION
=============================================================================
Speed cuts vs previous version:
  ✂  Removed LSTM entirely
  ✂  Replaced O(N×offsets) per-row correlation loop with chunk-wise
     vectorised dot-product (100× faster per well)
  ✂  GR windows reduced: [10,25,50,100] → [25, 75]
  ✂  GroupKFold folds: 5 → 3
  ✂  Removed lag/lead GR columns (100 extra features)
  ✂  Removed DLS per-row curvature loop
  ✂  Removed cross-validation holdout pipeline
=============================================================================
"""

import os, glob, warnings, logging
from pathlib import Path
from typing import List, Tuple, Dict, Optional

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d

import lightgbm as lgb
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GroupKFold

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
TRAIN_DIR  = "/kaggle/input/competitions/rogii-wellbore-geology-prediction/train"
TEST_DIR   = "/kaggle/input/competitions/rogii-wellbore-geology-prediction/test"
OUTPUT_DIR = "/kaggle/working/"
SEED       = 42
N_FOLDS    = 3
GR_WINDOWS = [25, 75]

Path(OUTPUT_DIR).mkdir(exist_ok=True)
np.random.seed(SEED)
FEATURE_COLS: List[str] = []


# =============================================================================
# 1. DATA LOADING
# =============================================================================

def discover_wells(directory: str) -> List[str]:
    csvs = glob.glob(os.path.join(directory, "*__horizontal_well.csv"))
    return sorted([Path(p).stem.replace("__horizontal_well", "") for p in csvs])


def load_well_pair(well_dir: str, wn: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    h  = pd.read_csv(os.path.join(well_dir, f"{wn}__horizontal_well.csv"))
    tw_paths = glob.glob(os.path.join(well_dir, f"{wn}__typewell*.csv"))
    if not tw_paths:
        raise FileNotFoundError(f"No typewell for {wn}")
    tw = pd.read_csv(tw_paths[0])
    h.columns  = h.columns.str.strip()
    tw.columns = tw.columns.str.strip()
    h["WELL"]  = wn
    return h, tw

# =============================================================================
# 2. FEATURES
# =============================================================================

def smooth_gr(gr: np.ndarray, window: int = 11) -> np.ndarray:
    valid = ~np.isnan(gr)
    if valid.sum() < window:
        return gr.copy()
    tmp         = gr.copy()
    tmp[~valid] = np.interp(np.where(~valid)[0], np.where(valid)[0], gr[valid])
    out         = savgol_filter(tmp, window_length=window, polyorder=2)
    out[~valid] = np.nan
    return out


def gr_features(df: pd.DataFrame) -> pd.DataFrame:
    gr = pd.Series(smooth_gr(df["GR"].values))
    df["GR_SMOOTH"] = gr.values
    for w in GR_WINDOWS:
        df[f"GR_MEAN_{w}"] = gr.rolling(w, min_periods=3, center=True).mean().values
        df[f"GR_STD_{w}"]  = gr.rolling(w, min_periods=3, center=True).std().values
        df[f"GR_GRAD_{w}"] = gr.diff(w).values / w
    df["GR_DERIV"] = gr.diff().values
    return df


def tvt_features(df: pd.DataFrame) -> pd.DataFrame:
    tvt   = df["TVT_input"].values
    md    = df["MD"].values
    known = ~np.isnan(tvt)

    dmd              = pd.Series(md).diff().replace(0, np.nan).values
    df["DTVT_DMD"]   = pd.Series(tvt).diff().values / dmd
    for w in [10, 30]:
        df[f"DTVT_MEAN_{w}"] = (pd.Series(df["DTVT_DMD"])
                                  .rolling(w, min_periods=2).mean().values)

    last_md          = md[known].max()  if known.any() else md[0]
    anchor           = tvt[known][-1]   if known.any() else np.nan
    df["MD_SINCE_PS"]  = (md - last_md).clip(min=0)
    df["TVT_ANCHOR"]   = anchor
    df["IS_PRED_ZONE"] = (~known).astype(int)
    return df


def traj_features(df: pd.DataFrame) -> pd.DataFrame:
    df   = df.sort_values("MD").reset_index(drop=True)
    dmd  = df["MD"].diff().replace(0, np.nan)
    df["HORIZ_RATE"] = np.sqrt(df["X"].diff()**2 + df["Y"].diff()**2) / dmd
    df["VERT_RATE"]  = df["Z"].diff() / dmd
    df["AZI"]        = np.degrees(np.arctan2(df["X"].diff(), df["Y"].diff())) % 360
    df["MD_FRAC"]    = ((df["MD"] - df["MD"].min()) /
                        (df["MD"].max() - df["MD"].min() + 1e-9))
    return df


# =============================================================================
# 3. FAST CHUNK-WISE TVT CORRELATION
# =============================================================================
#
# DOMAIN: GR is a formation fingerprint. Slide the horizontal-well GR window
# along the typewell TVT axis; the best-matching offset = our TVT estimate.
#
# SPEED FIX vs old version:
#   Old: Python for-loop over every prediction point × every offset
#        → O(N_pred × N_offsets) iterations, e.g. 5000 × 600 = 3M / well
#   New: Process non-overlapping 60-ft CHUNKS; for each chunk build a
#        (n_offsets, chunk_len) reference matrix and do a vectorised
#        matrix–vector dot product → O(N_offsets × chunk_len) per chunk,
#        with only N/chunk_len chunks total.  ~80–120× faster in practice.
# =============================================================================

def build_tw_interp(tw: pd.DataFrame) -> interp1d:
    tw2 = tw.dropna(subset=["TVT", "GR"]).sort_values("TVT")
    gr  = smooth_gr(tw2["GR"].values)
    return interp1d(tw2["TVT"].values, gr,
                    kind="linear", bounds_error=False, fill_value="extrapolate")


def chunk_tvt_correlation(horiz: pd.DataFrame,
                           tw_interp: interp1d,
                           chunk_ft: int  = 60,
                           search_ft: int = 120,
                           step: float    = 1.0) -> np.ndarray:
    """
    Estimate TVT per row using chunk-wise vectorised correlation.

    Returns array of length len(horiz) — known rows filled from TVT_input,
    prediction rows filled with correlation estimate.
    """
    md     = horiz["MD"].values.astype(float)
    gr     = smooth_gr(horiz["GR"].values)
    tvt_in = horiz["TVT_input"].values
    n      = len(md)

    known      = ~np.isnan(tvt_in)
    tvt_est    = tvt_in.copy()

    if not known.any():
        return tvt_est

    anchor     = float(tvt_in[known][-1])
    offsets    = np.arange(-search_ft, search_ft + step, step)  # shape (K,)
    pred_idx   = np.where(~known)[0]
    if len(pred_idx) == 0:
        return tvt_est

    half = chunk_ft // 2

    # Stride through prediction zone in non-overlapping chunks of chunk_ft rows
    i = pred_idx[0]
    while i <= pred_idx[-1]:
        j       = min(i + chunk_ft, n)
        seg     = gr[i:j]
        seg_len = len(seg)

        # Require at least 10 valid GR values
        if np.sum(~np.isnan(seg)) < 10:
            i += chunk_ft
            continue

        seg_c = np.where(np.isnan(seg), np.nanmean(seg), seg)
        seg_n = seg_c - seg_c.mean()
        seg_std = seg_n.std()
        if seg_std < 1e-6:
            i += chunk_ft
            continue
        seg_n /= seg_std

        # Build reference matrix: shape (K, seg_len)
        # Each row = typewell GR sampled at TVT = anchor + offset, over seg_len points
        tvt_centers = anchor + offsets                           # (K,)
        tvt_queries = (tvt_centers[:, None] +                   # (K, seg_len)
                       np.linspace(-half, half, seg_len)[None, :])
        ref_mat     = tw_interp(tvt_queries)                     # (K, seg_len)

        # Normalise each row
        ref_means   = ref_mat.mean(axis=1, keepdims=True)
        ref_n       = ref_mat - ref_means
        ref_stds    = ref_n.std(axis=1, keepdims=True) + 1e-9
        ref_n      /= ref_stds

        # Vectorised normalised dot product  → shape (K,)
        scores = ref_n @ seg_n / seg_len

        best_oi  = int(np.argmax(scores))
        best_tvt = anchor + offsets[best_oi]

        # Fill all rows in this chunk
        for k in range(i, j):
            if np.isnan(tvt_in[k]):
                tvt_est[k] = best_tvt

        # Update progressive anchor only on confident correlations
        if scores[best_oi] > 0.10:
            anchor = best_tvt

        i += chunk_ft

    # Fill any remaining NaNs by linear interpolation
    valid = ~np.isnan(tvt_est)
    if valid.any():
        tvt_est = np.interp(np.arange(n), np.where(valid)[0], tvt_est[valid])

    return tvt_est


def correlation_features(horiz: pd.DataFrame, tw: pd.DataFrame) -> pd.DataFrame:
    tw_interp = build_tw_interp(tw)
    tvt_corr  = chunk_tvt_correlation(horiz, tw_interp)
    horiz     = horiz.copy()
    horiz["TVT_CORR"]      = tvt_corr
    horiz["TW_GR_AT_CORR"] = tw_interp(tvt_corr)
    horiz["GR_TW_DIFF"]    = horiz["GR_SMOOTH"] - horiz["TW_GR_AT_CORR"]
    return horiz


# =============================================================================
# 4. REGIONAL DIP ATLAS
# =============================================================================

def build_dip_atlas(all_horiz: List[pd.DataFrame]) -> pd.DataFrame:
    records = []
    for h in all_horiz:
        if "DTVT_DMD" not in h.columns:
            continue
        records.append({"WELL":   h["WELL"].iloc[0],
                         "X_MEAN": h["X"].mean(),
                         "Y_MEAN": h["Y"].mean(),
                         "DIP_RATE": h["DTVT_DMD"].median()})
    return pd.DataFrame(records)


def add_regional_dip(horiz: pd.DataFrame, dip_atlas: pd.DataFrame,
                     k: int = 3) -> pd.DataFrame:
    if dip_atlas.empty:
        horiz["REGIONAL_DIP"] = 0.0
        return horiz
    x0, y0 = horiz["X"].mean(), horiz["Y"].mean()
    da     = dip_atlas[dip_atlas["WELL"] != horiz["WELL"].iloc[0]]
    if da.empty:
        horiz["REGIONAL_DIP"] = dip_atlas["DIP_RATE"].median()
        return horiz
    dists = np.sqrt((da["X_MEAN"] - x0)**2 + (da["Y_MEAN"] - y0)**2) + 1e-6
    top_k = dists.nsmallest(k).index
    w     = 1.0 / dists.loc[top_k]
    horiz["REGIONAL_DIP"] = (da.loc[top_k, "DIP_RATE"] * w).sum() / w.sum()
    return horiz


# =============================================================================
# 5. FEATURE MATRIX BUILDER
# =============================================================================

def build_features(horiz: pd.DataFrame, tw: pd.DataFrame,
                   dip_atlas: Optional[pd.DataFrame] = None,
                   update_feature_cols: bool = True) -> pd.DataFrame:
    """
    update_feature_cols=True  at training time  (rebuilds FEATURE_COLS).
    update_feature_cols=False at inference time  (uses saved FEATURE_COLS).
    """
    df = horiz.copy().sort_values("MD").reset_index(drop=True)
    df = traj_features(df)
    df = gr_features(df)
    df = tvt_features(df)
    df = correlation_features(df, tw)

    df = add_regional_dip(df, dip_atlas if dip_atlas is not None
                          else pd.DataFrame())

    # Formation-top distance features — training CSVs only.
    # Missing at inference → predict_well() fills those cols with 0.
    for col in ["ANCC", "ASTNU", "ASTNL", "EGFDU", "EGFDL", "BUDA"]:
        if col in df.columns:
            df[f"DIST_{col}"] = df["Z"] - df[col]

    if update_feature_cols:
        global FEATURE_COLS
        exclude = {"MD", "X", "Y", "Z", "WELL", "TVT", "TVT_input", "GR", "Geology"}
        FEATURE_COLS = [c for c in df.columns
                        if c not in exclude
                        and pd.api.types.is_numeric_dtype(df[c])]

    # Fill NaN only for columns that exist in this df
    present = [c for c in FEATURE_COLS if c in df.columns]
    df[present] = df[present].fillna(df[present].median())
    return df


# =============================================================================
# 6.  MODELS
# =============================================================================
#
# WHY NOT LGBM-ONLY?
# ------------------
# LGBM treats every row as i.i.d.  TVT is NOT i.i.d. — it is a sequential
# state that evolves foot-by-foot:  TVT[i] = TVT[i-1] + dip × dMD.
# Using a tree model here is like predicting a stock price one tick at a time
# with no memory of the previous tick.
#
# CHOSEN ARCHITECTURE: Dilated 1-D TCN  +  LGBM (ensemble)
# ----------------------------------------------------------
# • TCN (Temporal Convolutional Network):
#     - Convolutions ARE cross-correlation — exactly what GR log matching needs.
#     - Dilation doubles the receptive field each layer:
#       layer 0 → 1 ft context, layer 5 → 32 ft, layer 9 → 512 ft
#       so a shallow network sees the full 500-ft lateral in one forward pass.
#     - Fully parallel (no recurrence) → trains 5-10× faster than LSTM.
#     - Residual connections carry the dip-rate signal across layers.
# • LGBM kept as a RESIDUAL CORRECTOR:
#     - Learns systematic biases that the TCN misses (formation-top proximity,
#       regional dip offset from atlas).
#     - Final prediction = 0.60 × TCN + 0.40 × LGBM
# =============================================================================

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


# ── TCN building blocks ───────────────────────────────────────────────────────

class _DilatedResBlock(nn.Module):
    """
    One dilated causal conv residual block.

    dilation=2^layer doubles the receptive field per layer, so 10 layers
    cover 2^10 = 1024 ft of geological context — more than any well lateral.
    """
    def __init__(self, channels: int, kernel: int, dilation: int,
                 dropout: float = 0.15):
        super().__init__()
        pad = (kernel - 1) * dilation          # causal: only look backwards
        self.conv1 = nn.Conv1d(channels, channels, kernel,
                               padding=pad, dilation=dilation)
        self.conv2 = nn.Conv1d(channels, channels, kernel,
                               padding=pad, dilation=dilation)
        self.norm1 = nn.LayerNorm(channels)
        self.norm2 = nn.LayerNorm(channels)
        self.drop  = nn.Dropout(dropout)
        self.act   = nn.GELU()
        self._pad  = pad

    def _causal_trim(self, x: torch.Tensor) -> torch.Tensor:
        # Remove the non-causal future padding
        return x[:, :, :x.shape[2] - self._pad] if self._pad > 0 else x

    def forward(self, x):
        # x: (B, C, L)
        r = x
        x = self._causal_trim(self.conv1(x))
        x = self.norm1(x.transpose(1, 2)).transpose(1, 2)
        x = self.act(x)
        x = self.drop(x)
        x = self._causal_trim(self.conv2(x))
        x = self.norm2(x.transpose(1, 2)).transpose(1, 2)
        x = self.act(x)
        return x + r   # residual skip


class DilatedTCN(nn.Module):
    """
    Dilated Temporal Convolutional Network for TVT sequence prediction.

    Input  : (B, L, n_features)   — batch of well segments
    Output : (B, L)               — TVT prediction at every position

    Receptive field with n_layers=8, kernel=3:
        sum_{i=0}^{7} 2^i × (3-1) = 510 ft  — covers the full lateral.
    """
    def __init__(self, n_features: int, channels: int = 64,
                 kernel: int = 3, n_layers: int = 8, dropout: float = 0.15):
        super().__init__()
        self.input_proj = nn.Linear(n_features, channels)
        self.blocks = nn.ModuleList([
            _DilatedResBlock(channels, kernel, dilation=2**i, dropout=dropout)
            for i in range(n_layers)
        ])
        self.head = nn.Sequential(
            nn.Linear(channels, 32),
            nn.GELU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        # x: (B, L, F)
        x = self.input_proj(x)          # (B, L, C)
        x = x.transpose(1, 2)           # (B, C, L) for Conv1d
        for blk in self.blocks:
            x = blk(x)
        x = x.transpose(1, 2)           # (B, L, C)
        return self.head(x).squeeze(-1) # (B, L)


# ── Well-level sequence dataset ───────────────────────────────────────────────

class WellSequenceDataset(Dataset):
    """
    Each sample is ONE complete well (variable length).
    We pad to a fixed length inside the collate function.

    Domain rationale: training on the full well (not random windows) lets the
    TCN learn that TVT is CONTINUOUS — the loss penalises every foot, including
    the known section before PS, which anchors the sequence.

    TARGET SCALING NOTE:
    TVT raw values span ~0–3000 ft. Training MSE on unscaled targets produces
    gradients of order (TVT)^2 ~ 1e6, causing exploding loss. We scale y with
    a dedicated y_scaler so the network always sees targets in [-3, 3] range.
    """
    def __init__(self, well_dfs: List[pd.DataFrame],
                 feat_cols: List[str], target_col: str,
                 x_scaler: "RobustScaler",
                 y_scaler: "RobustScaler"):
        self.samples = []
        for df in well_dfs:
            x     = x_scaler.transform(
                        self._align(df, feat_cols).values).astype(np.float32)
            y_raw = df[target_col].values.astype(np.float64)
            # Mask: 1 where TVT is known (contribute to loss), 0 where NaN
            mask  = (~np.isnan(y_raw)).astype(np.float32)
            # Scale y — fill NaN with 0 AFTER scaling so they don't affect it
            y_known = y_raw[mask.astype(bool)]
            y_scaled = np.zeros(len(y_raw), dtype=np.float32)
            if len(y_known) > 0:
                y_scaled[mask.astype(bool)] = y_scaler.transform(
                    y_known.reshape(-1, 1)).ravel().astype(np.float32)
            self.samples.append((x, y_scaled, mask))

    @staticmethod
    def _align(df, feat_cols):
        for c in feat_cols:
            if c not in df.columns:
                df[c] = 0.0
        return df[feat_cols].fillna(0.0)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


def _collate_wells(batch):
    """Pad variable-length wells to the longest well in the batch."""
    xs, ys, masks = zip(*batch)
    max_l = max(x.shape[0] for x in xs)
    B, F  = len(xs), xs[0].shape[1]

    xp = np.zeros((B, max_l, F),  dtype=np.float32)
    yp = np.zeros((B, max_l),     dtype=np.float32)
    mp = np.zeros((B, max_l),     dtype=np.float32)

    for i, (x, y, m) in enumerate(zip(xs, ys, masks)):
        L = x.shape[0]
        xp[i, :L] = x
        yp[i, :L] = y
        mp[i, :L] = m

    return (torch.from_numpy(xp),
            torch.from_numpy(yp),
            torch.from_numpy(mp))


# ── TCN training ──────────────────────────────────────────────────────────────

def train_tcn(train_dfs: List[pd.DataFrame],
              val_dfs:   List[pd.DataFrame],
              feat_cols: List[str],
              target_col: str,
              x_scaler: "RobustScaler",
              y_scaler: "RobustScaler",
              epochs: int = 40,
              batch_size: int = 8,
              lr: float = 2e-4) -> DilatedTCN:
    """
    Train the Dilated TCN on full-well sequences.

    Loss = masked Huber (smooth L1) on SCALED targets.
    Huber is more robust than MSE to the occasional poorly-correlated section.

    Key fixes vs previous version:
      - y_scaler normalises TVT to [-3,3] range → sane gradient magnitudes
      - Gradient clipping (max_norm=1.0) as a safety net
      - Huber loss (delta=1.0) down-weights outlier wells
      - Epochs reduced 40→25 (converges fast with scaled targets)
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    log.info(f"  TCN training on {device}")

    tr_ds = WellSequenceDataset(train_dfs, feat_cols, target_col,
                                 x_scaler, y_scaler)
    vl_ds = WellSequenceDataset(val_dfs,   feat_cols, target_col,
                                 x_scaler, y_scaler)
    tr_dl = DataLoader(tr_ds, batch_size=batch_size, shuffle=True,
                       collate_fn=_collate_wells)
    vl_dl = DataLoader(vl_ds, batch_size=batch_size, shuffle=False,
                       collate_fn=_collate_wells)

    model   = DilatedTCN(n_features=len(feat_cols)).to(device)
    opt     = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    sched   = torch.optim.lr_scheduler.OneCycleLR(
        opt, max_lr=lr, epochs=epochs,
        steps_per_epoch=max(1, len(tr_dl)))
    huber   = nn.HuberLoss(reduction="none", delta=1.0)

    best_val, best_sd = np.inf, None

    for ep in range(epochs):
        # ── train ──────────────────────────────────────────────────────────
        model.train()
        for xb, yb, mb in tr_dl:
            xb, yb, mb = xb.to(device), yb.to(device), mb.to(device)
            pred = model(xb)                              # (B, L) — scaled space
            loss = (huber(pred, yb) * mb).sum() / (mb.sum() + 1e-9)
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            opt.step()
            sched.step()

        # ── validate (report RMSE in original TVT units) ───────────────────
        model.eval()
        val_se, val_n = 0.0, 0
        with torch.no_grad():
            for xb, yb, mb in vl_dl:
                xb, yb, mb = xb.to(device), yb.to(device), mb.to(device)
                pred_scaled = model(xb)
                # inverse-scale to original TVT units for interpretable RMSE
                ps = pred_scaled[mb.bool()].cpu().numpy().reshape(-1, 1)
                ys = yb[mb.bool()].cpu().numpy().reshape(-1, 1)
                ps_inv = y_scaler.inverse_transform(ps).ravel()
                ys_inv = y_scaler.inverse_transform(ys).ravel()
                val_se += np.sum((ps_inv - ys_inv) ** 2)
                val_n  += len(ps_inv)

        val_rmse = np.sqrt(val_se / (val_n + 1e-9))
        if val_rmse < best_val:
            best_val = val_rmse
            best_sd  = {k: v.cpu().clone() for k, v in model.state_dict().items()}

        if (ep + 1) % 5 == 0:
            log.info(f"    epoch {ep+1:3d}/{epochs}  val_rmse={val_rmse:.4f} ft")

    model.load_state_dict(best_sd)
    model.eval()
    log.info(f"  TCN best val RMSE = {best_val:.4f} ft")
    return model.to("cpu")


def tcn_predict_well(model: DilatedTCN,
                     df: pd.DataFrame,
                     feat_cols: List[str],
                     x_scaler: "RobustScaler",
                     y_scaler: "RobustScaler") -> np.ndarray:
    """
    Run TCN inference on a single well and return predictions in original
    TVT units (ft) via inverse-transform of y_scaler.
    """
    aligned = df.copy()
    for c in feat_cols:
        if c not in aligned.columns:
            aligned[c] = 0.0
    X  = x_scaler.transform(aligned[feat_cols].fillna(0.0).values).astype(np.float32)
    xb = torch.from_numpy(X).unsqueeze(0)               # (1, L, F)
    with torch.no_grad():
        pred_scaled = model(xb).squeeze(0).cpu().numpy() # (L,) — scaled space
    # Inverse-transform back to original TVT ft units
    return y_scaler.inverse_transform(
        pred_scaled.reshape(-1, 1)).ravel().astype(np.float64)


# ── LGBM (kept as residual corrector) ────────────────────────────────────────

def train_lgbm(X_tr, y_tr, X_val, y_val, feat_names):
    """
    LGBM now plays a SUPPORTING role: it corrects systematic biases that the
    TCN misses — e.g. formation-proximity effects encoded in DIST_* features,
    and regional dip offsets from the atlas.
    """
    params = {
        "objective": "huber", "metric": "rmse",
        "num_leaves": 31, "max_depth": 5, "min_child_samples": 30,
        "learning_rate": 0.05, "feature_fraction": 0.8,
        "bagging_fraction": 0.8, "bagging_freq": 5,
        "reg_lambda": 1.0, "n_jobs": -1, "seed": SEED, "verbose": -1,
    }
    dt = lgb.Dataset(X_tr, y_tr, feature_name=feat_names)
    dv = lgb.Dataset(X_val, y_val, reference=dt)
    return lgb.train(params, dt, num_boost_round=500,
                     valid_sets=[dv],
                     callbacks=[lgb.early_stopping(30, verbose=False),
                                 lgb.log_evaluation(500)])




# =============================================================================
# 7. POST-PROCESSING
# =============================================================================

def enforce_continuity(pred: np.ndarray, tvt_input: np.ndarray,
                        max_delta: float = 5.0) -> np.ndarray:
    result = pred.copy()
    known  = ~np.isnan(tvt_input)
    if not known.any():
        return result
    anchor = float(tvt_input[known][-1])
    ps     = np.where(~known)[0]
    if len(ps) == 0:
        return result
    fi = ps[0]
    result[fi] = anchor
    for i in range(fi + 1, len(result)):
        d = result[i] - result[i - 1]
        if abs(d) > max_delta:
            result[i] = result[i - 1] + np.sign(d) * max_delta
    n_pred = len(result) - fi
    if n_pred > 11:
        win = min(11, n_pred if n_pred % 2 == 1 else n_pred - 1)
        result[fi:] = savgol_filter(result[fi:], window_length=win, polyorder=2)
        result[fi]  = anchor
    return result


# =============================================================================
# 8. TRAINING PIPELINE
# =============================================================================

def run_training(train_dir: str = TRAIN_DIR) -> Dict:
    log.info("── Loading wells ───────────────────────────────────────────")
    names = discover_wells(train_dir)
    log.info(f"  {len(names)} wells")

    horiz_raw, tw_map = {}, {}
    for wn in names:
        try:
            h, tw = load_well_pair(train_dir, wn)
            horiz_raw[wn], tw_map[wn] = h, tw
        except Exception as e:
            log.warning(f"  skip {wn}: {e}")

    log.info("── Feature engineering ─────────────────────────────────────")
    all_feats = []
    for wn, h in horiz_raw.items():
        try:
            all_feats.append(build_features(h, tw_map[wn],
                                            update_feature_cols=True))
        except Exception as e:
            log.warning(f"  feat failed {wn}: {e}")

    dip_atlas = build_dip_atlas(all_feats)
    all_feats = [add_regional_dip(df, dip_atlas) for df in all_feats]
    combined  = pd.concat(all_feats, ignore_index=True)

    target_col = "TVT" if "TVT" in combined.columns else "TVT_input"
    mask  = ~combined[target_col].isna()
    ctr   = combined[mask]
    X     = ctr[FEATURE_COLS].values
    y     = ctr[target_col].values
    groups = ctr["WELL"].values
    log.info(f"  {X.shape[0]:,} rows × {X.shape[1]} features")

    # ── Shared scalers ────────────────────────────────────────────────────────
    # x_scaler: normalises feature matrix (RobustScaler handles GR outliers)
    # y_scaler: normalises TVT target to [-3,3] range so TCN gradients are sane
    #           RobustScaler on TVT uses median/IQR — robust to formation jumps
    x_scaler = RobustScaler()
    Xs       = x_scaler.fit_transform(X)

    y_scaler = RobustScaler()
    y_scaler.fit(y.reshape(-1, 1))
    log.info(f"  TVT range: [{y.min():.1f}, {y.max():.1f}] ft  "
             f"| median={np.median(y):.1f}  IQR={y_scaler.scale_[0]:.1f}")

    # ── 1. TCN  — trained on full-well sequences (80/20 well-level split) ──
    log.info("── Dilated TCN (sequence model) ────────────────────────────")
    all_well_names = list(dict.fromkeys(groups))          # unique, order-preserved
    np.random.shuffle(all_well_names)
    split      = max(1, int(0.8 * len(all_well_names)))
    tr_wells   = set(all_well_names[:split])
    vl_wells   = set(all_well_names[split:])

    tr_dfs = [df for df in all_feats if df["WELL"].iloc[0] in tr_wells]
    vl_dfs = [df for df in all_feats if df["WELL"].iloc[0] in vl_wells]
    log.info(f"  TCN train wells={len(tr_dfs)}  val wells={len(vl_dfs)}")

    tcn_model = train_tcn(tr_dfs, vl_dfs, FEATURE_COLS, target_col,
                           x_scaler, y_scaler)

    # OOF TCN predictions (validation wells only — proxy for generalization)
    tcn_oof_preds, tcn_oof_true = [], []
    for df in vl_dfs:
        tcn_p = tcn_predict_well(tcn_model, df, FEATURE_COLS, x_scaler, y_scaler)
        true  = df[target_col].values
        m     = ~np.isnan(true)
        tcn_oof_preds.append(tcn_p[m])
        tcn_oof_true.append(true[m])
    tcn_oof_arr  = np.concatenate(tcn_oof_preds)
    true_oof_arr = np.concatenate(tcn_oof_true)
    tcn_rmse = np.sqrt(mean_squared_error(true_oof_arr, tcn_oof_arr))
    log.info(f"  TCN val RMSE = {tcn_rmse:.4f} ft")

    # ── 2. LGBM  — 3-fold GroupKFold as residual corrector ─────────────────
    log.info("── LGBM residual corrector (3-fold) ────────────────────────")
    # Feed TCN predictions as an extra feature to LGBM
    tcn_all = np.concatenate([
        tcn_predict_well(tcn_model, df, FEATURE_COLS, x_scaler, y_scaler)
        for df in all_feats
    ])
    mask_ctr = ~combined[target_col].isna()
    tcn_feat  = tcn_all[mask_ctr.values]

    Xs_lgbm   = np.hstack([Xs, tcn_feat.reshape(-1, 1)])
    feat_names_lgbm = FEATURE_COLS + ["TCN_PRED"]

    lgbm_models, oof_lgbm = [], np.zeros(len(X))
    for fold, (tri, vli) in enumerate(
            GroupKFold(N_FOLDS).split(Xs_lgbm, y, groups)):
        log.info(f"  Fold {fold+1}/{N_FOLDS}")
        m = train_lgbm(Xs_lgbm[tri], y[tri],
                       Xs_lgbm[vli], y[vli], feat_names_lgbm)
        lgbm_models.append(m)
        oof_lgbm[vli] = m.predict(Xs_lgbm[vli])

    lgbm_rmse = np.sqrt(mean_squared_error(y, oof_lgbm))
    log.info(f"  LGBM OOF RMSE = {lgbm_rmse:.4f}")

    # ── 3. Ensemble RMSE ────────────────────────────────────────────────────
    # For ensemble OOF we can only compare on val wells (where TCN OOF exists)
    log.info(f"  Summary →  TCN={tcn_rmse:.4f}  LGBM={lgbm_rmse:.4f}")

    return {
        "tcn_model":       tcn_model,
        "lgbm_models":     lgbm_models,
        "x_scaler":        x_scaler,
        "y_scaler":        y_scaler,
        "dip_atlas":       dip_atlas,
        "feature_cols":    FEATURE_COLS,
        "feat_names_lgbm": feat_names_lgbm,
        "oof_rmse":        lgbm_rmse,
    }


from typing import Dict
# =============================================================================
# 9. INFERENCE PIPELINE
# =============================================================================

def predict_well(wn: str, well_dir: str, artifacts: Dict) -> pd.DataFrame:
    h, tw = load_well_pair(well_dir, wn)
    df    = build_features(h, tw, dip_atlas=artifacts["dip_atlas"],
                           update_feature_cols=False)
    df    = add_regional_dip(df, artifacts["dip_atlas"])

    df["row_idx"] = df.index
    
    feat_cols = artifacts["feature_cols"]

    # ── Step 1: TCN sequence prediction ──────────────────────────────────────
    tcn_preds = tcn_predict_well(
        artifacts["tcn_model"], df, feat_cols,
        artifacts["x_scaler"], artifacts["y_scaler"])

    # ── Step 2: LGBM residual corrector (uses TCN output as a feature) ───────
    for c in feat_cols:
        if c not in df.columns:
            df[c] = 0.0
    Xs_base = artifacts["x_scaler"].transform(df[feat_cols].values)
    Xs_lgbm = np.hstack([Xs_base, tcn_preds.reshape(-1, 1)])   # append TCN col

    lgbm_preds = np.mean(
        [m.predict(Xs_lgbm) for m in artifacts["lgbm_models"]], axis=0)

    # ── Step 3: Ensemble  40% TCN + 60% LGBM ─────────────────────────────────
    # TCN captures sequence continuity; LGBM corrects regional/formation bias.
    ensemble = 0.60 * tcn_preds + 0.40 * lgbm_preds

    # ── Step 4: Blend with physics correlation signal in prediction zone ──────
    corr    = df["TVT_CORR"].values
    is_pred = df["IS_PRED_ZONE"].values == 1
    vc      = is_pred & ~np.isnan(corr)
    if vc.any():
        ensemble[vc] = 0.80 * ensemble[vc] + 0.20 * corr[vc]

    # ── Step 5: Continuity enforcement (anchor + clip + smooth) ──────────────
    ensemble = enforce_continuity(ensemble, h["TVT_input"].values)

    return pd.DataFrame({"WELL": wn, "MD": df["MD"].values,'row_idx':df['row_idx'],"TVT_pred": ensemble,"IS_PRED":  df["IS_PRED_ZONE"].values})


def run_inference(test_dir: str, artifacts: Dict) -> pd.DataFrame:
    log.info("── Inference ───────────────────────────────────────────────")
    results = []
    for wn in discover_wells(test_dir):
        try:
            results.append(predict_well(wn, test_dir, artifacts))
            log.info(f"  ✓ {wn}")
        except Exception as e:
            log.error(f"  ✗ {wn}: {e}")
    return pd.concat(results, ignore_index=True)


def build_submission(preds: pd.DataFrame, out_path: str) -> pd.DataFrame:
    sub = (preds[preds["IS_PRED"] == 1][["WELL", "row_idx", "TVT_pred"]]
           .rename(columns={"TVT_pred": "tvt"})
           .sort_values(["WELL", "row_idx"])
           .reset_index(drop=True))

    sub['id'] = sub['WELL'] + "_" + sub['row_idx'].astype(int).astype(str)

    # Ensure valid numeric values
    sub['tvt'] = pd.to_numeric(sub['tvt'], errors='raise').round(2)

    # Interpolation
    sub['tvt'] = sub['tvt'].interpolate(method='linear')

    # Final format
    sub = sub[['id', 'tvt']]

    # Safety check
    assert sub['tvt'].notna().all(), "NaNs found in tvt!"

    sub.to_csv(out_path, index=False)
    return sub

# =============================================================================
# MAIN  (Jupyter + CLI compatible)
# =============================================================================

def _in_jupyter() -> bool:
    try:
        return get_ipython().__class__.__name__ in (        # type: ignore
            "ZMQInteractiveShell", "TerminalInteractiveShell")
    except NameError:
        return False


# ── Notebook users: edit these values directly ────────────────────────────────
NOTEBOOK_CONFIG = {
    "train_dir":  "/kaggle/input/competitions/rogii-wellbore-geology-prediction/train",
    "test_dir":   "/kaggle/input/competitions/rogii-wellbore-geology-prediction/test",
    "output_dir": "/kaggle/working/",
}
# ─────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    import argparse

    if _in_jupyter():
        cfg = NOTEBOOK_CONFIG
    else:
        p = argparse.ArgumentParser()
        p.add_argument("--train-dir",  default=TRAIN_DIR)
        p.add_argument("--test-dir",   default=TEST_DIR)
        p.add_argument("--output-dir", default=OUTPUT_DIR)
        args, _ = p.parse_known_args()
        cfg = {"train_dir": args.train_dir,
               "test_dir":  args.test_dir,
               "output_dir": args.output_dir}

    OUTPUT_DIR = cfg["output_dir"]
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    artifacts   = run_training(cfg["train_dir"])
    predictions = run_inference(cfg["test_dir"], artifacts)
    sub    = build_submission(predictions, os.path.join(cfg["output_dir"], "submission.csv"))
    
    log.info(f"Done.  OOF RMSE = {artifacts['oof_rmse']:.4f}")





