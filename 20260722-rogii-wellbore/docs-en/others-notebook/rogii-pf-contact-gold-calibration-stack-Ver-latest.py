# %% [markdown]
# # ROGII : PF + Contact + Gold Calibration Stack
# 
# **Goal**  
# Predict `TVT` in the evaluation zone of each horizontal well using a conservative, physically meaningful stack anchored on the last known `TVT_input`, then refined with PF/beam geometry, contact-based reconstruction, and a final controlled blend.
# 
# ## What this notebook does
# 
# This notebook builds a layered submission pipeline:
# 
# 1. **Anchor prediction** at the last known `TVT_input`
# 2. **PF / beam path generation** to follow GR-to-typewell alignment
# 3. **Selector logic** to choose the most plausible path per well
# 4. **Final SP45 / Fleongg blend** to combine two strong candidate branches
# 5. **Guarded contact override** for overlap-like wells where a reconstruction is trusted
# 6. **Gold visible-prefix calibration** to probe which candidate family is safest under prefix backtests
# 7. **Final audit** to verify submission format, row order, and non-finite values
# 
# ## Why this notebook matters
# 
# This is the current **submit base** and the strongest notebook in our development path.  
# It is not just a single model, but a physically guided stack that tries to balance:
# 
# - local continuity from the known prefix
# - coarse geological alignment from GR and typewell matching
# - conservative blending to avoid unstable jumps
# - special handling for overlap/contact wells
# - hidden-tail robustness through prefix-aware calibration
# 
# ## Core ideas
# 
# ### 1. Last-known anchor
# The strongest baseline is still to hold near the last observed `TVT_input`.  
# Most improvements are small corrections around this anchor, not large extrapolations.
# 
# ### 2. PF / beam signal
# The PF and beam paths extract useful structure from horizontal GR and typewell GR alignment.  
# This is the main source of signal beyond the flat baseline.
# 
# ### 3. Selector-based blending
# The notebook computes several PF variants and blends them by well-specific selector logic.  
# This makes the stack more stable than using a single path everywhere.
# 
# ### 4. Final SP45 / Fleongg blend
# The final prediction combines two candidate branches with a tunable weight.  
# In this notebook, that final blend is one of the main knobs for small but meaningful LB changes.
# 
# ### 5. Guarded contact override
# For wells that overlap the train set, a contact-based reconstruction can be extremely strong.  
# But it is only applied when the known prefix check is good enough, so the override stays guarded instead of reckless.
# 
# ### 6. Gold prefix calibration
# The gold overlay runs a visible-prefix style backtest and chooses among candidate paths conservatively.  
# This is useful for studying whether a candidate improvement is real or just public-board noise.
# 
# ## Important notebook layers
# 
# - **Cell 13**: `PP.w_sub1` controls the learned-path vs likelihood-path balance.
# - **Cell 15**: selector logic and PF/beam path combination.
# - **Cell 19 / 21 / 23 / 25**: SP45 candidate build, projection, Fleongg candidate, and final blend.
# - **Cell 27**: guarded contact override.
# - **Cell 31**: gold visible-prefix calibration.
# - **Cell 33**: audit and submission checks.
# 
# ## What we learned
# 
# - A simple slope extrapolation is not enough.
# - The last-known TVT anchor is very strong.
# - GR carries real signal, but it is coarse and must be normalized carefully.
# - Overlap/contact wells can be solved very well, but only with a guard.
# - Tiny blend changes matter more than large architectural changes once the stack is already strong.
# - Seed / refork variance can mislead public LB interpretation.
# 
# ## Practical interpretation
# 
# This notebook is best understood as a **conservative physics-guided ensemble** rather than a pure ML model.  
# It deliberately prefers:
# 
# - physical plausibility over aggressive extrapolation
# - stable hidden behavior over public refork luck
# - small controlled changes over broad unvalidated shifts
# 
# ## Submission contract
# 
# The final output must remain:
# 
# ```text
# submission.csv

# %% [markdown]
# ## 1. Import Dependancies

# %% cell 2

import os, sys, glob, time, json, hashlib, warnings, subprocess, multiprocessing
from pathlib import Path
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

# ---- determinism -----------------------------------------------------------------
SEED = 42
os.environ.setdefault("PYTHONHASHSEED", str(SEED))
np.random.seed(SEED)
try:
    import random as _random; _random.seed(SEED)
except Exception:
    pass

# ---- numba (required for the PF/beam kernels; degrade to slow-but-valid if absent) -
try:
    from numba import njit
    HAVE_NUMBA = True
except Exception:                                   # pragma: no cover
    HAVE_NUMBA = False
    def njit(*a, **k):                              # no-op decorator fallback
        def deco(f): return f
        return deco(a[0]) if a and callable(a[0]) else deco

# ---- scientific stack ------------------------------------------------------------
from scipy.spatial import cKDTree
from scipy.signal import savgol_filter
from joblib import Parallel, delayed
import joblib

# ---- optional libs: import lazily, never crash at module load --------------------
def _try_import(name):
    try:
        return __import__(name)
    except Exception:
        return None
HAVE_LGB = _try_import("lightgbm") is not None
HAVE_CAT = _try_import("catboost") is not None

# ---- runtime knobs (all overridable via environment) -----------------------------
def _envint(k, d):  return int(os.environ.get(k, str(d)))
def _envflag(k, d): return os.environ.get(k, str(d)) == "1"

# Gold profile MUST default to conservative (preserves the public-LB anchor behaviour).
os.environ.setdefault("ROGII_GOLD_PROFILE", "conservative")
os.environ.setdefault("SHOW_FIGS", "0")             # off by default for headless rerun safety

print("env | numba:", HAVE_NUMBA, "| lightgbm:", HAVE_LGB, "| catboost:", HAVE_CAT,
      "| gold profile:", os.environ["ROGII_GOLD_PROFILE"])

# %% [markdown]
# ## 2. Robust data-path resolution
# 
# `find_data_dir()` accepts the standard competition mounts, then any mounted folder under
# `/kaggle/input/**` that contains a `sample_submission.csv` next to `train/` and `test/`.
# It **verifies** the three required entries exist before returning.

# %% cell 4

def find_data_dir():
    """Locate the competition data dir; verify train/, test/, sample_submission.csv exist."""
    cands = [
        Path("/kaggle/input/competitions/rogii-wellbore-geology-prediction"),
        Path("/kaggle/input/rogii-wellbore-geology-prediction"),
        Path(os.environ.get("ROGII_DATA", "")),       # local/dev override
    ]
    for p in glob.glob("/kaggle/input/**/sample_submission.csv", recursive=True):
        cands.append(Path(p).parent)
    seen = set()
    for c in cands:
        if not c or str(c) in seen:
            continue
        seen.add(str(c))
        try:
            if (c / "train").is_dir() and (c / "test").is_dir() and (c / "sample_submission.csv").is_file():
                return c
        except Exception:
            pass
    raise FileNotFoundError(
        "Could not locate ROGII data (need train/, test/, sample_submission.csv under /kaggle/input). "
        "Attach the competition dataset, or set ROGII_DATA for local runs."
    )

def find_artifact_dir():
    """Optional: ravaghi precomputed-feature artifact (train.csv/test.csv). None if absent."""
    explicit = Path("/kaggle/input/datasets/ravaghi/wellbore-geology-prediction-artifacts")
    cands = [explicit, explicit / "data"]
    for p in glob.glob("/kaggle/input/**/train.csv", recursive=True):
        cands.append(Path(p).parent)
    for c in cands:
        try:
            if (c / "train.csv").is_file():
                return c
        except Exception:
            pass
    return None

def find_fleongg_csv():
    """Optional: a pre-made fleongg submission csv (offline fallback for the fleongg candidate)."""
    pats = [
        "/kaggle/input/**/fleongg_pretrained_submission*.csv",
        "/kaggle/input/**/fleongg*submission*.csv",
        "/kaggle/working/fleongg_pretrained_submission.csv",
    ]
    for pat in pats:
        for p in sorted(glob.glob(pat, recursive=True)):
            try:
                df = pd.read_csv(p, nrows=5)
                if {"id", "tvt"}.issubset(df.columns):
                    return Path(p)
            except Exception:
                pass
    return None

DATA = find_data_dir()
OUT  = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path(".")
OUT.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR = find_artifact_dir()
FLEONGG_CSV  = find_fleongg_csv()

class CFG:
    # unified config: BOTH the old (.dataset_path/.artifacts_path) and the modern
    # (.DATA/.OUT/...) attribute names resolve to the same verified directories, so every
    # carried-over code path works without per-cell path patching.
    dataset_path   = DATA
    artifacts_path = ARTIFACT_DIR if ARTIFACT_DIR is not None else DATA
    DATA = DATA
    OUT  = OUT
    seed = SEED
    n_splits = 5
    n_jobs = min(8, multiprocessing.cpu_count())
    metric = None                                    # set after sklearn import below
    PF_SEEDS = 128
    PF_PARTICLES = 500
    PF_SCALES = (3., 5., 8., 12.)
    FAST = _envflag("FAST", 0)
    N_TRAIN_WELLS = _envint("N_TRAIN_WELLS", 0)      # 0 = all
    USE_GPU = os.environ.get("USE_GPU", "auto")
    SHOW_FIGS = os.environ.get("SHOW_FIGS", "0") == "1"

from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge
CFG.metric = root_mean_squared_error

print("DATA        :", CFG.DATA)
print("OUT         :", CFG.OUT)
print("ARTIFACT_DIR:", ARTIFACT_DIR)
print("FLEONGG_CSV :", FLEONGG_CSV)
print("cores       :", CFG.n_jobs, "| FAST:", CFG.FAST)

# %% [markdown]
# ## 3. Device detection & shared utilities
# 
# Real NVIDIA GPU detection via `nvidia-smi`; CPU parameters are used automatically when no GPU
# is present, so no GPU-only parameter is ever hard-coded without a fallback.

# %% cell 6

def device():
    """('gpu'|'cpu', label). Honours CFG.USE_GPU override; else probes nvidia-smi."""
    if CFG.USE_GPU == "cpu": return "cpu", "CPU"
    if CFG.USE_GPU == "gpu": return "gpu", "GPU"
    try:
        if subprocess.run(["nvidia-smi"], capture_output=True).returncode == 0:
            return "gpu", "GPU"
    except Exception:
        pass
    return "cpu", "CPU"

DEVICE, DEVICE_LABEL = device()
print("device:", DEVICE_LABEL)

def rmse(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float(np.sqrt(np.mean((a - b) ** 2)))

def split_id(series):
    """Robust id parsing: 'well_rowidx' -> (well, int rowidx). Never fixed-width slicing."""
    s = series.astype(str)
    parts = s.str.rsplit("_", n=1, expand=True)
    if parts.shape[1] != 2 or parts[1].isna().any():
        raise RuntimeError("Unexpected id format; expected '<well>_<rowindex>'")
    well = parts[0]
    row_idx = parts[1].astype(int)
    return well, row_idx

def list_wells(split):
    base = CFG.DATA / split
    return sorted(p.stem.replace("__horizontal_well", "")
                  for p in base.glob("*__horizontal_well.csv"))

POSTPROCESSORS = []        # populated as stages fire; reported in the final summary
DATASETS_FOUND = {"competition": str(DATA),
                  "artifact": str(ARTIFACT_DIR) if ARTIFACT_DIR else None,
                  "fleongg_csv": str(FLEONGG_CSV) if FLEONGG_CSV else None}

# %% [markdown]
# ## 4. Tracking engine - numba particle-filter & beam kernels
# 
# These JIT kernels (single ANCC-anchored PF, Z-velocity-coupled PF, Viterbi beam, and the
# 128-seed likelihood-weighted PF "workhorse") are carried verbatim from the reference pipeline
# (LB-validated). They release the GIL (`nogil=True`) so the per-well loop parallelises across
# threads. Defined before the SP45 driver so the SP45 beam ensemble binds the fast numba beam.

# %% cell 8
# ---- single particle filters (ANCC-anchored & Z-velocity-coupled), numba ---------
PF_N = 600; ANCC_N = 600
PF_MOM = 0.993; PF_VN = 0.005; PF_PN = 0.01
PF_GR_SIG_MIN = 10.; PF_GR_SIG_MAX = 60.; PF_GR_SIG_DEF = 30.
PF_GR_WIN = 5; PF_GR_WT = 0.3; PF_RESAMP = 0.5; PF_ROUGH_P = 0.2; PF_ROUGH_V = 0.003
ANCC_ALPHA = 0.998; ANCC_RN = 0.002; ANCC_PN = 0.005; ANCC_IS = 0.3; ANCC_RP = 0.1; ANCC_RR = 0.001

BEAMS = [(10,20.,144.,2,"cons"),(10,8.,64.,2,"loose"),(8,35.,220.,1,"vcons"),
         (10,14.,90.,5,"sm5"),(20,4.,36.,3,"vloose"),(12,12.,100.,3,"mid"),(15,25.,180.,2,"stiff")]

@njit(cache=True)
def _interp1(grid, v, vmin, step):
    i = int((v - vmin) / step)
    if i < 0: return grid[0]
    n = len(grid) - 1
    if i >= n: return grid[n]
    t = (v - vmin) / step - i
    return grid[i]*(1.-t) + grid[i+1]*t

@njit(cache=True)
def _resamp(pos, aux, w, N, rp, rv):
    cum = np.zeros(N+1)
    for j in range(N): cum[j+1] = cum[j]+w[j]
    u0 = np.random.uniform(0., 1./N); np2 = np.empty(N); na = np.empty(N); ci = 0
    for j in range(N):
        u = u0+j/N
        while ci < N-1 and cum[ci+1] < u: ci += 1
        np2[j] = pos[ci]+rp*np.random.randn(); na[j] = aux[ci]+rv*np.random.randn()
    return np2, na

@njit(cache=True)
def _beam_jit(sgr, tw_gr, si, BS, mc, es):
    n = len(sgr); nt = len(tw_gr); MAX = BS*6
    bidx = np.zeros(BS, np.int64); bidx[0] = si
    bcost = np.full(BS, 1e30); bcost[0] = 0.; bn = np.int64(1)
    hI = np.zeros((n, BS), np.int64); hP = np.zeros((n, BS), np.int64)
    cI = np.zeros(MAX, np.int64); cC = np.full(MAX, 1e30); cP = np.zeros(MAX, np.int64)
    for step in range(n):
        gv = sgr[step]; nc = np.int64(0)
        for bi in range(bn):
            idx = bidx[bi]; cost = bcost[bi]
            for d in range(-2, 3):
                ni = idx+d
                if ni < 0 or ni >= nt: continue
                tot = cost+(gv-tw_gr[ni])**2/es+mc*(d if d >= 0 else -d)
                fnd = np.int64(-1)
                for ci in range(nc):
                    if cI[ci] == ni: fnd = ci; break
                if fnd >= 0:
                    if tot < cC[fnd]: cC[fnd] = tot; cP[fnd] = bi
                else:
                    if nc < MAX: cI[nc] = ni; cC[nc] = tot; cP[nc] = bi; nc += 1
        kept = min(BS, nc)
        for i in range(kept):
            mi = i
            for j in range(i+1, nc):
                if cC[j] < cC[mi]: mi = j
            if mi != i:
                cI[i], cI[mi] = cI[mi], cI[i]; cC[i], cC[mi] = cC[mi], cC[i]; cP[i], cP[mi] = cP[mi], cP[i]
        hI[step, :kept] = cI[:kept]; hP[step, :kept] = cP[:kept]
        bidx[:kept] = cI[:kept]; bcost[:kept] = cC[:kept]; bn = kept
    best = np.int64(0)
    for b in range(1, bn):
        if bcost[b] < bcost[best]: best = b
    path = np.zeros(n, np.int64); b = best
    for s in range(n-1, -1, -1): path[s] = hI[s, b]; b = hP[s, b]
    return path

@njit(cache=True)
def _pf_ancc(md_v, z_v, gr_v, gg, vmin, step, gs, ls, ir, N, ALPHA, RN, PN, IS, RP, RR, RESAMP):
    pos = np.empty(N); rate = np.empty(N); w = np.ones(N)/N
    for j in range(N):
        pos[j] = ls+IS*np.random.randn(); rate[j] = ir+0.01*np.random.randn()
    pts = np.empty(len(md_v)); std_ = np.empty(len(md_v)); pm = md_v[0]-1.
    for i in range(len(md_v)):
        dm = md_v[i]-pm; dm = max(dm, 1.)
        for j in range(N):
            rate[j] = ALPHA*rate[j]+RN*np.random.randn(); pos[j] += rate[j]*dm+PN*np.random.randn()
            tvt_j = pos[j]-z_v[i]; tvt_j = max(tvt_j, vmin-50.); tvt_j = min(tvt_j, vmin+len(gg)*step+50.)
            pos[j] = tvt_j+z_v[i]
        if not np.isnan(gr_v[i]):
            ws = 0.
            for j in range(N):
                eg = _interp1(gg, pos[j]-z_v[i], vmin, step); d = (gr_v[i]-eg)/gs
                lk = max(np.exp(-0.5*d*d) if d*d < 600. else 0., 1e-300); w[j] *= lk; ws += w[j]
            if ws > 0.:
                for j in range(N): w[j] /= ws
            else:
                for j in range(N): w[j] = 1./N
        ne = 0.
        for j in range(N): ne += w[j]*w[j]
        if 1./ne < RESAMP*N:
            pos, rate = _resamp(pos, rate, w, N, RP, RR)
            for j in range(N): w[j] = 1./N
        tv = 0.
        for j in range(N): tv += w[j]*(pos[j]-z_v[i])
        pts[i] = tv; va = 0.
        for j in range(N): va += w[j]*(pos[j]-z_v[i]-tv)**2
        std_[i] = va**0.5; pm = md_v[i]
    return pts, std_

@njit(cache=True)
def _pf_z(md_v, z_v, gr_v, gr_sm_v, gg_p, gg_s, vmin, step, gs, ip, iv, beta, icpt, zsig, N,
         MOM, VN, PN, GR_WT, RP, RV, RESAMP):
    pos = np.empty(N); vel = np.empty(N); w = np.ones(N)/N
    for j in range(N):
        pos[j] = ip+0.5*np.random.randn(); vel[j] = iv+0.02*np.random.randn()
    pts = np.empty(len(md_v)); std_ = np.empty(len(md_v)); pm = md_v[0]-1.; pz = z_v[0]-1.
    for i in range(len(md_v)):
        dm = md_v[i]-pm; dm = max(dm, 1.); dzd = (z_v[i]-pz)/dm; ve = beta*dzd+icpt
        for j in range(N):
            vel[j] = MOM*vel[j]+VN*np.random.randn(); pos[j] += vel[j]*dm+PN*np.random.randn()
            pos[j] = max(pos[j], vmin-50.); pos[j] = min(pos[j], vmin+len(gg_p)*step+50.)
        if not np.isnan(gr_v[i]):
            ws = 0.
            for j in range(N):
                ep = _interp1(gg_p, pos[j], vmin, step); dp = (gr_v[i]-ep)/gs
                lp = max(np.exp(-0.5*dp*dp) if dp*dp < 600. else 0., 1e-300)
                if not np.isnan(gr_sm_v[i]):
                    es = _interp1(gg_s, pos[j], vmin, step); ds = (gr_sm_v[i]-es)/(gs*1.5)
                    lsm = max(np.exp(-0.5*ds*ds) if ds*ds < 600. else 0., 1e-300); lk = (1.-GR_WT)*lp+GR_WT*lsm
                else: lk = lp
                lk = max(lk, 1e-300); w[j] *= lk; ws += w[j]
            if ws > 0.:
                for j in range(N): w[j] /= ws
            else:
                for j in range(N): w[j] = 1./N
        ws2 = 0.
        for j in range(N):
            dv = (vel[j]-ve)/max(zsig*2., 0.005); lz = max(np.exp(-0.5*dv*dv) if dv*dv < 600. else 0., 1e-300)
            w[j] *= lz; ws2 += w[j]
        if ws2 > 0.:
            for j in range(N): w[j] /= ws2
        else:
            for j in range(N): w[j] = 1./N
        ne = 0.
        for j in range(N): ne += w[j]*w[j]
        if 1./ne < RESAMP*N:
            pos, vel = _resamp(pos, vel, w, N, RP, RV)
            for j in range(N): w[j] = 1./N
        wm = 0.
        for j in range(N): wm += w[j]*pos[j]
        pts[i] = wm; va = 0.
        for j in range(N): va += w[j]*(pos[j]-wm)**2
        std_[i] = va**0.5; pm = md_v[i]; pz = z_v[i]
    return pts, std_

def _grid(tw_tvt, tw_gr, step=0.2):
    tmin = float(tw_tvt.min()); tmax = float(tw_tvt.max())
    tvt_g = np.arange(tmin, tmax+step, step)
    return np.interp(tvt_g, tw_tvt, tw_gr).astype(np.float64), float(tmin), float(step)

def _gr_sig(hw, tw_tvt, tw_gr):
    kn = hw[hw.TVT_input.notna() & hw.GR.notna()]
    if len(kn) < 20: return float(PF_GR_SIG_DEF)
    return float(np.clip(np.std(kn.GR.values-np.interp(kn.TVT_input.values, tw_tvt, tw_gr)),
                         PF_GR_SIG_MIN, PF_GR_SIG_MAX))

def _nn(arr, v):
    i = int(np.searchsorted(arr, v, "left"))
    if i >= len(arr): return len(arr)-1
    if i > 0 and abs(arr[i-1]-v) <= abs(arr[i]-v): return i-1
    return i

def _smooth(vals, fb, r):
    s = pd.Series(vals, dtype="float32").interpolate(limit_direction="both").fillna(fb)
    return (s.rolling(r*2+1, center=True, min_periods=1).mean() if r > 0 else s).to_numpy(np.float32)

def beam_search(gr_h, tw_tvt, tw_gr, start_tvt, bs, mc, es, r):
    si = _nn(tw_tvt, start_tvt); sgr = _smooth(gr_h, float(np.nanmean(tw_gr)), r).astype(np.float64)
    return tw_tvt[_beam_jit(sgr, tw_gr.astype(np.float64), si, bs, float(mc), float(es))].astype(np.float32)

def run_pf_ancc(hw, tw_tvt, tw_gr, N=ANCC_N):
    gs = _gr_sig(hw, tw_tvt, tw_gr); kn = hw[hw.TVT_input.notna()]; ev = hw[hw.TVT_input.isna()]
    if len(ev) == 0: return np.array([]), np.array([])
    ls = float(kn.TVT_input.iloc[-1]+kn.Z.iloc[-1])
    tail = kn.tail(30); dt = np.diff(tail.TVT_input.values); dz = np.diff(tail.Z.values); dm = np.diff(tail.MD.values); m = dm > 0
    ir = float(np.median((dt+dz)[m]/dm[m])) if m.sum() >= 3 else 0.
    gg, gmin, gst = _grid(tw_tvt, tw_gr)
    pts, std = _pf_ancc(ev.MD.values.astype(np.float64), ev.Z.values.astype(np.float64), ev.GR.values.astype(np.float64),
                        gg, gmin, gst, gs, ls, ir, N, ANCC_ALPHA, ANCC_RN, ANCC_PN, ANCC_IS, ANCC_RP, ANCC_RR, PF_RESAMP)
    return pts.astype(np.float32), std.astype(np.float32)

def run_pf_z(hw, tw_tvt, tw_gr, N=PF_N):
    gs = _gr_sig(hw, tw_tvt, tw_gr); tw_s = pd.Series(tw_gr).rolling(PF_GR_WIN, center=True, min_periods=1).mean().values.astype(np.float32)
    kna = hw[hw.TVT_input.notna()]; ev = hw[hw.TVT_input.isna()]
    if len(ev) == 0: return np.array([]), np.array([])
    dz_k = np.diff(kna.Z.values); dvt = np.diff(kna.TVT_input.values); dmd_k = np.diff(kna.MD.values); m2 = dmd_k > 0
    if m2.sum() >= 10:
        vz = dz_k[m2]/dmd_k[m2]; vt = dvt[m2]/dmd_k[m2]; A = np.column_stack([vz, np.ones_like(vz)])
        c, _, _, _ = np.linalg.lstsq(A, vt, rcond=None)
        beta, icpt, zsig = float(c[0]), float(c[1]), max(float(np.std(vt-(c[0]*vz+c[1]))), 0.001)
    else: beta, icpt, zsig = -1., 0., 0.1
    t2 = kna.tail(20); dvt2 = np.diff(t2.TVT_input.values); dmd2 = np.diff(t2.MD.values); m3 = dmd2 > 0
    iv = float(np.median(dvt2[m3]/dmd2[m3])) if m3.sum() >= 3 else 0.
    gg, gmin, gst = _grid(tw_tvt, tw_gr); gs2, _, _ = _grid(tw_tvt, tw_s)
    gr_sm = hw.GR.rolling(PF_GR_WIN, center=True, min_periods=1).mean()
    pts, std = _pf_z(ev.MD.values.astype(np.float64), ev.Z.values.astype(np.float64), ev.GR.values.astype(np.float64),
                     gr_sm.loc[ev.index].values.astype(np.float64), gg, gs2, gmin, gst, gs,
                     float(kna.TVT_input.iloc[-1]), iv, beta, icpt, zsig, N,
                     PF_MOM, PF_VN, PF_PN, PF_GR_WT, PF_ROUGH_P, PF_ROUGH_V, PF_RESAMP)
    return pts.astype(np.float32), std.astype(np.float32)

def multi_scale_ncc(kgr, ktvt, hgr, hws=(8, 15, 25), stride=3):
    out = []
    for hw in hws:
        win = 2*hw+1; nk = len(kgr); nh = len(hgr)
        if nk < win+1 or nh == 0:
            out.append((np.full(nh, ktvt[-1], np.float32), np.zeros(nh, np.float32))); continue
        kg = pd.Series(kgr).rolling(5, center=True, min_periods=1).mean().values.astype(np.float32)
        hg = pd.Series(hgr).rolling(5, center=True, min_periods=1).mean().values.astype(np.float32)
        sts = np.arange(0, nk-win+1, stride, dtype=np.int32)
        if len(sts) == 0:
            out.append((np.full(nh, ktvt[-1], np.float32), np.zeros(nh, np.float32))); continue
        C = kg[sts[:, None]+np.arange(win, dtype=np.int32)[None, :]].astype(np.float32)
        Cn = (C-C.mean(1, keepdims=True))/(C.std(1, keepdims=True)+1e-6)
        hp = np.pad(hg, hw, mode="edge"); H = hp[np.arange(nh)[:, None]+np.arange(win)[None, :]].astype(np.float32)
        Hn = (H-H.mean(1, keepdims=True))/(H.std(1, keepdims=True)+1e-6)
        ncc = Hn@Cn.T/win; best = ncc.argmax(1); score = ncc.max(1).astype(np.float32)
        out.append((ktvt[np.clip(sts[best]+hw, 0, nk-1)].astype(np.float32), score))
    tvts = np.stack([o[0] for o in out], 1); scores = np.stack([o[1] for o in out], 1)
    sw = np.exp(3.*scores); sw /= sw.sum(1, keepdims=True)+1e-9
    return out, (tvts*sw).sum(1).astype(np.float32)

# %% cell 9
# ---- 128-seed likelihood-weighted particle filter (the workhorse), numba ---------
@njit(cache=True, nogil=True)
def _pf_lik_allseeds(md_v, z_v, gr_v, gg, vmin, step, gs, ls, ir, N, n_seeds, seed_base,
                     MOM, VN, PN, RP, RR, RESAMP, init_spr):
    n = len(md_v); preds = np.empty((n_seeds, n)); liks = np.empty(n_seeds); tmax = vmin + len(gg)*step
    for s in range(n_seeds):
        np.random.seed(seed_base + s)
        pos = np.empty(N); rate = np.empty(N); w = np.ones(N)/N
        for j in range(N):
            pos[j] = ls + init_spr*np.random.randn(); rate[j] = ir + 0.01*np.random.randn()
        log_lik = 0.0; prev_md = md_v[0] - 1.0
        for i in range(n):
            dm = md_v[i] - prev_md
            if dm < 1.0: dm = 1.0
            for j in range(N):
                rate[j] = MOM*rate[j] + VN*np.random.randn(); pos[j] += rate[j]*dm + PN*np.random.randn()
                tvt_j = pos[j] - z_v[i]
                if tvt_j < vmin-100.: tvt_j = vmin-100.
                if tvt_j > tmax+100.: tvt_j = tmax+100.
                pos[j] = tvt_j + z_v[i]
            avg_lk = 0.0
            for j in range(N):
                eg = _interp1(gg, pos[j]-z_v[i], vmin, step); d = (gr_v[i]-eg)/gs; dd = d*d
                if dd > 600.: dd = 600.
                lk = np.exp(-0.5*dd)
                if lk < 1e-300: lk = 1e-300
                avg_lk += w[j]*lk; w[j] = w[j]*lk
            if avg_lk < 1e-300: avg_lk = 1e-300
            log_lik += np.log(avg_lk)
            ws = 0.0
            for j in range(N): ws += w[j]
            if ws > 0.0:
                for j in range(N): w[j] /= ws
            else:
                for j in range(N): w[j] = 1./N
            neff = 0.0
            for j in range(N): neff += w[j]*w[j]
            neff = 1.0/neff
            if neff < RESAMP*N:
                cum = np.empty(N); c = 0.0
                for j in range(N): c += w[j]; cum[j] = c
                u0 = np.random.uniform(0., 1./N); newpos = np.empty(N); newrate = np.empty(N); ci = 0
                for j in range(N):
                    u = u0 + j/N
                    while ci < N-1 and cum[ci] < u: ci += 1
                    newpos[j] = pos[ci] + RP*np.random.randn(); newrate[j] = rate[ci] + RR*np.random.randn()
                for j in range(N): pos[j] = newpos[j]; rate[j] = newrate[j]; w[j] = 1./N
            est = 0.0
            for j in range(N): est += w[j]*(pos[j]-z_v[i])
            preds[s, i] = est; prev_md = md_v[i]
        liks[s] = log_lik
    return preds, liks

def lik_pf(hw, tw, n_particles=CFG.PF_PARTICLES, n_seeds=CFG.PF_SEEDS, scales=CFG.PF_SCALES,
           init_spr=4.5, seed_base=0, with_quality=False):
    """Likelihood-weighted PF ensemble. Returns ({pf_scale_X: pred_eval}, ev_index[, quality])."""
    tw_s = tw.sort_values("TVT"); tw_tvt = tw_s.TVT.values.astype(float)
    tw_gr = tw_s.GR.fillna(tw_s.GR.mean()).values.astype(float)
    kn = hw[hw.TVT_input.notna()]; ev = hw[hw.TVT_input.isna()]
    if len(ev) == 0: return {}, np.array([]), {}
    last = kn.iloc[-1]; ls = float(last.TVT_input) + float(last.Z)
    tw_at_k = np.interp(kn.TVT_input.values, tw_tvt, tw_gr)
    gs = float(np.clip(np.nanstd(kn.GR.fillna(0).values - tw_at_k), 10., 60.))
    tail = kn.tail(30); dt = np.diff(tail.TVT_input.values); dz = np.diff(tail.Z.values); dm = np.diff(tail.MD.values); m = dm > 0
    ir = float(np.median((dt+dz)[m]/dm[m])) if m.sum() >= 3 else 0.0
    gg, gmin, gst = _grid(tw_tvt, tw_gr)
    gr_v = hw.GR.interpolate(limit_direction="both").fillna(tw_gr.mean()).values.astype(float)[ev.index]
    preds, liks = _pf_lik_allseeds(ev.MD.values.astype(float), ev.Z.values.astype(float), gr_v,
                                   gg, gmin, gst, gs, ls, ir, n_particles, n_seeds, seed_base,
                                   0.998, 0.002, 0.005, 0.1, 0.001, 0.5, init_spr)
    ln = liks - liks.max(); out = {}
    for sc in scales:
        wts = np.exp(ln/float(sc)); wts /= wts.sum(); out[f"pf_scale_{sc:g}"] = (wts[:, None]*preds).sum(0)
    out["pf_mean"] = preds.mean(0)
    q = {}
    if with_quality:
        q = {"pf_best_ll": float(liks.max())/len(ev), "pf_ll_spread": float(liks.std()),
             "pf_pt_std": preds.std(0).astype(np.float32), "pf_gr_sig": gs}
    return out, ev.index.values, q

# JIT warm-up so timings below are representative
_m = np.linspace(1, 50, 20); _z = np.zeros(20); _g = np.full(20, 50.); _gg = np.linspace(45, 55, 100)
_pf_ancc(_m, _z, _g, _gg, 45., .1, 20., 50., 0., 8, .998, .002, .005, .3, .1, .001, .5)
_pf_z(_m, _z, _g, _g, _gg, _gg, 45., .1, 20., 50., 0., -1., 0., .1, 8, .993, .005, .01, .3, .2, .003, .5)
_beam_jit(np.random.randn(30), np.random.randn(50), 25, 8, 15., 100.)
_pf_lik_allseeds(_m, _z, _g, _gg, 45., .1, 20., 50., 0., 64, 4, 0, .998, .002, .005, .1, .001, .5, 4.5)
print("trackers compiled.")

def fig_tracker_vs_truth(wid):
    import matplotlib.pyplot as plt
    hw, tw = load_well(wid); kn = hw[hw.TVT_input.notna()]; ev = hw[hw.TVT_input.isna()]
    tw_tvt = tw.TVT.to_numpy(np.float32); tw_gr = tw.GR.to_numpy(np.float32); last = float(kn.TVT_input.iloc[-1])
    pf, _ = run_pf_ancc(hw, tw_tvt, tw_gr); out, _, _ = lik_pf(hw, tw, scales=(3.,))
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(ev.MD, ev.TVT, lw=2.2, color="black", label="True TVT", zorder=5)
    ax.plot(ev.MD, np.full(len(ev), last), lw=1.1, color="gray", ls=":", label="last-known baseline")
    ax.plot(ev.MD, pf, lw=1.0, color="tab:blue", alpha=.8, label="single particle filter")
    ax.plot(ev.MD, out["pf_scale_3"], lw=1.5, color="crimson", alpha=.9, label="128-seed lik-weighted PF")
    ax.set_xlabel("MD (ft)"); ax.set_ylabel("TVT (ft)"); ax.invert_yaxis(); ax.grid(alpha=.25)
    ax.set_title(f"Well {wid}: trackers vs ground truth - the lik-PF resists drift"); ax.legend(loc="best")
    plt.tight_layout(); plt.show()

# %% [markdown]
# ## 5. Spatial priors & per-well feature builders
# 
# `FormationPlaneKNN` fits a local plane to each formation-contact surface from neighbouring
# offset wells (leave-self-out); `DenseANCCImputer` does distance-weighted ANCC imputation.
# `build_well` turns one well into a feature row-set; `lik_pf` features feed the boosters.

# %% cell 11
if "FORMATIONS" not in globals():
    # the 6 ROGII formation/contact columns (confirmed by the pretrained features.json:
    # tvtF_ANCC/ASTNU/ASTNL/EGFDU/EGFDL/BUDA). Fallback only if no earlier cell defined it.
    FORMATIONS = ["ANCC", "ASTNU", "ASTNL", "EGFDU", "EGFDL", "BUDA"]

PLANE_K = 10; DENSE_SPW = 60; DENSE_K = 20

def robust_slope(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float); m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 2 or np.std(x[m]) < 1e-6: return 0.
    return float(np.polyfit(x[m], y[m], 1)[0])

def affine_cal(kgr, tw_at_k, min_pts=20):
    v = np.isfinite(kgr) & np.isfinite(tw_at_k)
    if v.sum() < min_pts or np.std(tw_at_k[v]) < 1e-6:
        return 1., float(np.nanmean(kgr)-np.nanmean(tw_at_k)) if v.any() else 0.
    a, b = np.polyfit(tw_at_k[v], kgr[v], 1); return float(a), float(b)

def seg_b_well(ktvt, kz, form_col):
    bv = ktvt+kz-form_col; n = len(bv); b_full = float(np.median(bv))
    b_late = float(np.median(bv[max(0, n-50):])) if n >= 5 else b_full
    t1, t2 = n//3, 2*n//3
    b_early = float(np.median(bv[:max(1, t1)])) if t1 > 0 else b_full
    b_mid = float(np.median(bv[t1:max(t1+1, t2)])) if t2 > t1 else b_full
    w = np.exp(0.02*np.arange(n)); w /= w.sum()
    return b_full, b_early, b_mid, b_late, float(np.dot(w, bv))

class FormationPlaneKNN:
    def __init__(self, well_ids, data_dir):
        # tolerant: only request columns that exist; drop on X/Y only (formation markers are
        # sparse in horizontal logs, so an unconditional dropna() would empty every well).
        rows = []
        for wid in well_ids:
            fp = data_dir / f"{wid}__horizontal_well.csv"
            if not fp.exists(): continue
            try:
                cols = pd.read_csv(fp, nrows=0).columns
                use = [c for c in (["X", "Y"] + FORMATIONS) if c in cols]
                if "X" not in use or "Y" not in use: continue
                df = pd.read_csv(fp, usecols=use).dropna(subset=["X", "Y"])
            except Exception:
                continue
            if len(df) == 0: continue
            row = {"wid": wid, "x": float(df.X.median()), "y": float(df.Y.median())}
            for c in FORMATIONS:
                row[f"{c}_m"] = float(df[c].median()) if (c in df.columns and df[c].notna().any()) else np.nan
            rows.append(row)
        self.ok = len(rows) > 0
        self.df = pd.DataFrame(rows)
        if not self.ok:
            self.wmap = {}; self.scale = np.array([1., 1.]); self.tree = None
            self.xa = np.zeros(0); self.ya = np.zeros(0); self.fa = np.zeros((0, len(FORMATIONS)))
            print("[warn] FormationPlaneKNN: no usable wells -> spatial-plane features degraded (NaN)", flush=True)
            return
        self.wmap = {w: i for i, w in enumerate(self.df["wid"])}
        fa = self.df[[f"{c}_m" for c in FORMATIONS]].to_numpy(np.float64)
        col_mean = np.nanmean(fa, axis=0) if np.isfinite(fa).any() else np.zeros(fa.shape[1])
        col_mean = np.where(np.isfinite(col_mean), col_mean, 0.0)
        nanpos = np.where(np.isnan(fa)); fa[nanpos] = np.take(col_mean, nanpos[1])
        self.fa = fa
        xy = self.df[["x", "y"]].to_numpy(); self.scale = np.where(xy.std(0) < 1e-3, 1., xy.std(0))
        self.tree = cKDTree(xy/self.scale); self.xa = self.df.x.to_numpy(); self.ya = self.df.y.to_numpy()
    def impute(self, xy_q, self_wid=None, k=PLANE_K):
        xy_q = np.atleast_2d(np.asarray(xy_q, float))
        if self.tree is None:
            n = len(xy_q)
            return np.full((n, len(FORMATIONS)), np.nan, np.float32), np.full(n, np.inf, np.float32)
        q = xy_q/self.scale; nf = min(k+5, len(self.df)); dist, idx = self.tree.query(q, k=nf, workers=-1)
        if self_wid in self.wmap: dist = np.where(idx == self.wmap[self_wid], np.inf, dist)
        ordr = np.argpartition(dist, min(k-1, nf-1), 1)[:, :k]
        dk = np.take_along_axis(dist, ordr, 1); ik = np.take_along_axis(idx, ordr, 1)
        vk = np.isfinite(dk); w = np.where(vk, 1./(dk+1e-3), 0.).astype(np.float64)
        xn = self.xa[ik]; yn = self.ya[ik]; fn = self.fa[ik]; wx = w*xn; wy = w*yn
        A = np.zeros((len(q), 3, 3))
        A[:,0,0]=(wx*xn).sum(1); A[:,0,1]=(wx*yn).sum(1); A[:,0,2]=wx.sum(1)
        A[:,1,0]=A[:,0,1]; A[:,1,1]=(wy*yn).sum(1); A[:,1,2]=wy.sum(1)
        A[:,2,0]=A[:,0,2]; A[:,2,1]=A[:,1,2]; A[:,2,2]=w.sum(1)
        A[:,0,0]+=1e-9; A[:,1,1]+=1e-9; A[:,2,2]+=1e-9
        rhs = np.stack([(wx[:,:,None]*fn).sum(1), (wy[:,:,None]*fn).sum(1), (w[:,:,None]*fn).sum(1)], 1)
        try: coef = np.linalg.solve(A, rhs)
        except:
            coef = np.zeros((len(q), 3, 6))
            for r in range(len(q)):
                try: coef[r] = np.linalg.pinv(A[r])@rhs[r]
                except: pass
        Xq = xy_q[:,0]; Yq = xy_q[:,1]
        pred = (Xq[:,None]*coef[:,0,:]+Yq[:,None]*coef[:,1,:]+coef[:,2,:]).astype(np.float32)
        pred[~vk.any(1)] = self.fa.mean(0)
        return pred, np.where(vk, dk, np.inf).min(1).astype(np.float32)

class DenseANCCImputer:
    def __init__(self, well_ids, data_dir, spw=DENSE_SPW):
        xs, ys, an, wd = [], [], [], []
        for wid in well_ids:
            fp = data_dir / f"{wid}__horizontal_well.csv"
            if not fp.exists(): continue
            try:
                cols = pd.read_csv(fp, nrows=0).columns
                if not {"X", "Y", "ANCC"}.issubset(cols): continue
                df = pd.read_csv(fp, usecols=["X", "Y", "ANCC"]).dropna(subset=["X", "Y", "ANCC"])
            except Exception:
                continue
            if len(df) == 0: continue
            ix = np.linspace(0, len(df)-1, min(spw, len(df)), dtype=int); s = df.iloc[ix]
            xs.append(s.X.values); ys.append(s.Y.values); an.append(s.ANCC.values); wd.extend([wid]*len(s))
        self.ok = len(xs) > 0
        if not self.ok:
            self.xy = np.zeros((0, 2)); self.ancc = np.zeros(0, np.float32); self.wids = np.array([])
            self.scale = np.array([1., 1.]); self.tree = None
            print("[warn] DenseANCCImputer: no usable wells -> dense-ANCC features degraded (NaN)", flush=True)
            return
        self.xy = np.column_stack([np.concatenate(xs), np.concatenate(ys)])
        self.ancc = np.concatenate(an).astype(np.float32); self.wids = np.array(wd)
        self.scale = np.where(self.xy.std(0) < 1e-3, 1., self.xy.std(0)); self.tree = cKDTree(self.xy/self.scale)
    def impute(self, xy_q, self_wid=None, k=DENSE_K, nfetch=5000):
        xy_q = np.atleast_2d(xy_q)
        if self.tree is None:
            n = len(xy_q)
            return (np.full(n, np.nan, np.float32), np.full(n, np.nan, np.float32), np.full(n, np.inf, np.float32))
        q = xy_q/self.scale; nf = min(nfetch, len(self.ancc))
        dist, idx = self.tree.query(q, k=nf, workers=-1)
        if self_wid: dist = np.where(self.wids[idx] == self_wid, np.inf, dist)
        ordr = np.argpartition(dist, min(k-1, nf-1), 1)[:, :k]
        dk = np.take_along_axis(dist, ordr, 1); ik = np.take_along_axis(idx, ordr, 1)
        vk = np.isfinite(dk); w = np.where(vk, 1./(dk+1e-3), 0.); sw = w.sum(1); safe = np.where(sw < 1e-9, 1., sw)
        a = self.ancc[ik]; ap = (a*w).sum(1)/safe; ap = np.where(sw < 1e-9, float(self.ancc.mean()), ap)
        var = ((a-ap[:,None])**2*w).sum(1)/safe
        return ap.astype(np.float32), np.sqrt(np.maximum(var, 0.)).astype(np.float32), np.where(vk, dk, np.inf).min(1).astype(np.float32)

_FI = None; _DI = None
ANCH_OFFS = np.array([-80,-40,-20,-10,-5,0,5,10,20,40,80], np.float32)
BEAM_OFFS = np.array([-40,-20,-10,-5,-3,0,3,5,10,20,40], np.float32)
SC_OFFS = np.array([-30,-15,-8,-4,-2,0,2,4,8,15,30], np.float32)
PF_OFFS = SC_OFFS.copy()

# %% cell 12
def build_well(hw_path, tw_path, is_train, likpf_map=None):
    global _FI, _DI
    wid = Path(hw_path).stem.replace("__horizontal_well", "")
    try: hw = pd.read_csv(hw_path); tw = pd.read_csv(tw_path).sort_values("TVT")
    except: return None
    if is_train and "TVT" not in hw.columns: return None
    kn = hw[hw.TVT_input.notna()]; ev = hw[hw.TVT_input.isna()]
    if len(ev) == 0 or len(kn) < 10: return None
    if is_train and hw.TVT.isna().all(): return None
    tw_tvt = tw.TVT.to_numpy(np.float32); tw_gr = tw.GR.to_numpy(np.float32)
    if len(tw_tvt) < 3: return None
    pf_a, std_a = run_pf_ancc(hw, tw_tvt, tw_gr)
    if len(pf_a) == 0: return None
    pf_z, std_z = run_pf_z(hw, tw_tvt, tw_gr)
    pf_use = pf_a.astype(np.float32); std_use = std_a.astype(np.float32)
    has_z = len(pf_z) == len(pf_a) and not np.any(np.isnan(pf_z))
    lk = kn.iloc[-1]; last_tvt = float(lk.TVT_input)
    gr_full = hw.GR.astype(float).interpolate(limit_direction="both").fillna(float(np.nanmean(tw_gr)))
    hgr = gr_full.iloc[ev.index[0]:].to_numpy(np.float32); kgr = gr_full.iloc[:len(kn)].to_numpy(np.float32)
    bpaths = {tag: beam_search(hgr, tw_tvt, tw_gr, last_tvt, bs, mc, es, r) for (bs, mc, es, r, tag) in BEAMS}
    beam_ref = (bpaths["cons"]+bpaths["sm5"])/2.
    ktvt = kn.TVT_input.to_numpy(np.float32)
    sc_res, sc_ens = multi_scale_ncc(kgr, ktvt, hgr, hws=(8, 15, 25), stride=3)
    sc8, sc8s = sc_res[0]; sc15, sc15s = sc_res[1]; sc25, sc25s = sc_res[2]; sc_cons = (sc8+sc15+sc25)/3.
    sc_trust = float(np.clip(len(kn)/200., 0., 0.6)); hyb_ref = (1-sc_trust)*beam_ref+sc_trust*sc_ens
    tw_at_k = np.interp(ktvt, tw_tvt, tw_gr).astype(np.float32); a_cal, b_cal = affine_cal(kgr, tw_at_k)
    kmd = kn.MD.to_numpy(np.float32); kz = kn.Z.to_numpy(np.float32)
    pfx_rmse = float(np.sqrt(np.mean((kgr-tw_at_k)**2)))
    slp_all = robust_slope(kmd, ktvt); slp_50 = robust_slope(kmd[-50:], ktvt[-50:]); slp_z = robust_slope(kz, ktvt)
    swid = wid if is_train else None
    xy_ev = ev[["X","Y"]].to_numpy(np.float64); xy_kn = kn[["X","Y"]].to_numpy(np.float64)
    form_ev, knn_d = _FI.impute(xy_ev, self_wid=swid); form_kn, _ = _FI.impute(xy_kn, self_wid=swid)
    z_kn = kn.Z.to_numpy(np.float32); z_ev = ev.Z.to_numpy(np.float32)
    tvt_fs = {}; form_rmse = {}; form_list = []
    for fi2, fn in enumerate(FORMATIONS):
        b_full, b_early, b_mid, b_late, b_wls = seg_b_well(ktvt, z_kn, form_kn[:, fi2])
        tvt_f = (-z_ev+form_ev[:, fi2]+b_full).astype(np.float32)
        tvt_fs[f"tvtF_{fn}"]=tvt_f; tvt_fs[f"tvtFw_{fn}"]=(-z_ev+form_ev[:,fi2]+b_wls).astype(np.float32)
        tvt_fs[f"tvtF50_{fn}"]=(-z_ev+form_ev[:,fi2]+b_late).astype(np.float32)
        tvt_fs[f"bw_{fn}"]=np.float32(b_full); tvt_fs[f"bww_{fn}"]=np.float32(b_wls); tvt_fs[f"bw50_{fn}"]=np.float32(b_late)
        tvt_fs[f"bw_early_{fn}"]=np.float32(b_early); tvt_fs[f"bw_mid_{fn}"]=np.float32(b_mid)
        form_rmse[fn]=float(np.sqrt(np.mean((ktvt-(-z_kn+form_kn[:,fi2]+b_full))**2))); form_list.append(tvt_f)
    fs = np.stack(form_list, 1)
    form_mean_d=(fs.mean(1)-last_tvt).astype(np.float32); form_std_d=fs.std(1).astype(np.float32); form_rng_d=(fs.max(1)-fs.min(1)).astype(np.float32)
    d_ancc, d_std, d_dist = _DI.impute(xy_ev, self_wid=swid); d_kn, d_std_kn, _ = _DI.impute(xy_kn, self_wid=swid)
    _, b_de, b_dm, b_dl, b_dw = seg_b_well(ktvt, z_kn, d_kn); b_d = float(np.median(ktvt+z_kn-d_kn))
    tvt_dense=(-z_ev+d_ancc+b_d).astype(np.float32); tvt_densew=(-z_ev+d_ancc+b_dw).astype(np.float32); tvt_dense50=(-z_ev+d_ancc+b_dl).astype(np.float32)
    res_kn = ktvt+z_kn-d_kn; d_rmse=float(np.sqrt(np.mean(res_kn**2))); d_bias=float(np.mean(res_kn)); d_nb_std=float(np.mean(d_std_kn))
    all_sigs=[pf_use]+list(bpaths.values())+[sc8,sc15,sc25,sc_ens,tvt_fs["tvtF_ANCC"],tvt_dense]
    sig_mat=np.stack(all_sigs,1); sig_std=sig_mat.std(1).astype(np.float32); sig_mean=(sig_mat.mean(1)-last_tvt).astype(np.float32)
    gr_s=pd.Series(gr_full.values); rolls={}
    for w in [5,21,51,101]:
        r=gr_s.rolling(w,center=True,min_periods=1); rolls[f"grm{w}"]=r.mean().iloc[ev.index].values.astype(np.float32); rolls[f"grs{w}"]=r.std().fillna(0).iloc[ev.index].values.astype(np.float32)
    for lag in [1,5,15,30]:
        rolls[f"glag{lag}"]=gr_s.shift(lag).bfill().iloc[ev.index].values.astype(np.float32); rolls[f"glead{lag}"]=gr_s.shift(-lag).ffill().iloc[ev.index].values.astype(np.float32)
    gr_d1=gr_s.diff().fillna(0.).iloc[ev.index].values.astype(np.float32); gr_d2=gr_s.diff().diff().fillna(0.).iloc[ev.index].values.astype(np.float32)
    gr_env=gr_s.rolling(21,center=True,min_periods=1).max().iloc[ev.index].values.astype(np.float32)
    gr_nrg=np.sqrt(np.maximum((gr_s**2).rolling(21,center=True,min_periods=1).mean(),0.)).iloc[ev.index].values.astype(np.float32)
    hmd=ev.MD.to_numpy(np.float32); md_since=hmd-float(lk.MD)
    slp_b_all=(last_tvt+slp_all*md_since).astype(np.float32); slp_b_50=(last_tvt+slp_50*md_since).astype(np.float32)
    mdd=hw.MD.diff().replace(0,np.nan)
    dzdmd=(hw.Z.diff()/mdd).iloc[ev.index].values.astype(np.float32); dxdmd=(hw.X.diff()/mdd).iloc[ev.index].values.astype(np.float32); dydmd=(hw.Y.diff()/mdd).iloc[ev.index].values.astype(np.float32)
    nh=len(ev); frac=(np.arange(nh)/max(nh-1,1)).astype(np.float32)
    def sc(v): return np.full(nh, np.float32(v), np.float32)
    feats={"well":wid,"id":[f"{wid}_{i}" for i in ev.index],"last_known_tvt":sc(last_tvt),
        "pf_ancc":pf_use,"pf_ancc_std":std_use,"pf_ancc_delta":(pf_use-last_tvt).astype(np.float32),
        "pf_z":(pf_z.astype(np.float32) if has_z else sc(last_tvt)),"pf_z_delta":((pf_z-last_tvt).astype(np.float32) if has_z else sc(0.)),
        "pf_vs_z":((pf_use-pf_z.astype(np.float32)) if has_z else sc(0.)),
        **{f"beam_{t}_d":(p-np.float32(last_tvt)).astype(np.float32) for t,p in bpaths.items()},
        "beam_mean_d":np.stack([(p-last_tvt) for p in bpaths.values()],1).mean(1).astype(np.float32),
        "beam_std_d":np.stack([(p-last_tvt) for p in bpaths.values()],1).std(1).astype(np.float32),
        "beam_med_d":np.median(np.stack([(p-last_tvt) for p in bpaths.values()],1),1).astype(np.float32),
        "sc8_d":(sc8-np.float32(last_tvt)).astype(np.float32),"sc8_sc":sc8s,"sc15_d":(sc15-np.float32(last_tvt)).astype(np.float32),"sc15_sc":sc15s,
        "sc25_d":(sc25-np.float32(last_tvt)).astype(np.float32),"sc25_sc":sc25s,"sc_cons_d":(sc_cons-np.float32(last_tvt)).astype(np.float32),
        "sc_ens_d":(sc_ens-np.float32(last_tvt)).astype(np.float32),"sc_trust":sc(sc_trust),"hyb_d":(hyb_ref-np.float32(last_tvt)).astype(np.float32),
        "sig_std":sig_std,"sig_mean_d":sig_mean,**tvt_fs,**{f"frm_rmse_{fn}":sc(form_rmse[fn]) for fn in FORMATIONS},
        "form_mean_d":form_mean_d,"form_std_d":form_std_d,"form_rng_d":form_rng_d,
        "spatial_ancc_d":(form_ev[:,0]-np.float32(np.interp(last_tvt,tw_tvt,tw_gr))),"spatial_knn_dist":knn_d,
        "dense_ancc":d_ancc,"dense_std":d_std,"dense_dist":d_dist,"tvt_dense_d":(tvt_dense-last_tvt).astype(np.float32),
        "tvt_densew_d":(tvt_densew-last_tvt).astype(np.float32),"tvt_dense50_d":(tvt_dense50-last_tvt).astype(np.float32),
        "dense_rmse":sc(d_rmse),"dense_bias":sc(d_bias),"dense_nb_std":sc(d_nb_std),
        "pf_vs_spatial":(pf_use-tvt_fs["tvtF_ANCC"]).astype(np.float32),"pf_vs_dense":(pf_use-tvt_dense).astype(np.float32),
        "spatial_vs_dense":(tvt_fs["tvtF_ANCC"]-tvt_dense).astype(np.float32),"beam_vs_spatial":(bpaths["cons"]-tvt_fs["tvtF_ANCC"]).astype(np.float32),
        "sc_vs_beam":(sc_ens-bpaths["cons"]).astype(np.float32),"cal_a":sc(a_cal),"cal_b":sc(b_cal),
        "pfx_rmse":sc(pfx_rmse),"known_len":sc(len(kn)),"eval_len":sc(nh),"slp_all":sc(slp_all),"slp_50":sc(slp_50),"slp_z":sc(slp_z),
        "slp_b_d_all":(slp_b_all-last_tvt).astype(np.float32),"slp_b_d_50":(slp_b_50-last_tvt).astype(np.float32),
        "ktvt_range":sc(float(np.ptp(ktvt))),"ktvt_std":sc(float(ktvt.std())),"md_since":md_since,"frac":frac,"frac2":frac**2,"sqrt_frac":np.sqrt(frac),
        "z":z_ev,"dx":(ev.X-float(lk.X)).to_numpy(np.float32),"dy":(ev.Y-float(lk.Y)).to_numpy(np.float32),"dz":(z_ev-float(lk.Z)).astype(np.float32),
        "dxy":np.sqrt((ev.X-float(lk.X))**2+(ev.Y-float(lk.Y))**2).to_numpy(np.float32),"dzdmd":dzdmd,"dxdmd":dxdmd,"dydmd":dydmd,
        "gr":hgr,"gr_d1":gr_d1,"gr_d2":gr_d2,"gr_env":gr_env,"gr_nrg":gr_nrg,
        "gr_vs_tw_anc":hgr-np.float32(np.interp(last_tvt,tw_tvt,tw_gr)),"gr_vs_slp_all":hgr-np.interp(slp_b_all,tw_tvt,tw_gr).astype(np.float32),
        **{f"tda{int(o)}":hgr-np.float32(np.interp(last_tvt+o,tw_tvt,tw_gr)) for o in ANCH_OFFS},
        **{f"tdbc{int(o)}":hgr-np.interp(beam_ref+o,tw_tvt,tw_gr).astype(np.float32) for o in BEAM_OFFS},
        **{f"tdsc{int(o)}":hgr-np.interp(sc_ens+o,tw_tvt,tw_gr).astype(np.float32) for o in SC_OFFS},
        **{f"tdpf{int(o)}":hgr-np.interp(pf_use+o,tw_tvt,tw_gr).astype(np.float32) for o in PF_OFFS},
        "tw_range":sc(float(np.ptp(tw_tvt))),"tw_gr_mean":sc(float(tw_gr.mean()))}
    for k,v in rolls.items(): feats[k]=v
    res = pd.DataFrame(feats)
    if is_train: res["target"]=(ev.TVT.to_numpy(np.float32)-np.float32(last_tvt))
    return res

def init_imputers(train_wids):
    global _FI, _DI
    _FI = FormationPlaneKNN(train_wids, CFG.DATA/"train"); _DI = DenseANCCImputer(train_wids, CFG.DATA/"train")

def _likpf_rows(wid, split):
    hw, tw = load_well(wid, split)
    out, idx, _ = lik_pf(hw, tw)
    if not len(out): return None
    d = {"id": [f"{wid}_{i}" for i in idx]}
    for k, v in out.items():
        d["likpf_" + k.replace("pf_scale_", "scale_").replace("pf_mean", "mean")] = v.astype(np.float32)
    return pd.DataFrame(d)

def build_likpf(wids, split):
    # threads are safe here: the lik-PF numba kernel is compiled with nogil=True, so it
    # releases the GIL and parallelises across threads (no pickling of numba code needed).
    res = Parallel(n_jobs=CFG.n_jobs, prefer="threads")(delayed(_likpf_rows)(w, split) for w in wids)
    return pd.concat([r for r in res if r is not None], ignore_index=True)

def build_features(wids, split, is_train):
    paths = [CFG.DATA/split/f"{w}__horizontal_well.csv" for w in wids]
    res = Parallel(n_jobs=CFG.n_jobs, prefer="threads")(
        delayed(build_well)(str(p), str(p.parent/f"{p.stem.replace('__horizontal_well','')}__typewell.csv"), is_train)
        for p in paths if (p.parent/f"{p.stem.replace('__horizontal_well','')}__typewell.csv").exists())
    parts = [r for r in res if r is not None]
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()

def add_likpf_features(df, likpf):
    df = df.merge(likpf, on="id", how="left")
    for c in [c for c in likpf.columns if c != "id"]:
        df[c] = df[c].fillna(df["last_known_tvt"]); df[c+"_d"] = (df[c]-df["last_known_tvt"]).astype(np.float32)
    return df

# %% cell 13
def _device():
    if CFG.USE_GPU == "cpu": return "cpu", "CPU"
    if CFG.USE_GPU == "gpu": return "gpu", "GPU"
    try:  # detect a real NVIDIA GPU (Kaggle GPU accelerator) via nvidia-smi
        import subprocess
        if subprocess.run(["nvidia-smi"], capture_output=True).returncode == 0:
            return "gpu", "GPU"
    except Exception:
        pass
    return "cpu", "CPU"

def lgb_configs(dev):
    base = dict(boosting_type="gbdt", objective="regression", verbose=-1, n_jobs=-1, max_bin=255)
    if dev == "gpu": base.update(device_type="gpu", gpu_use_dp=False)
    n = 600 if CFG.FAST else 5000
    return [
        dict(**base, num_leaves=255, min_child_samples=15, subsample=0.8, subsample_freq=1,
             colsample_bytree=0.8, reg_lambda=3.0, reg_alpha=0.05, learning_rate=0.03, n_estimators=n, seed=123),
        dict(**base, num_leaves=64, min_child_samples=40, subsample=0.474, subsample_freq=1,
             colsample_bytree=0.393, reg_lambda=95.75, reg_alpha=10.79, min_child_weight=0.24,
             learning_rate=0.0093, n_estimators=min(2*n, 10000), random_state=0),
        dict(**base, num_leaves=64, min_child_samples=40, subsample=0.474, subsample_freq=1,
             colsample_bytree=0.393, reg_lambda=95.75, reg_alpha=10.79, min_child_weight=0.24,
             learning_rate=0.0093, n_estimators=min(2*n, 10000), random_state=29),
    ]

def cb_configs(dev):
    tt = "GPU" if dev == "gpu" else "CPU"
    n = 800 if CFG.FAST else 8000
    return [
        dict(iterations=n, depth=7, l2_leaf_reg=2.0, min_data_in_leaf=15, border_count=254,
             loss_function="RMSE", task_type=tt, od_type="Iter", od_wait=300, verbose=0, learning_rate=0.02, random_seed=7),
        dict(iterations=n, depth=7, l2_leaf_reg=2.0, min_data_in_leaf=15, border_count=254,
             loss_function="RMSE", task_type=tt, od_type="Iter", od_wait=300, verbose=0, learning_rate=0.03, random_seed=123),
    ]

def train_stack(train_df, test_df, features):
    from lightgbm import LGBMRegressor, early_stopping, log_evaluation
    from catboost import CatBoostRegressor
    from sklearn.model_selection import GroupKFold
    from sklearn.linear_model import Ridge
    dev, devname = _device(); print("device:", devname)
    X = train_df[features].values.astype(np.float32); y = train_df["target"].values.astype(np.float32)
    g = train_df["well"].values; Xt = test_df[features].values.astype(np.float32)
    cv = GroupKFold(CFG.n_splits); oof_cols = {}; test_cols = {}
    def run(name, make, fit_kw, is_lgb):
        # LightGBM: slice to best_iteration_ via num_iteration. CatBoost: use_best_model
        # already trims to the best tree, and its predict() takes no num_iteration kwarg.
        oof = np.zeros(len(train_df)); tp = np.zeros(len(test_df))
        for tr, va in cv.split(X, y, groups=g):
            m = make(); m.fit(X[tr], y[tr], eval_set=[(X[va], y[va])], **fit_kw)
            if is_lgb:
                it = m.best_iteration_
                oof[va] = m.predict(X[va], num_iteration=it); tp += m.predict(Xt, num_iteration=it) / CFG.n_splits
            else:
                oof[va] = m.predict(X[va]); tp += m.predict(Xt) / CFG.n_splits
        oof_cols[name] = oof; test_cols[name] = tp
        print(f"  {name}: OOF RMSE={rmse(y, oof):.4f}", flush=True)
    for i, p in enumerate(lgb_configs(dev)):
        run(f"lgb{i}", lambda p=p: LGBMRegressor(**p),
            dict(eval_metric="rmse", callbacks=[early_stopping(250, verbose=False), log_evaluation(0)]), True)
    for i, p in enumerate(cb_configs(dev)):
        run(f"cb{i}", lambda p=p: CatBoostRegressor(**p),
            dict(early_stopping_rounds=250, use_best_model=True), False)
    OOF = pd.DataFrame(oof_cols); TEST = pd.DataFrame(test_cols)
    rid = Ridge(alpha=1.66, positive=True, fit_intercept=True); meta = np.zeros(len(train_df))
    for tr, va in cv.split(OOF.values, y, groups=g):
        rid.fit(OOF.values[tr], y[tr]); meta[va] = rid.predict(OOF.values[va])
    rid.fit(OOF.values, y); meta_test = rid.predict(TEST.values)
    print(f"  ridge-stack OOF RMSE={rmse(y, meta):.4f}")
    return meta, meta_test, OOF, TEST

# %% cell 14
class PP:   # tuned on 773-well GroupKFold OOF (Nelder-Mead + grid; the optimum is flat)
    alpha = 1.0         # global scale on the learned delta (tuned ~1.0)
    tau = 85.0          # warm-up length in ft: damps the first feet after PS (tuned ~90)
    w_pf = 0.0          # blending the model with the single PF no longer helps once lik-PF is a feature
    w_sub1 = 0.60       # weight on the learned model; lik-PF gets 1-w_sub1. CV optimum ~0.68 (flat
                        # 0.55-0.68); 0.60 is a small hedge toward the drift-robust lik-PF for LB transfer.
    sub2_scale = "scale_5"   # which likelihood-scale of the lik-PF to use as sub2 (3/5/8 ~equivalent)
    sg_win = 61         # per-well Savitzky-Golay smoothing window (effect is small, ~0.01 ft)
    sg_poly = 3

def warmup(md_since, tau): return 1.-np.exp(-np.maximum(md_since, 0.)/tau) if tau > 1e-6 else 1.0

def make_prediction(df, model_delta, likpf):
    last = df["last_known_tvt"].values.astype(float)
    pf_delta = df["pf_ancc"].values.astype(float) - last
    lp = df[f"likpf_{PP.sub2_scale}"].values.astype(float) - last
    sub1 = PP.alpha*warmup(df["md_since"].values.astype(float), PP.tau)*(model_delta*(1-PP.w_pf)+pf_delta*PP.w_pf)
    delta = PP.w_sub1*sub1 + (1-PP.w_sub1)*lp
    pred = last + delta
    # per-well Savitzky-Golay smoothing
    out = pred.copy(); dfx = df.reset_index(drop=True)
    for _, idx in dfx.groupby("well", sort=False).groups.items():
        pos = dfx.index.get_indexer(idx); v = pred[pos]; n = len(v); wl = min(PP.sg_win, n)
        if wl % 2 == 0: wl -= 1
        if wl >= PP.sg_poly+2: out[pos] = savgol_filter(v, wl, PP.sg_poly)
    return out

# %% [markdown]
# ## 6. SP45 candidate engine - physics, multi-scale lik-PF, beam, selector
# 
# `tvt_from_contacts` is the closed-form geometric reconstruction. `run_pf_lik_ensemble_scales`
# runs the 128-seed likelihood-weighted PF at scales 3/5/8/12; `run_beam_ensemble` uses the numba
# beam (bound above); `selector_well_code`/`apply_selector_variant` pick the per-well blend that
# won on GroupKFold OOF. (The reference notebook's slower NumPy beam duplicate is removed - the
# numba beam defined in section 4 is bound here, matching the original deployed behaviour.)

# %% cell 16
SELECTOR_N_EVAL_THRESHOLD = 4840.0
SELECTOR_Z_SPAN_THRESHOLDS = (136.73000000000016, 185.5133333333342)

SELECTOR_BIN_VARIANTS = {
    0: 'pf_scale_5_hold_0.2',
    1: 'pf_scale_3_hold_0.15',
    2: 'pf_scale_12_beam_0.2_hold_0.15',
    3: 'pf_scale_5_hold_0.15',
    4: 'pf_scale_5_beam_0.05_hold_0.05',
    5: 'pf_scale_12_beam_0.2_hold_0.05',
}

SELECTOR_GLOBAL_VARIANT = 'pf_scale_8_hold_0.2'
SELECTOR_SCALES = (3.0, 5.0, 8.0, 12.0)

FORMATION_COLS = ['ANCC', 'ASTNU', 'ASTNL', 'EGFDU', 'EGFDL', 'BUDA']

BEAM_CONFIGS = [
    (10, 20.0, 144.0, 2),
    (10,  8.0,  64.0, 2),
    ( 8, 35.0, 220.0, 1),
    (10, 14.0,  90.0, 5),
    (20,  4.0,  36.0, 3),
    (12, 12.0, 100.0, 3),
    (15, 25.0, 180.0, 2),
    (20, 30.0, 200.0, 2),
    (15, 10.0,  80.0, 4),
    (25,  6.0,  50.0, 3),
    (10, 40.0, 300.0, 1),
    (12, 18.0, 120.0, 5),
    (30,  8.0,  70.0, 2),
    (10, 50.0, 400.0, 0),
]


def tvt_from_contacts(hw_tr, tw_tr, ref_col='EGFDU'):
    tw_g = tw_tr.dropna(subset=['Geology'])
    ref_tvt = tw_g[tw_g['Geology'] == ref_col]['TVT'].min()
    if np.isnan(ref_tvt):
        ref_col = tw_g['Geology'].iloc[0]
        ref_tvt = tw_g[tw_g['Geology'] == ref_col]['TVT'].min()
    offset = (hw_tr['TVT'] - (ref_tvt - (hw_tr['Z'] - hw_tr[ref_col]))).mean()
    return ref_tvt - (hw_tr['Z'] - hw_tr[ref_col]) + offset


def load_well(wid, split='train'):
    base = CFG.dataset_path / split
    hw = pd.read_csv(base / f'{wid}__horizontal_well.csv')
    tw = pd.read_csv(base / f'{wid}__typewell.csv')
    return hw, tw


def run_particle_filter(hw, tw, n_particles=500, seed=42):
    tw_s   = tw.sort_values('TVT')
    tw_tvt = tw_s['TVT'].values.astype(float)
    tw_gr  = tw_s['GR'].fillna(tw_s['GR'].mean()).values.astype(float)

    kn = hw[hw['TVT_input'].notna()]
    ev = hw[hw['TVT_input'].isna()]
    if len(ev) == 0:
        return hw['TVT_input'].values.astype(float).copy(), 0.0

    last     = kn.iloc[-1]
    last_tvt = float(last['TVT_input'])
    last_Z   = float(last['Z'])
    last_MD  = float(last['MD'])

    tw_at_k = np.interp(kn['TVT_input'].values, tw_tvt, tw_gr)
    gs = float(np.clip(np.nanstd(kn['GR'].fillna(0).values - tw_at_k), 10., 60.))

    tail = kn.tail(30)
    dt = np.diff(tail['TVT_input'].values)
    dz = np.diff(tail['Z'].values)
    dm = np.diff(tail['MD'].values)
    m  = dm > 0
    ir = float(np.median((dt + dz)[m] / dm[m])) if m.sum() >= 3 else 0.0

    N   = n_particles
    rng = np.random.default_rng(seed)
    ls   = last_tvt + last_Z
    pos  = ls + 4.5 * rng.standard_normal(N)  # sp45 patch (sel15 vb best)
    rate = ir + 0.01 * rng.standard_normal(N)
    w    = np.ones(N) / N

    MOM = 0.998; VN = 0.002; PN = 0.005; RP = 0.1; RR = 0.001; RESAMP = 0.5

    md_v = ev['MD'].values.astype(float)
    z_v  = ev['Z'].values.astype(float)
    # Interpolate GR gaps before tracking
    gr_interp = hw['GR'].interpolate(limit_direction='both').fillna(tw_gr.mean())
    gr_v = gr_interp.values.astype(float)[ev.index]

    out_vals = hw['TVT_input'].values.astype(float).copy()
    res = np.empty(len(ev))
    prev_MD = last_MD
    log_lik = 0.0

    for i in range(len(ev)):
        dm_step = max(md_v[i] - prev_MD, 1.0)
        rate = MOM * rate + VN * rng.standard_normal(N)
        pos  = pos + rate * dm_step + PN * rng.standard_normal(N)
        tvt_p = pos - z_v[i]
        tvt_p = np.clip(tvt_p, tw_tvt[0] - 100, tw_tvt[-1] + 100)
        pos   = tvt_p + z_v[i]

        eg = np.interp(tvt_p, tw_tvt, tw_gr)
        d  = (gr_v[i] - eg) / gs
        lk = np.exp(-0.5 * np.minimum(d**2, 600.))
        lk = np.maximum(lk, 1e-300)
        avg_lk = float((w * lk).sum())
        log_lik += np.log(max(avg_lk, 1e-300))
        w = w * lk
        ws = w.sum()
        w = w / ws if ws > 0 else np.ones(N) / N

        n_eff = 1.0 / (w**2).sum()
        if n_eff < RESAMP * N:
            cum = np.cumsum(w)
            u0  = rng.uniform(0, 1.0 / N)
            idx = np.clip(np.searchsorted(cum, u0 + np.arange(N) / N), 0, N - 1)
            pos  = pos[idx]  + RP * rng.standard_normal(N)
            rate = rate[idx] + RR * rng.standard_normal(N)
            w    = np.ones(N) / N

        res[i] = float(np.dot(w, pos - z_v[i]))
        prev_MD = md_v[i]

    out_vals[list(ev.index)] = res
    return out_vals, log_lik


def run_pf_lik_ensemble(hw, tw, n_particles=500, n_seeds=128, scale=5.0):
    preds = []
    liks  = []
    for s in range(n_seeds):
        p, ll = run_particle_filter(hw, tw, n_particles=n_particles, seed=s)
        preds.append(p)
        liks.append(ll)

    liks   = np.array(liks)
    liks_n = liks - liks.max()
    weights = np.exp(liks_n / scale)
    weights /= weights.sum()

    return (weights[:, None] * np.stack(preds, 0)).sum(0)


def run_pf_lik_ensemble_scales(hw, tw, scales=SELECTOR_SCALES, n_particles=500, n_seeds=128):
    preds = []
    liks = []
    for s in range(n_seeds):
        p, ll = run_particle_filter(hw, tw, n_particles=n_particles, seed=s)
        preds.append(p)
        liks.append(ll)
    pred_arr = np.stack(preds, 0)
    liks = np.array(liks)
    liks_n = liks - liks.max()
    out = {}
    for scale in scales:
        weights = np.exp(liks_n / float(scale))
        weights /= weights.sum()
        out[f'pf_scale_{scale:g}'] = (weights[:, None] * pred_arr).sum(0)
    out['pf_mean'] = pred_arr.mean(0)
    return out


# (NumPy beam_search removed; numba beam_search from section 4 is bound here)

def run_beam_ensemble(hw, tw):
    kn = hw[hw['TVT_input'].notna()]
    ev = hw[hw['TVT_input'].isna()]
    if len(ev) == 0:
        return hw['TVT_input'].values.astype(float).copy()

    last_tvt = float(kn.iloc[-1]['TVT_input'])
    tw_s  = tw.sort_values('TVT')
    tw_tvt = tw_s['TVT'].values.astype(float)
    tw_gr  = tw_s['GR'].fillna(tw_s['GR'].mean()).values.astype(float)

    gr_all = hw['GR'].interpolate(limit_direction='both').fillna(tw_gr.mean()).values.astype(float)
    hgr    = gr_all[ev.index]

    beam_results = [beam_search(hgr, tw_tvt, tw_gr, last_tvt, bs, mc, es, r)
                    for (bs, mc, es, r) in BEAM_CONFIGS]

    beam_mean = np.stack(beam_results, 0).mean(0)

    out = hw['TVT_input'].values.astype(float).copy()
    out[list(ev.index)] = beam_mean
    return out


def selector_well_code(hw):
    eval_mask = hw['TVT_input'].isna().to_numpy()
    n_eval = float(eval_mask.sum())
    z_eval = hw.loc[eval_mask, 'Z'].values.astype(float)
    z_span = float(np.nanmax(z_eval) - np.nanmin(z_eval)) if len(z_eval) else 0.0
    n_bin = int(n_eval > SELECTOR_N_EVAL_THRESHOLD)
    z_bin = int(np.searchsorted(SELECTOR_Z_SPAN_THRESHOLDS, z_span, side='right'))
    code = n_bin + 2 * z_bin
    variant = SELECTOR_BIN_VARIANTS.get(code, SELECTOR_GLOBAL_VARIANT)
    return code, variant, n_eval, z_span


def parse_selector_variant(name):
    parts = name.split('_')
    scale = float(parts[2])
    beam_weight = 0.0
    hold_weight = 0.0
    if 'beam' in parts:
        beam_weight = float(parts[parts.index('beam') + 1])
    if 'hold' in parts:
        hold_weight = float(parts[parts.index('hold') + 1])
    return scale, beam_weight, hold_weight


def apply_selector_variant(name, pf_by_scale, tvt_beam, last_known_tvt):
    scale, beam_weight, hold_weight = parse_selector_variant(name)
    base = pf_by_scale.get(f'pf_scale_{scale:g}')
    if base is None:
        base = pf_by_scale[SELECTOR_GLOBAL_VARIANT.split('_beam_')[0].split('_hold_')[0]]
    pred = (1.0 - beam_weight) * base + beam_weight * tvt_beam
    pred = (1.0 - hold_weight) * pred + hold_weight * last_known_tvt
    return pred

# %% [markdown]
# ## 7. Optional boosted stack (LightGBM x3 + CatBoost x2 -> Ridge), koolbox-free
# 
# The reference notebook trained this with `koolbox.Trainer`, a hard import that crashed the whole
# run when the offline wheel failed. Here it is a **pure sklearn `GroupKFold`** stack. It runs
# **only** when the ravaghi precomputed-feature artifact (`train.csv` *and* `test.csv`) is mounted,
# and contributes `0.3*stack` to the pre-projection SP45 blend - exactly the original composition.
# If the artifact is absent or any step fails, it returns `None` and the SP45 candidate degrades
# cleanly to pure physics/PF/beam/selector. The learned-model signal still enters the final blend
# through the fleongg candidate (section 10) at weight 0.45.

# %% cell 18

def _artifact_csv(name):
    """Find train.csv/test.csv under the artifact dir (root or /data)."""
    if ARTIFACT_DIR is None:
        return None
    for c in (ARTIFACT_DIR / name, ARTIFACT_DIR / "data" / name):
        if c.is_file():
            return c
    return None

def _apply_pp(df, model_delta, pf_delta, alpha=1.0, tau=85.0, w_pf=0.09):
    d = model_delta * (1 - w_pf) + pf_delta * w_pf
    if tau:
        d = d * (1.0 - np.exp(-np.maximum(df["md_since"].values.astype(float), 0.0) / tau))
    return d * alpha

def _sg_smooth_col(df, col, sg_w=17, sg_p=3):
    df = df.copy()
    for _, g in df.groupby("well", sort=False):
        v = g[col].values.astype(float); n = len(v); wl = min(sg_w, n)
        if wl % 2 == 0: wl -= 1
        if wl >= sg_p + 2:
            v = savgol_filter(v, wl, sg_p)
        df.loc[g.index, col] = v
    return df

def build_boosted_stack_from_artifact():
    """Return {id: tvt} from a sklearn GroupKFold LGB+Cat->Ridge stack on the artifact, or None."""
    tr_path, te_path = _artifact_csv("train.csv"), _artifact_csv("test.csv")
    if tr_path is None or te_path is None or not (HAVE_LGB and HAVE_CAT):
        print("boosted stack: artifact train/test.csv or lgb/catboost missing -> skipped")
        return None
    try:
        train_df = pd.read_csv(tr_path, low_memory=False)
        test_df  = pd.read_csv(te_path, low_memory=False)
        need = {"well", "id", "target", "last_known_tvt", "pf_ancc", "md_since"}
        if not need.issubset(train_df.columns) or not {"id", "last_known_tvt", "pf_ancc", "md_since"}.issubset(test_df.columns):
            print("boosted stack: artifact missing required columns -> skipped")
            return None
        feats = [c for c in train_df.columns if c not in {"well", "id", "target"} and c in test_df.columns]
        X  = train_df[feats].values.astype(np.float32)
        y  = train_df["target"].values.astype(np.float32)
        g  = train_df["well"].values
        Xt = test_df[feats].values.astype(np.float32)

        from lightgbm import LGBMRegressor, early_stopping, log_evaluation
        from catboost import CatBoostRegressor
        dev, lbl = device(); print("boosted stack device:", lbl)
        base = dict(objective="regression", verbose=-1, n_jobs=-1, max_bin=255, boosting_type="gbdt")
        if dev == "gpu": base.update(device_type="gpu", gpu_use_dp=False)
        n = 600 if CFG.FAST else 5000
        lgb_cfgs = [
            dict(**base, num_leaves=255, min_child_samples=15, subsample=0.8, subsample_freq=1,
                 colsample_bytree=0.8, reg_lambda=3.0, reg_alpha=0.05, learning_rate=0.03, n_estimators=n, seed=123),
            dict(**base, num_leaves=64, min_child_samples=40, subsample=0.4744, subsample_freq=1,
                 colsample_bytree=0.3928, reg_lambda=95.754, reg_alpha=10.788, min_child_weight=0.2408,
                 learning_rate=0.009345, n_estimators=min(2*n, 10000), random_state=0),
            dict(**base, num_leaves=64, min_child_samples=40, subsample=0.4744, subsample_freq=1,
                 colsample_bytree=0.3928, reg_lambda=95.754, reg_alpha=10.788, min_child_weight=0.2408,
                 learning_rate=0.009345, n_estimators=min(2*n, 10000), random_state=29),
        ]
        tt = "GPU" if dev == "gpu" else "CPU"
        nc = 800 if CFG.FAST else 8000
        cat_cfgs = [
            dict(iterations=nc, depth=7, l2_leaf_reg=2.0, min_data_in_leaf=15, border_count=254,
                 loss_function="RMSE", task_type=tt, od_type="Iter", od_wait=300, verbose=0, learning_rate=0.02, random_seed=7),
            dict(iterations=nc, depth=7, l2_leaf_reg=2.0, min_data_in_leaf=15, border_count=254,
                 loss_function="RMSE", task_type=tt, od_type="Iter", od_wait=300, verbose=0, learning_rate=0.03, random_seed=123),
        ]
        cv = GroupKFold(CFG.n_splits)
        oof_cols, test_cols = {}, {}
        def _run(name, make, fit_kw, is_lgb):
            oof = np.zeros(len(train_df)); tp = np.zeros(len(test_df))
            for tr, va in cv.split(X, y, groups=g):
                m = make(); m.fit(X[tr], y[tr], eval_set=[(X[va], y[va])], **fit_kw)
                if is_lgb:
                    it = m.best_iteration_
                    oof[va] = m.predict(X[va], num_iteration=it); tp += m.predict(Xt, num_iteration=it) / CFG.n_splits
                else:
                    oof[va] = m.predict(X[va]); tp += m.predict(Xt) / CFG.n_splits
            oof_cols[name] = oof; test_cols[name] = tp
            print(f"  {name}: OOF RMSE(delta)={rmse(y, oof):.4f}", flush=True)
        for i, p in enumerate(lgb_cfgs):
            _run(f"lgb{i}", lambda p=p: LGBMRegressor(**p),
                 dict(eval_metric="rmse", callbacks=[early_stopping(250, verbose=False), log_evaluation(0)]), True)
        for i, p in enumerate(cat_cfgs):
            _run(f"cb{i}", lambda p=p: CatBoostRegressor(**p),
                 dict(early_stopping_rounds=250, use_best_model=True), False)
        OOF = pd.DataFrame(oof_cols).values; TEST = pd.DataFrame(test_cols).values
        rid = Ridge(alpha=1.66, positive=True, fit_intercept=True)
        rid.fit(OOF, y); meta_test = rid.predict(TEST)

        pf_test = test_df["pf_ancc"].values.astype(float) - test_df["last_known_tvt"].values.astype(float)
        test_df = test_df.copy()
        test_df["pred"] = test_df["last_known_tvt"].values.astype(float) + _apply_pp(test_df, meta_test, pf_test)
        test_df = _sg_smooth_col(test_df, "pred")
        out = dict(zip(test_df["id"].astype(str), test_df["pred"].astype(float)))
        print(f"boosted stack OK: {len(feats)} feats, {len(out)} test preds")
        return out
    except Exception as e:
        print("boosted stack failed (kept physics/PF only):", e)
        return None

BOOSTED = build_boosted_stack_from_artifact()
if BOOSTED is not None:
    POSTPROCESSORS.append("boosted_stack_0.3")

# %% [markdown]
# ## 8. SP45 candidate - per-well tracking, MD-safe, robust ids
# 
# For every test well we run the 128-seed lik-PF ensemble, the beam ensemble, and the learned
# selector. We map predictions back by **within-well row index** parsed via `rsplit('_', 1)`
# (never fixed-width slicing). **The reference notebook's unsafe `hw_te['TVT_input'] =
# hw_tr['TVT_input'].values` row-index copy is removed** - exact-overlap gain is recovered later
# by the MD-validated guarded contact override (section 11), which is `>=` the blend by
# construction. If the boosted stack exists, the pre-projection blend is `0.3*stack + 0.7*PF`;
# otherwise it is pure PF/selector.

# %% cell 20

def build_sp45_candidate():
    sample = pd.read_csv(CFG.DATA / "sample_submission.csv")
    sample["well"], sample["row_idx"] = split_id(sample["id"])
    test_wells = list_wells("test")
    fallback = float("nan")

    sub2 = {}                                          # physics/PF/beam/selector
    for i, wid in enumerate(test_wells, 1):
        hw_te, tw_te = load_well(wid, "test")
        try:
            pf_by_scale = run_pf_lik_ensemble_scales(
                hw_te, tw_te, n_particles=CFG.PF_PARTICLES, n_seeds=CFG.PF_SEEDS)
        except Exception as e:
            print(f"  [{wid}] PF failed ({e}); last-known fallback")
            lk = hw_te["TVT_input"].dropna()
            lv = float(lk.iloc[-1]) if len(lk) else 0.0
            tvt = hw_te["TVT_input"].fillna(lv).values.astype(float)
            pf_by_scale = {f"pf_scale_{s:g}": tvt.copy() for s in SELECTOR_SCALES}
        try:
            tvt_beam = run_beam_ensemble(hw_te, tw_te)
        except Exception as e:
            print(f"  [{wid}] beam failed ({e})"); tvt_beam = pf_by_scale["pf_scale_8"].copy()

        code, variant, n_eval, z_span = selector_well_code(hw_te)
        lk = hw_te["TVT_input"].dropna()
        last_known = float(lk.iloc[-1]) if len(lk) else float(np.nanmean(pf_by_scale["pf_scale_8"]))
        tvt_sel = apply_selector_variant(variant, pf_by_scale, tvt_beam, last_known)

        g = sample[sample["well"] == wid]
        for rid, ridx in zip(g["id"].astype(str).values, g["row_idx"].astype(int).values):
            if 0 <= ridx < len(tvt_sel) and np.isfinite(tvt_sel[ridx]):
                sub2[rid] = float(tvt_sel[ridx])
        print(f"  [{i}/{len(test_wells)}] {wid}: variant={variant} n_eval={n_eval:.0f} z_span={z_span:.1f} rows={len(g)}")

    # global fallback value for any missing id
    vals = np.array(list(sub2.values()), float)
    fb = float(np.nanmean(vals)) if len(vals) else 0.0

    sub = sample[["id"]].copy()
    s2 = sub["id"].astype(str).map(sub2).astype(float)
    if BOOSTED is not None:
        s1 = sub["id"].astype(str).map(BOOSTED).astype(float)
        s1 = s1.where(np.isfinite(s1), s2)             # missing stack rows -> physics
        blended = 0.3 * s1 + 0.7 * s2
    else:
        blended = s2
    sub["tvt"] = blended.where(np.isfinite(blended), fb).astype(float)
    return sub

_sp45 = build_sp45_candidate()
_sp45.to_csv(OUT / "submission.csv", index=False)      # working copy for the projection step
print("SP45 pre-projection written:", _sp45.shape)
POSTPROCESSORS.append("sp45_pf_beam_selector")

# %% [markdown]
# ## 9. Robust low-order projection post-process
# 
# Per well, robustly fit `dU = TVT + Z - anchor` against normalised MD with an IRLS deg-4
# polynomial (Tukey-style reweighting), then blend `0.25*raw + 0.75*fit`. This denoises PF jitter
# and down-weights wrong-branch outliers. Defensive per-well fallback to raw; ids parsed robustly.
# Overwrites the working `submission.csv` and saves it as the SP45 candidate.

# %% cell 22

def _robfit(s, y, deg=4):
    if len(s) < deg + 2:
        return y.copy()
    c = np.polyfit(s, y, deg)
    for _ in range(4):
        r = y - np.polyval(c, s)
        sc = np.median(np.abs(r)) * 1.4826 + 1e-6
        c = np.polyfit(s, y, deg, w=1.0 / (1.0 + (r / (2.0 * sc)) ** 2))
    return np.polyval(c, s)

def apply_projection():
    base = pd.read_csv(OUT / "submission.csv")
    base["well"], base["row_idx"] = split_id(base["id"])
    out = dict(zip(base["id"].astype(str).values, base["tvt"].astype(float).values))
    n_ok = 0
    for wid, g in base.groupby("well"):
        try:
            hw = pd.read_csv(CFG.DATA / "test" / f"{wid}__horizontal_well.csv")
            kn = hw[hw["TVT_input"].notna()]
            if len(kn) < 5:
                continue
            last = kn.iloc[-1]
            anchor = float(last["TVT_input"]) + float(last["Z"])
            ps, end = float(last["MD"]), float(hw["MD"].iloc[-1])
            gi = g.sort_values("row_idx")
            ri = gi["row_idx"].values.astype(int)
            Z  = hw["Z"].values[ri].astype(float)
            md = hw["MD"].values[ri].astype(float)
            s  = (md - ps) / max(end - ps, 1e-6)
            tvt = gi["tvt"].values.astype(float)
            fit_full = (anchor + _robfit(s, (tvt + Z) - anchor, 4)) - Z
            tvt_fit = 0.25 * tvt + 0.75 * fit_full
            if not np.all(np.isfinite(tvt_fit)):
                continue
            for rid, v in zip(gi["id"].astype(str).values, tvt_fit):
                out[rid] = float(v)
            n_ok += 1
        except Exception as e:
            print("  proj fallback", wid, e)
    final = base[["id"]].copy()
    final["tvt"] = final["id"].astype(str).map(out).astype(float)
    final[["id", "tvt"]].to_csv(OUT / "submission.csv", index=False)
    final[["id", "tvt"]].to_csv(OUT / "sp45_projection_submission.csv", index=False)
    print(f"projection applied to {n_ok} wells; SP45 candidate saved", final.shape)

apply_projection()
POSTPROCESSORS.append("sp45_projection_deg4")

# %% [markdown]
# ## 10. fleongg candidate (pretrained inference, with offline fallbacks)
# 
# Priority: (1) if a pretrained-booster dataset (`lgb*.pkl` + `features.json`) is mounted, run the
# modern feature build + inference; (2) else if an offline `fleongg_pretrained_submission.csv` is
# attached and its ids cover the sample, use it directly (fast, stable); (3) else if
# `ROGII_TRAIN_FROM_SCRATCH=1`, train the modern stack live; (4) else the fleongg candidate equals
# SP45 so the final blend becomes a clean no-op. This guarantees a valid candidate with no internet.

# %% cell 24

def _find_models():
    for f in glob.glob("/kaggle/input/**/features.json", recursive=True):
        d = Path(f).parent
        if list(d.glob("lgb*.pkl")):
            return d
    d = OUT / "models"
    return d if (d / "features.json").exists() and list(d.glob("lgb*.pkl")) else None

def build_fleongg_candidate(sample):
    ids = sample["id"].astype(str)
    models_dir = _find_models()

    # (1) pretrained inference -----------------------------------------------------
    if models_dir is not None:
        try:
            print("fleongg: INFERENCE from", models_dir, flush=True)
            train_wids = list_wells("train")
            test_wids  = list_wells("test")
            if CFG.N_TRAIN_WELLS:
                train_wids = train_wids[:CFG.N_TRAIN_WELLS]
            init_imputers(train_wids)
            likpf_test = build_likpf(test_wids, "test")
            test_df = add_likpf_features(build_features(test_wids, "test", is_train=False), likpf_test).reset_index(drop=True)
            feats = json.load(open(models_dir / "features.json"))
            for c in feats:
                if c not in test_df.columns: test_df[c] = 0.0
            Xt = test_df[feats].values.astype(np.float32)
            models = [joblib.load(p) for p in sorted(models_dir.glob("lgb*.pkl"))]
            meta_test = np.mean([m.predict(Xt) for m in models], axis=0)
            test_pred = make_prediction(test_df, meta_test, None)
            fb = float(np.nanmean(test_df["last_known_tvt"].to_numpy(float)))
            out = sample[["id"]].copy()
            out["tvt"] = ids.map(dict(zip(test_df["id"].astype(str), test_pred))).astype(float)
            _bad = ~np.isfinite(out["tvt"].to_numpy(float))
            if _bad.any():
                out.loc[_bad, "tvt"] = fb
                print(f"fleongg inference: clamped {int(_bad.sum())} non-finite preds to fallback", flush=True)
            POSTPROCESSORS.append("fleongg_pretrained_inference")
            return out
        except Exception as e:
            print("fleongg inference failed -> trying offline fallbacks:", e)

    # (2) offline csv that covers the sample ---------------------------------------
    if FLEONGG_CSV is not None:
        try:
            f = pd.read_csv(FLEONGG_CSV)[["id", "tvt"]].copy()
            f["id"] = f["id"].astype(str)
            cover = set(f["id"])
            if set(ids).issubset(cover) and np.isfinite(f["tvt"].to_numpy(float)).all():
                out = sample[["id"]].copy()
                out["tvt"] = ids.map(dict(zip(f["id"], f["tvt"].astype(float)))).astype(float)
                print(f"fleongg: using offline csv {FLEONGG_CSV.name} (covers all sample ids)")
                POSTPROCESSORS.append("fleongg_offline_csv")
                return out
            print("fleongg: offline csv does not cover sample ids -> skip")
        except Exception as e:
            print("fleongg offline csv failed:", e)

    # (3) train from scratch (opt-in; slow) ----------------------------------------
    if os.environ.get("ROGII_TRAIN_FROM_SCRATCH", "0") == "1" and HAVE_LGB and HAVE_CAT:
        try:
            print("fleongg: TRAIN from scratch (ROGII_TRAIN_FROM_SCRATCH=1)", flush=True)
            train_wids = list_wells("train"); test_wids = list_wells("test")
            if CFG.N_TRAIN_WELLS: train_wids = train_wids[:CFG.N_TRAIN_WELLS]
            init_imputers(train_wids)
            likpf_tr = build_likpf(train_wids, "train"); likpf_te = build_likpf(test_wids, "test")
            train_df = add_likpf_features(build_features(train_wids, "train", True), likpf_tr)
            test_df  = add_likpf_features(build_features(test_wids, "test", False), likpf_te).reset_index(drop=True)
            feats = [c for c in train_df.columns if c not in {"well","id","target"}
                     and not (c.startswith("likpf_scale_") or c == "likpf_mean") and c in test_df.columns]
            _, meta_test, _, _ = train_stack(train_df, test_df, feats)
            test_pred = make_prediction(test_df, meta_test, None)
            fb = float(train_df["last_known_tvt"].mean() + train_df["target"].mean())
            out = sample[["id"]].copy()
            out["tvt"] = ids.map(dict(zip(test_df["id"].astype(str), test_pred))).fillna(fb).astype(float)
            POSTPROCESSORS.append("fleongg_trained_from_scratch")
            return out
        except Exception as e:
            print("fleongg train-from-scratch failed:", e)

    # (4) degrade to SP45 (blend no-op) --------------------------------------------
    print("fleongg: no model/csv -> candidate = SP45 (blend becomes no-op)")
    out = pd.read_csv(OUT / "sp45_projection_submission.csv")[["id", "tvt"]].copy()
    POSTPROCESSORS.append("fleongg_equals_sp45")
    return out

_sample = pd.read_csv(CFG.DATA / "sample_submission.csv")
_fleongg = build_fleongg_candidate(_sample)
_fleongg[["id", "tvt"]].to_csv(OUT / "submission.csv", index=False)            # fleongg candidate
_fleongg[["id", "tvt"]].to_csv(OUT / "fleongg_pretrained_submission.csv", index=False)
print("fleongg candidate written:", _fleongg.shape)

# %% [markdown]
# ## 11. Final blend - `0.55*SP45 + 0.45*fleongg`
# 
# Inner-join on id (count-checked), sweep candidate weights for the report, write the selected
# `0.55/0.45` blend. Both inputs are validated for finiteness first.

# %% cell 26

def _read_sub(path, label):
    f = pd.read_csv(path)[["id", "tvt"]].copy()
    f["id"] = f["id"].astype(str); f["tvt"] = f["tvt"].astype(float)
    if not np.isfinite(f["tvt"].to_numpy(float)).all():
        raise RuntimeError(f"non-finite tvt in {label}")
    return f

BLEND_W_SP45 = 0.55
sp45 = _read_sub(OUT / "sp45_projection_submission.csv", "sp45")
fle  = _read_sub(OUT / "submission.csv", "fleongg")
m = sp45.rename(columns={"tvt": "tvt_sp45"}).merge(
        fle.rename(columns={"tvt": "tvt_fle"}), on="id", how="inner")
if not (len(m) == len(sp45) == len(fle)):
    raise RuntimeError(f"blend id mismatch sp45={len(sp45)} fle={len(fle)} merged={len(m)}")

rows = []
for w in (0.50, 0.52, 0.55, 0.58, 0.60):
    tvt = w * m["tvt_sp45"] + (1 - w) * m["tvt_fle"]
    diff = (tvt - m["tvt_sp45"]).to_numpy(float)
    rows.append(dict(w_sp45=w, rows=len(m), mean=float(tvt.mean()), std=float(tvt.std()),
                     rmse_vs_sp45=float(np.sqrt((diff**2).mean())),
                     p95_abs=float(np.quantile(np.abs(diff), 0.95))))
pd.DataFrame(rows).to_csv(OUT / "sp45_fleongg_blend_report.csv", index=False)
print(pd.DataFrame(rows).to_string(index=False))

blend = m[["id"]].copy()
blend["tvt"] = (BLEND_W_SP45 * m["tvt_sp45"] + (1 - BLEND_W_SP45) * m["tvt_fle"]).astype(float)
# preserve sample id order exactly
order = pd.read_csv(CFG.DATA / "sample_submission.csv")["id"].astype(str)
blend = blend.set_index("id").reindex(order).reset_index()
assert blend["tvt"].notna().all(), "blend lost ids vs sample"
blend[["id", "tvt"]].to_csv(OUT / "submission.csv", index=False)
print(f"final blend written (w_sp45={BLEND_W_SP45}):", blend.shape)
POSTPROCESSORS.append(f"final_blend_sp45_{BLEND_W_SP45:.2f}")

# --- learned-signal (no-op) detection -------------------------------------------
_blend_max_rmse = max(r["rmse_vs_sp45"] for r in rows)
LEARNED_FLEONGG_ACTIVE = _blend_max_rmse > 1e-6
if not LEARNED_FLEONGG_ACTIVE:
    print("\n[!] BLEND INACTIVE: fleongg candidate == SP45 (rmse_vs_sp45=0 at every weight).")
    print("    The 0.45 learned branch contributed nothing; result is pure physics/PF + override.")
    print("    Attach fleongg 'rogii-claude-models-pub' (or the offline CSV) to activate it.")
else:
    print(f"[ok] fleongg branch active (max rmse_vs_sp45={_blend_max_rmse:.3f}).")

# %% [markdown]
# ## 12. Guarded contact override (MD-validated, deterministic)
# 
# For every well that also exists in train, reconstruct `TVT` from the **train** typewell contacts,
# sort by MD, and self-check against the **test** copy's visible prefix interpolated **by MD**.
# Override only if (a) >= 100 valid reconstructed rows, (b) >= 50 comparable known-prefix rows in
# the train MD range, and (c) known-prefix RMSE < 1.0 ft. Otherwise keep the blend. Ids parsed via
# `rsplit`; no row-index alignment. Deterministic and `>=` the blend by construction.

# %% cell 28

def tvt_from_contacts_arr(hw_tr, tw_tr, ref_col="EGFDU"):
    tw_g = tw_tr.dropna(subset=["Geology"])
    ref_tvt = tw_g[tw_g["Geology"] == ref_col]["TVT"].min()
    if np.isnan(ref_tvt):
        ref_col = tw_g["Geology"].iloc[0]
        ref_tvt = tw_g[tw_g["Geology"] == ref_col]["TVT"].min()
    offset = (hw_tr["TVT"] - (ref_tvt - (hw_tr["Z"] - hw_tr[ref_col]))).mean()
    return (ref_tvt - (hw_tr["Z"] - hw_tr[ref_col]) + offset).to_numpy(float)

def guarded_contact_override():
    sub = pd.read_csv(OUT / "submission.csv")
    well, row_idx = split_id(sub["id"])
    sub["well"], sub["row_idx"] = well, row_idx
    pred = dict(zip(sub["id"].astype(str), sub["tvt"].astype(float)))
    train_wells = set(list_wells("train"))
    n_ok = n_skip = 0
    for wid, g in sub.groupby("well"):
        if wid not in train_wells:
            continue
        try:
            hw_te = pd.read_csv(CFG.DATA / "test"  / f"{wid}__horizontal_well.csv")
            hw_tr = pd.read_csv(CFG.DATA / "train" / f"{wid}__horizontal_well.csv")
            tw_tr = pd.read_csv(CFG.DATA / "train" / f"{wid}__typewell.csv")
            phys = tvt_from_contacts_arr(hw_tr, tw_tr)
            md_raw = hw_tr["MD"].to_numpy(float)
            mfin = np.isfinite(phys) & np.isfinite(md_raw)
            if mfin.sum() < 100:
                n_skip += 1; continue
            o = np.argsort(md_raw[mfin]); md_tr = md_raw[mfin][o]; ph_tr = phys[mfin][o]
            kn = hw_te[hw_te["TVT_input"].notna()]
            kn = kn[(kn["MD"] >= md_tr[0]) & (kn["MD"] <= md_tr[-1])]
            if len(kn) < 50:
                n_skip += 1; continue
            rk = float(np.sqrt(np.mean(
                (np.interp(kn["MD"].to_numpy(float), md_tr, ph_tr) - kn["TVT_input"].to_numpy(float)) ** 2)))
            if not np.isfinite(rk) or rk > 1.0:
                print(f"  override SKIP {wid} known-prefix rmse={rk:.3f} (keeping blend)"); n_skip += 1; continue
            md_te = hw_te["MD"].to_numpy(float); n_row = 0
            for rid, ri in zip(g["id"].astype(str).values, g["row_idx"].astype(int).values):
                if 0 <= ri < len(md_te) and md_tr[0] <= md_te[ri] <= md_tr[-1]:
                    pred[rid] = float(np.interp(md_te[ri], md_tr, ph_tr)); n_row += 1
            print(f"  override OK {wid} rmse={rk:.4f} rows={n_row}/{len(g)}"); n_ok += 1
        except Exception as e:
            print("  override fallback", wid, e); n_skip += 1
    new = sub["id"].astype(str).map(pred).astype(float)
    assert new.notna().all() and np.isfinite(new.to_numpy(float)).all(), "override produced NaN"
    # disagreement audit: distance between the blended candidate (which carries any learned
    # signal) and the contact-interpolated truth on override wells. Large gap => the learned
    # model would generalize poorly to unseen wells, where no override can rescue it.
    _pre = sub["tvt"].astype(float).to_numpy(); _post = new.to_numpy(float)
    _da = pd.DataFrame({"well": sub["well"].values, "d": np.abs(_pre - _post)})
    for _wid, _gg in _da[_da["well"].isin(train_wells)].groupby("well"):
        if len(_gg):
            print(f"  disagree {_wid}: blend-vs-contact mean={_gg['d'].mean():.2f} "
                  f"p95={_gg['d'].quantile(.95):.2f} max={_gg['d'].max():.2f}")
    sub["tvt"] = new
    sub[["id", "tvt"]].to_csv(OUT / "submission.csv", index=False)
    print(f"guarded override done: overridden={n_ok} skipped={n_skip}")
    return n_ok

_n_override = guarded_contact_override()
if _n_override:
    POSTPROCESSORS.append("guarded_contact_override")

# %% [markdown]
# ## 13. Strict submission audit (deterministic)
# 
# Re-reads `submission.csv` against `sample_submission.csv`: columns exactly `["id","tvt"]`, equal
# row count, identical id order, all tvt finite, no duplicate ids. Writes `submission_audit.json`.

# %% cell 30

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def strict_audit(tag, write_json=False):
    sub = pd.read_csv(OUT / "submission.csv")
    sample = pd.read_csv(CFG.DATA / "sample_submission.csv")
    assert list(sub.columns) == ["id", "tvt"], f"columns {list(sub.columns)}"
    assert len(sub) == len(sample), f"rows {len(sub)} vs {len(sample)}"
    assert sub["id"].astype(str).equals(sample["id"].astype(str)), "id order != sample"
    assert not sub["id"].duplicated().any(), "duplicate ids"
    tvt = sub["tvt"].to_numpy(float)
    assert np.isfinite(tvt).all(), "non-finite tvt"
    info = dict(rows=int(len(sub)), columns=list(sub.columns), id_order_matches_sample=True,
                tvt_min=float(tvt.min()), tvt_max=float(tvt.max()),
                tvt_mean=float(tvt.mean()), tvt_std=float(tvt.std()),
                sha256_submission_csv=sha256_file(OUT / "submission.csv"))
    if write_json:
        with open(OUT / "submission_audit.json", "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, sort_keys=True)
    print(f"audit[{tag}] OK:", info)
    return info

_audit_blend = strict_audit("post-override", write_json=True)
# keep an inspectable pre-gold anchor
pd.read_csv(OUT / "submission.csv").to_csv(OUT / "submission_pre_gold.csv", index=False)

# %% [markdown]
# ## 14. Conservative gold visible-prefix calibration
# 
# Carried from the reference pipeline (LB-validated), mojibake-normalised, and **wrapped so any
# failure cannot halt the notebook** - on error the audited blend+override submission is kept. It
# makes a per-well move only when a backtest on the visible prefix proves a geology/PF candidate
# beats the default tracker; `ROGII_GOLD_PROFILE=conservative` is the default. On a hidden test set
# with no train overlap, the move conditions rarely fire, so the public anchor is preserved.

# %% cell 32
def _run_gold_calibration():

    # Gold visible-prefix calibration overlay.
    # It runs AFTER the public final blend and guarded contact override.
    # The public submission remains the anchor; this layer only makes a per-well move
    # when the visible-prefix backtest says a geology/PF candidate beats the default tracker.
    import os as _gold_os
    import glob as _gold_glob
    import json as _gold_json
    import time as _gold_time
    import hashlib as _gold_hashlib
    from pathlib import Path as _GoldPath

    import numpy as _gold_np
    import pandas as _gold_pd

    _GOLD_ENABLE = _gold_os.environ.get('ROGII_GOLD_PREFIX_CAL', '1') == '1'
    _GOLD_PROFILE = _gold_os.environ.get('ROGII_GOLD_PROFILE', 'balanced').strip().lower()
    _GOLD_INCLUDE_PF = _gold_os.environ.get('ROGII_GOLD_INCLUDE_PF', '1') == '1'
    _GOLD_CAL_SEEDS = int(_gold_os.environ.get('ROGII_GOLD_CAL_SEEDS', '24'))
    _GOLD_FINAL_SEEDS = int(_gold_os.environ.get('ROGII_GOLD_FINAL_SEEDS', '48'))
    _GOLD_PARTICLES = int(_gold_os.environ.get('ROGII_GOLD_PARTICLES', '350'))
    _GOLD_CUT_FRACS = tuple(float(x) for x in _gold_os.environ.get('ROGII_GOLD_CUT_FRACS', '0.55,0.70,0.84').split(',') if x.strip())
    _GOLD_MAX_WELLS = int(_gold_os.environ.get('ROGII_GOLD_MAX_WELLS', '1000000'))

    _GOLD_PROFILES = {
        'conservative': dict(min_gain=1.00, max_best=9.0, min_consistency=0.67, base=0.06, gain_scale=0.12, margin_scale=0.04, quality_bonus=0.02, cap=0.22, clip_base=8.0, clip_gain=3.0, clip_max=18.0, delta_soft=22.0, p95_hard=55.0),
        'balanced':     dict(min_gain=0.55, max_best=12.0, min_consistency=0.50, base=0.08, gain_scale=0.20, margin_scale=0.06, quality_bonus=0.04, cap=0.36, clip_base=10.0, clip_gain=4.5, clip_max=28.0, delta_soft=30.0, p95_hard=75.0),
        'aggressive':   dict(min_gain=0.25, max_best=15.0, min_consistency=0.34, base=0.12, gain_scale=0.32, margin_scale=0.10, quality_bonus=0.06, cap=0.56, clip_base=14.0, clip_gain=7.0, clip_max=45.0, delta_soft=42.0, p95_hard=110.0),
    }
    if _GOLD_PROFILE not in _GOLD_PROFILES:
        print(f'Unknown ROGII_GOLD_PROFILE={_GOLD_PROFILE!r}; using balanced')
        _GOLD_PROFILE = 'balanced'


    def _gold_work_dir():
        return _GoldPath('/kaggle/working') if _GoldPath('/kaggle/working').exists() else _GoldPath('.')


    def _gold_find_data():
        candidates = []
        obj = globals().get('CFG')
        if obj is not None:
            for attr in ('dataset_path', 'DATA'):
                if hasattr(obj, attr):
                    candidates.append(_GoldPath(getattr(obj, attr)))
        candidates.extend([
            _GoldPath('/kaggle/input/competitions/rogii-wellbore-geology-prediction'),
            _GoldPath('/kaggle/input/rogii-wellbore-geology-prediction'),
            _GoldPath('.'),
        ])
        for c in candidates:
            try:
                if (c / 'train').exists() and (c / 'test').exists() and (c / 'sample_submission.csv').exists():
                    return c
            except Exception:
                pass
        for p in _gold_glob.glob('/kaggle/input/**/sample_submission.csv', recursive=True):
            c = _GoldPath(p).parent
            if (c / 'train').exists() and (c / 'test').exists():
                return c
        raise RuntimeError('Could not locate ROGII data directory')


    def _gold_split_ids(df):
        out = df.copy()
        parts = out['id'].astype(str).str.rsplit('_', n=1, expand=True)
        if parts.shape[1] != 2:
            raise RuntimeError('Unexpected id format; expected well_rowindex')
        out['well'] = parts[0]
        out['row_idx'] = parts[1].astype(int)
        return out


    def _gold_rmse(a, b):
        a = _gold_np.asarray(a, dtype=float)
        b = _gold_np.asarray(b, dtype=float)
        m = _gold_np.isfinite(a) & _gold_np.isfinite(b)
        if int(m.sum()) == 0:
            return float('inf')
        d = a[m] - b[m]
        return float(_gold_np.sqrt(_gold_np.mean(d * d)))


    def _gold_sha256(path):
        h = _gold_hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''):
                h.update(chunk)
        return h.hexdigest()


    def _gold_robust_poly_predict(x_known, y_known, x_all, deg):
        x_known = _gold_np.asarray(x_known, dtype=float)
        y_known = _gold_np.asarray(y_known, dtype=float)
        x_all = _gold_np.asarray(x_all, dtype=float)
        m = _gold_np.isfinite(x_known) & _gold_np.isfinite(y_known)
        x_known = x_known[m]
        y_known = y_known[m]
        if len(x_known) < 3:
            fill = float(_gold_np.nanmedian(y_known)) if len(y_known) else 0.0
            return _gold_np.full_like(x_all, fill, dtype=float)
        deg = int(min(max(1, deg), len(x_known) - 1))
        x0 = float(x_known[0])
        xs = float(_gold_np.nanmax(x_known) - _gold_np.nanmin(x_known))
        if (not _gold_np.isfinite(xs)) or xs < 1e-6:
            xs = 1.0
        xk = (x_known - x0) / xs
        xa = (x_all - x0) / xs
        try:
            coef = _gold_np.polyfit(xk, y_known, deg)
            for _ in range(5):
                fit = _gold_np.polyval(coef, xk)
                res = y_known - fit
                sc = 1.4826 * float(_gold_np.nanmedian(_gold_np.abs(res - _gold_np.nanmedian(res)))) + 1e-6
                weights = 1.0 / (1.0 + (res / (2.5 * sc)) ** 2)
                coef = _gold_np.polyfit(xk, y_known, deg, w=weights)
            return _gold_np.polyval(coef, xa).astype(float)
        except Exception:
            return _gold_np.full_like(x_all, float(_gold_np.nanmedian(y_known)), dtype=float)


    def _gold_variant_grid():
        variants = set()
        try:
            variants.update(SELECTOR_BIN_VARIANTS.values())
            variants.add(SELECTOR_GLOBAL_VARIANT)
        except Exception:
            pass
        for scale in (3, 5, 8, 12):
            for hold in (0.0, 0.05, 0.10, 0.15, 0.20, 0.25):
                variants.add(f'pf_scale_{scale:g}_hold_{hold:g}')
            for beam in (0.05, 0.10, 0.20, 0.30):
                for hold in (0.0, 0.05, 0.10, 0.15, 0.20):
                    variants.add(f'pf_scale_{scale:g}_beam_{beam:g}_hold_{hold:g}')
        return sorted(variants)


    def _gold_tvt_from_contacts(hw_tr, tw_tr, ref_col='EGFDU'):
        tw_g = tw_tr.dropna(subset=['Geology']) if 'Geology' in tw_tr.columns else tw_tr.copy()
        if 'Geology' in tw_g.columns and ref_col in hw_tr.columns:
            ref_tvt = tw_g.loc[tw_g['Geology'] == ref_col, 'TVT'].min()
            if _gold_np.isnan(ref_tvt):
                ref_col = tw_g['Geology'].iloc[0]
                ref_tvt = tw_g.loc[tw_g['Geology'] == ref_col, 'TVT'].min()
            offset = (hw_tr['TVT'] - (ref_tvt - (hw_tr['Z'] - hw_tr[ref_col]))).mean()
            return (ref_tvt - (hw_tr['Z'] - hw_tr[ref_col]) + offset).to_numpy(dtype=float)
        return hw_tr['TVT'].to_numpy(dtype=float)


    def _gold_contact_candidate(wid, hw, data_dir):
        out = {}
        try:
            hw_tr_path = data_dir / 'train' / f'{wid}__horizontal_well.csv'
            tw_tr_path = data_dir / 'train' / f'{wid}__typewell.csv'
            if not hw_tr_path.exists() or not tw_tr_path.exists():
                return out
            hw_tr = _gold_pd.read_csv(hw_tr_path)
            tw_tr = _gold_pd.read_csv(tw_tr_path)
            phys = _gold_tvt_from_contacts(hw_tr, tw_tr)
            md = hw_tr['MD'].to_numpy(dtype=float)
            m = _gold_np.isfinite(md) & _gold_np.isfinite(phys)
            if int(m.sum()) < 100:
                return out
            order = _gold_np.argsort(md[m])
            md_s = md[m][order]
            ph_s = phys[m][order]
            pred = _gold_np.interp(hw['MD'].to_numpy(dtype=float), md_s, ph_s, left=_gold_np.nan, right=_gold_np.nan)
            out['contact_md_lookup'] = pred.astype(float)
        except Exception:
            return out
        return out


    def _gold_poly_candidates(hw_masked):
        out = {}
        tvt = hw_masked['TVT_input'].to_numpy(dtype=float)
        md = hw_masked['MD'].to_numpy(dtype=float)
        z = hw_masked['Z'].to_numpy(dtype=float)
        kn = _gold_np.flatnonzero(_gold_np.isfinite(tvt) & _gold_np.isfinite(md) & _gold_np.isfinite(z))
        if len(kn) < 30:
            return out
        u = tvt + z
        for tail in (80, 160, 320, 640, 1000000):
            sel = kn[-min(int(tail), len(kn)):]
            if len(sel) < 30:
                continue
            tag = 'all' if tail >= 1000000 else f'tail{tail}'
            for deg in (1, 2, 3):
                if len(sel) < deg + 12:
                    continue
                uhat = _gold_robust_poly_predict(md[sel], u[sel], md, deg)
                out[f'poly_u_deg{deg}_{tag}'] = (uhat - z).astype(float)
        return out


    def _gold_surface_candidates(hw_masked, wid, data_dir):
        out = {}
        tvt = hw_masked['TVT_input'].to_numpy(dtype=float)
        z = hw_masked['Z'].to_numpy(dtype=float)
        xy = hw_masked[['X', 'Y']].to_numpy(dtype=float)
        kn = _gold_np.isfinite(tvt) & _gold_np.isfinite(z) & _gold_np.isfinite(xy).all(axis=1)
        if int(kn.sum()) < 30:
            return out
        formations = list(globals().get('FORMATIONS', ['ANCC', 'ASTNU', 'ASTNL', 'EGFDU', 'EGFDL', 'BUDA']))
        fi = globals().get('_FI', globals().get('FI', None))
        di = globals().get('_DI', globals().get('DI', None))
        surf_names = []
        try:
            if fi is not None:
                form_all, _ = fi.impute(xy, self_wid=None)
                form_all = _gold_np.asarray(form_all, dtype=float)
                for i, fn in enumerate(formations[:form_all.shape[1]]):
                    f = form_all[:, i]
                    good = kn & _gold_np.isfinite(f)
                    if int(good.sum()) < 30:
                        continue
                    b_med = float(_gold_np.nanmedian(tvt[good] + z[good] - f[good]))
                    out[f'surface_{fn}_median'] = (-z + f + b_med).astype(float)
                    surf_names.append(f'surface_{fn}_median')
                    if callable(globals().get('seg_b_well')):
                        try:
                            b_full, _, _, b_late, b_wls = seg_b_well(
                                tvt[good].astype(_gold_np.float32),
                                z[good].astype(_gold_np.float32),
                                f[good].astype(_gold_np.float32),
                            )
                            out[f'surface_{fn}_full'] = (-z + f + float(b_full)).astype(float)
                            out[f'surface_{fn}_late'] = (-z + f + float(b_late)).astype(float)
                            out[f'surface_{fn}_wls'] = (-z + f + float(b_wls)).astype(float)
                            surf_names.extend([f'surface_{fn}_full', f'surface_{fn}_late', f'surface_{fn}_wls'])
                        except Exception:
                            pass
        except Exception as e:
            print('surface imputer skipped', wid, e)
        try:
            if di is not None:
                dense, _, _ = di.impute(xy, self_wid=None)
                dense = _gold_np.asarray(dense, dtype=float)
                good = kn & _gold_np.isfinite(dense)
                if int(good.sum()) >= 30:
                    b_med = float(_gold_np.nanmedian(tvt[good] + z[good] - dense[good]))
                    out['dense_ancc_median'] = (-z + dense + b_med).astype(float)
                    surf_names.append('dense_ancc_median')
                    if callable(globals().get('seg_b_well')):
                        try:
                            b_full, _, _, b_late, b_wls = seg_b_well(
                                tvt[good].astype(_gold_np.float32),
                                z[good].astype(_gold_np.float32),
                                dense[good].astype(_gold_np.float32),
                            )
                            out['dense_ancc_full'] = (-z + dense + float(b_full)).astype(float)
                            out['dense_ancc_late'] = (-z + dense + float(b_late)).astype(float)
                            out['dense_ancc_wls'] = (-z + dense + float(b_wls)).astype(float)
                            surf_names.extend(['dense_ancc_full', 'dense_ancc_late', 'dense_ancc_wls'])
                        except Exception:
                            pass
        except Exception as e:
            print('dense imputer skipped', wid, e)
        ens_names = [n for n in surf_names if n in out]
        if len(ens_names) >= 2:
            errs = _gold_np.array([_gold_rmse(out[n][kn], tvt[kn]) for n in ens_names], dtype=float)
            finite = _gold_np.isfinite(errs)
            if int(finite.sum()) >= 2:
                names = [n for n, ok in zip(ens_names, finite) if ok]
                errs = errs[finite]
                weights = 1.0 / _gold_np.maximum(errs, 0.25) ** 2
                weights = weights / weights.sum()
                mat = _gold_np.vstack([out[n] for n in names])
                out['surface_weighted_prefix'] = (weights[:, None] * mat).sum(axis=0).astype(float)
        out.update(_gold_contact_candidate(wid, hw_masked, data_dir))
        return out


    def _gold_pf_candidates(hw_masked, tw, variants, n_seeds, n_particles):
        out = {}
        if not _GOLD_INCLUDE_PF:
            return out
        if not callable(globals().get('run_pf_lik_ensemble_scales')) or not callable(globals().get('apply_selector_variant')):
            return out
        kn = hw_masked[hw_masked['TVT_input'].notna()]
        ev = hw_masked[hw_masked['TVT_input'].isna()]
        if len(kn) < 30 or len(ev) == 0:
            return out
        try:
            pf_by_scale = run_pf_lik_ensemble_scales(
                hw_masked,
                tw,
                scales=tuple(globals().get('SELECTOR_SCALES', (3.0, 5.0, 8.0, 12.0))),
                n_particles=int(n_particles),
                n_seeds=int(n_seeds),
            )
            try:
                tvt_beam = run_beam_ensemble(hw_masked, tw)
            except Exception:
                tvt_beam = pf_by_scale.get('pf_mean')
                if tvt_beam is None:
                    tvt_beam = next(iter(pf_by_scale.values()))
            last_known_tvt = float(kn['TVT_input'].iloc[-1])
            for variant in variants:
                try:
                    pred = apply_selector_variant(variant, pf_by_scale, tvt_beam, last_known_tvt)
                    if pred is not None and len(pred) == len(hw_masked):
                        out['pf|' + variant] = _gold_np.asarray(pred, dtype=float)
                except Exception:
                    pass
        except Exception as e:
            print('PF calibration skipped:', e)
        return out


    def _gold_candidate_pool(wid, hw_masked, tw, data_dir, variants, include_pf=True, n_seeds=24, n_particles=350):
        pool = {}
        pool.update(_gold_poly_candidates(hw_masked))
        pool.update(_gold_surface_candidates(hw_masked, wid, data_dir))
        if include_pf:
            pool.update(_gold_pf_candidates(hw_masked, tw, variants, n_seeds=n_seeds, n_particles=n_particles))
        clean = {}
        for name, pred in pool.items():
            arr = _gold_np.asarray(pred, dtype=float)
            if len(arr) == len(hw_masked) and _gold_np.isfinite(arr).sum() >= max(20, len(hw_masked) // 20):
                clean[name] = arr
        return clean


    def _gold_default_pf_name(hw):
        try:
            return 'pf|' + selector_well_code(hw)[1]
        except Exception:
            try:
                return 'pf|' + SELECTOR_GLOBAL_VARIANT
            except Exception:
                return None


    def _gold_calibrate_well(wid, hw, tw, data_dir, variants):
        tvt = hw['TVT_input'].to_numpy(dtype=float)
        is_known = _gold_np.isfinite(tvt)
        is_hidden = ~is_known
        if not bool(is_hidden.any()):
            return None
        first_hidden = int(_gold_np.flatnonzero(is_hidden)[0])
        known_prefix = _gold_np.flatnonzero(is_known & (_gold_np.arange(len(hw)) < first_hidden))
        if len(known_prefix) < 140:
            return dict(well=wid, status='skip_short_prefix', known_prefix=int(len(known_prefix)))
        cuts = []
        for frac in _GOLD_CUT_FRACS:
            cut_pos = int(round(len(known_prefix) * float(frac)))
            cut_pos = max(50, min(cut_pos, len(known_prefix) - 35))
            if cut_pos <= 0 or cut_pos >= len(known_prefix):
                continue
            cutoff_idx = int(known_prefix[cut_pos - 1])
            hold_idx = known_prefix[cut_pos:]
            if len(hold_idx) >= 35:
                cuts.append((float(frac), cutoff_idx, hold_idx))
        if not cuts:
            return dict(well=wid, status='skip_no_holdout', known_prefix=int(len(known_prefix)))
        scores = {}
        cut_rows = []
        default_name = _gold_default_pf_name(hw)
        for frac, cutoff_idx, hold_idx in cuts:
            hw_m = hw.copy(deep=True)
            hw_m.loc[hw_m.index > cutoff_idx, 'TVT_input'] = _gold_np.nan
            pool = _gold_candidate_pool(
                wid, hw_m, tw, data_dir, variants,
                include_pf=_GOLD_INCLUDE_PF,
                n_seeds=_GOLD_CAL_SEEDS,
                n_particles=_GOLD_PARTICLES,
            )
            y = tvt[hold_idx]
            row = {'well': wid, 'cut_frac': frac, 'holdout_rows': int(len(hold_idx)), 'candidates': int(len(pool))}
            local = []
            for name, pred in pool.items():
                err = _gold_rmse(pred[hold_idx], y)
                if _gold_np.isfinite(err):
                    scores.setdefault(name, []).append(err)
                    local.append((err, name))
            local.sort()
            if local:
                row['best_name'] = local[0][1]
                row['best_rmse'] = float(local[0][0])
                if default_name in pool:
                    row['default_rmse'] = float(_gold_rmse(pool[default_name][hold_idx], y))
                else:
                    row['default_rmse'] = float('nan')
            cut_rows.append(row)
        if not scores:
            return dict(well=wid, status='skip_no_scores', known_prefix=int(len(known_prefix)))
        agg = {}
        for name, vals in scores.items():
            vals = _gold_np.asarray(vals, dtype=float)
            agg[name] = float(_gold_np.nanmedian(vals) + 0.10 * _gold_np.nanstd(vals))
        ordered = sorted((v, k) for k, v in agg.items() if _gold_np.isfinite(v))
        if not ordered:
            return dict(well=wid, status='skip_nonfinite_scores', known_prefix=int(len(known_prefix)))
        best_score, best_name = ordered[0]
        second_score = ordered[1][0] if len(ordered) > 1 else best_score
        if default_name is not None and default_name in agg:
            default_score = float(agg[default_name])
        else:
            pf_scores = [v for k, v in agg.items() if k.startswith('pf|')]
            default_score = float(_gold_np.nanmedian(pf_scores)) if pf_scores else float(second_score)
        consistency = 0.0
        comparable = 0
        for row in cut_rows:
            if _gold_np.isfinite(row.get('default_rmse', _gold_np.nan)):
                comparable += 1
                if row.get('best_rmse', float('inf')) <= row['default_rmse'] - 0.25:
                    consistency += 1.0
        if comparable:
            consistency /= comparable
        else:
            winners = [r.get('best_name') for r in cut_rows if r.get('best_name')]
            consistency = float(sum(w == best_name for w in winners)) / max(1, len(winners))
        return dict(
            well=wid,
            status='ok',
            known_prefix=int(len(known_prefix)),
            cuts=int(len(cut_rows)),
            candidate_count=int(len(agg)),
            best_name=best_name,
            best_score=float(best_score),
            second_score=float(second_score),
            default_name=default_name,
            default_score=float(default_score),
            gain=float(default_score - best_score),
            rank_margin=float(second_score - best_score),
            consistency=float(consistency),
            cut_rows=cut_rows,
        )


    def _gold_alpha(report, delta_rmse, delta_p95, profile_name):
        p = _GOLD_PROFILES[profile_name]
        if report.get('status') != 'ok':
            return 0.0
        gain = float(report.get('gain', 0.0))
        best = float(report.get('best_score', float('inf')))
        margin = float(report.get('rank_margin', 0.0))
        consistency = float(report.get('consistency', 0.0))
        if (not _gold_np.isfinite(best)) or best > p['max_best'] or gain < p['min_gain'] or consistency < p['min_consistency']:
            return 0.0
        alpha = p['base']
        alpha += p['gain_scale'] * min(max(gain, 0.0), 5.0) / 5.0
        alpha += p['margin_scale'] * min(max(margin, 0.0), 3.0) / 3.0
        if best <= 5.0:
            alpha += p['quality_bonus']
        best_name = str(report.get('best_name', ''))
        if (best_name.startswith('surface_') or best_name.startswith('dense_') or best_name.startswith('poly_') or best_name.startswith('contact_')) and consistency >= 0.67:
            alpha += 0.03 if profile_name != 'aggressive' else 0.06
        if _gold_np.isfinite(delta_rmse) and delta_rmse > p['delta_soft']:
            alpha *= max(0.20, p['delta_soft'] / max(delta_rmse, 1e-6))
        if _gold_np.isfinite(delta_p95) and delta_p95 > p['p95_hard']:
            return 0.0
        return float(min(p['cap'], max(0.0, alpha)))


    def _gold_profile_output(base_sub, candidate_by_id, reports_by_well, profile_name):
        prof = _GOLD_PROFILES[profile_name]
        out = base_sub.copy()
        move_rows = []
        for wid, rep in reports_by_well.items():
            ids = out.loc[out['well'] == wid, 'id'].astype(str).tolist()
            if not ids:
                continue
            cand = _gold_np.array([candidate_by_id.get(i, _gold_np.nan) for i in ids], dtype=float)
            idx = out.index[out['well'] == wid].to_numpy()
            base = out.loc[idx, 'tvt'].to_numpy(dtype=float)
            ok = _gold_np.isfinite(cand) & _gold_np.isfinite(base)
            if int(ok.sum()) != len(base):
                rep = dict(rep)
                rep['apply_status'] = 'skip_nonfinite_candidate'
                move_rows.append(rep)
                continue
            diff = cand - base
            delta_rmse = float(_gold_np.sqrt(_gold_np.mean(diff * diff))) if len(diff) else float('nan')
            delta_p95 = float(_gold_np.quantile(_gold_np.abs(diff), 0.95)) if len(diff) else float('nan')
            alpha = _gold_alpha(rep, delta_rmse, delta_p95, profile_name)
            gain = max(0.0, float(rep.get('gain', 0.0)))
            max_move = min(prof['clip_max'], prof['clip_base'] + prof['clip_gain'] * _gold_np.sqrt(gain + 1e-9))
            ramp = 1.0 - _gold_np.exp(-_gold_np.arange(len(diff), dtype=float) / max(80.0, 0.12 * max(1, len(diff))))
            move = _gold_np.clip(alpha * ramp * diff, -max_move, max_move)
            out.loc[idx, 'tvt'] = base + move
            row = dict(rep)
            row.update(dict(
                profile=profile_name,
                alpha=float(alpha),
                delta_rmse_vs_public=float(delta_rmse),
                delta_p95_vs_public=float(delta_p95),
                max_move_clip=float(max_move),
                applied_rows=int(len(idx)),
                mean_abs_move=float(_gold_np.mean(_gold_np.abs(move))) if len(move) else 0.0,
                max_abs_move=float(_gold_np.max(_gold_np.abs(move))) if len(move) else 0.0,
                apply_status='applied' if alpha > 0 else 'kept_public',
            ))
            move_rows.append(row)
        return out, move_rows


    def _gold_reapply_guarded_contact_override(sub_df, data_dir):
        sub = _gold_split_ids(sub_df[['id', 'tvt']])
        pred = dict(zip(sub['id'].astype(str), sub['tvt'].astype(float)))
        train_wells = set(p.stem.replace('__horizontal_well', '') for p in (data_dir / 'train').glob('*__horizontal_well.csv'))
        n_ok = 0
        n_skip = 0
        for wid, g in sub.groupby('well'):
            if wid not in train_wells:
                continue
            try:
                hw_te = _gold_pd.read_csv(data_dir / 'test' / f'{wid}__horizontal_well.csv')
                hw_tr = _gold_pd.read_csv(data_dir / 'train' / f'{wid}__horizontal_well.csv')
                tw_tr = _gold_pd.read_csv(data_dir / 'train' / f'{wid}__typewell.csv')
                phys = _gold_tvt_from_contacts(hw_tr, tw_tr)
                md_raw = hw_tr['MD'].to_numpy(dtype=float)
                m = _gold_np.isfinite(phys) & _gold_np.isfinite(md_raw)
                if int(m.sum()) < 100:
                    n_skip += 1
                    continue
                order = _gold_np.argsort(md_raw[m])
                md_tr = md_raw[m][order]
                ph_tr = phys[m][order]
                kn = hw_te[hw_te['TVT_input'].notna()]
                kn = kn[(kn['MD'] >= md_tr[0]) & (kn['MD'] <= md_tr[-1])]
                if len(kn) < 50:
                    n_skip += 1
                    continue
                rk = _gold_rmse(_gold_np.interp(kn['MD'].to_numpy(dtype=float), md_tr, ph_tr), kn['TVT_input'].to_numpy(dtype=float))
                if (not _gold_np.isfinite(rk)) or rk > 1.0:
                    n_skip += 1
                    continue
                md_te = hw_te['MD'].to_numpy(dtype=float)
                n_row = 0
                for rid, ri in zip(g['id'].astype(str).values, g['row_idx'].values):
                    ri = int(ri)
                    if 0 <= ri < len(md_te):
                        mte = float(md_te[ri])
                        if md_tr[0] <= mte <= md_tr[-1]:
                            pred[rid] = float(_gold_np.interp(mte, md_tr, ph_tr))
                            n_row += 1
                print('gold contact override OK %s rmse=%.4f rows=%d/%d' % (wid, rk, n_row, len(g)))
                n_ok += 1
            except Exception as e:
                print('gold contact override fallback', wid, e)
                n_skip += 1
        sub['tvt'] = sub['id'].astype(str).map(pred).astype(float)
        print('gold contact override done: overridden=%d skipped=%d' % (n_ok, n_skip))
        return sub[['id', 'tvt']]


    def _gold_validate_and_write(sub, sample, path):
        out = sub[['id', 'tvt']].copy()
        out['id'] = out['id'].astype(str)
        out['tvt'] = out['tvt'].astype(float)
        if list(out.columns) != ['id', 'tvt']:
            raise RuntimeError('bad output columns')
        if len(out) != len(sample):
            raise RuntimeError('bad output length')
        if not out['id'].equals(sample['id'].astype(str)):
            raise RuntimeError('id order mismatch')
        if not _gold_np.isfinite(out['tvt'].to_numpy(dtype=float)).all():
            raise RuntimeError('non-finite tvt in output')
        out.to_csv(path, index=False)
        return out


    if not _GOLD_ENABLE:
        print('Gold visible-prefix calibration disabled; keeping public submission.csv')
    else:
        _gold_t0 = _gold_time.time()
        _GOLD_WORK = _gold_work_dir()
        _GOLD_DATA = _gold_find_data()
        _gold_sample = _gold_pd.read_csv(_GOLD_DATA / 'sample_submission.csv')[['id']].copy()
        _gold_sample['id'] = _gold_sample['id'].astype(str)
        _gold_base = _gold_pd.read_csv(_GOLD_WORK / 'submission.csv')[['id', 'tvt']].copy()
        _gold_base['id'] = _gold_base['id'].astype(str)
        _gold_base['tvt'] = _gold_base['tvt'].astype(float)
        _gold_validate_and_write(_gold_base, _gold_sample, _GOLD_WORK / 'submission_public_self_verified.csv')
        _gold_base = _gold_split_ids(_gold_base)
        _gold_variants = _gold_variant_grid()
        print('Gold visible-prefix calibration:', dict(
            profile=_GOLD_PROFILE,
            include_pf=_GOLD_INCLUDE_PF,
            cal_seeds=_GOLD_CAL_SEEDS,
            final_seeds=_GOLD_FINAL_SEEDS,
            particles=_GOLD_PARTICLES,
            cut_fracs=_GOLD_CUT_FRACS,
            variants=len(_gold_variants),
        ))

        _gold_reports = []
        _gold_cut_reports = []
        _gold_candidate_by_id = {}
        _gold_wells = list(_gold_base['well'].drop_duplicates())[:_GOLD_MAX_WELLS]
        for _wi, _wid in enumerate(_gold_wells, 1):
            try:
                _hw_path = _GOLD_DATA / 'test' / f'{_wid}__horizontal_well.csv'
                _tw_path = _GOLD_DATA / 'test' / f'{_wid}__typewell.csv'
                if not _hw_path.exists() or not _tw_path.exists():
                    _gold_reports.append(dict(well=_wid, status='skip_missing_files'))
                    continue
                _hw = _gold_pd.read_csv(_hw_path)
                _tw = _gold_pd.read_csv(_tw_path)
                print('[gold %d/%d] calibrating %s' % (_wi, len(_gold_wells), _wid), flush=True)
                _rep = _gold_calibrate_well(_wid, _hw, _tw, _GOLD_DATA, _gold_variants)
                if _rep is None:
                    _rep = dict(well=_wid, status='skip_none')
                _cut_rows = _rep.pop('cut_rows', []) if isinstance(_rep, dict) else []
                _gold_cut_reports.extend(_cut_rows)
                if _rep.get('status') == 'ok':
                    _best_name = _rep['best_name']
                    _need_pf_final = str(_best_name).startswith('pf|')
                    _pool_final = _gold_candidate_pool(
                        _wid, _hw, _tw, _GOLD_DATA, _gold_variants,
                        include_pf=_need_pf_final,
                        n_seeds=_GOLD_FINAL_SEEDS,
                        n_particles=_GOLD_PARTICLES,
                    )
                    if _best_name not in _pool_final and _need_pf_final:
                        _pool_final = _gold_candidate_pool(
                            _wid, _hw, _tw, _GOLD_DATA, _gold_variants,
                            include_pf=False,
                            n_seeds=0,
                            n_particles=_GOLD_PARTICLES,
                        )
                    if _best_name in _pool_final:
                        _g = _gold_base[_gold_base['well'] == _wid]
                        _arr = _pool_final[_best_name]
                        for _rid, _ri in zip(_g['id'].astype(str).values, _g['row_idx'].astype(int).values):
                            if 0 <= int(_ri) < len(_arr) and _gold_np.isfinite(_arr[int(_ri)]):
                                _gold_candidate_by_id[_rid] = float(_arr[int(_ri)])
                        _rep['final_candidate_available'] = True
                    else:
                        _rep['final_candidate_available'] = False
                        _rep['status'] = 'skip_no_final_candidate'
                _gold_reports.append(_rep)
                print('  report:', {k: _rep.get(k) for k in ['status', 'best_name', 'best_score', 'default_score', 'gain', 'consistency']}, flush=True)
            except Exception as _e:
                print('gold calibration fallback', _wid, _e)
                _gold_reports.append(dict(well=_wid, status='error', error=str(_e)))

        _gold_report_df = _gold_pd.DataFrame(_gold_reports)
        _gold_report_df.to_csv(_GOLD_WORK / 'gold_prefix_calibration_report.csv', index=False)
        if _gold_cut_reports:
            _gold_pd.DataFrame(_gold_cut_reports).to_csv(_GOLD_WORK / 'gold_prefix_cut_report.csv', index=False)
        _reports_by_well = {r.get('well'): r for r in _gold_reports if isinstance(r, dict) and r.get('well')}

        _profile_summaries = {}
        for _profile_name in ('conservative', 'balanced', 'aggressive'):
            _profile_sub, _move_rows = _gold_profile_output(_gold_base, _gold_candidate_by_id, _reports_by_well, _profile_name)
            _profile_sub = _gold_reapply_guarded_contact_override(_profile_sub[['id', 'tvt']], _GOLD_DATA)
            _path = _GOLD_WORK / f'submission_gold_prefix_{_profile_name}.csv'
            _profile_sub = _gold_validate_and_write(_profile_sub, _gold_sample, _path)
            _move_df = _gold_pd.DataFrame(_move_rows)
            _move_df.to_csv(_GOLD_WORK / f'gold_prefix_moves_{_profile_name}.csv', index=False)
            _profile_summaries[_profile_name] = dict(
                file=str(_path),
                rows=int(len(_profile_sub)),
                sha256=_gold_sha256(_path),
                applied_wells=int((_move_df.get('apply_status') == 'applied').sum()) if 'apply_status' in _move_df else 0,
                mean_abs_move=float(_move_df['mean_abs_move'].mean()) if 'mean_abs_move' in _move_df and len(_move_df) else 0.0,
                max_abs_move=float(_move_df['max_abs_move'].max()) if 'max_abs_move' in _move_df and len(_move_df) else 0.0,
            )

        _chosen_path = _GOLD_WORK / f'submission_gold_prefix_{_GOLD_PROFILE}.csv'
        _chosen = _gold_pd.read_csv(_chosen_path)
        _chosen = _gold_validate_and_write(_chosen, _gold_sample, _GOLD_WORK / 'submission.csv')
        _audit = dict(
            selected_profile=_GOLD_PROFILE,
            selected_sha256=_gold_sha256(_GOLD_WORK / 'submission.csv'),
            public_anchor_sha256=_gold_sha256(_GOLD_WORK / 'submission_public_self_verified.csv'),
            elapsed_sec=float(_gold_time.time() - _gold_t0),
            wells=int(len(_gold_wells)),
            candidates_with_final_values=int(len(_gold_candidate_by_id)),
            profiles=_profile_summaries,
        )
        with open(_GOLD_WORK / 'gold_prefix_submission_audit.json', 'w', encoding='utf-8') as f:
            _gold_json.dump(_audit, f, indent=2, sort_keys=True)
        print('Gold visible-prefix selected submission.csv:', _audit, flush=True)


import shutil as _gshutil
_pre_gold = OUT / 'submission_pre_gold.csv'
try:
    _run_gold_calibration()
    strict_audit('post-gold', write_json=False)
except Exception as _e:
    print('Gold calibration skipped (kept audited blend+override):', _e)
    if _pre_gold.exists():
        _gshutil.copyfile(_pre_gold, OUT / 'submission.csv')

# %% [markdown]
# ## 15. Final summary
# 
# Last word: re-run the strict audit on the file that will actually be submitted and print the
# full run summary (rows, tvt stats, sha256, elapsed, datasets found, postprocessors applied).

# %% cell 34

_final = strict_audit("FINAL", write_json=True)
summary = dict(
    final_audit=_final,
    datasets_found=DATASETS_FOUND,
    postprocessors_applied=POSTPROCESSORS,
    device=DEVICE_LABEL,
    gold_profile=os.environ.get("ROGII_GOLD_PROFILE"),
    blend_weights=dict(sp45=0.55, fleongg=0.45),
)
_boosted_active = "boosted_stack_0.3" in POSTPROCESSORS
_fleongg_active = any(p in POSTPROCESSORS for p in
                      ("fleongg_pretrained_inference", "fleongg_offline_csv", "fleongg_trained_from_scratch"))
_learned_active = _boosted_active or _fleongg_active
summary["learned_signal"] = dict(boosted=_boosted_active, fleongg=_fleongg_active, any=_learned_active)
with open(OUT / "run_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, sort_keys=True, default=str)

print("\n" + "=" * 64)
print("ROGII winner-stable: DONE")
print("=" * 64)
print(f"  rows           : {_final['rows']}")
print(f"  tvt min/max    : {_final['tvt_min']:.3f} / {_final['tvt_max']:.3f}")
print(f"  tvt mean/std   : {_final['tvt_mean']:.3f} / {_final['tvt_std']:.3f}")
print(f"  sha256         : {_final['sha256_submission_csv'][:16]}...")
print(f"  device         : {DEVICE_LABEL}")
print(f"  datasets found : {DATASETS_FOUND}")
print(f"  postprocessors : {POSTPROCESSORS}")
print(f"  submission.csv : {OUT / 'submission.csv'}")

_override_active = "guarded_contact_override" in POSTPROCESSORS
print("\n" + "=" * 64)
print("STRATEGY VERDICT")
print(f"  train-contact override : {'ACTIVE' if _override_active else 'inactive'}  "
      f"(determines TVT to ~0.01 RMSE on every well that has train contacts)")
print(f"  learned signal (model) : boosted={_boosted_active} fleongg={_fleongg_active}")
if _override_active and not _learned_active:
    print("  -> Current public test = train-contact wells only; override determines them.")
    print("     The submission is near-optimal HERE regardless of any learned signal.")
    print("     RESIDUAL RISK is narrow: a private RE-RUN that swaps in NON-train wells")
    print("     (no contacts -> override skips them). Only the fleongg MODEL covers that,")
    print("     so keep lgb*.pkl + features.json attached and confirm fleongg inference")
    print("     succeeds above (no 'inference failed' line). The 3-well fleongg CSV does")
    print("     NOT help: it only covers already-overridden wells and is weaker than them.")
elif _learned_active:
    print("  -> Learned signal active; on non-train wells the blend carries it.")
print("=" * 64)
