# Extracted from dz-dtvt-eda (dz-dtvt-eda.ipynb)
# For analysis only — check license-ledger before adopting.

# --- cell 2 ---
# === How the method works, in one picture (self-contained; safe to run before the setup cells) ===
import numpy as _np
import matplotlib.pyplot as _plt
from matplotlib.patches import FancyBboxPatch as _FBox

_fig = _plt.figure(figsize=(15.5, 6.4))
_ax = _fig.add_axes([0, 0, 1, 1]); _ax.set_xlim(0, 15.5); _ax.set_ylim(0, 6.4); _ax.axis("off")

def _box(x, y, w, h, title, body, fc):
    _ax.add_patch(_FBox((x, y), w, h, boxstyle="round,pad=0.10", fc=fc, ec="0.25", lw=1.3))
    _ax.text(x + w / 2, y + h - 0.34, title, ha="center", fontsize=11.5, weight="bold")
    _ax.text(x + w / 2, y + (h - 0.5) / 2, body, ha="center", va="center", fontsize=9.3)

def _arrow(x0, y0, x1, y1):
    _ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                 arrowprops=dict(arrowstyle="-|>", lw=2.2, color="0.25"))

# --- inputs (left column) ---
_box(0.25, 4.45, 3.9, 1.6, "THE WELL'S OWN PATH",
     "surveyed every foot:\nheading + measured depth change ($-dZ$)", "#dce9f7")
_box(0.25, 2.45, 3.9, 1.6, "LAST KNOWN POINT",
     "TVT is measured until the\nPrediction Start -- the anchor", "#dce9f7")
_box(0.25, 0.45, 3.9, 1.6, "THE NEIGHBOURHOOD",
     "773 offset wells + rock-surface maps\n$\\rightarrow$ local tilt of the layer\n(how steep + which direction)", "#dcf0dc")

# --- engine (centre) ---
_box(5.1, 1.55, 5.6, 3.4, "WALK THE WELL, ONE STEP AT A TIME", "", "#fdf3dc")
_ax.text(7.9, 3.95, r"$TVT \;\leftarrow\; TVT \;+\; \kappa \times (\,-dZ \;+\; drift\,)$",
         ha="center", fontsize=14)
_ax.text(6.55, 3.35, "measured\nfrom the path", ha="center", fontsize=8.5, color="#1f5fa8")
_ax.text(8.6, 3.35, "layer tilt seen by neighbours,\nprojected on this well's heading", ha="center",
         fontsize=8.5, color="#2c7a2c")
_ax.text(7.9, 2.55, r"$\kappa$ = the trust dial (0-1): neighbours far away? late in the well?"
         "\ndrilling along-strike? $\\rightarrow$ trust less, stay closer to 'no change'",
         ha="center", fontsize=9.3, style="italic")
_ax.text(7.9, 1.95, "(every setting learned from the 773 wells,\neach validated as if it were unseen)",
         ha="center", fontsize=8.3, color="0.35")

# --- output (right): small real-shaped illustration ---
_axo = _fig.add_axes([0.755, 0.16, 0.225, 0.62])
_x = _np.linspace(0, 1, 300)
_truth = 26 * _x + 9 * _np.sin(5.1 * _x) + 3.5 * _np.sin(11 * _x + 1.2)
_pred = 0.75 * _truth + 2.2 * _np.sin(3 * _x)
_axo.plot(_x, _truth, color="tab:orange", lw=2.4, label="truth (hidden)")
_axo.plot(_x, _pred, color="tab:green", lw=2.0, label="prediction")
_axo.plot(_x, 0 * _x, "--", color="grey", lw=1.4, label="'no change'")
_axo.plot(0, 0, "ko", ms=7, zorder=5)
_axo.annotate("anchor", (0, 0), xytext=(0.04, 12), fontsize=9,
              arrowprops=dict(arrowstyle="->", lw=1))
_axo.set_xticks([]); _axo.set_yticks([])
_axo.set_xlabel("along the lateral $\\rightarrow$", fontsize=9)
_axo.set_ylabel("TVT", fontsize=9)
_axo.set_title("OUTPUT: TVT for every\nremaining foot of the well", fontsize=10.5, weight="bold")
_axo.legend(fontsize=8, loc="upper left", frameon=False)

# --- arrows ---
_arrow(4.15, 5.25, 5.15, 4.35)
_arrow(4.15, 3.25, 5.15, 3.25)
_arrow(4.15, 1.25, 5.15, 2.15)
_arrow(10.7, 3.25, 11.55, 3.25)
_plt.show()

# --- cell 3 ---
import os
import kagglehub

# Competition data: mounted input when running on Kaggle, kagglehub cache elsewhere.
path = "/kaggle/input/rogii-wellbore-geology-prediction"
if not os.path.isdir(path):
    path = kagglehub.competition_download("rogii-wellbore-geology-prediction")

print("Path to competition files:", path)

# --- cell 4 ---
import glob
import os
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

train_dir = os.path.join(path, "train")

hw_files = sorted(glob.glob(os.path.join(train_dir, "*__horizontal_well.csv")))

# Pick one well at random (seeded for reproducibility — change/remove the seed to reshuffle)
random.seed(42)
hw_file = random.choice(hw_files)
well_id = os.path.basename(hw_file).split("__")[0]

well = pd.read_csv(hw_file)
print(f"Loaded well {well_id}: {well.shape}")
well.head()

# --- cell 6 ---
md = well["MD"]

dz = well["Z"].diff()
dtvt = well["TVT"].diff()

# --- cell 7 ---
_, ax = plt.subplots(2, 1, figsize=(12, 6))

ax[0].plot(md, -dz, label="dz")
ax[0].plot(md, dtvt, label="dtvt")
ax[0].set_xlabel("MD")
ax[0].set_ylabel("Vertical Interval")
ax[1].plot(md, np.cumsum(-dz), label="dz")
ax[1].plot(md, np.cumsum(dtvt), label="dtvt")
ax[1].set_xlabel("MD")
ax[1].set_ylabel("Vertical Interval")
ax[0].legend()
ax[1].legend()
plt.show()

# --- cell 9 ---
# Fit the PER-STEP relationship, then integrate (cumsum) the prediction.
# Fitting cumsum-to-cumsum directly chases a hysteresis loop (the build section
# and the lateral trace different paths), so it drifts. Fitting the deltas and
# then cumsumming distributes the a-correction onto each step, where it belongs.
mask = dz.notna() & dtvt.notna()
a, b = np.polyfit(-dz[mask].to_numpy(), dtvt[mask].to_numpy(), 1)

dtvt_pred = a * (-dz) + b  # per-step prediction

resid = dtvt[mask] - dtvt_pred[mask]
r2 = 1.0 - np.sum(resid ** 2) / np.sum((dtvt[mask] - dtvt[mask].mean()) ** 2)
print(f"dtvt = {a:.4f} * (-dz) + {b:.4f}   (R^2 = {r2:.4f})")

# All cumulative curves on one plot (leading NaN step -> 0 so each starts at 0)
cum_naive = (-dz).fillna(0).cumsum()
cum_true = dtvt.fillna(0).cumsum()
cum_pred = dtvt_pred.fillna(0).cumsum()

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(md, cum_naive, label="cumsum(-dz)  (naive)")
ax.plot(md, cum_true, label="cumsum(dtvt)  (truth)", lw=2)
ax.plot(md, cum_pred, "--", color="tab:red", label=f"cumsum(pred)  a={a:.3f}, b={b:.3f}")
ax.set_xlabel("MD")
ax.set_ylabel("cumulative vertical interval")
ax.set_title(f"Well {well_id}: reconstruct cumsum(dtvt) from fitted per-step deltas")
ax.legend()
plt.show()

# --- cell 11 ---
# Per-well least-squares parameters for the map  dtvt = a * (-dz) + b, over ALL wells.
# ORACLE fit: uses the full TVT column, so this characterises the *target*
# parameter distribution across the training set (not a test-time estimate).
def fit_ab(fp):
    w = pd.read_csv(fp, usecols=["Z", "TVT"])
    x = -w["Z"].diff()
    y = w["TVT"].diff()
    m = x.notna() & y.notna()
    a_i, b_i = np.polyfit(x[m].to_numpy(), y[m].to_numpy(), 1)
    return os.path.basename(fp).split("__")[0], a_i, b_i


params = pd.DataFrame(
    [fit_ab(fp) for fp in hw_files], columns=["well_id", "a", "b"]
)
print(f"Fitted {len(params)} wells")
print(params[["a", "b"]].describe().to_string())

# Distributions of a and b
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
for axis, col, color in zip(ax, ["a", "b"], ["tab:blue", "tab:orange"]):
    axis.hist(params[col], bins=50, color=color, edgecolor="white")
    axis.axvline(params[col].median(), color="k", ls="--", lw=1, label="median")
    axis.set_title(f"{col}   (median {params[col].median():.3f}, std {params[col].std():.3f})")
    axis.set_ylabel("count")
    axis.legend()
ax[0].set_xlabel("a  (slope of dtvt vs -dz)")
ax[1].set_xlabel("b  (intercept)")
plt.tight_layout()
plt.show()

# --- cell 12 ---
# --- b-cluster diagnostic + symmetry check (reuses `params` from the cell above) ---
# The two b-modes are separated by a gap at ~0, so cluster by sign of b.
params["b_pos"] = params["b"] >= 0
neg = params.loc[~params["b_pos"], "b"]
pos = params.loc[params["b_pos"], "b"]

print(f"neg (b<0):  {len(neg):3d} wells  mean {neg.mean():+.4f}  std {neg.std():.4f}")
print(f"pos (b>=0): {len(pos):3d} wells  mean {pos.mean():+.4f}  std {pos.std():.4f}")
print("--- symmetry about 0 ---")
print(f"mean(neg) + mean(pos) = {neg.mean() + pos.mean():+.4f}   (0 => modes mirror)")
print(f"|mean neg| {abs(neg.mean()):.4f}  vs  mean pos {pos.mean():.4f}")
print(f"overall b: median {params['b'].median():+.4f}  skew {params['b'].skew():+.3f}")

# Minimal scatter: (a, b) coloured by sign(b)
fig, ax = plt.subplots(figsize=(6, 5))
for lbl, sub, c in [("b < 0", params[~params["b_pos"]], "tab:red"),
                    ("b >= 0", params[params["b_pos"]], "tab:blue")]:
    ax.scatter(sub["a"], sub["b"], s=10, alpha=0.5, color=c, label=lbl)
ax.axhline(0, color="k", lw=0.8)
ax.set_xlabel("a")
ax.set_ylabel("b")
ax.set_title("Per-well (a, b) coloured by sign(b)")
ax.legend()
plt.show()

# --- cell 13 ---
# Global X-Y map of every well trajectory, coloured by its b-cluster (sign of b).
from matplotlib.lines import Line2D

b_sign = dict(zip(params["well_id"], params["b"] >= 0))  # well_id -> b >= 0
n_pos = int((params["b"] >= 0).sum())
n_neg = len(params) - n_pos

fig, ax = plt.subplots(figsize=(9, 9))
step = 25  # subsample points per trajectory for speed
for fp in hw_files:
    wid = os.path.basename(fp).split("__")[0]
    xy = pd.read_csv(fp, usecols=["X", "Y"]).iloc[::step]
    ax.plot(xy["X"], xy["Y"], color="tab:blue" if b_sign[wid] else "tab:red", lw=0.4, alpha=0.5)

ax.legend(
    [Line2D([0], [0], color="tab:blue"), Line2D([0], [0], color="tab:red")],
    [f"b >= 0  (n={n_pos})", f"b < 0  (n={n_neg})"],
)
ax.set_aspect("equal")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Horizontal well trajectories, coloured by sign(b)")
plt.show()

# --- cell 14 ---
# Overlay Z "striations" (isodepth contours) on the trajectory map to test whether
# depth — rather than drilling direction — is what separates the b-clusters.
import matplotlib.tri as mtri
from matplotlib.lines import Line2D

b_sign = dict(zip(params["well_id"], params["b"] >= 0))

hx, hy, zc, trajs = [], [], [], []
for fp in hw_files:
    wid = os.path.basename(fp).split("__")[0]
    w = pd.read_csv(fp, usecols=["X", "Y", "Z", "TVT_input"])
    lat = w["TVT_input"].isna()  # lateral (unknown-TVT) portion == the target depth
    hx.append(w["X"].mean())
    hy.append(w["Y"].mean())
    zc.append(w["Z"][lat].mean() if lat.any() else w["Z"].mean())
    trajs.append((w["X"].iloc[::25], w["Y"].iloc[::25], b_sign[wid]))
zc = np.array(zc)

# Quantitative: does depth separate the clusters?
pos = (params["b"] >= 0).to_numpy()
print(f"corr(lateral Z, b) = {np.corrcoef(zc, params['b'])[0, 1]:.3f}")
print(f"Z | b>=0: mean {zc[pos].mean():.0f}  std {zc[pos].std():.0f}")
print(f"Z | b<0 : mean {zc[~pos].mean():.0f}  std {zc[~pos].std():.0f}")

fig, ax = plt.subplots(figsize=(9, 9))
cf = ax.tricontourf(mtri.Triangulation(np.array(hx), np.array(hy)), zc,
                    levels=14, cmap="Greys_r", alpha=0.55)
plt.colorbar(cf, ax=ax, label="lateral Z (depth)", shrink=0.8)
for xx, yy, is_pos in trajs:
    ax.plot(xx, yy, color="tab:blue" if is_pos else "tab:red", lw=0.5, alpha=0.7)
ax.legend([Line2D([0], [0], color="tab:blue"), Line2D([0], [0], color="tab:red")],
          ["b >= 0", "b < 0"])
ax.set_aspect("equal")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Well trajectories (sign b) over Z striations (isodepth)")
plt.show()

# --- cell 15 ---
# Visualise the dip axis two ways: (left) on the structural surface, (right) via b(heading).
import matplotlib.tri as mtri

# (i) Authoritative dip from the ANCC formation-top surface: plane fit ANCC ~ X + Y.
random.seed(0)
struct = pd.concat(
    pd.read_csv(fp, usecols=["X", "Y", "ANCC"]).iloc[::50].dropna()
    for fp in random.sample(hw_files, 150)
)
pX, pY, _ = np.linalg.lstsq(
    np.column_stack([struct["X"], struct["Y"], np.ones(len(struct))]),
    struct["ANCC"], rcond=None)[0]
downdip = np.degrees(np.arctan2(-pY, -pX)) % 360   # direction ANCC deepens fastest
updip = (downdip + 180) % 360
strike = (downdip + 90) % 180

# (ii) Per-well intercept b and lateral heading azimuth (heading = built during build, read from X,Y).
def b_and_heading(fp):
    w = pd.read_csv(fp, usecols=["X", "Y", "Z", "TVT", "TVT_input"])
    x = -w["Z"].diff(); y = w["TVT"].diff(); m = x.notna() & y.notna()
    b = np.polyfit(x[m].to_numpy(), y[m].to_numpy(), 1)[1]
    s = np.where(w["TVT_input"].notna().to_numpy())[0].max()  # end of known (build) section
    az = np.degrees(np.arctan2(w["Y"].iloc[-1] - w["Y"].iloc[s],
                               w["X"].iloc[-1] - w["X"].iloc[s])) % 360
    return b, az

bh = pd.DataFrame([b_and_heading(fp) for fp in hw_files], columns=["b", "az"])
c1, c2 = np.linalg.lstsq(
    np.column_stack([np.cos(np.radians(bh["az"])), np.sin(np.radians(bh["az"]))]),
    bh["b"], rcond=None)[0]
th0 = np.degrees(np.arctan2(c2, c1)) % 360  # heading that maximises b (== up-dip)
D = np.hypot(c1, c2)
print(f"ANCC surface: down-dip {downdip:.0f}deg  up-dip {updip:.0f}deg  strike {strike:.0f}deg")
print(f"b(heading) peaks at {th0:.0f}deg (== up-dip),  amplitude D = {D:.4f}")

fig, ax = plt.subplots(1, 2, figsize=(16, 7))
# left: structural surface + dip/strike axes
cf = ax[0].tricontourf(mtri.Triangulation(struct["X"].values, struct["Y"].values),
                       struct["ANCC"].values, levels=16, cmap="Greys_r")
plt.colorbar(cf, ax=ax[0], label="ANCC formation-top depth", shrink=0.8)
cx, cy = struct["X"].mean(), struct["Y"].mean()
L = (struct["X"].max() - struct["X"].min()) * 0.28
for ang, txt, col in [(downdip, f"down-dip {downdip:.0f}deg", "tab:red"),
                      (updip, f"up-dip {updip:.0f}deg", "tab:cyan")]:
    ax[0].annotate("", xy=(cx + L*np.cos(np.radians(ang)), cy + L*np.sin(np.radians(ang))),
                   xytext=(cx, cy), arrowprops=dict(arrowstyle="-|>", color=col, lw=2.5))
    ax[0].text(cx + 1.05*L*np.cos(np.radians(ang)), cy + 1.05*L*np.sin(np.radians(ang)),
               txt, color=col, ha="center", fontsize=9)
for s in (strike, strike + 180):
    ax[0].plot([cx, cx + L*np.cos(np.radians(s))], [cy, cy + L*np.sin(np.radians(s))],
               color="tab:green", ls="--", lw=1.5)
ax[0].set_aspect("equal"); ax[0].set_xlabel("X"); ax[0].set_ylabel("Y")
ax[0].set_title("Dip axis on the structural (ANCC) surface")
# right: b vs heading + cosine fit
ax[1].scatter(bh["az"], bh["b"], s=10, c=np.where(bh["b"] >= 0, "tab:blue", "tab:red"), alpha=0.5)
azg = np.linspace(0, 360, 361)
ax[1].plot(azg, D*np.cos(np.radians(azg - th0)), "k-", lw=2, label=f"{D:.3f}*cos(az-{th0:.0f}deg)")
ax[1].axhline(0, color="grey", lw=0.8)
ax[1].axvline(th0, color="tab:cyan", ls=":", label="up-dip heading (b max)")
ax[1].axvline((th0 + 180) % 360, color="tab:red", ls=":", label="down-dip heading (b min)")
ax[1].set_xlabel("lateral heading azimuth (deg)"); ax[1].set_ylabel("b")
ax[1].set_title("b is set by heading relative to the dip axis"); ax[1].legend(fontsize=8)
plt.tight_layout()
plt.show()

# --- cell 16 ---
# --- Fit the regional dip vector (D, theta0) from b(heading). Reuses `bh`; no file reads. ---
# Model:  b = c0 + D*cos(az - theta0)  ==  c0 + c1*cos(az) + c2*sin(az)   (linear in c0, c1, c2)
def fit_dipole(az_deg, b, trim_sigma=3.0):
    az = np.radians(az_deg)
    M = np.column_stack([np.ones_like(az), np.cos(az), np.sin(az)])
    coef = np.linalg.lstsq(M, b, rcond=None)[0]
    resid = b - M @ coef
    keep = np.abs(resid) <= trim_sigma * resid.std()          # drop far-off (near-strike/noisy) wells
    c0, c1, c2 = np.linalg.lstsq(M[keep], b[keep], rcond=None)[0]
    return c0, np.hypot(c1, c2), np.degrees(np.arctan2(c2, c1)) % 360, keep

az_all = bh["az"].to_numpy()
b_all = bh["b"].to_numpy()

# Held-out check (80/20): does the 2-parameter model generalise to unseen wells?
rng = np.random.default_rng(0)
idx = rng.permutation(len(bh))
tr, te = idx[: int(0.8 * len(bh))], idx[int(0.8 * len(bh)):]
c0t, Dt, tht, _ = fit_dipole(az_all[tr], b_all[tr])
resid_te = b_all[te] - (c0t + Dt * np.cos(np.radians(az_all[te] - tht)))
print(f"held-out (20%): residual std {resid_te.std():.4f}  vs  std(b) {b_all[te].std():.4f}"
      f"   ({1 - resid_te.var() / b_all[te].var():.1%} variance explained)")

# Final fit on all wells (3-sigma trim) -> the regional dip constants to keep
c0, D, theta0, keep = fit_dipole(az_all, b_all)
print(f"regional dip:  D = {D:.4f}   theta0 = {theta0:.1f} deg (up-dip heading)"
      f"   intercept c0 = {c0:+.4f}   (trimmed {(~keep).sum()} outliers)")


def b_pred(az_deg):
    """Test-time estimate of the drift intercept b from lateral heading azimuth (degrees)."""
    return c0 + D * np.cos(np.radians(np.asarray(az_deg, dtype=float) - theta0))

# --- cell 18 ---
# Same cumsum-type plot as before, but comparing the fittings:
#   naive (a=1,b=0) | truth | ORACLE-FREE regional (a=1, b=b_pred(heading)) | oracle per-well fit
def heading_az(w):
    s = np.where(w["TVT_input"].notna().to_numpy())[0].max()  # end of known (build) section
    return np.degrees(np.arctan2(w["Y"].iloc[-1] - w["Y"].iloc[s],
                                 w["X"].iloc[-1] - w["X"].iloc[s])) % 360

random.seed(3)  # change to resample wells
sample = random.sample(hw_files, 6)
fig, axes = plt.subplots(2, 3, figsize=(17, 8))
for ax, fp in zip(axes.ravel(), sample):
    w = pd.read_csv(fp, usecols=["MD", "X", "Y", "Z", "TVT", "TVT_input"])
    dz = w["Z"].diff(); dtvt = w["TVT"].diff()
    az = heading_az(w); bhat = float(b_pred(az))
    m = dz.notna() & dtvt.notna()
    a_o, b_o = np.polyfit(-dz[m].to_numpy(), dtvt[m].to_numpy(), 1)  # per-well oracle (ceiling)

    cum_true = dtvt.fillna(0).cumsum()
    cum_naive = (-dz).fillna(0).cumsum()
    cum_reg = (-dz + bhat).fillna(0).cumsum()          # regional: a=1, b=b_pred(heading)
    cum_orc = (a_o * (-dz) + b_o).fillna(0).cumsum()   # oracle per-well fit

    ax.plot(w["MD"], cum_naive, color="tab:blue", lw=1, label="cumsum(-dz) naive")
    ax.plot(w["MD"], cum_true, color="tab:orange", lw=2, label="cumsum(dtvt) truth")
    ax.plot(w["MD"], cum_reg, "--", color="tab:red", lw=1.8, label="regional b_pred(heading)")
    ax.plot(w["MD"], cum_orc, ":", color="k", lw=1, label="oracle per-well fit")
    end_err = abs((cum_reg - cum_true).iloc[-1])
    ax.set_title(f"{os.path.basename(fp)[:8]}  az={az:.0f}deg  b_hat={bhat:+.3f}  endErr={end_err:.0f}")
    ax.set_xlabel("MD")
axes[0, 0].legend(fontsize=7)
axes[0, 0].set_ylabel("cumulative vertical interval")
axes[1, 0].set_ylabel("cumulative vertical interval")
plt.tight_layout()
plt.show()

# --- cell 21 ---
# Run the regional model (a=1, b=b_pred) for ALL training wells and diagnose the end error.
# Exact identity:  endErr = (1 - a_o)*sum(-dz)  +  (b_pred - b_o)*N
#                           \___ slope (a!=1) __/   \_ intercept-b error x lateral length _/
recs = []
for fp in hw_files:
    w = pd.read_csv(fp, usecols=["X", "Y", "Z", "TVT", "TVT_input"])
    dz = w["Z"].diff(); dtvt = w["TVT"].diff(); m = dz.notna() & dtvt.notna()
    a_o, b_o = np.polyfit(-dz[m].to_numpy(), dtvt[m].to_numpy(), 1)  # oracle per-well fit
    bhat = float(b_pred(heading_az(w)))                             # regional prediction (a=1)
    N = int(m.sum()); sum_ndz = float((-dz[m]).sum())
    recs.append((os.path.basename(fp).split("__")[0], a_o, b_o, bhat, N,
                 (1 - a_o) * sum_ndz, (bhat - b_o) * N))
recon = pd.DataFrame(recs, columns=["well_id", "a_o", "b_o", "b_pred", "N", "term_a", "term_b"])
recon["endErr"] = recon["term_a"] + recon["term_b"]
ae = recon["endErr"].abs()

print(f"All {len(recon)} wells | |endErr|: median {ae.median():.0f}  mean {ae.mean():.0f}  "
      f"p90 {ae.quantile(.9):.0f}  max {ae.max():.0f}")
print(f"median |term_a| (a!=1) = {recon.term_a.abs().median():.0f}   "
      f"median |term_b| (b err x N) = {recon.term_b.abs().median():.0f}")
print(f"corr(|endErr|,|term_b|) {ae.corr(recon.term_b.abs()):.2f}  >  "
      f"corr(|endErr|,|term_a|) {ae.corr(recon.term_a.abs()):.2f}   |   "
      f"intercept term dominates in {(recon.term_b.abs() > recon.term_a.abs()).mean():.0%} of wells")

fig, ax = plt.subplots(1, 3, figsize=(17, 5))
# (1) intercept b: regional prediction vs oracle. Regional saturates at +/-D (few wells drill along strike).
sc = ax[0].scatter(recon["b_o"], recon["b_pred"], s=12, c=ae, cmap="viridis", alpha=0.7)
plt.colorbar(sc, ax=ax[0], label="|endErr|")
lim = [recon["b_o"].min(), recon["b_o"].max()]
ax[0].plot(lim, lim, "k--", lw=1, label="y = x")
ax[0].axhline(D, color="grey", ls=":"); ax[0].axhline(-D, color="grey", ls=":")
ax[0].set_xlabel("oracle b_o"); ax[0].set_ylabel("regional b_pred")
ax[0].set_title("Intercept b: regional saturates at +/-D (dotted); |b_o| ranges ~2x wider")
ax[0].legend(fontsize=8)
# (2) slope a: the a=1 assumption
ax[1].hist(recon["a_o"], bins=50, color="tab:blue", edgecolor="white")
ax[1].axvline(1.0, color="k", ls="--", label="assumed a=1")
ax[1].set_xlabel("oracle a_o"); ax[1].set_ylabel("count")
ax[1].set_title("Slope a: assumed 1 (fine except the tails)"); ax[1].legend()
# (3) which term drives endErr
ax[2].scatter(recon.term_a.abs(), recon.term_b.abs(), s=12, c=ae, cmap="viridis", alpha=0.7)
mx = max(recon.term_a.abs().max(), recon.term_b.abs().max())
ax[2].plot([0, mx], [0, mx], "k--", lw=1)
ax[2].set_xlabel("|term_a|  (slope error)"); ax[2].set_ylabel("|term_b|  (b error x N)")
ax[2].set_title("Above diagonal => intercept term dominates")
plt.tight_layout()
plt.show()

# --- cell 22 ---
# --- Local dip-magnitude model (tops-free): interpolate D_local(X,Y), reproject onto heading. ---
# D_local = b_o / cos(az - theta0) is a SIGN-FREE dip magnitude that is spatially smooth
# (Moran's I ~0.46), so kNN-interpolating it gives a per-well b that captures LOCAL dip
# strength, not just the global average. Uses only X, Y and heading -> no tops needed.
K = 10  # neighbours (leave-one-out optimum)

rows = []
for fp in hw_files:
    w = pd.read_csv(fp, usecols=["X", "Y", "Z", "TVT", "TVT_input"])
    dz = w["Z"].diff(); dtvt = w["TVT"].diff(); m = dz.notna() & dtvt.notna()
    a_o, b_o = np.polyfit(-dz[m].to_numpy(), dtvt[m].to_numpy(), 1)
    s = np.where(w["TVT_input"].notna().to_numpy())[0].max()
    az = np.degrees(np.arctan2(w["Y"].iloc[-1] - w["Y"].iloc[s],
                               w["X"].iloc[-1] - w["X"].iloc[s])) % 360
    rows.append((os.path.basename(fp).split("__")[0], w["X"].iloc[s], w["Y"].iloc[s],
                 az, a_o, b_o, int(m.sum()), float((-dz[m]).sum())))
loc = pd.DataFrame(rows, columns=["well_id", "hX", "hY", "az", "a_o", "b_o", "N", "sum_ndz"])

proj = np.cos(np.radians(loc["az"].to_numpy() - theta0))   # heading projection onto the dip axis
usable = np.abs(proj) > 0.3                                 # near-strike wells are bad D_local sources
D_local = np.where(usable, loc["b_o"].to_numpy() / proj, np.nan)

Hxy = loc[["hX", "hY"]].to_numpy()
d2 = ((Hxy[:, None, :] - Hxy[None, :, :]) ** 2).sum(-1)
np.fill_diagonal(d2, np.inf)                               # leave-one-out (exclude self)
order = np.argsort(d2, axis=1)

b_local = np.empty(len(loc))
for i in range(len(loc)):
    nb = [j for j in order[i] if usable[j]][:K]            # K nearest wells with a usable D_local
    b_local[i] = np.nanmean(D_local[nb]) * proj[i]
loc["b_glob"] = b_pred(loc["az"].to_numpy())              # previous global cosine model
loc["b_loc"] = b_local
bloc = dict(zip(loc["well_id"], loc["b_loc"]))            # used by the 2x3 plot below
bglo = dict(zip(loc["well_id"], loc["b_glob"]))

# Re-score  endErr = (1 - a_o)*sum(-dz) + (b_pred - b_o)*N  for both models
for col, name in [("b_glob", "global"), ("b_loc", "local ")]:
    e = ((1 - loc["a_o"]) * loc["sum_ndz"] + (loc[col] - loc["b_o"]) * loc["N"]).abs()
    print(f"{name}: |endErr| median {e.median():5.0f}  mean {e.mean():5.0f}  "
          f"p90 {e.quantile(.9):5.0f}  max {e.max():5.0f}")

# --- cell 23 ---
# Same 2x3 cumsum plot as before, now adding the LOCAL dip-magnitude model (green)
# alongside the global one (red dashed). Titles show endErr improving global -> local.
random.seed(3)  # same six wells as before
sample = random.sample(hw_files, 6)
fig, axes = plt.subplots(2, 3, figsize=(17, 8))
for ax, fp in zip(axes.ravel(), sample):
    wid = os.path.basename(fp).split("__")[0]
    w = pd.read_csv(fp, usecols=["MD", "Z", "TVT"])
    dz = w["Z"].diff(); dtvt = w["TVT"].diff(); m = dz.notna() & dtvt.notna()
    a_o, b_o = np.polyfit(-dz[m].to_numpy(), dtvt[m].to_numpy(), 1)

    cum_true = dtvt.fillna(0).cumsum()
    cum_naive = (-dz).fillna(0).cumsum()
    cum_glob = (-dz + bglo[wid]).fillna(0).cumsum()   # global cosine model
    cum_loc = (-dz + bloc[wid]).fillna(0).cumsum()    # local dip-magnitude model
    cum_orc = (a_o * (-dz) + b_o).fillna(0).cumsum()  # oracle (ceiling)

    ax.plot(w["MD"], cum_naive, color="tab:blue", lw=0.8, label="naive")
    ax.plot(w["MD"], cum_true, color="tab:orange", lw=2, label="truth")
    ax.plot(w["MD"], cum_glob, "--", color="tab:red", lw=1.3, label="global b_pred")
    ax.plot(w["MD"], cum_loc, "-", color="tab:green", lw=1.6, label="local b_pred")
    ax.plot(w["MD"], cum_orc, ":", color="k", lw=1, label="oracle")
    eg = abs((cum_glob - cum_true).iloc[-1]); el = abs((cum_loc - cum_true).iloc[-1])
    ax.set_title(f"{wid[:8]}  endErr glob={eg:.0f} -> loc={el:.0f}")
    ax.set_xlabel("MD")
axes[0, 0].legend(fontsize=7)
axes[0, 0].set_ylabel("cumulative vertical interval")
axes[1, 0].set_ylabel("cumulative vertical interval")

plt.tight_layout()
plt.show()

# --- cell 24 ---
# --- Investigate the a-outliers. Finding: the a-anomaly lives in the BUILD section, where
#     TVT is KNOWN (TVT_input) -> a can be recovered at test time by fitting on that section. ---
rows = []
for fp in hw_files:
    w = pd.read_csv(fp, usecols=["X", "Y", "Z", "TVT", "TVT_input"])
    dz = w["Z"].diff()
    dtvt = w["TVT"].diff(); m = dz.notna() & dtvt.notna()
    x = (-dz[m]).to_numpy(); y = dtvt[m].to_numpy()
    a_o, b_o = np.polyfit(x, y, 1)
    r2 = 1.0 - np.sum((y - (a_o * x + b_o)) ** 2) / np.sum((y - y.mean()) ** 2)
    di = w["TVT_input"].diff(); mk = dz.notna() & di.notna()      # KNOWN (build) section only
    a_build = np.polyfit((-dz[mk]).to_numpy(), di[mk].to_numpy(), 1)[0]
    s = np.where(w["TVT_input"].notna().to_numpy())[0].max()
    rows.append((os.path.basename(fp).split("__")[0], fp, a_o, a_build, r2, w["X"].iloc[s], w["Y"].iloc[s]))
aout = pd.DataFrame(rows, columns=["well_id", "fp", "a", "a_build", "r2", "hX", "hY"])
aout["da"] = (aout["a"] - 1).abs()
out = aout[aout["da"] > 0.12].sort_values("da", ascending=False)

print(f"a-outliers |a-1|>0.12: {len(out)}/{len(aout)} ({len(out)/len(aout):.1%})")
print(f"corr(|a-1|, fit R^2) = {aout['da'].corr(aout['r2']):+.3f}   "
      f"(outliers median R^2 {out['r2'].median():.2f} vs {aout[aout.da <= 0.12]['r2'].median():.2f})")
H = aout[["hX", "hY"]].to_numpy(); d2 = ((H[:, None] - H[None]) ** 2).sum(-1); np.fill_diagonal(d2, np.inf)
nn = np.argmin(d2, axis=1); isout = (aout["da"] > 0.12).to_numpy()
print(f"P(nearest well also outlier | outlier) = {isout[nn][isout].mean():.1%}  (base rate {isout.mean():.1%})")

# The fix: a fitted on the KNOWN section recovers the oracle a (no tops, no oracle).
print(f"\nbuild-section a (test-time available): corr(a_build, a_oracle) = {aout['a'].corr(aout['a_build']):.3f}")
print(f"  median slope error vs oracle:  a=1 -> {(1 - aout['a']).abs().median():.4f}   "
      f"a_build -> {(aout['a_build'] - aout['a']).abs().median():.4f}")
print(f"  on the {len(out)} outliers: corr(a_build, a_oracle) = {out['a'].corr(out['a_build']):.3f}")

# --- cell 25 ---
# (1) cumsum(-dz) vs cumsum(dtvt) profiles of the 9 worst a-outliers.
#     Note the divergence happens BEFORE the grey dotted line (end of build) -> a is a build effect.
worst = out.head(9)
fig, axes = plt.subplots(3, 3, figsize=(16, 11))
for ax, (_, r) in zip(axes.ravel(), worst.iterrows()):
    w = pd.read_csv(r["fp"], usecols=["MD", "Z", "TVT", "TVT_input"])
    dz = w["Z"].diff(); dtvt = w["TVT"].diff()
    ax.plot(w["MD"], (-dz).fillna(0).cumsum(), color="tab:blue", label="cumsum(-dz)")
    ax.plot(w["MD"], dtvt.fillna(0).cumsum(), color="tab:orange", lw=2, label="cumsum(dtvt)")
    bnd = w["MD"].iloc[np.where(w["TVT_input"].notna().to_numpy())[0].max()]
    ax.axvline(bnd, color="grey", ls=":", lw=1)  # end of known (build) section
    ax.set_title(f"{r['well_id'][:8]}  a={r['a']:.2f}  R2={r['r2']:.2f}")
    ax.set_xlabel("MD")
axes[0, 0].legend(fontsize=8)
plt.tight_layout()
plt.show()

# (2) X-Y location of the a-outliers vs all wells (scattered, not clustered; a>1 red / a<1 blue).
fig, ax = plt.subplots(figsize=(9, 9))
ax.scatter(aout["hX"], aout["hY"], s=8, color="lightgrey", label="all wells")
sc = ax.scatter(out["hX"], out["hY"], s=40, c=out["a"], cmap="coolwarm", vmin=0.7, vmax=1.3,
                edgecolor="k", linewidth=0.4, label="a-outliers")
plt.colorbar(sc, ax=ax, label="a")
ax.set_aspect("equal"); ax.set_xlabel("X"); ax.set_ylabel("Y")
ax.set_title(f"a-outliers (|a-1|>0.12, n={len(out)}) vs all wells"); ax.legend()
plt.show()

# --- cell 26 ---
# Before/after the a-correction on the 9 worst a-outliers, holding b = b_local:
#   before = a=1 (current model)   vs   after = a=a_build (fit on the known/build section).
# Note: a_build slightly OVERSHOOTS a_oracle (build anomaly is stronger than the well average),
# so it usually fixes the well but can overcorrect the most extreme cases.
worst = out.head(9)
fig, axes = plt.subplots(3, 3, figsize=(16, 11))
for ax, (_, r) in zip(axes.ravel(), worst.iterrows()):
    w = pd.read_csv(r["fp"], usecols=["MD", "Z", "TVT"])
    dz = w["Z"].diff(); dtvt = w["TVT"].diff()
    bL = bloc[r["well_id"]]                                     # local dip-magnitude b
    cum_true = dtvt.fillna(0).cumsum()
    cum_before = (1.0 * (-dz) + bL).fillna(0).cumsum()         # a = 1
    cum_after = (r["a_build"] * (-dz) + bL).fillna(0).cumsum()  # a = a_build
    ax.plot(w["MD"], cum_true, color="tab:orange", lw=2, label="truth")
    ax.plot(w["MD"], cum_before, "--", color="tab:red", lw=1.4, label="before (a=1)")
    ax.plot(w["MD"], cum_after, "-", color="tab:green", lw=1.6, label="after (a=a_build)")
    eb = abs((cum_before - cum_true).iloc[-1]); ea = abs((cum_after - cum_true).iloc[-1])
    ax.set_title(f"{r['well_id'][:8]}  a={r['a']:.2f} a_build={r['a_build']:.2f}  endErr {eb:.0f}->{ea:.0f}")
    ax.set_xlabel("MD")
axes[0, 0].legend(fontsize=8)
plt.tight_layout()
plt.show()

# --- cell 27 ---
# Does lambda shrinkage improve accuracy?  a_pred = 1 + lambda*(a_build - 1).
# Aggregate scoreboard (lambda wins in every group) + the same 9 worst a-outliers.
LAM = 0.7  # cross-validated optimum over all 773 wells (flat over [0.6, 0.85])

agg = loc.merge(aout[["well_id", "a_build"]], on="well_id")  # loc has a_o, b_o, b_loc, N, sum_ndz
def endErr(lam):
    a_pred = 1 + lam * (agg["a_build"] - 1)
    return ((a_pred - agg["a_o"]) * agg["sum_ndz"] + (agg["b_loc"] - agg["b_o"]) * agg["N"]).abs()
is_out = (agg["a_o"] - 1).abs() > 0.12
print(f"{'group':20s} {'a=1':>7s} {'a_build':>8s} {'lam=0.7':>8s}")
for name, msk in [("all 773 (median)", np.ones(len(agg), bool)),
                  ("37 outliers (med)", is_out.to_numpy()),
                  ("736 normal (med)", (~is_out).to_numpy())]:
    print(f"{name:20s} {endErr(0)[msk].median():7.0f} {endErr(1)[msk].median():8.0f} {endErr(LAM)[msk].median():8.0f}")

worst = out.head(9)
fig, axes = plt.subplots(3, 3, figsize=(16, 11))
for ax, (_, r) in zip(axes.ravel(), worst.iterrows()):
    w = pd.read_csv(r["fp"], usecols=["MD", "Z", "TVT"])
    dz = w["Z"].diff(); dtvt = w["TVT"].diff()
    bL = bloc[r["well_id"]]; a_lam = 1 + LAM * (r["a_build"] - 1)
    cum_true = dtvt.fillna(0).cumsum()
    c1 = (1.0 * (-dz) + bL).fillna(0).cumsum()          # a = 1 (before)
    cab = (r["a_build"] * (-dz) + bL).fillna(0).cumsum()  # raw a_build (lam=1)
    clam = (a_lam * (-dz) + bL).fillna(0).cumsum()      # lambda-shrunk
    ax.plot(w["MD"], cum_true, color="tab:orange", lw=2, label="truth")
    ax.plot(w["MD"], c1, "--", color="tab:red", lw=1.1, label="a=1 (before)")
    ax.plot(w["MD"], cab, ":", color="tab:grey", lw=1.3, label="a_build (lam=1)")
    ax.plot(w["MD"], clam, "-", color="tab:green", lw=1.7, label=f"lam={LAM} shrunk")
    e1 = abs((c1 - cum_true).iloc[-1]); eab = abs((cab - cum_true).iloc[-1]); el = abs((clam - cum_true).iloc[-1])
    ax.set_title(f"{r['well_id'][:8]} a_o={r['a']:.2f} a_b={r['a_build']:.2f}  endErr {e1:.0f}/{eab:.0f}/{el:.0f}")
    ax.set_xlabel("MD")
axes[0, 0].legend(fontsize=7)
plt.tight_layout()
plt.show()

# --- cell 29 ---
# === Per-point TVT RMSE scoreboard (THE competition metric, per task .pptx slide 14) ===
# Anchor at PS (last known TVT_input), predict the lateral, pool (pred - true) over every
# predicted foot-step across all wells, RMSE. Replaces the (PS-unaware) endErr proxy.
# Cross the a-work (a=1 / a_build / lambda-shrunk) with the b-work (0 / global / local).
ref = loc.merge(aout[["well_id", "a_build"]], on="well_id").set_index("well_id")
a_variants = {"a=1": lambda r: 1.0,
              "a_build": lambda r: r.a_build,
              "a_lam0.7": lambda r: 1 + 0.7 * (r.a_build - 1)}
b_variants = {"b=0": lambda r: 0.0, "b_global": lambda r: r.b_glob, "b_local": lambda r: r.b_loc}

keys = ["oracle"] + [f"{an}|{bn}" for an in a_variants for bn in b_variants]
sq = {k: 0.0 for k in keys}; n = {k: 0 for k in keys}
for fp in hw_files:
    r = ref.loc[os.path.basename(fp).split("__")[0]]
    w = pd.read_csv(fp, usecols=["Z", "TVT", "TVT_input"])
    dz = w["Z"].diff().to_numpy(); tvt = w["TVT"].to_numpy()
    s = int(np.where(w["TVT_input"].notna().to_numpy())[0].max())  # PS point

    def acc(key, a, b):
        pred = tvt[s] + np.nancumsum((a * (-dz) + b)[s + 1:])       # reconstruct lateral TVT from PS
        err = pred - tvt[s + 1:]
        sq[key] += np.nansum(err ** 2); n[key] += int(np.isfinite(err).sum())

    for an, af in a_variants.items():
        for bn, bf in b_variants.items():
            acc(f"{an}|{bn}", af(r), bf(r))
    acc("oracle", r.a_o, r.b_o)

rmse = {k: np.sqrt(sq[k] / n[k]) for k in keys}
print("Pooled per-point TVT RMSE (lower = better):\n")
print(f"{'':10s}" + "".join(f"{bn:>10s}" for bn in b_variants))
for an in a_variants:
    print(f"{an:10s}" + "".join(f"{rmse[an + '|' + bn]:10.2f}" for bn in b_variants))
print(f"\nbest model  a=1 , b_local : {rmse['a=1|b_local']:.2f}")
print(f"oracle a,b (floor)        : {rmse['oracle']:.2f}")

# --- cell 30 ---
# Why is RMSE ~21 (oracle ~12) when per-step dTVT is easy to fit?  TVT is the running INTEGRAL
# of dTVT, so per-step errors ACCUMULATE. Also: row-wise (per-well) RMSE vs the pooled metric.
per = []
for fp in hw_files:
    r = ref.loc[os.path.basename(fp).split("__")[0]]  # ref from the scoreboard cell (a_o, b_o, b_loc)
    w = pd.read_csv(fp, usecols=["Z", "TVT", "TVT_input"])
    dz = w["Z"].diff().to_numpy(); tvt = w["TVT"].to_numpy()
    s = int(np.where(w["TVT_input"].notna().to_numpy())[0].max())
    lat = slice(s + 1, None)

    def wr(a, b):
        pred = tvt[s] + np.nancumsum((a * (-dz) + b)[lat]); e = pred - tvt[lat]
        return np.sqrt(np.nanmean(e ** 2))
    step_res = np.diff(tvt)[s:] - (r.a_o * (-dz[s + 1:]) + r.b_o)   # oracle per-step dTVT residual
    per.append((wr(1.0, r.b_loc), wr(r.a_o, r.b_o), int(np.isfinite(tvt[lat]).sum()), np.nanstd(step_res)))
P = pd.DataFrame(per, columns=["rmse_model", "rmse_oracle", "Nlat", "resid_std"])

print("Row-wise (per-well) RMSE vs the pooled metric:")
print(f"  a=1,b_local :  pooled {rmse['a=1|b_local']:5.1f}  |  per-well median {P.rmse_model.median():.1f}"
      f"  mean {P.rmse_model.mean():.1f}  p90 {P.rmse_model.quantile(.9):.1f}")
print(f"  oracle a,b  :  pooled {rmse['oracle']:5.1f}  |  per-well median {P.rmse_oracle.median():.1f}"
      f"  mean {P.rmse_oracle.mean():.1f}  p90 {P.rmse_oracle.quantile(.9):.1f}")
print(f"\nWhy even the oracle floors at ~{P.rmse_oracle.median():.0f}: it fits dTVT to only "
      f"{P.resid_std.median():.3f} ft/step, but integrated over ~{P.Nlat.median():.0f} steps —")
print(f"  IID noise would give just {(P.resid_std * np.sqrt(P.Nlat / 2)).median():.1f} ft; actual median is "
      f"{P.rmse_oracle.median():.1f} ft (~{P.rmse_oracle.median() / (P.resid_std * np.sqrt(P.Nlat / 2)).median():.0f}x).")
print("  => per-step residuals are AUTOCORRELATED (dip drifts along the lateral) so they add coherently.")
print("     Beating ~12 needs along-lateral dip (GR<->typewell), not a constant (a,b).")

fig, ax = plt.subplots(figsize=(9, 4))
ax.hist(P["rmse_model"], bins=60, alpha=0.6, color="tab:green", label="a=1, b_local (per-well)")
ax.hist(P["rmse_oracle"], bins=60, alpha=0.6, color="tab:blue", label="oracle (per-well)")
ax.axvline(rmse["a=1|b_local"], color="tab:green", ls="--", lw=1.5, label="pooled (model)")
ax.axvline(rmse["oracle"], color="tab:blue", ls="--", lw=1.5, label="pooled (oracle)")
ax.set_xlabel("per-well lateral RMSE (ft)"); ax.set_ylabel("wells")
ax.set_title("Per-well RMSE: pooled (dashed) sits above the median — the long/bulge tail inflates it")
ax.legend(fontsize=8)
plt.show()

# --- cell 32 ---
# === Oracle ladder in the LEVEL domain + kappa-shrunk deployable ===
# All "oracle" fits are per-well fits on the true lateral TVT (upper bounds for each model family).
# One pass to cache lateral arrays; reuses hw_files and bloc (b_local dict) from earlier cells.
lat_data = []  # (well_id, dz_lat, U, R0)  with U = cumsum(-dz) on the lateral, R0 = TVT - anchor
for fp in hw_files:
    w = pd.read_csv(fp, usecols=["Z", "TVT", "TVT_input"])
    z = w["Z"].to_numpy(); tvt = w["TVT"].to_numpy()
    s = int(np.where(w["TVT_input"].notna().to_numpy())[0].max())
    dzl = np.diff(z)[s:]
    lat_data.append((os.path.basename(fp).split("__")[0],
                     dzl, np.cumsum(-dzl), tvt[s + 1:] - tvt[s]))

def pooled_rmse(pred_fn):
    sq = n = 0
    for wid, dzl, U, R0 in lat_data:
        e = pred_fn(wid, dzl, U, R0) - R0
        sq += np.nansum(e ** 2); n += int(np.isfinite(e).sum())
    return np.sqrt(sq / n)

def fit_spline(K):
    """b(MD) piecewise-constant over K equal segments -> linear-spline drift, single PS anchor."""
    def fn(wid, dzl, U, R0):
        t = np.arange(1, len(U) + 1.0); edges = np.linspace(0, len(U), K + 1)
        phi = np.column_stack([np.clip(t - edges[j], 0, edges[j + 1] - edges[j]) for j in range(K)])
        c = np.linalg.lstsq(phi, R0 - U, rcond=None)[0]
        return U + phi @ c
    return fn

ladder = {
    "hold TVT at PS (a=0,b=0)": lambda wid, dzl, U, R0: np.zeros_like(U),
    "LEVEL fit TVT ~ Z (2 dof)": lambda wid, dzl, U, R0: (lambda A: A @ np.linalg.lstsq(A, R0, rcond=None)[0])(
        np.column_stack([U, np.ones_like(U)])),
    "LEVEL fit U + b*t (anchored)": lambda wid, dzl, U, R0: U + (lambda t: t * (np.nansum((R0 - U) * t) / np.nansum(t * t)))(
        np.arange(1, len(U) + 1.0)),
}
print("Pooled per-point TVT RMSE — oracle families (level domain):")
for name, fn in ladder.items():
    print(f"  {name:34s}: {pooled_rmse(fn):6.2f}")
Ks = [1, 2, 4, 8, 16, 32]
spline_scores = [pooled_rmse(fit_spline(K)) for K in Ks]
for K, sc in zip(Ks, spline_scores):
    print(f"  spline b(MD), K={K:2d} segments        : {sc:6.2f}")

# --- deployable: kappa-shrunk integration of the existing b_local drift ---
num = den = 0.0
for wid, dzl, U, R0 in lat_data:
    Mdrift = np.cumsum(-dzl + bloc[wid])
    num += np.nansum(Mdrift * R0); den += np.nansum(Mdrift * Mdrift)
kopt = num / den
def blend(k): return pooled_rmse(lambda wid, dzl, U, R0: k * np.cumsum(-dzl + bloc[wid]))
print(f"\nDeployable kappa-shrink:  pred = TVT_PS + kappa * cumsum(-dz + b_local)")
for k in [0.0, 0.25, kopt, 0.5, 1.0]:
    tag = " (hold)" if k == 0 else (" (current model)" if k == 1 else (" <-- kappa*" if k == kopt else ""))
    print(f"  kappa={k:5.3f}: {blend(k):6.2f}{tag}")

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(Ks, spline_scores, "o-", color="tab:purple", label="spline-b(MD) oracle")
ax.axhspan(2, 3, color="tab:green", alpha=0.15, label="target 2-3 RMSE")
for y, lbl in [(12.38, "old delta-OLS oracle"), (15.91, "hold"), (14.53, "deployable kappa*")]:
    ax.axhline(y, ls=":", lw=1, color="grey"); ax.text(30, y, lbl, fontsize=7, va="bottom", ha="right")
ax.set_xscale("log", base=2); ax.set_xticks(Ks); ax.set_xticklabels(Ks)
ax.set_xlabel("K (segments of b along the lateral)"); ax.set_ylabel("pooled RMSE (ft)")
ax.set_title("Oracle RMSE collapses with a few dof of along-lateral drift: K=4 hits the 2-3 target")
ax.legend(fontsize=8)
plt.show()

# --- cell 35 ---
# === LOO spline-coefficient prediction: build fields, predict, row-wise RMSE scoreboard ===
sp_Ks = [1, 2, 4, 8, 16]
sp_wells = []
for sp_fp in hw_files:
    _w = pd.read_csv(sp_fp, usecols=["X", "Y", "Z", "TVT", "TVT_input"])
    _z = _w["Z"].to_numpy(); _tvt = _w["TVT"].to_numpy()
    _X = _w["X"].to_numpy(); _Y = _w["Y"].to_numpy()
    _s = int(np.where(_w["TVT_input"].notna().to_numpy())[0].max())
    _dzl = np.diff(_z)[_s:]
    sp_wells.append(dict(wid=os.path.basename(sp_fp).split("__")[0], s=_s, X=_X, Y=_Y, tvt=_tvt,
                         U=np.cumsum(-_dzl), R0=_tvt[_s + 1:] - _tvt[_s], n=len(_dzl)))

for wi, wd in enumerate(sp_wells):
    wd["wi"] = wi; wd["seg"] = {}
    t = np.arange(1, wd["n"] + 1.0)
    for K in sp_Ks:
        edges = np.linspace(0, wd["n"], K + 1)
        phi = np.column_stack([np.clip(t - edges[j], 0, edges[j + 1] - edges[j]) for j in range(K)])
        c = np.linalg.lstsq(phi, wd["R0"] - wd["U"], rcond=None)[0]   # oracle segment drift rates
        mid, proj = [], []
        for j in range(K):
            f0 = wd["s"] + 1 + int(edges[j])
            f1 = min(wd["s"] + 1 + max(int(edges[j + 1]) - 1, int(edges[j])), len(wd["X"]) - 1)
            az = np.degrees(np.arctan2(wd["Y"][f1] - wd["Y"][f0], wd["X"][f1] - wd["X"][f0])) % 360
            mid.append(((wd["X"][f0] + wd["X"][f1]) / 2, (wd["Y"][f0] + wd["Y"][f1]) / 2))
            proj.append(np.cos(np.radians(az - theta0)))
        wd["seg"][K] = dict(phi=phi, c=c, mid=np.array(mid), proj=np.array(proj))

# deprojected dip-magnitude fields: rows (midX, midY, D=c/proj, well_index), usable |proj|>0.3
sp_fields = {K: np.array([(wd["seg"][K]["mid"][j, 0], wd["seg"][K]["mid"][j, 1],
                           wd["seg"][K]["c"][j] / wd["seg"][K]["proj"][j], wd["wi"])
                          for wd in sp_wells for j in range(K)
                          if abs(wd["seg"][K]["proj"][j]) > 0.3]) for K in sp_Ks}

def sp_predict(wd, K, k=10):
    """LOO kNN prediction of a well's segment drift rates (own well excluded from the field)."""
    F = sp_fields[K]; Fo = F[F[:, 3] != wd["wi"]]; sg = wd["seg"][K]
    chat = np.empty(K); dhat = np.empty(K)
    for j in range(K):
        d2 = (Fo[:, 0] - sg["mid"][j, 0]) ** 2 + (Fo[:, 1] - sg["mid"][j, 1]) ** 2
        dhat[j] = np.mean(Fo[np.argpartition(d2, k)[:k], 2])
        chat[j] = dhat[j] * sg["proj"][j]
    return chat, dhat

sp_res = {}
for wd in sp_wells:
    wd["chat"] = {}; wd["dhat"] = {}
    for K in sp_Ks:
        wd["chat"][K], wd["dhat"][K] = sp_predict(wd, K)

def sp_rowwise(pred_fn):
    return np.array([np.sqrt(np.nanmean((pred_fn(wd) - wd["R0"]) ** 2)) for wd in sp_wells])

sp_res["hold"] = sp_rowwise(lambda wd: np.zeros_like(wd["R0"]))
sp_res["const b_local (kappa=1)"] = sp_rowwise(
    lambda wd: wd["U"] + bloc[wd["wid"]] * np.arange(1, wd["n"] + 1.0))
sp_res["const b_local (kappa*)"] = sp_rowwise(
    lambda wd: 0.293 * (wd["U"] + bloc[wd["wid"]] * np.arange(1, wd["n"] + 1.0)))
for K in sp_Ks:
    sp_res[f"spline-pred K={K}"] = sp_rowwise(lambda wd, K=K: wd["U"] + wd["seg"][K]["phi"] @ wd["chat"][K])
sp_kappa = {}
for K in sp_Ks:  # global 1-dof shrink of the predicted drift (in-sample; move into CV later)
    num = sum(np.nansum((wd["U"] + wd["seg"][K]["phi"] @ wd["chat"][K]) * wd["R0"]) for wd in sp_wells)
    den = sum(np.nansum((wd["U"] + wd["seg"][K]["phi"] @ wd["chat"][K]) ** 2) for wd in sp_wells)
    sp_kappa[K] = num / den
    sp_res[f"spline-pred K={K} shrunk"] = sp_rowwise(
        lambda wd, K=K: sp_kappa[K] * (wd["U"] + wd["seg"][K]["phi"] @ wd["chat"][K]))
sp_res["oracle K=4 (ceiling)"] = sp_rowwise(lambda wd: wd["U"] + wd["seg"][4]["phi"] @ wd["seg"][4]["c"])

print(f"{'method':28s} {'rowwise mean':>12s} {'median':>8s} {'p90':>8s}")
for name, v in sp_res.items():
    print(f"{name:28s} {v.mean():12.2f} {np.median(v):8.2f} {np.percentile(v, 90):8.2f}")
print("\nkappa per K:", {K: round(sp_kappa[K], 3) for K in sp_Ks})

# --- why it works: coefficient predictability + spatial autocorrelation (K=4) ---
_tc = np.concatenate([wd["seg"][4]["c"] for wd in sp_wells])
_pc = np.concatenate([wd["chat"][4] for wd in sp_wells])
print(f"\nLOO-predicted vs oracle coefficients (K=4): corr = {np.corrcoef(_tc, _pc)[0, 1]:.3f}")
_dt, _dp = [], []
for wd in sp_wells:
    sg = wd["seg"][4]
    for j in range(4):
        if abs(sg["proj"][j]) > 0.3:
            _dt.append(sg["c"][j] / sg["proj"][j]); _dp.append(wd["dhat"][4][j])
print(f"deprojected magnitudes only (sign removed):  corr = {np.corrcoef(_dt, _dp)[0, 1]:.3f}"
      "   <- spatial skill beyond heading")
_F = sp_fields[4]; _XY = _F[:, :2]; _D = _F[:, 2]
_d2 = ((_XY[:, None, :] - _XY[None, :, :]) ** 2).sum(-1); np.fill_diagonal(_d2, np.inf)
_knn = np.argsort(_d2, axis=1)[:, :8]; _x = _D - _D.mean()
_mor = (len(_x) / (len(_x) * 8)) * sum(_x[i] * _x[_knn[i]].sum() for i in range(len(_x))) / np.sum(_x ** 2)
print(f"Moran's I of the segment dip-magnitude field (K=4): {_mor:+.3f}")

# --- cell 36 ---
# True TVT vs the different estimates on the HARDEST wells (largest true lateral drift = worst
# case for hold; exactly where prediction has to earn its keep). Reuses sp_wells/sp_res/sp_kappa.
sp_hard = np.argsort(sp_res["hold"])[::-1][:6]
fig, axes = plt.subplots(2, 3, figsize=(17, 9))
for ax, i in zip(axes.ravel(), sp_hard):
    wd = sp_wells[i]
    steps = np.arange(1, wd["n"] + 1.0); anchor = wd["tvt"][wd["s"]]
    p_holdline = np.full(wd["n"], anchor)
    p_const = anchor + 0.293 * (wd["U"] + bloc[wd["wid"]] * steps)      # old best (const-b kappa*)
    p_k4 = anchor + wd["U"] + wd["seg"][4]["phi"] @ wd["chat"][4]        # spline-pred K=4 (raw)
    p_k16 = anchor + sp_kappa[16] * (wd["U"] + wd["seg"][16]["phi"] @ wd["chat"][16])
    p_orc = anchor + wd["U"] + wd["seg"][4]["phi"] @ wd["seg"][4]["c"]   # oracle K=4 ceiling
    truth = anchor + wd["R0"]

    ax.plot(steps, truth, color="tab:orange", lw=2.2, label="truth")
    ax.plot(steps, p_holdline, "--", color="grey", lw=1, label="hold")
    ax.plot(steps, p_const, ":", color="tab:blue", lw=1.3, label="const-b kappa* (old best)")
    ax.plot(steps, p_k4, color="tab:green", lw=1.6, label="spline-pred K=4")
    ax.plot(steps, p_k16, color="tab:red", lw=1.2, label="spline-pred K=16 shrunk")
    ax.plot(steps, p_orc, "k:", lw=1, label="oracle K=4")
    e = lambda p: np.sqrt(np.nanmean((p - truth) ** 2))
    ax.set_title(f"{wd['wid'][:8]}  hold={e(p_holdline):.0f}  const={e(p_const):.0f}  "
                 f"K4={e(p_k4):.0f}  K16s={e(p_k16):.0f}  orc={e(p_orc):.1f}", fontsize=9)
    ax.set_xlabel("lateral step")
axes[0, 0].legend(fontsize=7)
axes[0, 0].set_ylabel("TVT"); axes[1, 0].set_ylabel("TVT")
plt.tight_layout()
plt.show()

# --- cell 38 ---
# === What "spatially-grouped 5-fold CV" means (and why random folds are leaky here) ===
# Random folds leave a held-out well's nearest neighbours in training — the kNN field can copy
# from wells a few hundred ft away, which mimics LOO, not deployment on an unseen region.
# Spatial folds hold out whole regions: quantile bands along the field's principal (SW-NE) axis.
cv_heels = np.array([(wd["X"][wd["s"]], wd["Y"][wd["s"]]) for wd in sp_wells])
cv_rng = np.random.default_rng(0)
cv_fold_rand = cv_rng.permutation(len(cv_heels)) % 5

_Hc = cv_heels - cv_heels.mean(0)
_axis = np.linalg.svd(_Hc, full_matrices=False)[2][0]          # principal axis of the field
_proj = _Hc @ _axis
_edges = np.quantile(_proj, np.linspace(0, 1, 6)); _edges[-1] += 1
cv_fold_spat = np.digitize(_proj, _edges[1:-1])                # 5 near-equal bands (kept for CV)

# leakage stats: is the nearest neighbour in the same fold? how far is the nearest TRAIN well?
_d2 = ((cv_heels[:, None, :] - cv_heels[None, :, :]) ** 2).sum(-1)
np.fill_diagonal(_d2, np.inf)
_nn = np.argmin(_d2, axis=1)
for _name, _f in [("random ", cv_fold_rand), ("spatial", cv_fold_spat)]:
    _dtrain = np.array([np.sqrt(_d2[i][_f != _f[i]].min()) for i in range(len(_f))])
    print(f"{_name}: nearest neighbour in SAME fold {(_f == _f[_nn]).mean():5.1%}   "
          f"dist to nearest TRAIN well: median {np.median(_dtrain):6.0f} ft   p90 {np.percentile(_dtrain, 90):6.0f} ft")
print("(the LOO kNN donors sit a few hundred ft away -> random CV keeps them; spatial CV removes them)")

fig, ax = plt.subplots(1, 2, figsize=(16, 7.5))
_cmap = plt.get_cmap("tab10")
for _a, (_name, _f) in zip(ax, [("random 5-fold (leaky: neighbours stay in train)", cv_fold_rand),
                                ("spatially-grouped 5-fold (honest: whole regions held out)", cv_fold_spat)]):
    for k in range(5):
        _m = _f == k
        _a.scatter(cv_heels[_m, 0], cv_heels[_m, 1], s=10, color=_cmap(k), label=f"fold {k+1} (n={_m.sum()})")
    _a.set_aspect("equal"); _a.set_title(_name, fontsize=11); _a.set_xlabel("X")
    _a.legend(fontsize=8, markerscale=1.5)
ax[0].set_ylabel("Y")
plt.show()

# --- cell 39 ---
# === 5-fold CV: random folds vs spatially-grouped folds ===
# Field built from TRAINING folds only; kappa fit on training wells (LOO within train);
# every well scored exactly once as held-out. Reuses sp_wells / sp_Ks / cv_fold_rand / cv_fold_spat.
def cv_make_field(K, train_set):
    return np.array([(wd["seg"][K]["mid"][j, 0], wd["seg"][K]["mid"][j, 1],
                      wd["seg"][K]["c"][j] / wd["seg"][K]["proj"][j], wd["wi"])
                     for wd in sp_wells if wd["wi"] in train_set
                     for j in range(K) if abs(wd["seg"][K]["proj"][j]) > 0.3])

def cv_predict(wd, K, F, exclude_self, k=10, want_dist=False):
    Fo = F[F[:, 3] != wd["wi"]] if exclude_self else F
    sg = wd["seg"][K]; ch = np.empty(K); dd = []
    for j in range(K):
        d2 = (Fo[:, 0] - sg["mid"][j, 0]) ** 2 + (Fo[:, 1] - sg["mid"][j, 1]) ** 2
        nb = np.argpartition(d2, min(k, len(Fo) - 1))[:k]
        ch[j] = np.mean(Fo[nb, 2]) * sg["proj"][j]
        if want_dist: dd.append(np.sqrt(np.median(d2[nb])))
    return (ch, np.median(dd)) if want_dist else ch

cv_results = {}; cv_donor4 = np.empty(len(sp_wells))   # median donor distance (spatial, K=4)
for scheme, fold in [("random", cv_fold_rand), ("spatial", cv_fold_spat)]:
    pw = {f"K{K}{s}": np.empty(len(sp_wells)) for K in sp_Ks for s in ("", "s")}
    kaps = {K: [] for K in sp_Ks}
    for f in range(5):
        train = set(np.where(fold != f)[0]); test = np.where(fold == f)[0]
        for K in sp_Ks:
            F = cv_make_field(K, train)
            num = den = 0.0                          # kappa on TRAIN (LOO within train)
            for wi in train:
                wd = sp_wells[wi]
                p = wd["U"] + wd["seg"][K]["phi"] @ cv_predict(wd, K, F, exclude_self=True)
                num += np.nansum(p * wd["R0"]); den += np.nansum(p * p)
            kap = num / den; kaps[K].append(kap)
            for wi in test:
                wd = sp_wells[wi]
                if scheme == "spatial" and K == 4:
                    ch, cv_donor4[wi] = cv_predict(wd, K, F, exclude_self=False, want_dist=True)
                else:
                    ch = cv_predict(wd, K, F, exclude_self=False)
                p = wd["U"] + wd["seg"][K]["phi"] @ ch
                pw[f"K{K}"][wi] = np.sqrt(np.nanmean((p - wd["R0"]) ** 2))
                pw[f"K{K}s"][wi] = np.sqrt(np.nanmean((kap * p - wd["R0"]) ** 2))
    cv_results[scheme] = dict(pw=pw, kappas={K: np.mean(v) for K, v in kaps.items()})

cv_hold = np.array([np.sqrt(np.nanmean(wd["R0"] ** 2)) for wd in sp_wells])
print(f"{'method':18s} {'random mean':>11s} {'med':>6s} | {'spatial mean':>12s} {'med':>6s}")
print(f"{'hold':18s} {cv_hold.mean():11.2f} {np.median(cv_hold):6.2f} | {cv_hold.mean():12.2f} {np.median(cv_hold):6.2f}")
for K in sp_Ks:
    for suf, tag in [("", ""), ("s", " shrunk")]:
        r = cv_results["random"]["pw"][f"K{K}{suf}"]; s_ = cv_results["spatial"]["pw"][f"K{K}{suf}"]
        print(f"{f'spline K={K}{tag}':18s} {r.mean():11.2f} {np.median(r):6.2f} | {s_.mean():12.2f} {np.median(s_):6.2f}")
print("mean kappa:", {sch: {K: round(v, 2) for K, v in cv_results[sch]['kappas'].items()} for sch in cv_results})

# --- salvage analysis: spatial-CV performance vs donor distance (K=4, kappa=0.6) ---
print("\nspatial CV, K=4 shrunk vs hold, binned by median donor distance:")
_pm = cv_results["spatial"]["pw"]["K4s"]
for lo, hi in [(0, 2000), (2000, 5000), (5000, 10000), (10000, 20000), (20000, 1e9)]:
    m = (cv_donor4 >= lo) & (cv_donor4 < hi)
    if m.sum():
        print(f"  {lo:6.0f}-{min(hi, 99999):6.0f} ft (n={m.sum():3d}): model {_pm[m].mean():6.2f}   "
              f"hold {cv_hold[m].mean():6.2f}   model wins {( _pm[m] < cv_hold[m]).mean():4.0%}")
print("=> signal transfers out to ~5,000 ft of donors, then hold wins: gate trust by donor distance.")

# --- cell 41 ---
# === Is random CV actually leaky for OUR deployment? Check where the real test wells sit. ===
# At test time we may build the donor field from ALL 773 training wells. So the question is only:
# are the test wells' donor distances in the LOO regime (<~5,000 ft) or the extrapolation regime?
test_files = sorted(glob.glob(os.path.join(path, "test", "*__horizontal_well.csv")))
tK = 4
tFX, tFY = [], []                      # training K=4 segment midpoints (the donor field)
theels = []
for _fp in hw_files:
    _w = pd.read_csv(_fp, usecols=["X", "Y", "TVT_input"])
    _s = int(np.where(_w["TVT_input"].notna().to_numpy())[0].max())
    theels.append((_w["X"].iloc[_s], _w["Y"].iloc[_s]))
    _n = len(_w) - _s - 1; _edges = np.linspace(0, _n, tK + 1)
    for j in range(tK):
        _f0 = _s + 1 + int(_edges[j]); _f1 = min(_s + 1 + max(int(_edges[j + 1]) - 1, int(_edges[j])), len(_w) - 1)
        tFX.append((_w["X"].iloc[_f0] + _w["X"].iloc[_f1]) / 2); tFY.append((_w["Y"].iloc[_f0] + _w["Y"].iloc[_f1]) / 2)
tFX = np.array(tFX); tFY = np.array(tFY); theels = np.array(theels)

fig, ax = plt.subplots(figsize=(9, 9))
ax.scatter(theels[:, 0], theels[:, 1], s=8, color="lightgrey", label="train wells (n=773)")
print(f"{'test well':10s} {'lateral pts':>11s}   donor dist per K=4 segment (ft, median of 10 nearest)")
for _fp, _c in zip(test_files, ["tab:red", "tab:blue", "tab:green"]):
    _wid = os.path.basename(_fp).split("__")[0]
    _w = pd.read_csv(_fp, usecols=["X", "Y", "TVT_input"])
    _s = int(np.where(_w["TVT_input"].notna().to_numpy())[0].max())
    _n = len(_w) - _s - 1; _edges = np.linspace(0, _n, tK + 1); _dd = []
    for j in range(tK):
        _f0 = _s + 1 + int(_edges[j]); _f1 = min(_s + 1 + max(int(_edges[j + 1]) - 1, int(_edges[j])), len(_w) - 1)
        _mx, _my = (_w["X"].iloc[_f0] + _w["X"].iloc[_f1]) / 2, (_w["Y"].iloc[_f0] + _w["Y"].iloc[_f1]) / 2
        _d2 = (tFX - _mx) ** 2 + (tFY - _my) ** 2
        _dd.append(np.sqrt(np.median(np.partition(_d2, 10)[:10])))
    ax.plot(_w["X"].iloc[::25], _w["Y"].iloc[::25], color=_c, lw=2.5, label=f"TEST {_wid}")
    print(f"{_wid:10s} {_n:11d}   " + "  ".join(f"{d:7.0f}" for d in _dd))
ax.set_aspect("equal"); ax.legend(); ax.set_xlabel("X"); ax.set_ylabel("Y")
ax.set_title("Test wells sit INSIDE the training field: donors at 0.8-2.2 kft << 5 kft range\n"
             "-> deployment is the LOO/random-CV regime; spatial CV is the (unneeded) worst case")
plt.show()

# --- cell 42 ---
# === Buffered LOO: re-rank K and kappa at the TEST wells' actual donor distances ===
# LOO donors sit ~500 ft away; the real test wells' donors sit 0.8-2.2 kft. Excluding all donors
# within radius R of each target segment simulates that regime and answers: does the K ranking
# hold, and what kappa is calibrated there? Reuses sp_wells / sp_Ks.
buf_Rs = [0, 500, 1000, 1500, 2000, 3000]
buf = {}
for K in sp_Ks:
    F = np.array([(wd["seg"][K]["mid"][j, 0], wd["seg"][K]["mid"][j, 1],
                   wd["seg"][K]["c"][j] / wd["seg"][K]["proj"][j], wd["wi"])
                  for wd in sp_wells for j in range(K) if abs(wd["seg"][K]["proj"][j]) > 0.3])
    preds = {R: [None] * len(sp_wells) for R in buf_Rs}
    for wd in sp_wells:
        sg = wd["seg"][K]; Fo = F[F[:, 3] != wd["wi"]]
        ch = {R: np.empty(K) for R in buf_Rs}
        for j in range(K):
            d2 = (Fo[:, 0] - sg["mid"][j, 0]) ** 2 + (Fo[:, 1] - sg["mid"][j, 1]) ** 2
            ordj = np.argsort(d2)
            for R in buf_Rs:
                sel = ordj[d2[ordj] >= R * R][:10]         # 10 nearest donors OUTSIDE radius R
                ch[R][j] = np.mean(Fo[sel, 2]) * sg["proj"][j]
        for R in buf_Rs:
            preds[R][wd["wi"]] = wd["U"] + sg["phi"] @ ch[R]
    for R in buf_Rs:
        kap = (sum(np.nansum(p * wd["R0"]) for p, wd in zip(preds[R], sp_wells))
               / sum(np.nansum(p * p) for p in preds[R]))
        shr = np.array([np.sqrt(np.nanmean((kap * p - wd["R0"]) ** 2)) for p, wd in zip(preds[R], sp_wells)])
        raw = np.array([np.sqrt(np.nanmean((p - wd["R0"]) ** 2)) for p, wd in zip(preds[R], sp_wells)])
        buf[(K, R)] = dict(kap=kap, raw=raw.mean(), shr=shr.mean(), shr_med=np.median(shr))

buf_hold = np.array([np.sqrt(np.nanmean(wd["R0"] ** 2)) for wd in sp_wells]).mean()
print(f"hold rowwise mean: {buf_hold:.2f}\n")
print("SHRUNK rowwise-mean RMSE vs donor-exclusion radius R (ft):")
print(f"{'K':>4s}" + "".join(f"{R:>9d}" for R in buf_Rs))
for K in sp_Ks:
    print(f"{K:4d}" + "".join(f"{buf[(K, R)]['shr']:9.2f}" for R in buf_Rs))
print("\nkappa(R):")
for K in sp_Ks:
    print(f"K={K:2d}: " + "  ".join(f"R{R}:{buf[(K, R)]['kap']:.2f}" for R in buf_Rs))

fig, ax = plt.subplots(figsize=(9, 5))
for K, c in zip(sp_Ks, plt.cm.viridis(np.linspace(0.1, 0.85, len(sp_Ks)))):
    ax.plot(buf_Rs, [buf[(K, R)]["shr"] for R in buf_Rs], "o-", color=c, label=f"K={K} shrunk")
ax.axhline(buf_hold, color="grey", ls="--", lw=1, label="hold")
ax.axvspan(800, 2200, color="tab:green", alpha=0.12, label="test wells' donor range")
ax.set_xlabel("donor-exclusion radius R (ft)"); ax.set_ylabel("rowwise mean RMSE (ft)")
ax.set_title("K=16 + kappa(R) stays best through the test-well donor regime")
ax.legend(fontsize=8)
plt.show()

# --- cell 44 ---
# === Adaptive kappa(d): per-segment trust from donor distance + rowwise-vs-POOLED audit ===
# Reuses sp_wells (K=16 segments). Per-step drift g = -dz + c_hat(segment); each segment's
# contribution is shrunk by kappa(bin of its donor distance). kappa_b solved in closed form
# jointly across buffer regimes R in {0,1000,1500,2000} (shared curve, 5 dof).
aK = 16
aRs = [0, 1000, 1500, 2000]
aF = np.array([(wd["seg"][aK]["mid"][j, 0], wd["seg"][aK]["mid"][j, 1],
                wd["seg"][aK]["c"][j] / wd["seg"][aK]["proj"][j], wd["wi"])
               for wd in sp_wells for j in range(aK) if abs(wd["seg"][aK]["proj"][j]) > 0.3])

a_data = {R: {} for R in aRs}
for wd in sp_wells:
    Fo = aF[aF[:, 3] != wd["wi"]]
    sg = wd["seg"][aK]
    edges = np.linspace(0, wd["n"], aK + 1)
    segid = np.clip(np.searchsorted(edges[1:], np.arange(1, wd["n"] + 1.0), side="left"), 0, aK - 1)
    ndz = np.diff(np.r_[0.0, wd["U"]])                    # recover -dz per lateral step from U
    d2m = [(Fo[:, 0] - sg["mid"][j, 0]) ** 2 + (Fo[:, 1] - sg["mid"][j, 1]) ** 2 for j in range(aK)]
    for R in aRs:
        ch = np.empty(aK); dd = np.empty(aK)
        for j in range(aK):
            ordj = np.argsort(d2m[j]); sel = ordj[d2m[j][ordj] >= R * R][:10]
            ch[j] = np.mean(Fo[sel, 2]) * sg["proj"][j]; dd[j] = np.sqrt(np.median(d2m[j][sel]))
        a_data[R][wd["wi"]] = (ndz + ch[segid], dd, segid)  # per-step drift estimate g, seg donor dist

A_BINS = [0, 750, 1500, 2500, 4000, 1e18]; nB = len(A_BINS) - 1
def a_G(g, dd, segid):
    bstep = np.digitize(dd, A_BINS[1:-1])[segid]
    return np.column_stack([np.cumsum(np.where(bstep == b, g, 0.0)) for b in range(nB)])

_A = np.zeros((nB, nB)); _y = np.zeros(nB)
for R in aRs:
    for wd in sp_wells:
        G = a_G(*a_data[R][wd["wi"]])
        _A += G.T @ G; _y += G.T @ wd["R0"]
kappa_bins = np.linalg.solve(_A, _y)
print("adaptive kappa per donor-distance bin (ft):")
for i in range(nB):
    print(f"  {A_BINS[i]:5.0f}-{min(A_BINS[i+1], 99999):5.0f}: kappa = {kappa_bins[i]:.3f}")

def a_scores(pred_fn, R):
    sq = n_ = 0; rw = []
    for wd in sp_wells:
        e = pred_fn(*a_data[R][wd["wi"]]) - wd["R0"]
        sq += np.nansum(e ** 2); n_ += int(np.isfinite(e).sum()); rw.append(np.sqrt(np.nanmean(e ** 2)))
    return np.mean(rw), np.median(rw), np.sqrt(sq / n_)

_hrw = np.mean([np.sqrt(np.nanmean(wd["R0"] ** 2)) for wd in sp_wells])
_hpool = np.sqrt(sum(np.nansum(wd["R0"] ** 2) for wd in sp_wells)
                 / sum(int(np.isfinite(wd["R0"]).sum()) for wd in sp_wells))
print(f"\n{'regime':>7s} {'method':20s} {'rowwise mean':>12s} {'med':>6s} {'POOLED (LB metric)':>18s}")
print(f"{'any':>7s} {'hold':20s} {_hrw:12.2f} {'':6s} {_hpool:18.2f}")
for R in aRs:
    kg = (sum(np.nansum(np.cumsum(a_data[R][wd['wi']][0]) * wd["R0"]) for wd in sp_wells)
          / sum(np.nansum(np.cumsum(a_data[R][wd['wi']][0]) ** 2) for wd in sp_wells))
    m1 = a_scores(lambda g, dd, si, kg=kg: kg * np.cumsum(g), R)
    m2 = a_scores(lambda g, dd, si: a_G(g, dd, si) @ kappa_bins, R)
    print(f"{R:7d} {f'global kappa={kg:.2f}':20s} {m1[0]:12.2f} {m1[1]:6.2f} {m1[2]:18.2f}")
    print(f"{R:7d} {'adaptive kappa(d)':20s} {m2[0]:12.2f} {m2[1]:6.2f} {m2[2]:18.2f}")
print("\n=> adaptive kappa(d) wins in every regime; pooled ~ rowwise + ~2.4 ft (LB reads pooled).")

# --- cell 46 ---
# === TVT curves: current best model (K=16 spline-pred + adaptive kappa(d)) across the error spectrum ===
# 9 wells at quantiles of per-well model RMSE (best -> median -> worst). Reuses sp_wells, a_data,
# a_G, kappa_bins from the adaptive-kappa cell (R=0 regime = deployment-like donor distances).
viz_rw = []
for wd in sp_wells:
    g, dd, si = a_data[0][wd["wi"]]
    pred = a_G(g, dd, si) @ kappa_bins
    viz_rw.append(np.sqrt(np.nanmean((pred - wd["R0"]) ** 2)))
viz_rw = np.array(viz_rw)
viz_order = np.argsort(viz_rw)
viz_qs = [0.02, 0.15, 0.30, 0.50, 0.65, 0.80, 0.90, 0.96, 1.0]
viz_pick = [viz_order[min(int(q * (len(viz_order) - 1)), len(viz_order) - 1)] for q in viz_qs]

fig, axes = plt.subplots(3, 3, figsize=(17, 12))
for ax, wi in zip(axes.ravel(), viz_pick):
    wd = sp_wells[wi]
    g, dd, si = a_data[0][wd["wi"]]
    steps = np.arange(1, wd["n"] + 1.0)
    anchor = wd["tvt"][wd["s"]]
    truth = anchor + wd["R0"]
    p_model = anchor + a_G(g, dd, si) @ kappa_bins
    p_orc = anchor + wd["U"] + wd["seg"][16]["phi"] @ wd["seg"][16]["c"]
    e_m = np.sqrt(np.nanmean((p_model - truth) ** 2))
    e_h = np.sqrt(np.nanmean((anchor - truth) ** 2))
    ax.plot(steps, truth, color="tab:orange", lw=2.2, label="truth")
    ax.plot(steps, np.full(wd["n"], anchor), "--", color="grey", lw=1, label="hold")
    ax.plot(steps, p_model, color="tab:green", lw=1.7, label="best model (K=16, adaptive kappa)")
    ax.plot(steps, p_orc, "k:", lw=1, label="oracle K=16 (ceiling)")
    ax.set_title(f"{wd['wid'][:8]}   model RMSE {e_m:.1f}  (hold {e_h:.1f})   "
                 f"donors ~{np.median(dd):.0f} ft", fontsize=9)
    ax.set_xlabel("lateral step")
for r in range(3):
    axes[r, 0].set_ylabel("TVT (ft)")
axes[0, 0].legend(fontsize=8)
fig.suptitle("Best model TVT reconstructions, wells sampled from best (top-left) to worst (bottom-right)",
             y=1.005, fontsize=12)
plt.tight_layout()
plt.show()

# --- cell 47 ---
# === Donor-disagreement check (NEGATIVE result, recorded) ===
# Hypothesis: variance among the 10 donors flags unreliable segments -> use as a 2nd kappa input.
# Reuses sp_wells + aF (K=16 donor field) from the adaptive-kappa cell. R=0 regime.
_errs, _diss, _dists = [], [], []
_wellstats = {}
for wd in sp_wells:
    Fo = aF[aF[:, 3] != wd["wi"]]; sg = wd["seg"][16]
    ds = np.empty(16); dd = np.empty(16); chat = np.empty(16)
    for j in range(16):
        d2 = (Fo[:, 0] - sg["mid"][j, 0]) ** 2 + (Fo[:, 1] - sg["mid"][j, 1]) ** 2
        sel = np.argpartition(d2, 10)[:10]
        chat[j] = np.mean(Fo[sel, 2]) * sg["proj"][j]
        ds[j] = np.std(Fo[sel, 2]) * abs(sg["proj"][j])   # donor disagreement, b-units
        dd[j] = np.sqrt(np.median(d2[sel]))
    _errs.extend(np.abs(chat - sg["c"])); _diss.extend(ds); _dists.extend(dd)
    _wellstats[wd["wid"]] = (np.mean(ds), np.median(dd))
_errs, _diss, _dists = map(np.array, (_errs, _diss, _dists))
print(f"per-segment corr(|coef error|, donor disagreement) = {np.corrcoef(_errs, _diss)[0, 1]:.3f}")
print(f"per-segment corr(|coef error|, donor distance)     = {np.corrcoef(_errs, _dists)[0, 1]:.3f}")
for _t in ["a9c9b150", "896d15b9"]:                      # the two failure wells from the TVT-curve grid
    _m, _d = _wellstats[_t]
    print(f"  {_t}: mean disagreement {_m:.4f} (percentile {(_diss < _m).mean():.0%}), donors ~{_d:.0f} ft")
print("""
CONCLUSION (negative): disagreement barely predicts error (r=0.19 vs 0.14 for distance alone);
adding it to kappa moved pooled RMSE by only ~0.03 ft, and within each distance bin the fitted
kappas for low- vs high-disagreement segments are nearly identical. Decisively: the worst well
(896d15b9) had donors at the 0th percentile of disagreement -- they all agreed AND were all wrong.
The remaining failures are 'local geology genuinely differs from neighbours', which no donor
statistic can detect; only the well's own signal (GR <-> typewell) could catch them.""")

# --- cell 48 ---
# === Autopsy of 896d15b9: why all 10 donors were in "wrong agreement" ===
# Answer: they weren't wrong about the geology -- OUR PROJECTION was. The target drills along
# STRIKE (az ~221 vs strike 208/28), so cos(az - theta0) = -0.21: the cosine transfer pins its
# predicted drift to ~0 with the WRONG SIGN, while the true drift (+0.05 ft/step) implies the
# LOCAL dip direction is rotated from the global theta0=118.4. Near strike, the projection is
# maximally sensitive to that rotation (d cos/d theta ~ 1). The donors, all dip-aligned, are fine.
_T = [wd for wd in sp_wells if wd["wid"] == "896d15b9"][0]
_sg = _T["seg"][16]
_az = np.empty(16)
for j in range(16):
    _e = np.linspace(0, _T["n"], 17)
    _f0 = _T["s"] + 1 + int(_e[j]); _f1 = min(_T["s"] + 1 + max(int(_e[j + 1]) - 1, int(_e[j])), len(_T["X"]) - 1)
    _az[j] = np.degrees(np.arctan2(_T["Y"][_f1] - _T["Y"][_f0], _T["X"][_f1] - _T["X"][_f0])) % 360
print(f"target heading az ~{_az.mean():.0f} deg (strike = 208/28)   proj = cos(az-118.4) ~ {_sg['proj'].mean():+.2f}")
print(f"target TRUE drift c: +{_sg['c'].mean():.3f} ft/step   deprojected D = {np.mean(_sg['c']/_sg['proj']):+.3f}"
      f"  (z = -8.3 vs local field +0.037 +/- 0.031 -> the DEPROJECTION is the outlier, not the rock)")
print(f"near-strike wells in training (mean |proj|<0.3): "
      f"{sum(abs(wd['seg'][16]['proj']).mean() < 0.3 for wd in sp_wells)} of {len(sp_wells)}")

_Fo = aF[aF[:, 3] != _T["wi"]]
_chat = np.empty(16)
for j in range(16):
    _d2 = (_Fo[:, 0] - _sg["mid"][j, 0]) ** 2 + (_Fo[:, 1] - _sg["mid"][j, 1]) ** 2
    _chat[j] = np.mean(_Fo[np.argpartition(_d2, 10)[:10], 2]) * _sg["proj"][j]

_donw = ["6a8fa194", "71ccf778", "9314ff13", "992ce078", "aaaf3c03"]   # the distinct donor wells
_cx, _cy = _sg["mid"].mean(0); _L = 6000
fig, ax = plt.subplots(1, 2, figsize=(16, 7))
for wd in sp_wells:
    if abs(wd["X"][wd["s"]] - _cx) < 1.6 * _L and abs(wd["Y"][wd["s"]] - _cy) < 1.6 * _L \
            and wd["wid"] not in _donw + ["896d15b9"]:
        ax[0].plot(wd["X"][::30], wd["Y"][::30], color="lightgrey", lw=0.8, zorder=1)
for _wid in _donw:
    wd = [w for w in sp_wells if w["wid"] == _wid][0]
    ax[0].annotate("", xy=(wd["X"][-1], wd["Y"][-1]), xytext=(wd["X"][wd["s"]], wd["Y"][wd["s"]]),
                   arrowprops=dict(arrowstyle="-|>", color="tab:blue", lw=2))
    _D = np.mean(wd["seg"][16]["c"] / wd["seg"][16]["proj"])
    ax[0].text(wd["seg"][16]["mid"][:, 0].mean(), wd["seg"][16]["mid"][:, 1].mean() + 300,
               f"{_wid[:8]}\nD={_D:+.3f}", fontsize=7, color="tab:blue", ha="center")
ax[0].annotate("", xy=(_T["X"][-1], _T["Y"][-1]), xytext=(_T["X"][_T["s"]], _T["Y"][_T["s"]]),
               arrowprops=dict(arrowstyle="-|>", color="tab:orange", lw=3))
ax[0].text(_cx, _cy - 600, "TARGET 896d15b9\naz 221 (STRIKE!)", color="tab:orange",
           fontsize=9, ha="center", weight="bold")
for _ang, _lbl, _c in [(118.4, "up-dip 118", "tab:cyan"), (298.4, "down-dip 298", "tab:red"),
                       (208.4, "strike 208", "tab:green"), (28.4, "strike 28", "tab:green")]:
    ax[0].annotate("", xy=(_cx - 0.85 * _L + 1500 * np.cos(np.radians(_ang)),
                           _cy + 0.85 * _L + 1500 * np.sin(np.radians(_ang))),
                   xytext=(_cx - 0.85 * _L, _cy + 0.85 * _L),
                   arrowprops=dict(arrowstyle="->", color=_c, lw=1.5))
    ax[0].text(_cx - 0.85 * _L + 1900 * np.cos(np.radians(_ang)),
               _cy + 0.85 * _L + 1900 * np.sin(np.radians(_ang)), _lbl, fontsize=7, color=_c, ha="center")
ax[0].set_xlim(_cx - 1.4 * _L, _cx + 1.4 * _L); ax[0].set_ylim(_cy - 1.2 * _L, _cy + 1.4 * _L)
ax[0].set_aspect("equal"); ax[0].set_xlabel("X"); ax[0].set_ylabel("Y")
ax[0].set_title("896d15b9 drills along STRIKE; its 5 donor wells all drill up-dip (az 142-165)")
_xs = np.arange(16)
ax[1].bar(_xs - 0.2, _sg["c"], 0.4, color="tab:orange", label="true c (drift/step)")
ax[1].bar(_xs + 0.2, _chat, 0.4, color="tab:green", label="predicted c = D_hat * cos(az-118)")
ax[1].axhline(0, color="k", lw=0.8)
ax[1].set_xlabel("segment"); ax[1].set_ylabel("drift rate c (ft/step)")
ax[1].set_title("Near strike the cosine pins the prediction to ~0 with the wrong sign")
ax[1].legend(fontsize=8)
plt.tight_layout(); plt.show()

# does this blind spot threaten the submission? check the 3 test wells' headings
for fp in sorted(glob.glob(os.path.join(path, "test", "*__horizontal_well.csv"))):
    w = pd.read_csv(fp, usecols=["X", "Y", "TVT_input"])
    s = int(np.where(w["TVT_input"].notna().to_numpy())[0].max())
    azt = np.degrees(np.arctan2(w["Y"].iloc[-1] - w["Y"].iloc[s], w["X"].iloc[-1] - w["X"].iloc[s])) % 360
    pj = np.cos(np.radians(azt - 118.4))
    print(f"TEST {os.path.basename(fp).split('__')[0]}: az {azt:4.0f}  proj {pj:+.2f}  "
          f"{'NEAR-STRIKE: fall back toward hold!' if abs(pj) < 0.35 else 'dip-aligned -> safe'}")

# --- cell 49 ---
# === How does K affect RMSE? Fine sweep, oracle vs deployable (adaptive kappa + proj gate) ===
# Oracle must improve monotonically with K (more dof). The DEPLOYABLE curve is the question:
# donor-predicted coefficients get noisier as segments shrink. Runtime ~3 min (K=48,64 dominate).
ks_Ks = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
ks_Rs = [0, 1500]
ks_GATE = 0.35
ks_DB = [0, 750, 1500, 2500, 4000, 1e18]; ks_nD = len(ks_DB) - 1
ks_rows = []
for K in ks_Ks:
    segs = []
    for wd in sp_wells:                                    # rebuild segmentation at this K
        n = wd["n"]; t = np.arange(1, n + 1.0); edges = np.linspace(0, n, K + 1)
        phi = np.column_stack([np.clip(t - edges[j], 0, edges[j + 1] - edges[j]) for j in range(K)])
        c = np.linalg.lstsq(phi, wd["R0"] - wd["U"], rcond=None)[0]
        segid = np.clip(np.searchsorted(edges[1:], t, side="left"), 0, K - 1)
        mid = np.empty((K, 2)); proj = np.empty(K)
        for j in range(K):
            f0 = wd["s"] + 1 + int(edges[j])
            f1 = min(wd["s"] + 1 + max(int(edges[j + 1]) - 1, int(edges[j])), len(wd["X"]) - 1)
            az = np.degrees(np.arctan2(wd["Y"][f1] - wd["Y"][f0], wd["X"][f1] - wd["X"][f0])) % 360
            mid[j] = ((wd["X"][f0] + wd["X"][f1]) / 2, (wd["Y"][f0] + wd["Y"][f1]) / 2)
            proj[j] = np.cos(np.radians(az - theta0))
        segs.append(dict(phi=phi, c=c, segid=segid, mid=mid, proj=proj,
                         dzl=-np.diff(np.r_[0.0, wd["U"]])))
    F = np.array([(sg["mid"][j, 0], sg["mid"][j, 1], sg["c"][j] / sg["proj"][j], wd["wi"])
                  for wd, sg in zip(sp_wells, segs) for j in range(K) if abs(sg["proj"][j]) > 0.3])
    orw = [np.sqrt(np.nanmean((wd["U"] + sg["phi"] @ sg["c"] - wd["R0"]) ** 2))
           for wd, sg in zip(sp_wells, segs)]
    Gs = {R: [] for R in ks_Rs}
    for wd, sg in zip(sp_wells, segs):
        Fo = F[F[:, 3] != wd["wi"]]
        for R in ks_Rs:
            ch = np.empty(K); dd = np.empty(K)
            for j in range(K):
                d2 = (Fo[:, 0] - sg["mid"][j, 0]) ** 2 + (Fo[:, 1] - sg["mid"][j, 1]) ** 2
                ordj = np.argsort(d2); sel = ordj[d2[ordj] >= R * R][:10]
                ch[j] = np.mean(Fo[sel, 2]) * sg["proj"][j]; dd[j] = np.sqrt(np.median(d2[sel]))
            g = -sg["dzl"] + ch[sg["segid"]]
            g = np.where(np.abs(sg["proj"][sg["segid"]]) < ks_GATE, 0.0, g)   # proj gate
            bstep = np.digitize(dd, ks_DB[1:-1])[sg["segid"]]
            Gs[R].append(np.column_stack([np.cumsum(np.where(bstep == b, g, 0.0)) for b in range(ks_nD)]))
    rec = {"K": K, "oracle": np.mean(orw)}
    for R in ks_Rs:
        A = np.zeros((ks_nD, ks_nD)); y = np.zeros(ks_nD)
        for G, wd in zip(Gs[R], sp_wells):
            A += G.T @ G; y += G.T @ wd["R0"]
        kb = np.linalg.lstsq(A, y, rcond=None)[0]
        rw = [np.sqrt(np.nanmean((G @ kb - wd["R0"]) ** 2)) for G, wd in zip(Gs[R], sp_wells)]
        sq = sum(np.nansum((G @ kb - wd["R0"]) ** 2) for G, wd in zip(Gs[R], sp_wells))
        n_ = sum(int(np.isfinite(wd["R0"]).sum()) for wd in sp_wells)
        rec[f"R{R}"] = np.mean(rw); rec[f"R{R}_pooled"] = np.sqrt(sq / n_)
    ks_rows.append(rec)
ks_D = pd.DataFrame(ks_rows)
print(ks_D.round(2).to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(ks_D["K"], ks_D["oracle"], "s--", color="grey", label="oracle (rowwise mean)")
ax.plot(ks_D["K"], ks_D["R0"], "o-", color="tab:green", label="deployable, LOO donors (~500 ft)")
ax.plot(ks_D["K"], ks_D["R1500"], "o-", color="tab:red", label="deployable, R=1500 donors")
for col, c in [("R0", "tab:green"), ("R1500", "tab:red")]:
    kmin = ks_D.loc[ks_D[col].idxmin(), "K"]
    ax.axvline(kmin, color=c, ls=":", lw=1, alpha=0.6)
ax.set_xscale("log", base=2); ax.set_xticks(ks_Ks); ax.set_xticklabels(ks_Ks)
ax.set_xlabel("K (segments per lateral)"); ax.set_ylabel("rowwise mean RMSE (ft)")
ax.set_title("Oracle improves forever; the deployable is U-shaped with a flat basin at K~16-32\n"
             "(elbow ~ where segment length reaches the ~500 ft donor-well spacing)")
ax.legend(fontsize=8)
plt.show()

# --- cell 50 ---
# === Hindcast kappa (ledger #4): can the landing audit the donor field? (NEGATIVE, recorded) ===
# The last stretch before PS is near-lateral WITH TVT_input known -> measure the local drift
# c_obs there (test wells have this too!), compare to the donor field's heel prediction
# (delta = c_obs - D_hat * cos(az - theta0)), and try to correct/shrink the forward model.
# Reuses sp_wells, aF, a_data, aRs, A_BINS, nB from the adaptive-kappa cell. ~30 s.
hc_caps = [150, 300, 500]
hc_cobs, hc_pbar = {}, {}
for wd, _fp in zip(sp_wells, hw_files):
    assert os.path.basename(_fp).startswith(wd["wid"])
    _kn = pd.read_csv(_fp, usecols=["Z", "TVT_input"])
    _s = wd["s"]
    _dz = np.diff(_kn["Z"].to_numpy()[:_s + 1]); _dti = np.diff(_kn["TVT_input"].to_numpy()[:_s + 1])
    _dx = np.diff(wd["X"][:_s + 1]); _dy = np.diff(wd["Y"][:_s + 1])
    _ok = np.isfinite(_dti) & (np.abs(_dz) < 0.3 * np.hypot(_dx, _dy))   # near-lateral (incl > ~73 deg)
    _W, _i = 0, _s - 1
    while _i >= 0 and _ok[_i] and _W < max(hc_caps):
        _W += 1; _i -= 1
    hc_cobs[wd["wi"]] = {c: float(np.mean(_dti[_s - min(_W, c):_s] + _dz[_s - min(_W, c):_s]))
                         for c in hc_caps if min(_W, c) >= 30}
    if _W >= 30:
        _sl = slice(_s - min(_W, 500), _s)
        _azw = np.degrees(np.arctan2(_dy[_sl], _dx[_sl])) % 360
        hc_pbar[wd["wi"]] = float(np.mean(np.cos(np.radians(_azw - theta0))))
print(f"usable landing windows: {sum(len(v) > 0 for v in hc_cobs.values())}/{len(sp_wells)} wells "
      f"(dMD=1 ft rows; per-step drift sd ~0.01 -> c_obs SE ~0.0004 over 500 steps: nearly noise-free)")

hc_dheel = {R: np.zeros(len(sp_wells)) for R in aRs}     # heel donor-field D_hat per buffer regime
for wd in sp_wells:
    _Fo = aF[aF[:, 3] != wd["wi"]]
    _d2h = (_Fo[:, 0] - wd["X"][wd["s"]]) ** 2 + (_Fo[:, 1] - wd["Y"][wd["s"]]) ** 2
    _oh = np.argsort(_d2h)
    for R in aRs:
        hc_dheel[R][wd["wi"]] = np.mean(_Fo[_oh[_d2h[_oh] >= R * R][:10], 2])
hc_delta = {R: np.array([hc_cobs[wd["wi"]].get(500, np.nan) - hc_dheel[R][wd["wi"]] * hc_pbar.get(wd["wi"], np.nan)
                         for wd in sp_wells]) for R in aRs}
hc_delta = {R: np.where(np.isfinite(d), d, 0.0) for R, d in hc_delta.items()}

# --- evidence: delta predicts the donor field's error ONLY at the heel ---
hc_err = np.empty((len(sp_wells), 16))                   # forward coef error c_true - c_hat (R=0 donors)
for wd in sp_wells:
    _g, _dd, _si = a_data[0][wd["wi"]]
    _ndz = np.diff(np.r_[0.0, wd["U"]])
    hc_err[wd["wi"]] = wd["seg"][16]["c"] - np.array([(_g - _ndz)[_si == j][0] for j in range(16)])
hc_r = [np.corrcoef(hc_delta[0], hc_err[:, j])[0, 1] for j in range(16)]
for _cap in hc_caps:
    _dc = np.array([hc_cobs[wd["wi"]].get(_cap, np.nan) - hc_dheel[0][wd["wi"]] * hc_pbar.get(wd["wi"], np.nan)
                    for wd in sp_wells])
    _mm = np.isfinite(_dc)
    print(f"window {_cap:3d} steps: corr(delta, coef err seg1) = {np.corrcoef(_dc[_mm], hc_err[_mm, 0])[0, 1]:.2f}"
          f"   seg2 = {np.corrcoef(_dc[_mm], hc_err[_mm, 1])[0, 1]:.2f}")

# --- deployment variants, fit jointly over buffer regimes like the adaptive-kappa cell ---
def hc_G(wd, R, mode):
    _g, _dd, _si = a_data[R][wd["wi"]]
    _gated = np.abs(wd["seg"][16]["proj"][_si]) < 0.35
    _delta = hc_delta[R][wd["wi"]]
    _bs = np.digitize(_dd, A_BINS[1:-1])[_si]
    _cols = [np.cumsum(np.where((_bs == b) & ~_gated, _g, 0.0)) for b in range(nB)]
    if mode == "sub":                                    # gated segs: -dz + own landing drift, not zero
        _co = hc_cobs[wd["wi"]].get(500)
        _gs = np.diff(np.r_[0.0, wd["U"]]) + (_co if _co is not None else 0.0)
        _cols.append(np.cumsum(np.where(_gated if _co is not None else np.zeros_like(_gated), _gs, 0.0)))
    elif mode == "corr":                                 # per-step delta correction, per-segment weights
        for _msk in [_si == 0, _si == 1, _si == 2, _si >= 3]:
            _cols.append(np.cumsum(np.where(_msk, _delta, 0.0)))
    elif mode in ("split", "placebo"):                   # kappa x |delta| interaction (vs parity placebo)
        _hi = float(abs(_delta) > 0.01) if mode == "split" else float(wd["wi"] % 2)
        _B = np.column_stack(_cols)
        return np.column_stack([_B * (1 - _hi), _B * _hi])
    return np.column_stack(_cols)

def hc_fit(mode, label):
    _A = _y = None; _c0 = {}
    for R in aRs:
        for wd in sp_wells:
            G = hc_G(wd, R, mode)
            if R == 0:
                _c0[wd["wi"]] = G
            if _A is None:
                _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
            _A += G.T @ G; _y += G.T @ wd["R0"]
    _b = np.linalg.lstsq(_A, _y, rcond=None)[0]
    _msg = f"{label:34s}"
    for R in [0, 1500]:
        _rw, _sq, _n = [], 0.0, 0
        for wd in sp_wells:
            e = (_c0[wd["wi"]] if R == 0 else hc_G(wd, R, mode)) @ _b - wd["R0"]
            _rw.append(np.sqrt(np.nanmean(e ** 2))); _sq += np.nansum(e ** 2); _n += int(np.isfinite(e).sum())
        _msg += f"   R{R}: {np.mean(_rw):5.2f}/{np.sqrt(_sq / _n):5.2f}"
    print(_msg + ("" if mode in ("gate", "split", "placebo") else f"   w={np.round(_b[nB:], 2)}"))
    return _b, _c0

print(f"\n{'variant':34s}   {'rowwise/POOLED':>15s}  {'rowwise/POOLED':>16s}")
hc_b0, hc_c0 = hc_fit("gate", "baseline: gate + kappa(d)")
hc_bc, hc_cc = hc_fit("corr", "+ delta correction (seg 1,2,3,4+)")
hc_fit("sub", "gate -> substitute own c_obs")
hc_fit("split", "kappa x |delta| interaction")
hc_fit("placebo", "placebo split (well parity)")

for _wid in ["896d15b9", "43e16325"]:
    wd = [w for w in sp_wells if w["wid"] == _wid][0]
    _e0 = np.sqrt(np.nanmean((hc_c0[wd["wi"]] @ hc_b0 - wd["R0"]) ** 2))
    _ec = np.sqrt(np.nanmean((hc_cc[wd["wi"]] @ hc_bc - wd["R0"]) ** 2))
    print(f"  {_wid}: baseline {_e0:5.1f} -> corrected {_ec:5.1f}   "
          f"c_obs={hc_cobs[wd['wi']].get(500, np.nan):+.4f}  vs lateral c={wd['seg'][16]['c'].mean():+.4f}")
print("TEST wells' delta (they all have full landing windows):")
for _fp in sorted(glob.glob(os.path.join(path, "test", "*__horizontal_well.csv"))):
    _tw = pd.read_csv(_fp, usecols=["X", "Y", "Z", "TVT_input"])
    _tX = _tw["X"].to_numpy(); _tY = _tw["Y"].to_numpy(); _ti = _tw["TVT_input"].to_numpy()
    _s = int(np.where(np.isfinite(_ti))[0].max())
    _dz = np.diff(_tw["Z"].to_numpy()[:_s + 1]); _dti = np.diff(_ti[:_s + 1])
    _dx = np.diff(_tX[:_s + 1]); _dy = np.diff(_tY[:_s + 1])
    _ok = np.isfinite(_dti) & (np.abs(_dz) < 0.3 * np.hypot(_dx, _dy))
    _W, _i = 0, _s - 1
    while _i >= 0 and _ok[_i] and _W < 500:
        _W += 1; _i -= 1
    _sl = slice(_s - _W, _s)
    _co = np.mean(_dti[_sl] + _dz[_sl])
    _pb = np.mean(np.cos(np.radians(np.degrees(np.arctan2(_dy[_sl], _dx[_sl])) % 360 - theta0)))
    _d2h = (aF[:, 0] - _tX[_s]) ** 2 + (aF[:, 1] - _tY[_s]) ** 2
    _Dh = np.mean(aF[np.argpartition(_d2h, 10)[:10], 2])
    print(f"  {os.path.basename(_fp).split('__')[0]}: W={_W}  c_obs={_co:+.4f}  "
          f"field={_Dh * _pb:+.4f}  delta={_co - _Dh * _pb:+.4f}")

print("""
CONCLUSION (negative, ledger #4 closed): the landing measures heel drift essentially noise-free,
and its disagreement with the donor field DOES predict the field's error -- but only for the first
1-2 segments (r=0.49 at seg 1, ~0 from seg 3): along-well drift decorrelates in ~300-600 ft, the
same ~500 ft scale we found spatially. Level RMSE is dominated by drift accumulated over the WHOLE
lateral, so every variant lands within ~0.03 ft of baseline, and the kappa-split's "gain" is
matched by a parity placebo with the same parameter count. Decisive counter-case: 896d15b9's own
landing (+0.005/step) disagrees with its lateral (+0.046/step) -- the anomaly develops DOWNSTREAM
of PS, so pre-PS data cannot catch confidently-wrong donors either; only GR could. The 3 test
wells all have |delta| <= 0.017, so even a shipped correction would move them by well under 1 ft.
KEEP: gate + adaptive kappa(d) at K=16, no hindcast term.""")

fig, ax = plt.subplots(figsize=(9, 3.6))
ax.bar(np.arange(1, 17), hc_r, color=["tab:green" if r > 0.2 else "tab:blue" for r in hc_r])
ax.axhline(0, color="k", lw=0.8)
ax.set_xticks(range(1, 17)); ax.set_xlabel("forward segment j (K=16)")
ax.set_ylabel("corr(delta, coef err seg j)")
ax.set_title("The landing predicts the donor field's error at the heel only\n"
             "(signal dies within ~2 segments = ~600 ft along-well)")
plt.show()

# --- cell 51 ---
# === kNN estimator details (ledger #2): k, weighting, aggregation, anisotropy ===
# Everything so far used one fixed rule: unweighted mean of the 10 nearest field points.
# Sweep each dimension (LOO, per-regime kappa refit like the K-sweep, gate on). ~2 min.
# Reuses sp_wells (K=16 segs), aF, A_BINS, theta0.
kn_Rs = [0, 1500]
kn_TOP = 100
kn_top = {R: {} for R in kn_Rs}                          # top-100 donors per (well, seg, regime)
for wd in sp_wells:
    _keep = aF[:, 3] != wd["wi"]
    _kx, _ky = aF[_keep, 0], aF[_keep, 1]
    _sg = wd["seg"][16]
    for R in kn_Rs:
        _idx = np.empty((16, kn_TOP), dtype=np.int64); _ds = np.empty((16, kn_TOP))
        for j in range(16):
            _d2 = (_kx - _sg["mid"][j, 0]) ** 2 + (_ky - _sg["mid"][j, 1]) ** 2
            _cand = np.where(_d2 >= R * R)[0] if R else np.arange(len(_d2))
            _o = _cand[np.argpartition(_d2[_cand], kn_TOP)[:kn_TOP]]
            _o = _o[np.argsort(_d2[_o])]
            _idx[j] = np.where(_keep)[0][_o]; _ds[j] = np.sqrt(_d2[_o])
        kn_top[R][wd["wi"]] = (_idx, _ds)

kn_rows = []
def kn_refit(chdd, label):
    row = {"rule": label}
    for R in kn_Rs:
        Gs = []
        for wd in sp_wells:
            ch, dd = chdd[R][wd["wi"]]
            _sg = wd["seg"][16]
            _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                          np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
            g = np.diff(np.r_[0.0, wd["U"]]) + ch[_si]
            g = np.where(np.abs(_sg["proj"][_si]) < 0.35, 0.0, g)
            _bs = np.digitize(dd, A_BINS[1:-1])[_si]
            Gs.append(np.column_stack([np.cumsum(np.where(_bs == b, g, 0.0)) for b in range(nB)]))
        _A = np.zeros((nB, nB)); _y = np.zeros(nB)
        for G, wd in zip(Gs, sp_wells):
            _A += G.T @ G; _y += G.T @ wd["R0"]
        _kb = np.linalg.lstsq(_A, _y, rcond=None)[0]
        _rw, _sq, _n = [], 0.0, 0
        for G, wd in zip(Gs, sp_wells):
            e = G @ _kb - wd["R0"]
            _rw.append(np.sqrt(np.nanmean(e ** 2))); _sq += np.nansum(e ** 2); _n += int(np.isfinite(e).sum())
        row[f"R{R}_rw"], row[f"R{R}_pool"] = np.mean(_rw), np.sqrt(_sq / _n)
    kn_rows.append(row)
    print(f"{label:32s} R0 {row['R0_rw']:5.2f}/{row['R0_pool']:5.2f}   R1500 {row['R1500_rw']:5.2f}/{row['R1500_pool']:5.2f}")

def kn_make(agg):
    chdd = {R: {} for R in kn_Rs}
    for wd in sp_wells:
        _sg = wd["seg"][16]
        for R in kn_Rs:
            _idx, _ds = kn_top[R][wd["wi"]]
            ch = np.empty(16); dd = np.empty(16)
            for j in range(16):
                Dh, dj = agg(_idx[j], _ds[j])
                ch[j] = Dh * _sg["proj"][j]; dd[j] = dj
            chdd[R][wd["wi"]] = (ch, dd)
    return chdd

def kn_gauss(i, d, k, h):                                # kernel-weighted mean (underflow-clamped)
    w = np.exp(np.maximum(-d[:k] ** 2 / (2 * h ** 2), -700))
    return np.sum(w * aF[i[:k], 2]) / np.sum(w), np.median(d[:k])

for k in [3, 5, 7, 10, 15, 20, 30, 50, 100]:             # 1) how many donors?
    kn_refit(kn_make(lambda i, d, k=k: (np.mean(aF[i[:k], 2]), np.median(d[:k]))), f"k={k:3d} uniform")
for p in [1, 2]:                                         # 2) inverse-distance weighting
    kn_refit(kn_make(lambda i, d, p=p: (np.sum(np.maximum(d[:10], 50.) ** -p * aF[i[:10], 2])
                                        / np.sum(np.maximum(d[:10], 50.) ** -p), np.median(d[:10]))),
             f"k= 10 IDW 1/d^{p}")
for h in [300, 400, 500, 600, 750]:                      # 3) Gaussian kernel, bandwidth sweep
    kn_refit(kn_make(lambda i, d, h=h: kn_gauss(i, d, 15, h)), f"k= 15 gauss h={h}")
kn_refit(kn_make(lambda i, d: kn_gauss(i, d, 15, max(np.median(d[:15]), 100.0))), "k= 15 gauss h=dmed")
kn_refit(kn_make(lambda i, d: (np.median(aF[i[:10], 2]), np.median(d[:10]))), "k= 10 median")
kn_refit(kn_make(lambda i, d: (np.mean(np.sort(aF[i[:10], 2])[2:8]), np.median(d[:10]))), "k= 10 trimmed 20%")

def kn_perwell(i, d, kwn=10):                            # 4) aggregate per distinct donor WELL first
    _ws = aF[i, 3]; _first, _vals, _dist = {}, [], []
    for _q in range(len(i)):
        if _ws[_q] not in _first:
            _first[_ws[_q]] = len(_vals); _vals.append([aF[i[_q], 2]]); _dist.append(d[_q])
        else:
            _vals[_first[_ws[_q]]].append(aF[i[_q], 2])
    _o = np.argsort(_dist)[:kwn]
    return np.mean([np.mean(_vals[q]) for q in _o]), np.median([_dist[q] for q in _o])
kn_refit(kn_make(kn_perwell), "per-WELL mean, 10 wells")

_cu, _su = np.cos(np.radians(theta0)), np.sin(np.radians(theta0))
for _lam in [0.5, 2.0]:                                  # 5) anisotropic selection (strike vs dip)
    chdd = {R: {} for R in kn_Rs}
    for wd in sp_wells:
        _keep = aF[:, 3] != wd["wi"]
        _kx, _ky, _kD = aF[_keep, 0], aF[_keep, 1], aF[_keep, 2]
        _sg = wd["seg"][16]
        for R in kn_Rs:
            ch = np.empty(16); dd = np.empty(16)
            for j in range(16):
                _dx = _kx - _sg["mid"][j, 0]; _dy = _ky - _sg["mid"][j, 1]
                _du = _dx * _cu + _dy * _su; _dv = -_dx * _su + _dy * _cu
                _d2i = _dx ** 2 + _dy ** 2
                _cand = np.where(_d2i >= R * R)[0] if R else np.arange(len(_d2i))
                _sel = _cand[np.argpartition((_lam * _du ** 2 + _dv ** 2 / _lam)[_cand], 10)[:10]]
                ch[j] = np.mean(_kD[_sel]) * _sg["proj"][j]; dd[j] = np.sqrt(np.median(_d2i[_sel]))
            chdd[R][wd["wi"]] = (ch, dd)
    kn_refit(chdd, f"aniso lam={_lam} (dip x{np.sqrt(_lam):.1f})")

print("""
VERDICT (ledger #2): distance weighting is the one real win -- Gaussian kernel h=500 ft, k=15
(flat basin: k 15-18, h 500-600 identical). It self-adapts: near donors -> weight spread wide;
far donors -> collapse onto the nearest few. h=500 ft is the SAME ~500 ft scale as the K-elbow
segment length and the along-well drift decorrelation: it is the field's correlation length.
Negatives: median/trimmed lose (field noise has no heavy tails to defend against); per-WELL
aggregation loses badly (a donor well's 16 segments are independently informative -- the
'pseudo-replication' was signal, not bias); anisotropy loses in BOTH directions (the dip field
is isotropic at donor spacing); h=dmed loses (bandwidth is geological, not configurational).
K rechecked under the kernel rule: K=16 still optimal.
ADOPT: K=16 + gate + adaptive kappa(d) + kernel kNN(k=15, h=500).
LOO:   R0 7.76/9.83 -> 7.69/9.67     R1500 9.52/11.72 -> 9.41/11.53""")

kn_D = pd.DataFrame(kn_rows)
fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))
_ks = [3, 5, 7, 10, 15, 20, 30, 50, 100]
ax[0].plot(_ks, kn_D["R0_pool"][:9], "o-", color="tab:green", label="R=0 pooled")
ax[0].plot(_ks, kn_D["R1500_pool"][:9], "o-", color="tab:red", label="R=1500 pooled")
ax[0].set_xscale("log"); ax[0].set_xticks(_ks); ax[0].set_xticklabels(_ks)
ax[0].set_xlabel("k (donors, uniform mean)"); ax[0].set_ylabel("pooled RMSE (ft)")
ax[0].set_title("Uniform kNN: k=7-10, then donor dilution"); ax[0].legend(fontsize=8)
_hs = [300, 400, 500, 600, 750]
_hrows = kn_D.iloc[11:16]
for col, cc, lbl in [("R0_pool", "tab:green", "R=0"), ("R1500_pool", "tab:red", "R=1500")]:
    ax[1].plot(_hs, _hrows[col], "o-", color=cc, label=f"{lbl} kernel k=15")
    ax[1].axhline(kn_D[col][3], color=cc, ls="--", lw=1, alpha=0.6)
ax[1].set_xlabel("Gaussian bandwidth h (ft)"); ax[1].set_ylabel("pooled RMSE (ft)")
ax[1].set_title("Kernel weighting beats uniform k=10 (dashed)\nbest h = 500 ft = the field's correlation length")
ax[1].legend(fontsize=8)
plt.tight_layout(); plt.show()

# --- cell 54 ---
# === GR feasibility gate (for parked ledger #8): do the TEST wells even have lateral GR? ===
# The no-GR scope decision was driven by gappy horizontal GR logs. Census before ever investing.
gr_cov = []
for _fp in hw_files:
    _w = pd.read_csv(_fp, usecols=["GR", "TVT_input"])
    _ti = _w["TVT_input"].to_numpy(); _g = _w["GR"].to_numpy()
    gr_cov.append(np.isfinite(_g[int(np.where(np.isfinite(_ti))[0].max()) + 1:]).mean())
gr_cov = np.array(gr_cov)
print(f"TRAIN lateral GR finite fraction, pct[5,25,50,75,95]: {np.round(np.percentile(gr_cov, [5, 25, 50, 75, 95]), 2)}")
print(f"  wells <50% covered: {(gr_cov < 0.5).sum()}/{len(gr_cov)}   <10%: {(gr_cov < 0.1).sum()}")
for _fp in sorted(glob.glob(os.path.join(path, "test", "*__horizontal_well.csv"))):
    _w = pd.read_csv(_fp, usecols=["GR", "TVT_input"])
    _ti = _w["TVT_input"].to_numpy(); _g = _w["GR"].to_numpy()
    _s = int(np.where(np.isfinite(_ti))[0].max())
    _lat = np.isfinite(_g[_s + 1:])
    _best = _cur = 0
    for _b in ~_lat:
        _cur = _cur + 1 if _b else 0
        _best = max(_best, _cur)
    print(f"TEST {os.path.basename(_fp).split('__')[0]}: lateral GR {_lat.mean():.1%} finite, "
          f"longest gap {_best} rows of {len(_lat)}")
print("=> the 3 test wells are better-logged than the median training well; GR (#8) is feasible"
      "\n   whenever we choose to pursue it. Parked for now -- geometry first.")

# --- cell 55 ---
# === Ledger #3: residual spatial autopsy + stacking go/no-go (NEGATIVE, recorded) ===
# If the adopted model's LOO residuals still cluster in (X,Y), a second pass could mine them.
# Reuses aF, kn_top, kn_gauss from the kNN cell. Honest test = predict a well's residual from
# OTHER wells' own LOO residuals (those are deployable knowledge). ~2 min (correlogram is brute force).
ra_Dhat = {}
for wd in sp_wells:
    _idx, _ds = kn_top[0][wd["wi"]]
    ra_Dhat[wd["wi"]] = np.array([kn_gauss(_idx[j], _ds[j], 15, 500.0)[0] for j in range(16)])
ra_F = np.array([(wd["seg"][16]["mid"][j, 0], wd["seg"][16]["mid"][j, 1],
                  wd["seg"][16]["c"][j] / wd["seg"][16]["proj"][j] - ra_Dhat[wd["wi"]][j], wd["wi"])
                 for wd in sp_wells for j in range(16) if abs(wd["seg"][16]["proj"][j]) > 0.3])
_r = ra_F[:, 2] - ra_F[:, 2].mean()
print(f"residual field: {len(ra_F)} pts  sd(resid D) = {ra_F[:, 2].std():.4f} vs sd(D) = {aF[:, 2].std():.4f}"
      f"  -> field explains ~{1 - ra_F[:, 2].var() / aF[:, 2].var():.0%} of drift variance")
_BINS = np.array([0, 500, 1000, 2000, 4000, 8000])
_sums = np.zeros(5); _cnts = np.zeros(5)
for _a in range(0, len(ra_F), 1500):
    _X1 = ra_F[_a:_a + 1500]
    _d = np.sqrt((_X1[:, 0, None] - ra_F[None, :, 0]) ** 2 + (_X1[:, 1, None] - ra_F[None, :, 1]) ** 2)
    _same = _X1[:, 3, None] == ra_F[None, :, 3]
    _prod = np.outer(_r[_a:_a + 1500], _r)
    for _b in range(5):
        _m = (_d >= _BINS[_b]) & (_d < _BINS[_b + 1]) & ~_same
        _sums[_b] += _prod[_m].sum(); _cnts[_b] += _m.sum()
print("correlogram of LOO drift residuals (cross-well pairs):")
for _b in range(5):
    print(f"  {_BINS[_b]:5d}-{_BINS[_b+1]:5d} ft: corr = {_sums[_b] / _cnts[_b] / _r.var():+.3f}")
print("NEGATIVE short-range correlation = the smoother's signature (neighbours share my donors),")
print("i.e. the kernel already extracted all shared signal. Confirmed by the deployable test:")

def ra_stack(lam):                                       # 2nd pass: kernel kNN over residual field
    chdd = {R: {} for R in [0, 1500]}
    for wd in sp_wells:
        _keep = ra_F[:, 3] != wd["wi"]
        _kx, _ky, _kr = ra_F[_keep, 0], ra_F[_keep, 1], ra_F[_keep, 2]
        _sg = wd["seg"][16]
        for R in [0, 1500]:
            _idx, _ds = kn_top[R][wd["wi"]]
            ch = np.empty(16); dd = np.empty(16)
            for j in range(16):
                _Dh, dd[j] = kn_gauss(_idx[j], _ds[j], 15, 500.0)
                _d2 = (_kx - _sg["mid"][j, 0]) ** 2 + (_ky - _sg["mid"][j, 1]) ** 2
                _cand = np.where(_d2 >= R * R)[0] if R else np.arange(len(_d2))
                _sel = _cand[np.argpartition(_d2[_cand], 15)[:15]]
                _w = np.exp(np.maximum(-_d2[_sel] / 5e5, -700))
                ch[j] = (_Dh + lam * np.sum(_w * _kr[_sel]) / np.sum(_w)) * _sg["proj"][j]
            chdd[R][wd["wi"]] = (ch, dd)
    return chdd
for _lam in [0.25, 0.5, 1.0]:
    kn_refit(ra_stack(_lam), f"+ residual stack lam={_lam}")
print("=> stacking hurts at every lam: we are AT the donor-information floor (ledger #3 closed).")

# --- cell 56 ---
# === Ledger #6: local dip DIRECTION -- a (Dx,Dy) vector field instead of fixed theta0 (NEGATIVE) ===
# c = Dx*cos(az) + Dy*sin(az) fit per query point by kernel-weighted ridge toward the global dipole.
# Uses ALL donor segments (near-strike donors inform direction; no |proj| cut, no deprojection
# singularity). If local dip direction rotates, this should beat the scalar field. ~2 min.
for wd in sp_wells:                                      # per-segment azimuth (seg stores proj only)
    _n = wd["n"]; _e = np.linspace(0, _n, 17); _az = np.empty(16)
    for j in range(16):
        _f0 = wd["s"] + 1 + int(_e[j])
        _f1 = min(wd["s"] + 1 + max(int(_e[j + 1]) - 1, int(_e[j])), len(wd["X"]) - 1)
        _az[j] = np.arctan2(wd["Y"][_f1] - wd["Y"][_f0], wd["X"][_f1] - wd["X"][_f0])
    wd["seg"][16]["azr"] = _az
vf_F = np.array([(wd["seg"][16]["mid"][j, 0], wd["seg"][16]["mid"][j, 1], wd["seg"][16]["c"][j],
                  wd["seg"][16]["azr"][j], wd["wi"]) for wd in sp_wells for j in range(16)])
vf_B0 = 0.035 * np.array([np.cos(np.radians(theta0)), np.sin(np.radians(theta0))])

def vf_chdd(a0, h=500.0):
    chdd = {R: {} for R in [0, 1500]}
    for wd in sp_wells:
        _keep = vf_F[:, 4] != wd["wi"]
        _kx, _ky, _kc, _ka = vf_F[_keep, 0], vf_F[_keep, 1], vf_F[_keep, 2], vf_F[_keep, 3]
        _sg = wd["seg"][16]
        for R in [0, 1500]:
            ch = np.empty(16); dd = np.empty(16)
            for j in range(16):
                _d2 = (_kx - _sg["mid"][j, 0]) ** 2 + (_ky - _sg["mid"][j, 1]) ** 2
                _cand = np.where(_d2 >= R * R)[0] if R else np.arange(len(_d2))
                _sel = _cand[np.argpartition(_d2[_cand], 60)[:60]]
                _w = np.exp(np.maximum(-_d2[_sel] / (2 * h ** 2), -700))
                _cs, _sn, _cv = np.cos(_ka[_sel]), np.sin(_ka[_sel]), _kc[_sel]
                _a = a0 * _w.sum()
                _A = np.array([[np.sum(_w * _cs * _cs) + _a, np.sum(_w * _cs * _sn)],
                               [np.sum(_w * _cs * _sn), np.sum(_w * _sn * _sn) + _a]])
                _b = np.array([np.sum(_w * _cv * _cs), np.sum(_w * _cv * _sn)]) + _a * vf_B0
                _D = np.linalg.solve(_A, _b)
                ch[j] = _D[0] * np.cos(_sg["azr"][j]) + _D[1] * np.sin(_sg["azr"][j])
                dd[j] = np.median(np.sqrt(_d2[_sel])[np.argsort(_d2[_sel])][:15])
            chdd[R][wd["wi"]] = (ch, dd)
    return chdd

for _a0 in [0.1, 0.5]:
    kn_refit(vf_chdd(_a0), f"vector field a0={_a0} (gate)")
print("""=> loses globally at every ridge strength (and more ridge -> worse -> the global dipole
direction is already the best uniform answer). Per-well autopsy (bash sweep, recorded): the vector
field RESCUES wells whose donors span headings (43e16325: 46->13, a9c9b150: 8->3) but DESTROYS
896d15b9 (30->80): with heading-homogeneous donors the direction is unconstrained exactly at the
near-strike blind spot. The scalar field + gate stays (ledger #6 closed).""")

# --- cell 57 ---
# === Ledger #5: ensemble over K (CLOSED: ceiling confirmed at ~0.03 ft) ===
# Average the LEVEL predictions of kernel-kNN models at K in {12,16,24,32} (own field + kappa each).
def ab_build(KK):
    _segs = []
    for wd in sp_wells:
        _n = wd["n"]; _t = np.arange(1, _n + 1.0); _e = np.linspace(0, _n, KK + 1)
        _phi = np.column_stack([np.clip(_t - _e[j], 0, _e[j + 1] - _e[j]) for j in range(KK)])
        _c = np.linalg.lstsq(_phi, wd["R0"] - wd["U"], rcond=None)[0]
        _si = np.clip(np.searchsorted(_e[1:], _t, side="left"), 0, KK - 1)
        _mid = np.empty((KK, 2)); _proj = np.empty(KK)
        for j in range(KK):
            _f0 = wd["s"] + 1 + int(_e[j])
            _f1 = min(wd["s"] + 1 + max(int(_e[j + 1]) - 1, int(_e[j])), len(wd["X"]) - 1)
            _azd = np.degrees(np.arctan2(wd["Y"][_f1] - wd["Y"][_f0], wd["X"][_f1] - wd["X"][_f0])) % 360
            _mid[j] = ((wd["X"][_f0] + wd["X"][_f1]) / 2, (wd["Y"][_f0] + wd["Y"][_f1]) / 2)
            _proj[j] = np.cos(np.radians(_azd - theta0))
        _segs.append(dict(c=_c, segid=_si, mid=_mid, proj=_proj, ndz=np.diff(np.r_[0.0, wd["U"]])))
    _F = np.array([(sg["mid"][j, 0], sg["mid"][j, 1], sg["c"][j] / sg["proj"][j], wd["wi"])
                   for wd, sg in zip(sp_wells, _segs) for j in range(KK) if abs(sg["proj"][j]) > 0.3])
    _preds = {}
    for R in [0, 1500]:
        _Gs = []
        for wd, sg in zip(sp_wells, _segs):
            _keep = _F[:, 3] != wd["wi"]
            _kx, _ky, _kD = _F[_keep, 0], _F[_keep, 1], _F[_keep, 2]
            ch = np.empty(KK); dd = np.empty(KK)
            for j in range(KK):
                _d2 = (_kx - sg["mid"][j, 0]) ** 2 + (_ky - sg["mid"][j, 1]) ** 2
                _cand = np.where(_d2 >= R * R)[0] if R else np.arange(len(_d2))
                _sel = _cand[np.argpartition(_d2[_cand], 15)[:15]]
                _w = np.exp(np.maximum(-_d2[_sel] / 5e5, -700))
                ch[j] = (np.sum(_w * _kD[_sel]) / np.sum(_w)) * sg["proj"][j]
                dd[j] = np.sqrt(np.median(_d2[_sel]))
            _g = sg["ndz"] + ch[sg["segid"]]
            _g = np.where(np.abs(sg["proj"][sg["segid"]]) < 0.35, 0.0, _g)
            _bs = np.digitize(dd, A_BINS[1:-1])[sg["segid"]]
            _Gs.append(np.column_stack([np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]))
        _A = np.zeros((nB, nB)); _y = np.zeros(nB)
        for _G, wd in zip(_Gs, sp_wells):
            _A += _G.T @ _G; _y += _G.T @ wd["R0"]
        _kb = np.linalg.lstsq(_A, _y, rcond=None)[0]
        _preds[R] = [G @ _kb for G in _Gs]
    return _preds

def ab_score(preds):
    _out = {}
    for R in [0, 1500]:
        _rw, _sq, _n = [], 0.0, 0
        for _p, wd in zip(preds[R], sp_wells):
            _e = _p - wd["R0"]
            _rw.append(np.sqrt(np.nanmean(_e ** 2))); _sq += np.nansum(_e ** 2); _n += int(np.isfinite(_e).sum())
        _out[R] = (np.mean(_rw), np.sqrt(_sq / _n))
    return _out

ab_all = {}
for KK in [12, 16, 24, 32]:
    ab_all[KK] = ab_build(KK)
    _s = ab_score(ab_all[KK])
    print(f"K={KK:2d}:            R0 {_s[0][0]:5.2f}/{_s[0][1]:5.2f}   R1500 {_s[1500][0]:5.2f}/{_s[1500][1]:5.2f}")
ab_ens = {R: [np.mean([ab_all[KK][R][i] for KK in [12, 16, 24, 32]], axis=0)
              for i in range(len(sp_wells))] for R in [0, 1500]}
_s = ab_score(ab_ens)
print(f"ENSEMBLE:        R0 {_s[0][0]:5.2f}/{_s[0][1]:5.2f}   R1500 {_s[1500][0]:5.2f}/{_s[1500][1]:5.2f}")
print("=> +-0.03 ft vs single K=16: the flat-basin prediction confirmed, not worth 4x compute.")

# --- cell 58 ---
# === Ledger #7: PS-truncation robustness + the kappa anatomy it exposed ===
# What if the anchor sat earlier in the well? Rebuild EVERYTHING (segments, field, kappa) with
# PS moved back 500 / 1000 rows on every training well; score the original lateral rows too.
# Also tests the architectural question it raised: should kappa shrink -dZ at all?  ~2 min.
def ps_run(DL, drift_only=False):
    _tw = []
    for _fp, wd0 in zip(hw_files, sp_wells):
        _w = pd.read_csv(_fp, usecols=["Z", "TVT"])
        _Z = _w["Z"].to_numpy(); _tvt = _w["TVT"].to_numpy()
        _s = max(wd0["s"] - DL, 60)
        _ndz = -np.diff(_Z)[_s:]
        _tw.append(dict(wi=wd0["wi"], s=_s, X=wd0["X"], Y=wd0["Y"], U=np.cumsum(_ndz),
                        R0=_tvt[_s + 1:] - _tvt[_s], n=len(_ndz), delta=wd0["s"] - _s))
    _segs = []
    for wd in _tw:
        _n = wd["n"]; _t = np.arange(1, _n + 1.0); _e = np.linspace(0, _n, 17)
        _phi = np.column_stack([np.clip(_t - _e[j], 0, _e[j + 1] - _e[j]) for j in range(16)])
        _c = np.linalg.lstsq(_phi, wd["R0"] - wd["U"], rcond=None)[0]
        _si = np.clip(np.searchsorted(_e[1:], _t, side="left"), 0, 15)
        _mid = np.empty((16, 2)); _proj = np.empty(16)
        for j in range(16):
            _f0 = wd["s"] + 1 + int(_e[j])
            _f1 = min(wd["s"] + 1 + max(int(_e[j + 1]) - 1, int(_e[j])), len(wd["X"]) - 1)
            _azd = np.degrees(np.arctan2(wd["Y"][_f1] - wd["Y"][_f0], wd["X"][_f1] - wd["X"][_f0])) % 360
            _mid[j] = ((wd["X"][_f0] + wd["X"][_f1]) / 2, (wd["Y"][_f0] + wd["Y"][_f1]) / 2)
            _proj[j] = np.cos(np.radians(_azd - theta0))
        _segs.append(dict(c=_c, segid=_si, mid=_mid, proj=_proj, ndz=np.diff(np.r_[0.0, wd["U"]])))
    _F = np.array([(sg["mid"][j, 0], sg["mid"][j, 1], sg["c"][j] / sg["proj"][j], wd["wi"])
                   for wd, sg in zip(_tw, _segs) for j in range(16) if abs(sg["proj"][j]) > 0.3])
    _Gs = []; _offs = []
    for wd, sg in zip(_tw, _segs):
        _keep = _F[:, 3] != wd["wi"]
        _kx, _ky, _kD = _F[_keep, 0], _F[_keep, 1], _F[_keep, 2]
        ch = np.empty(16); dd = np.empty(16)
        for j in range(16):
            _d2 = (_kx - sg["mid"][j, 0]) ** 2 + (_ky - sg["mid"][j, 1]) ** 2
            _sel = np.argpartition(_d2, 15)[:15]
            _w = np.exp(np.maximum(-_d2[_sel] / 5e5, -700))
            ch[j] = (np.sum(_w * _kD[_sel]) / np.sum(_w)) * sg["proj"][j]
            dd[j] = np.sqrt(np.median(_d2[_sel]))
        _gated = np.abs(sg["proj"][sg["segid"]]) < 0.35
        if drift_only:
            _g = np.where(_gated, 0.0, ch[sg["segid"]]); _off = np.cumsum(sg["ndz"])
        else:
            _g = np.where(_gated, 0.0, sg["ndz"] + ch[sg["segid"]]); _off = np.zeros(wd["n"])
        _bs = np.digitize(dd, A_BINS[1:-1])[sg["segid"]]
        _Gs.append(np.column_stack([np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]))
        _offs.append(_off)
    _A = np.zeros((nB, nB)); _y = np.zeros(nB)
    for _G, _off, wd in zip(_Gs, _offs, _tw):
        _A += _G.T @ _G; _y += _G.T @ (wd["R0"] - _off)
    _kb = np.linalg.lstsq(_A, _y, rcond=None)[0]
    _rw, _sq, _n = [], 0.0, 0
    for _G, _off, wd in zip(_Gs, _offs, _tw):
        _e = (_off + _G @ _kb - wd["R0"])[wd["delta"]:]          # original lateral rows only
        _rw.append(np.sqrt(np.nanmean(_e ** 2))); _sq += np.nansum(_e ** 2); _n += int(np.isfinite(_e).sum())
    return np.mean(_rw), np.sqrt(_sq / _n)

print("scored on the ORIGINAL lateral rows (same rows as the baseline 7.69/9.67):")
for _DL in [500, 1000]:
    _m, _p = ps_run(_DL)
    print(f"  PS-{_DL:4d} rows, kappa*(dz+c): {_m:5.2f}/{_p:5.2f}")
_m, _p = ps_run(1000, drift_only=True)
print(f"  PS-1000 rows, dz + kappa*c:  {_m:5.2f}/{_p:5.2f}   (kappa on drift only)")
print("""=> graceful at -500, a CLIFF at -1000. Mechanism: kappa multiplies (-dZ + c_hat) jointly,
and in steep build rows -dZ is real vertical signal that must not be shrunk. At the TRUE PS this
joint shrinkage is load-bearing, not a bug -- kappa-on-drift-only scores 13.3 pooled vs 9.67
(bash sweep, recorded): wells STEER along the layer, so -dZ anti-correlates with true drift and
shrinking the whole step toward hold-at-anchor is the right prior for uncertain drift.
Deployment-safe: the test wells' PS sits at the landing, like training. Ledger #7 closed.""")

# --- cell 59 ---
# === Blending with the last-known (hold) baseline: the full kappa-structure space ===
# Hold IS kappa->0, so "blend model + hold" = richer kappa structures. Candidates, all fit by the
# usual closed form, judged by a 5-FOLD KAPPA-HOLDOUT (fit kappa on 4/5 of wells, score the held
# fifth) -- in-sample wins with many params are cheap, holdout wins are real. Reuses kn_top/kn_gauss.
bl_chdd = {R: {} for R in [0, 1500]}
for wd in sp_wells:
    _sg = wd["seg"][16]
    for R in [0, 1500]:
        _idx, _ds = kn_top[R][wd["wi"]]
        ch = np.empty(16); dd = np.empty(16)
        for j in range(16):
            _Dh, dd[j] = kn_gauss(_idx[j], _ds[j], 15, 500.0)
            ch[j] = _Dh * _sg["proj"][j]
        bl_chdd[R][wd["wi"]] = (ch, dd)

def bl_G(wd, R, mode):
    ch, dd = bl_chdd[R][wd["wi"]]
    _sg = wd["seg"][16]
    _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                  np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
    _ndz = np.diff(np.r_[0.0, wd["U"]])
    _pr = np.abs(_sg["proj"][_si]); _gated = _pr < 0.35
    _g = np.where(_gated, 0.0, _ndz + ch[_si])
    _bs = np.digitize(dd, A_BINS[1:-1])[_si]
    _pos = (_si + 0.5) / 16
    cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
    if mode == "softgate":                               # gated steps: fitted kappa instead of 0
        cols.append(np.cumsum(np.where(_gated, _ndz + ch[_si], 0.0)))
    elif mode == "dz|c":                                 # separate kappa for -dz vs c_hat per bin
        cols = [np.cumsum(np.where((_bs == b) & ~_gated, _ndz, 0.0)) for b in range(nB)] + \
               [np.cumsum(np.where((_bs == b) & ~_gated, ch[_si], 0.0)) for b in range(nB)]
    elif mode == "projcls":                              # kappa x |proj| class (soft-gate superset)
        _pc = np.digitize(_pr, [0.35, 0.7])
        cols = [np.cumsum(np.where((_bs == b) & (_pc == pc), _ndz + ch[_si], 0.0))
                for pc in range(3) for b in range(nB)]
    elif mode == "pos-lin":
        cols.append(np.cumsum(_g * _pos))
    elif mode == "pos-sqrt":
        cols.append(np.cumsum(_g * np.sqrt(_pos)))
    return np.column_stack(cols)

def bl_run(mode, folds=False):
    _lab = f"{mode:22s}" + ("holdout " if folds else "in-samp ")
    _beta = None
    for R in [0, 1500]:
        _Gs = {wd["wi"]: bl_G(wd, R, mode) for wd in sp_wells}
        def _fit(skip):
            _A = _y = None
            for wd in sp_wells:
                if skip is not None and wd["wi"] % 5 == skip:
                    continue
                G = _Gs[wd["wi"]]
                if _A is None:
                    _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
                _A += G.T @ G; _y += G.T @ wd["R0"]
            return np.linalg.lstsq(_A, _y, rcond=None)[0]
        _rw, _sq, _n = [], 0.0, 0
        for f in (range(5) if folds else [None]):
            _kb = _fit(f)
            _beta = _kb if R == 0 else _beta
            for wd in sp_wells:
                if folds and wd["wi"] % 5 != f:
                    continue
                _e = _Gs[wd["wi"]] @ _kb - wd["R0"]
                _rw.append(np.sqrt(np.nanmean(_e ** 2))); _sq += np.nansum(_e ** 2); _n += int(np.isfinite(_e).sum())
        _lab += f"  R{R}: {np.mean(_rw):5.2f}/{np.sqrt(_sq / _n):5.2f}"
    print(_lab)
    return _beta

for _m in ["adopted", "softgate", "dz|c", "projcls", "pos-lin", "pos-sqrt"]:
    _b = bl_run(_m)
    if _m == "softgate":
        print(f"    -> fitted kappa_gate = {_b[-1]:+.3f}: the hard gate was already right")
    if _m == "dz|c":
        print(f"    -> kappa_dz {np.round(_b[:nB], 2)} == kappa_c {np.round(_b[nB:], 2)}: joint shrinkage is optimal")
print("--- the honest comparison (kappa fit on 4/5 wells, scored on the held fifth) ---")
for _m in ["adopted", "softgate", "projcls", "pos-lin", "pos-sqrt"]:
    bl_run(_m, folds=True)
bl_beta = bl_run("pos-sqrt")
print(f"""
=> projcls wins in-sample and COLLAPSES under holdout (overfit); softgate/dz|c confirm the
   existing architecture. The one REAL winner is position decay: kappa(d) {np.round(bl_beta[:nB], 2)}
   plus {bl_beta[-1]:+.2f} * sqrt(position along lateral) -- trust the drift field less as
   accumulated error grows, i.e. the blend toward last-known TIGHTENS along the well.
   ADOPTED as the reference model (one extra parameter, wins all four holdout stats).
   Cumulative LOO gain since the LB submission: 9.67 -> 9.46 pooled (< 0.5 resubmit threshold).
   Also tested on top (recorded negative): trailing rolling -dZ 'steering trend' columns at 50 and
   300 ft -- holdout unchanged; the optimal per-step dz blend already carries that information.""")

# --- cell 60 ---
# === Consolidation audit: independent re-verification of every load-bearing computation ===
# Each check recomputes a quantity through a DIFFERENT code path and asserts agreement.
import numpy.testing as npt
aud = []
def _ok(name, cond):
    aud.append((name, bool(cond))); print(f"  {'PASS' if cond else 'FAIL'}  {name}")

# 1) PS index, anchor, target, and -dZ integration (raw CSV vs sp_wells)
for _wd in [sp_wells[13], sp_wells[400], sp_wells[772]]:
    _w = pd.read_csv(os.path.join(train_dir, f"{_wd['wid']}__horizontal_well.csv"))
    _ti = _w["TVT_input"].to_numpy(); _tvt = _w["TVT"].to_numpy(); _Z = _w["Z"].to_numpy()
    _s = int(np.where(np.isfinite(_ti))[0].max())
    _ok(f"{_wd['wid']}: PS index", _s == _wd["s"])
    _ok(f"{_wd['wid']}: target R0 rows s+1..end, anchored at s",
        np.allclose(_wd["R0"], _tvt[_s + 1:] - _tvt[_s], equal_nan=True) and _wd["n"] == len(_Z) - 1 - _s)
    _ok(f"{_wd['wid']}: U = integral of -dZ over lateral",
        np.allclose(_wd["U"], np.cumsum(-(np.diff(_Z)[_s:]))))
    _ok(f"{_wd['wid']}: TVT_input == TVT wherever given",
        np.nanmax(np.abs(_ti[:_s + 1] - _tvt[:_s + 1])) == 0.0)

# 2) spline ramp <-> segment-id consistency (phi increments must one-hot the segid)
_wd = sp_wells[123]; _sg = _wd["seg"][16]
_si = np.clip(np.searchsorted(np.linspace(0, _wd["n"], 17)[1:],
                              np.arange(1, _wd["n"] + 1.0), side="left"), 0, 15)
_dphi = np.diff(np.vstack([np.zeros(16), _sg["phi"]]), axis=0)
_pure = _dphi.max(1) > 0.999                             # steps that don't straddle a fractional edge
_ok(f"phi ramp == one-hot(segid) on all {int(_pure.sum())} non-straddle steps "
    f"({int((~_pure).sum())} edge-straddle steps use the documented next-segment convention)",
    np.array_equal(np.argmax(_dphi[_pure], axis=1), _si[_pure]) and np.allclose(_dphi.sum(1), 1.0))
_ok("spline LS normal equations satisfied (phi' r = 0)",
    np.abs(_sg["phi"].T @ (_wd["R0"] - _wd["U"] - _sg["phi"] @ _sg["c"])).max() < 1e-5 * _wd["n"])

# 3) donor field: deproject/reproject roundtrip + own-well exclusion
_rows = aF[np.random.default_rng(1).choice(len(aF), 200, replace=False)]
_ok("field D * proj == segment c (roundtrip, sampled)",
    all(abs(_r[2] * sp_wells[int(_r[3])]["seg"][16]["proj"][
        int(np.argmin((sp_wells[int(_r[3])]["seg"][16]["mid"] - _r[:2]) ** 2 @ np.ones(2)))]
        - sp_wells[int(_r[3])]["seg"][16]["c"][
        int(np.argmin((sp_wells[int(_r[3])]["seg"][16]["mid"] - _r[:2]) ** 2 @ np.ones(2)))]) < 1e-9
        for _r in _rows))
_idx, _ds = kn_top[0][sp_wells[50]["wi"]]
_ok("LOO: no own-well points among selected donors", (aF[_idx.ravel(), 3] != sp_wells[50]["wi"]).all())
_ok("buffered LOO: all donors respect d >= 1500", (kn_top[1500][sp_wells[50]["wi"]][1] >= 1500).all())

# 4) kernel weights: manual recompute of one segment's D_hat
_j = 7; _i, _d = kn_top[0][sp_wells[50]["wi"]]
_w = np.exp(-_d[_j][:15] ** 2 / (2 * 500.0 ** 2))
_ok("kernel kNN D_hat matches manual computation",
    abs(np.sum(_w * aF[_i[_j][:15], 2]) / np.sum(_w) - kn_gauss(_i[_j], _d[_j], 15, 500.0)[0]) < 1e-12)

# 5) metric identity: pooled^2 == row-count-weighted mean of rowwise^2
_rws = []; _ns = []; _sq = 0.0
for _wd in sp_wells[:100]:
    _e = _wd["R0"] - _wd["U"]                            # any residual works for the identity
    _rws.append(np.nanmean(_e ** 2)); _ns.append(int(np.isfinite(_e).sum())); _sq += np.nansum(_e ** 2)
_ok("pooled RMSE == sqrt(sum(n_w * rowwiseMSE_w) / sum(n_w))",
    abs(np.sqrt(_sq / sum(_ns)) - np.sqrt(np.sum(np.array(_rws) * np.array(_ns)) / sum(_ns))) < 1e-12)

# 6) submission reproducibility: independent straight-line reimplementation of one test well,
#    using the kappa printed by make_submission.py, compared against the shipped submission.csv
if os.path.exists("submission.csv"):
    _kap = np.array([0.812, 0.722, 0.618, 0.372, 0.109])
    _fp = os.path.join(path, "test", "000d7d20__horizontal_well.csv")
    _w = pd.read_csv(_fp); _ti = _w["TVT_input"].to_numpy()
    _s = int(np.where(np.isfinite(_ti))[0].max())
    _X = _w["X"].to_numpy(); _Y = _w["Y"].to_numpy(); _Z = _w["Z"].to_numpy()
    _n = len(_Z) - 1 - _s; _e16 = np.linspace(0, _n, 17)
    _pred = np.empty(_n); _lvl = _ti[_s]; _t = 0
    for _j in range(16):
        _f0 = _s + 1 + int(_e16[_j]); _f1 = min(_s + 1 + max(int(_e16[_j + 1]) - 1, int(_e16[_j])), len(_X) - 1)
        _azr = np.arctan2(_Y[_f1] - _Y[_f0], _X[_f1] - _X[_f0])
        _prj = np.cos(_azr - np.radians(theta0))
        _mx, _my = (_X[_f0] + _X[_f1]) / 2, (_Y[_f0] + _Y[_f1]) / 2
        _d2 = (aF[:, 0] - _mx) ** 2 + (aF[:, 1] - _my) ** 2
        _sel = np.argpartition(_d2, 15)[:15]
        _wt = np.exp(np.maximum(-_d2[_sel] / 5e5, -700))
        _chat = (np.sum(_wt * aF[_sel, 2]) / np.sum(_wt)) * _prj
        _kj = _kap[np.digitize(np.sqrt(np.median(_d2[_sel])), A_BINS[1:-1])]
        _gate = 0.0 if abs(_prj) < 0.35 else 1.0
        while _t < _n and _t < _e16[_j + 1]:
            _row = _s + 1 + _t
            _lvl += _kj * _gate * (-(_Z[_row] - _Z[_row - 1]) + _chat)
            _pred[_t] = _lvl; _t += 1
    _sub = pd.read_csv("submission.csv")
    _mine = _sub[_sub["id"].str.startswith("000d7d20")]["tvt"].to_numpy()
    # tolerance 0.02 ft: this check uses the PRINTED 3-decimal kappa, so ~4e-3 ft of accumulated
    # rounding is expected; anything beyond that would flag a real pipeline discrepancy
    _ok(f"submission.csv reproduced independently for 000d7d20 (max diff "
        f"{np.abs(_pred - _mine).max():.2e} ft, tol 0.02 for rounded kappa)",
        np.abs(_pred - _mine).max() < 0.02)
else:
    print("  SKIP  submission.csv not present")
print(f"\nAUDIT: {sum(c for _, c in aud)}/{len(aud)} checks passed")

# --- cell 61 ---
# === Worst-well gallery under the CURRENT BEST model (kernel kNN + kappa(d) - 0.55*sqrt(pos)) ===
# The 12 worst wells by rowwise RMSE (R=0 LOO), for visual failure analysis: where exactly does
# the best deployable diverge from truth, and would the oracle (drift representation) have coped?
ga_preds = {}
ga_kb = None
for R in [0]:
    _Gs = {}
    for wd in sp_wells:
        ch, dd = bl_chdd[R][wd["wi"]]
        _sg = wd["seg"][16]
        _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                      np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
        _g = np.where(np.abs(_sg["proj"][_si]) < 0.35, 0.0, np.diff(np.r_[0.0, wd["U"]]) + ch[_si])
        _bs = np.digitize(dd, A_BINS[1:-1])[_si]
        _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
        _cols.append(np.cumsum(_g * np.sqrt((_si + 0.5) / 16)))
        _Gs[wd["wi"]] = np.column_stack(_cols)
    _A = np.zeros((nB + 1, nB + 1)); _y = np.zeros(nB + 1)
    for wd in sp_wells:
        G = _Gs[wd["wi"]]; _A += G.T @ G; _y += G.T @ wd["R0"]
    ga_kb = np.linalg.lstsq(_A, _y, rcond=None)[0]
    for wd in sp_wells:
        ga_preds[wd["wi"]] = _Gs[wd["wi"]] @ ga_kb
ga_rw = np.array([np.sqrt(np.nanmean((ga_preds[wd["wi"]] - wd["R0"]) ** 2)) for wd in sp_wells])
print(f"best model rowwise mean {ga_rw.mean():.2f}, median {np.median(ga_rw):.2f} | "
      f"worst 12 wells account for {100 * np.sort(ga_rw)[-12:].mean() ** 2 * 12 / (ga_rw ** 2).sum():.0f}% "
      f"of total squared rowwise error")

ga_worst = np.argsort(ga_rw)[-12:][::-1]
fig, axes = plt.subplots(4, 3, figsize=(17, 15))
for ax, wi in zip(axes.ravel(), ga_worst):
    wd = sp_wells[wi]
    _sg = wd["seg"][16]
    _anchor = wd["tvt"][wd["s"]]
    _steps = np.arange(1, wd["n"] + 1)
    _, _ddw = bl_chdd[0][wd["wi"]]
    ax.plot(_steps, _anchor + wd["R0"], color="tab:orange", lw=2.2, label="truth")
    ax.plot(_steps, np.full(wd["n"], _anchor), "--", color="grey", lw=1, label="hold")
    ax.plot(_steps, _anchor + ga_preds[wd["wi"]], color="tab:green", lw=1.7, label="best model")
    ax.plot(_steps, _anchor + wd["U"] + _sg["phi"] @ _sg["c"], "k:", lw=1.2, label="oracle K=16")
    _e = np.sqrt(np.nanmean((ga_preds[wd["wi"]] - wd["R0"]) ** 2))
    _eh = np.sqrt(np.nanmean(wd["R0"] ** 2))
    ax.set_title(f"{wd['wid'][:8]}  model {_e:.1f} ft (hold {_eh:.1f})   "
                 f"donors ~{np.median(_ddw):.0f} ft   proj {np.mean(_sg['proj']):+.2f}", fontsize=9)
    ax.set_xlabel("lateral step")
for _r in range(4):
    axes[_r, 0].set_ylabel("TVT (ft)")
axes[0, 0].legend(fontsize=8)
fig.suptitle("The 12 WORST wells under the best deployable (LOO). Read: is the miss a level ramp "
             "(field wrong locally)\nor shape the oracle also lacks? Orange=truth, green=model, "
             "dotted=oracle ceiling, grey=hold.", y=1.0, fontsize=12)
plt.tight_layout()
plt.show()

# --- cell 63 ---
# === Diagnostic 1/4 -- GATE WELLS: how the gate metric |cos(az-theta0)| evolves along the well,
# and what it does to the TVT prediction. Also shows the UNGATED counterfactual, so the gate's
# damage-control trade is visible per well. Reuses bl_chdd, ga_kb, ga_preds.
d1_wids = ["43e16325", "896d15b9"]
fig, axes = plt.subplots(2, 2, figsize=(17, 10))
for _r, _wid in enumerate(d1_wids):
    wd = [w for w in sp_wells if w["wid"] == _wid][0]
    _sg = wd["seg"][16]
    _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                  np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
    _steps = np.arange(1, wd["n"] + 1)
    # continuous heading (100-step window) vs the per-segment staircase the model actually uses
    _W = 50
    _rows = wd["s"] + 1 + _steps.astype(int) - 1
    _r0 = np.clip(_rows - _W, 0, len(wd["X"]) - 1); _r1 = np.clip(_rows + _W, 0, len(wd["X"]) - 1)
    _azc = np.degrees(np.arctan2(wd["Y"][_r1] - wd["Y"][_r0], wd["X"][_r1] - wd["X"][_r0])) % 360
    _pcont = np.cos(np.radians(_azc - theta0))
    _pseg = _sg["proj"][_si]
    ax = axes[_r, 0]
    ax.plot(_steps, np.abs(_pcont), color="tab:blue", lw=1, label="|cos(az-theta0)|, 100-step heading")
    ax.step(_steps, np.abs(_pseg), color="k", lw=1.8, where="post", label="per-segment (used by model)")
    ax.axhline(0.35, color="tab:red", ls="--", lw=1.2, label="gate threshold 0.35")
    ax.fill_between(_steps, 0, 1, where=np.abs(_pseg) < 0.35, color="tab:red", alpha=0.08)
    ax.set_ylim(0, 1.05); ax.set_ylabel("|proj|"); ax.set_xlabel("lateral step")
    _gf = (np.abs(_sg["proj"]) < 0.35).sum()
    ax.set_title(f"{_wid}: gate metric along the lateral -- {_gf}/16 segments gated", fontsize=10)
    ax.legend(fontsize=8, loc="upper right")
    # TVT: truth / gated model / UNGATED counterfactual / oracle
    ch, dd = bl_chdd[0][wd["wi"]]
    _ndz = np.diff(np.r_[0.0, wd["U"]])
    _bs = np.digitize(dd, A_BINS[1:-1])[_si]
    _gu = _ndz + ch[_si]                                  # no gate
    _Gu = np.column_stack([np.cumsum(np.where(_bs == b, _gu, 0.0)) for b in range(nB)]
                          + [np.cumsum(_gu * np.sqrt((_si + 0.5) / 16))])
    _anchor = wd["tvt"][wd["s"]]
    ax = axes[_r, 1]
    ax.plot(_steps, _anchor + wd["R0"], color="tab:orange", lw=2.2, label="truth")
    ax.plot(_steps, _anchor + ga_preds[wd["wi"]], color="tab:green", lw=1.8, label="model (gated)")
    ax.plot(_steps, _anchor + _Gu @ ga_kb, color="tab:purple", lw=1.4, label="counterfactual: NO gate")
    ax.plot(_steps, _anchor + wd["U"] + _sg["phi"] @ _sg["c"], "k:", lw=1.1, label="oracle")
    ax.plot(_steps, np.full(wd["n"], _anchor), "--", color="grey", lw=1, label="hold")
    ax.fill_between(_steps, *ax.get_ylim(), where=np.abs(_pseg) < 0.35, color="tab:red", alpha=0.06)
    _eg = np.sqrt(np.nanmean((ga_preds[wd["wi"]] - wd["R0"]) ** 2))
    _eu = np.sqrt(np.nanmean((_Gu @ ga_kb - wd["R0"]) ** 2))
    ax.set_title(f"{_wid}: TVT -- gated {_eg:.1f} ft vs ungated {_eu:.1f} ft (red = gated span)", fontsize=10)
    ax.set_xlabel("lateral step"); ax.set_ylabel("TVT (ft)"); ax.legend(fontsize=8)
    print(f"{_wid}: |proj| range [{np.abs(_sg['proj']).min():.2f}, {np.abs(_sg['proj']).max():.2f}]"
          f"  gated {_gf}/16  RMSE gated {_eg:.1f} / ungated {_eu:.1f}"
          f"  true drift c mean {_sg['c'].mean():+.4f} ft/step")
plt.tight_layout(); plt.show()
print("""READ: |proj| sits at 0.15-0.25 for the ENTIRE lateral of both wells (16/16 segments) -- this
is not a threshold-tuning problem, these are true strike-drillers. The sharper mechanism: the
gate zeroes the whole step (-dZ + c_hat), so it discards the MEASURED trajectory term along with
the untrusted drift. 43e16325's +85 ft of TVT rise is mostly trajectory (true drift only
-0.008/step): ungated it scores 17.0 vs gated 45.8. But 896d15b9 is the mirror case (77.2
ungated vs 29.8 gated) because near strike the reprojected c_hat is sign-unreliable. Partial
fixes were already tested and failed the holdout guard: soft gate fits kappa_gate ~ 0.07 (blend
cell) and substituting the well's own landing drift was a wash (hindcast cell). One threshold
cannot serve both wells because the quantity that differs -- local dip direction -- is
unidentifiable from dip-aligned donors (vector-field ablation). Insurance premium accepted;
never fires on the dip-aligned test wells.
Post-diagnostic test (recorded): a gated-steps-keep-dz-only column fits kappa_gate_dz=0.09,
scores WORSE on holdout (9.84 vs 9.58 pooled R0) and just swaps the two wells' fates
(43e16325 46->40, 896d15b9 30->36): near-strike wells steer along their LOCAL layer, so
even their measured dz carries the unknown-sign local drift. Gate confirmed optimal.""")

# --- cell 65 ---
# === Diagnostic 2/4 -- WRONG-SIGN WELLS: the target vs the donors that misled it, on the map ===
# For each well: its trajectory + every donor segment its kernel actually used, coloured by
# deprojected drift D. If donors are genuinely opposite-signed to the target's true D, the local
# geology flips between them (information gap); if same-signed, the projection would be at fault.
d2_wids = ["389ae58f", "fb03ae90", "9dfff011"]
fig, axes = plt.subplots(1, 3, figsize=(18, 6.2))
for ax, _wid in zip(axes, d2_wids):
    wd = [w for w in sp_wells if w["wid"] == _wid][0]
    _sg = wd["seg"][16]
    _idx, _ds = kn_top[0][wd["wi"]]
    _don = np.unique(_idx[:, :15].ravel())               # union of the 15 kernel donors per segment
    _Dtrue = _sg["c"] / _sg["proj"]
    _cx, _cy = _sg["mid"].mean(0)
    _L = max(np.abs(aF[_don, 0] - _cx).max(), np.abs(aF[_don, 1] - _cy).max()) * 1.25 + 800
    for w2 in sp_wells:                                   # context wells, light grey
        if abs(w2["X"][w2["s"]] - _cx) < 1.3 * _L and abs(w2["Y"][w2["s"]] - _cy) < 1.3 * _L and w2["wi"] != wd["wi"]:
            ax.plot(w2["X"][::40], w2["Y"][::40], color="lightgrey", lw=0.6, zorder=1)
    _vm = 0.06
    ax.scatter(aF[_don, 0], aF[_don, 1], c=aF[_don, 2], cmap="RdBu_r", vmin=-_vm, vmax=_vm,
               s=42, edgecolors="k", linewidths=0.4, zorder=3, label="donor segments (D)")
    _sc = ax.scatter(_sg["mid"][:, 0], _sg["mid"][:, 1], c=_Dtrue, cmap="RdBu_r", vmin=-_vm, vmax=_vm,
                     s=130, marker="s", edgecolors="k", linewidths=1.2, zorder=4, label="target true D")
    ax.annotate("", xy=(wd["X"][-1], wd["Y"][-1]), xytext=(wd["X"][wd["s"]], wd["Y"][wd["s"]]),
                arrowprops=dict(arrowstyle="-|>", color="k", lw=1.6))
    for _ang, _lb in [(118.4, "up-dip"), (208.4, "strike")]:
        ax.annotate("", xy=(_cx - 0.8 * _L + 1300 * np.cos(np.radians(_ang)),
                            _cy + 0.8 * _L + 1300 * np.sin(np.radians(_ang))),
                    xytext=(_cx - 0.8 * _L, _cy + 0.8 * _L),
                    arrowprops=dict(arrowstyle="->", color="tab:green" if _lb == "strike" else "tab:cyan", lw=1.4))
        ax.text(_cx - 0.8 * _L + 1600 * np.cos(np.radians(_ang)), _cy + 0.8 * _L + 1600 * np.sin(np.radians(_ang)),
                _lb, fontsize=7, ha="center")
    _idxg = np.abs(_sg["proj"]) > 0.3
    _Dh = np.array([kn_gauss(_idx[j], _ds[j], 15, 500.0)[0] for j in range(16)])
    ax.set_xlim(_cx - 1.2 * _L, _cx + 1.2 * _L); ax.set_ylim(_cy - 1.2 * _L, _cy + 1.2 * _L)
    ax.set_aspect("equal"); ax.set_xlabel("X"); ax.set_ylabel("Y")
    ax.set_title(f"{_wid}: true D {np.mean(_Dtrue[_idxg]):+.3f} vs donors {np.mean(_Dh):+.3f}\n"
                 f"(squares = target segments, dots = its kernel donors)", fontsize=10)
    print(f"{_wid}: mean true D {np.mean(_Dtrue[_idxg]):+.4f} | kernel D_hat {np.mean(_Dh):+.4f} | "
          f"donor D spread {aF[_don, 2].std():.4f} | median donor dist {np.median(_ds[:, :15]):.0f} ft | "
          f"donors same sign as target: {(np.sign(aF[_don, 2]) == np.sign(np.mean(_Dtrue[_idxg]))).mean():.0%}")
fig.colorbar(_sc, ax=axes, label="deprojected drift D (ft/step)", fraction=0.02)
plt.show()
print("""READ -- and a correction to the gallery's 'wrong-sign' label: the donors are NOT
opposite-signed. In all three wells 92-100% of donor segments share the target's drift sign;
what differs is MAGNITUDE -- the kernel says D ~ +0.032-0.039 where the target's truth is
+0.020-0.024 (donors ~1.5x too strong). The TVT trend that LOOKED wrong-signed is trajectory-
dominated; the drift error is a same-sign overestimate that accumulates over 4-6k steps into a
20-70 ft ramp. So the misinforming signal is regression-to-neighbourhood-mean in reverse: these
targets sit in locally WEAK dip inside a strong-dip neighbourhood (9dfff011 most extreme: truth
flat, donors 2.2 kft away and unanimous). Same information gap as the under-call class, opposite
tail -- and no donor statistic distinguishes either tail from a typical well (donor spread here
is normal, 0.014-0.034).""")

# --- cell 67 ---
# === Diagnostic 3/4 -- MAGNITUDE UNDER-CALLS: was it kappa, or was the field already low? ===
# kappa is NOT global: effective kappa(step) = kappa_bin(donor distance) + w*sqrt(position),
# fit ONCE across all 773 wells (population-optimal shrinkage). Decompose each under-call into
# (a) field underestimate (D_hat < D_true before any kappa) and (b) kappa shrinkage on top.
d3_wids = ["1b1eba53", "d924e971", "197f8a5a"]
fig, axes = plt.subplots(3, 2, figsize=(16, 13))
for _r, _wid in enumerate(d3_wids):
    wd = [w for w in sp_wells if w["wid"] == _wid][0]
    _sg = wd["seg"][16]
    ch, dd = bl_chdd[0][wd["wi"]]
    _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                  np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
    _kseg = ga_kb[np.digitize(dd, A_BINS[1:-1])] + ga_kb[nB] * np.sqrt((np.arange(16) + 0.5) / 16)
    ax = axes[_r, 0]
    _xs = np.arange(16)
    ax.bar(_xs - 0.27, _sg["c"], 0.27, color="tab:orange", label="true c")
    ax.bar(_xs, ch, 0.27, color="tab:blue", label="field c_hat (BEFORE kappa)")
    ax.bar(_xs + 0.27, _kseg * ch, 0.27, color="tab:green", label="effective kappa * c_hat")
    ax.axhline(0, color="k", lw=0.7)
    _tw = ax.twinx()
    _tw.plot(_xs, _kseg, "k.--", lw=0.9, ms=5, label="effective kappa")
    _tw.set_ylim(0, 1.3); _tw.set_ylabel("effective kappa")
    ax.set_xlabel("segment"); ax.set_ylabel("drift (ft/step)")
    ax.set_title(f"{_wid}: field already low? kappa cut on top?  (donors ~{np.median(dd):.0f} ft)", fontsize=10)
    ax.legend(fontsize=8, loc="upper left"); _tw.legend(fontsize=8, loc="upper right")
    # decomposition in TVT space
    _ndz = np.diff(np.r_[0.0, wd["U"]])
    _anchor = wd["tvt"][wd["s"]]
    _steps = np.arange(1, wd["n"] + 1)
    _full = _anchor + wd["U"] + np.cumsum(ch[_si])        # kappa = 1 everywhere
    ax = axes[_r, 1]
    ax.plot(_steps, _anchor + wd["R0"], color="tab:orange", lw=2.2, label="truth")
    ax.plot(_steps, _anchor + ga_preds[wd["wi"]], color="tab:green", lw=1.8, label="model (with kappa)")
    ax.plot(_steps, _full, color="tab:blue", lw=1.3, label="field, kappa=1 (unshrunk)")
    ax.plot(_steps, _anchor + wd["U"] + _sg["phi"] @ _sg["c"], "k:", lw=1.1, label="oracle")
    ax.plot(_steps, np.full(wd["n"], _anchor), "--", color="grey", lw=1)
    _em = np.sqrt(np.nanmean((ga_preds[wd["wi"]] - wd["R0"]) ** 2))
    _ef = np.sqrt(np.nanmean((_full - _anchor - wd["R0"]) ** 2))
    ax.set_title(f"{_wid}: model {_em:.1f} ft | unshrunk field {_ef:.1f} ft", fontsize=10)
    ax.set_xlabel("lateral step"); ax.set_ylabel("TVT (ft)"); ax.legend(fontsize=8)
    _gm = np.abs(_sg["proj"]) > 0.3
    print(f"{_wid}: sum true drift {np.sum(_sg['c'][_gm] * wd['n'] / 16):+7.1f} ft | field kappa=1 "
          f"{np.sum(ch[_gm] * wd['n'] / 16):+7.1f} ft | after kappa {np.sum((_kseg * ch)[_gm] * wd['n'] / 16):+7.1f} ft"
          f" | kappa range [{_kseg.min():.2f},{_kseg.max():.2f}]")
plt.tight_layout(); plt.show()
print("""ANSWER to 'was a global kappa used / what distorted the signal': kappa is NOT one global
constant -- each segment gets kappa(donor-distance bin) + w*sqrt(position), fit once across all
773 wells; here that lands at 0.43-0.92 per segment. But the decomposition shows the field is
NOT the main culprit: kappa=1 totals land within ~20-35% of true total drift (d924e971 +141 vs
+179; 197f8a5a +146 vs +175). The dominant distortion is that kappa multiplies the WHOLE step
(-dZ + c_hat), so a well whose true level makes a large excursion gets that excursion
proportionally flattened toward hold: error ~ (kappa-1) x (true excursion) even when c_hat is
right. That is not an accident -- it is the bias half of the variance-bias trade kappa was fit
for, and the kappa-anatomy ablation showed removing it (kappa on drift only) costs 3.6 ft pooled
overall. These wells are the price paid; the 9dfff011 class is what the same shrinkage saves.
Un-distorting one tail re-inflates the other; only per-well evidence (not in the trajectory,
proven) could tell them apart.""")

# --- cell 69 ---
# === Diagnostic 4/4 -- DOWNSTREAM SHAPE CHANGES: cumsum(-dz) vs cumsum(dtvt) per well ===
# The drift signal is the gap between the two curves. A 2-piece linear fit to that gap locates
# the regime change ("knee"): before it the well behaves like its donors, after it the local
# drift rate changes -- information that exists nowhere at prediction time.
d4_wids = ["91b301ce", "42c538a1", "14fee784", "84c3b497"]
fig, axes = plt.subplots(2, 2, figsize=(16, 9.5))
for ax, _wid in zip(axes.ravel(), d4_wids):
    wd = [w for w in sp_wells if w["wid"] == _wid][0]
    _steps = np.arange(1, wd["n"] + 1)
    _drift = wd["R0"] - wd["U"]                          # cumulative drift = gap between the cumsums
    _best, _kn = None, None
    for _k in range(int(0.15 * wd["n"]), int(0.85 * wd["n"]), max(wd["n"] // 200, 1)):
        _r = 0.0
        for _sl in [slice(0, _k), slice(_k, wd["n"])]:
            _x = _steps[_sl] - _steps[_sl][0]
            _y = _drift[_sl] - _drift[_sl][0]
            _b = np.dot(_x, _y) / max(np.dot(_x, _x), 1e-9)
            _r += np.sum((_y - _b * _x) ** 2)
        if _best is None or _r < _best:
            _best, _kn = _r, _k
    _b1 = (_drift[_kn] - _drift[0]) / _kn
    _b2 = (_drift[-1] - _drift[_kn]) / (wd["n"] - _kn)
    ax.plot(_steps, wd["U"], color="tab:blue", lw=1.6, label="cumsum(-dz)  (trajectory)")
    ax.plot(_steps, wd["R0"], color="tab:orange", lw=2.0, label="cumsum(dtvt)  (truth)")
    ax.plot(_steps, _drift, color="tab:purple", lw=1.4, label="drift = gap between them")
    ax.axvline(_kn, color="k", ls=":", lw=1.2)
    ax.annotate(f"knee @ step {_kn} ({100 * _kn / wd['n']:.0f}%)\n"
                f"drift rate {_b1:+.4f} -> {_b2:+.4f} ft/step",
                xy=(_kn, _drift[_kn]), xytext=(_kn + 0.05 * wd["n"], _drift[_kn] + 0.25 * (_drift.max() - _drift.min() + 1)),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel("lateral step"); ax.set_ylabel("ft (anchored at PS)")
    ax.set_title(f"{_wid}", fontsize=10)
    ax.legend(fontsize=8)
    print(f"{_wid}: knee at {100 * _kn / wd['n']:3.0f}% of lateral | drift {_b1:+.4f} -> {_b2:+.4f} ft/step "
          f"(x{abs(_b2 / _b1) if abs(_b1) > 1e-4 else float('inf'):.1f} change)")
plt.tight_layout(); plt.show()
print("""READ: in all four wells the drift (purple) runs at one near-constant rate and then bends at a
knee 52-79% down the lateral: x1.6-3.2 rate jumps, and one outright reversal (91b301ce,
+0.046 -> -0.003). Before the knee the donor-informed rate is roughly right; after it the well
leaves what its neighbourhood measured. Neither donors, nor the landing (hindcast: signal
decorrelates ~600 ft past PS), nor the trajectory itself (steering covariates: nothing) carries
the knee's timing or new slope. This is the cleanest picture of the information boundary: a
per-row stratigraphic sensor (GR <-> typewell) is the only feature in the data that could see
the knee as it happens.""")

# --- cell 71 ---
# === Gate committee: alternative/additional signals for the near-strike gate (ADOPTED) ===
# The gate autopsy asked: can other metrics beside |cos(az-theta0)| decide when/what to predict
# in near-strike segments? New signal: the ANCC structural surface (per-row training column, like
# TVT test-absent but field-buildable) -- a kernel-weighted local PLANE fit gives the local dip
# DIRECTION theta_loc independent of drilling headings, exactly the quantity heading-homogeneous
# donors cannot constrain. Committee: |proj| says distrust the global reprojection; theta_loc says
# what to use instead; |theta_loc - theta0| < 60 deg says when theta_loc itself is trustworthy.
# ~2 min. Reuses sp_wells, aF, kn_top, kn_gauss, bl_chdd, A_BINS.
gt_SP = []
for _fp, wd in zip(hw_files, sp_wells):
    _w = pd.read_csv(_fp, usecols=["X", "Y", "ANCC"])
    _st = max(len(_w) // 120, 1)
    gt_SP.append(np.column_stack([_w["X"].to_numpy()[::_st], _w["Y"].to_numpy()[::_st],
                                  _w["ANCC"].to_numpy()[::_st], np.full(len(_w["X"][::_st]), wd["wi"])]))
gt_SP = np.vstack(gt_SP); gt_SP = gt_SP[np.isfinite(gt_SP[:, 2])]
_Xg = np.column_stack([np.ones(len(gt_SP)), gt_SP[:, 0] - gt_SP[:, 0].mean(), gt_SP[:, 1] - gt_SP[:, 1].mean()])
gt_gb = np.linalg.lstsq(_Xg, gt_SP[:, 2], rcond=None)[0]
print(f"ANCC surface: {len(gt_SP)} samples | global gradient dir "
      f"{np.degrees(np.arctan2(gt_gb[2], gt_gb[1])) % 360:.1f} deg, |grad| {np.hypot(gt_gb[1], gt_gb[2]):.4f}"
      f"   (b-dipole: up-dip 118.4, D=0.0350 -- same structure, two measurements)")

gt_Q = np.vstack([wd["seg"][16]["mid"] for wd in sp_wells])
gt_QW = np.concatenate([[wd["wi"]] * 16 for wd in sp_wells])
gt_AZ = np.empty(len(gt_Q)); _q = 0
for wd in sp_wells:
    _n = wd["n"]; _e = np.linspace(0, _n, 17)
    for j in range(16):
        _f0 = wd["s"] + 1 + int(_e[j]); _f1 = min(wd["s"] + 1 + max(int(_e[j + 1]) - 1, int(_e[j])), len(wd["X"]) - 1)
        gt_AZ[_q] = np.arctan2(wd["Y"][_f1] - wd["Y"][_f0], wd["X"][_f1] - wd["X"][_f0]); _q += 1
gt_TH = np.empty(len(gt_Q))
_H = 1500.0
for _q in range(len(gt_Q)):
    _d2 = (gt_SP[:, 0] - gt_Q[_q, 0]) ** 2 + (gt_SP[:, 1] - gt_Q[_q, 1]) ** 2
    _m = (_d2 < (4 * _H) ** 2) & (gt_SP[:, 3] != gt_QW[_q])
    if _m.sum() < 30:
        gt_TH[_q] = np.arctan2(gt_gb[2], gt_gb[1]); continue
    _wt = np.exp(-_d2[_m] / (2 * _H * _H))
    _x = gt_SP[_m, 0] - gt_Q[_q, 0]; _y = gt_SP[_m, 1] - gt_Q[_q, 1]; _z = gt_SP[_m, 2]
    _A = np.array([[np.sum(_wt), np.sum(_wt * _x), np.sum(_wt * _y)],
                   [np.sum(_wt * _x), np.sum(_wt * _x * _x), np.sum(_wt * _x * _y)],
                   [np.sum(_wt * _y), np.sum(_wt * _x * _y), np.sum(_wt * _y * _y)]])
    _r = np.array([np.sum(_wt * _z), np.sum(_wt * _x * _z), np.sum(_wt * _y * _z)])
    _bq = np.linalg.solve(_A, _r)
    gt_TH[_q] = np.arctan2(_bq[2], _bq[1])
gt_ROT = np.degrees(np.abs(np.arctan2(np.sin(gt_TH - np.radians(theta0)), np.cos(gt_TH - np.radians(theta0)))))
gt_Dh = {R: {} for R in [0, 1500]}
for wd in sp_wells:
    for R in [0, 1500]:
        _idx, _ds = kn_top[R][wd["wi"]]
        gt_Dh[R][wd["wi"]] = np.array([kn_gauss(_idx[j], _ds[j], 15, 500.0)[0] for j in range(16)])

def gt_run(mode, folds=False):
    _lab = f"{mode:20s}" + ("holdout" if folds else "in-samp"); _pw = {}
    for R in [0, 1500]:
        _Gs = {}; _qb = 0
        for wd in sp_wells:
            ch, dd = bl_chdd[R][wd["wi"]]
            _sg = wd["seg"][16]
            _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                          np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
            _ndz = np.diff(np.r_[0.0, wd["U"]])
            _gated = np.abs(_sg["proj"][_si]) < 0.35
            _g = np.where(_gated, 0.0, _ndz + ch[_si])
            _bs = np.digitize(dd, A_BINS[1:-1])[_si]
            _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
            _cols.append(np.cumsum(_g * np.sqrt((_si + 0.5) / 16)))
            if mode != "adopted":
                _chL = gt_Dh[R][wd["wi"]] * np.cos(gt_AZ[_qb:_qb + 16] - gt_TH[_qb:_qb + 16])
                _conf = gt_ROT[_qb:_qb + 16] < 60 if mode == "hybrid rot<60" else np.ones(16, bool)
                _subm = _gated & _conf[_si]
                _cols.append(np.cumsum(np.where(_subm, _ndz + _chL[_si], 0.0)))
            _qb += 16
            _Gs[wd["wi"]] = np.column_stack(_cols)
        def _fit(skip):
            _A = _y = None
            for wd in sp_wells:
                if skip is not None and wd["wi"] % 5 == skip:
                    continue
                G = _Gs[wd["wi"]]
                if _A is None:
                    _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
                _A += G.T @ G; _y += G.T @ wd["R0"]
            return np.linalg.lstsq(_A, _y, rcond=None)[0]
        _rw, _sq, _n = [], 0.0, 0
        for f in (range(5) if folds else [None]):
            _kb = _fit(f)
            for wd in sp_wells:
                if folds and wd["wi"] % 5 != f:
                    continue
                _e = _Gs[wd["wi"]] @ _kb - wd["R0"]
                _rww = np.sqrt(np.nanmean(_e ** 2))
                _rw.append(_rww); _sq += np.nansum(_e ** 2); _n += int(np.isfinite(_e).sum())
                if R == 0:
                    _pw[wd["wid"]] = _rww
        _lab += f"  R{R}: {np.mean(_rw):5.2f}/{np.sqrt(_sq / _n):5.2f}"
        if not folds and R == 0 and mode != "adopted":
            _lab += f"  kappa_sub={_kb[-1]:+.2f}"
    print(_lab)
    return _pw

gt_pw = {}
for _m in ["adopted", "hybrid all-gated", "hybrid rot<60"]:
    gt_pw[_m] = gt_run(_m)
for _m in ["adopted", "hybrid all-gated", "hybrid rot<60"]:
    gt_run(_m, folds=True)
print(f"\n{'well':10s} {'gated/16':>8s} {'rot(deg)':>9s}" + "".join(f"{m:>18s}" for m in gt_pw))
_qb = 0
for wd in sp_wells:
    _ng = int((np.abs(wd["seg"][16]["proj"]) < 0.35).sum())
    if _ng:
        _rot = np.median(gt_ROT[_qb:_qb + 16])
        print(f"{wd['wid']:10s} {_ng:8d} {_rot:9.0f}" + "".join(f"{gt_pw[m][wd['wid']]:18.1f}" for m in gt_pw))
    _qb += 16
print("""
VERDICT (ADOPTED: hybrid rot<60): the committee is |proj|<0.35 (distrust the global reprojection)
AND |theta_loc - theta0| < 60 deg (the surface's local direction is a moderate correction, trust
it) -> substitute g = -dz + D_hat*cos(az - theta_loc) with its own fitted kappa (~0.36); else fall
back to the zero-gate. All 6 gated wells score <= adopted (43e16325: 46 -> 4.5; 896d15b9 rot~80
falls back safely to 30); wins all four holdout stats; threshold is a plateau (60 == 75, only <45
degrades). Recorded negatives: theta_loc as a GLOBAL replacement for theta0 hurts (9.94 vs 9.46
pooled -- direction noise where cos is insensitive); plane-residual confidence loses to rotation.
Cumulative LOO since the LB submission: 9.67 -> 9.30 pooled (< 0.5 resubmit threshold). NOTE:
the 3 test wells have no gated segments, so this changes nothing in the current submission --
it is tail insurance, and the first crack in the near-strike blind spot.""")

fig, ax = plt.subplots(figsize=(10, 4))
_wids = [wd["wid"] for wd in sp_wells if (np.abs(wd["seg"][16]["proj"]) < 0.35).any()]
_xs = np.arange(len(_wids))
for _o, (_m, _c) in enumerate([("adopted", "grey"), ("hybrid all-gated", "tab:blue"), ("hybrid rot<60", "tab:green")]):
    ax.bar(_xs + 0.27 * (_o - 1), [gt_pw[_m][w] for w in _wids], 0.27, color=_c, label=_m)
ax.set_xticks(_xs); ax.set_xticklabels([w[:8] for w in _wids], fontsize=8)
ax.set_ylabel("rowwise RMSE (ft)")
ax.set_title("Near-strike wells: zero-gate vs theta_loc substitution (committee: rot<60 keeps every win,\n"
             "falls back to the safe gate where the surface direction contradicts the dipole)")
ax.legend(fontsize=8)
plt.tight_layout(); plt.show()

# --- cell 72 ---
# === Visualising the gate committee: the theta_loc direction field + before/after TVT ===
# Left: the local dip-direction field from the ANCC surface (arrow = theta_loc, colour = rotation
# away from the global dipole). The committee substitutes drift only where a NEAR-STRIKE well
# crosses a moderately-rotated zone; hot zones (rot > 60) fall back to the zero-gate.
# Bottom: TVT reconstructions of all 6 near-strike wells, old gate vs committee.
# Reuses gt_SP, gt_TH, gt_ROT, gt_Dh, gt_AZ, bl_chdd from the committee cell.
gv_wids = ["14ab73fb", "3a7dd95d", "42c538a1", "43e16325", "896d15b9", "eba6605e"]
gv_x0, gv_x1 = gt_SP[:, 0].min(), gt_SP[:, 0].max()
gv_y0, gv_y1 = gt_SP[:, 1].min(), gt_SP[:, 1].max()
gv_gx, gv_gy = np.meshgrid(np.linspace(gv_x0, gv_x1, 34), np.linspace(gv_y0, gv_y1, 26))
gv_u = np.full(gv_gx.shape, np.nan); gv_v = np.full(gv_gx.shape, np.nan); gv_r = np.full(gv_gx.shape, np.nan)
for _i in range(gv_gx.shape[0]):
    for _j in range(gv_gx.shape[1]):
        _d2 = (gt_SP[:, 0] - gv_gx[_i, _j]) ** 2 + (gt_SP[:, 1] - gv_gy[_i, _j]) ** 2
        _m = _d2 < 2000.0 ** 2
        if _m.sum() < 40:
            continue
        _w = np.exp(-_d2[_m] / (2 * 1500.0 ** 2))
        _x = gt_SP[_m, 0] - gv_gx[_i, _j]; _y = gt_SP[_m, 1] - gv_gy[_i, _j]; _z = gt_SP[_m, 2]
        _A = np.array([[np.sum(_w), np.sum(_w * _x), np.sum(_w * _y)],
                       [np.sum(_w * _x), np.sum(_w * _x * _x), np.sum(_w * _x * _y)],
                       [np.sum(_w * _y), np.sum(_w * _x * _y), np.sum(_w * _y * _y)]])
        _b = np.linalg.solve(_A, np.array([np.sum(_w * _z), np.sum(_w * _x * _z), np.sum(_w * _y * _z)]))
        _th = np.arctan2(_b[2], _b[1])
        gv_u[_i, _j], gv_v[_i, _j] = np.cos(_th), np.sin(_th)
        gv_r[_i, _j] = np.degrees(np.abs(np.arctan2(np.sin(_th - np.radians(theta0)),
                                                    np.cos(_th - np.radians(theta0)))))
fig, ax = plt.subplots(figsize=(15, 9))
_qv = ax.quiver(gv_gx, gv_gy, gv_u, gv_v, gv_r, cmap="coolwarm", clim=(0, 90),
                scale=42, width=0.0022, pivot="mid")
fig.colorbar(_qv, ax=ax, label="|theta_loc - theta0| (deg)", fraction=0.03)
for wd in sp_wells:
    ax.plot(wd["X"][::60], wd["Y"][::60], color="lightgrey", lw=0.4, zorder=1)
for _wid in gv_wids:
    wd = [w for w in sp_wells if w["wid"] == _wid][0]
    ax.plot(wd["X"][::20], wd["Y"][::20], color="k", lw=2.2, zorder=5)
    ax.annotate(_wid[:8], (wd["X"][wd["s"]], wd["Y"][wd["s"]]), fontsize=9, weight="bold",
                xytext=(6, 6), textcoords="offset points")
ax.annotate("", xy=(gv_x0 + 3200 * np.cos(np.radians(theta0)), gv_y1 - 4000 + 3200 * np.sin(np.radians(theta0))),
            xytext=(gv_x0, gv_y1 - 4000), arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=3))
ax.text(gv_x0, gv_y1 - 5400, "global up-dip 118.4", color="tab:green", fontsize=10, weight="bold")
ax.set_aspect("equal"); ax.set_xlabel("X"); ax.set_ylabel("Y")
ax.set_title("Local dip direction from the ANCC surface. Blue = agrees with the global dipole; "
             "red = rotated/contradicting.\nBold = the 6 near-strike wells the committee acts on "
             "(896d15b9 sits in a hot zone -> falls back to the zero-gate).")
plt.show()

# --- before/after TVT for the 6 wells (kappa refit for each variant, R=0, as in the committee cell) ---
def gv_pred(mode):
    _Gs = {}; _qb = 0
    for wd in sp_wells:
        ch, dd = bl_chdd[0][wd["wi"]]
        _sg = wd["seg"][16]
        _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                      np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
        _ndz = np.diff(np.r_[0.0, wd["U"]])
        _gated = np.abs(_sg["proj"][_si]) < 0.35
        _g = np.where(_gated, 0.0, _ndz + ch[_si])
        _bs = np.digitize(dd, A_BINS[1:-1])[_si]
        _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
        _cols.append(np.cumsum(_g * np.sqrt((_si + 0.5) / 16)))
        if mode == "committee":
            _chL = gt_Dh[0][wd["wi"]] * np.cos(gt_AZ[_qb:_qb + 16] - gt_TH[_qb:_qb + 16])
            _subm = _gated & (gt_ROT[_qb:_qb + 16] < 60)[_si]
            _cols.append(np.cumsum(np.where(_subm, _ndz + _chL[_si], 0.0)))
        _qb += 16
        _Gs[wd["wi"]] = np.column_stack(_cols)
    _A = _y = None
    for wd in sp_wells:
        G = _Gs[wd["wi"]]
        if _A is None:
            _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
        _A += G.T @ G; _y += G.T @ wd["R0"]
    _kb = np.linalg.lstsq(_A, _y, rcond=None)[0]
    return {wd["wi"]: _Gs[wd["wi"]] @ _kb for wd in sp_wells}
gv_old = gv_pred("adopted"); gv_new = gv_pred("committee")
fig, axes = plt.subplots(2, 3, figsize=(17, 9))
for ax, _wid in zip(axes.ravel(), gv_wids):
    wd = [w for w in sp_wells if w["wid"] == _wid][0]
    _anchor = wd["tvt"][wd["s"]]; _steps = np.arange(1, wd["n"] + 1)
    ax.plot(_steps, _anchor + wd["R0"], color="tab:orange", lw=2.2, label="truth")
    ax.plot(_steps, _anchor + gv_old[wd["wi"]], color="grey", lw=1.5, label="old gate (hold)")
    ax.plot(_steps, _anchor + gv_new[wd["wi"]], color="tab:green", lw=1.8, label="committee")
    _sg = wd["seg"][16]
    ax.plot(_steps, _anchor + wd["U"] + _sg["phi"] @ _sg["c"], "k:", lw=1, label="oracle")
    _e0 = np.sqrt(np.nanmean((gv_old[wd["wi"]] - wd["R0"]) ** 2))
    _e1 = np.sqrt(np.nanmean((gv_new[wd["wi"]] - wd["R0"]) ** 2))
    ax.set_title(f"{_wid}: {_e0:.1f} -> {_e1:.1f} ft", fontsize=10)
    ax.set_xlabel("lateral step"); ax.set_ylabel("TVT (ft)")
axes[0, 0].legend(fontsize=8)
fig.suptitle("Near-strike wells, old zero-gate vs theta_loc committee", y=1.0, fontsize=12)
plt.tight_layout(); plt.show()

# --- cell 73 ---
# === Can the tops temper the wrong-MAGNITUDE tails? (NEGATIVE, recorded) ===
# The surface gradient gives a full drift vector -> a second drift estimator c_surf = grad.heading.
# Hopes tested: (1) c_surf sharper than the donor field; (2) blend the two; (3) two-CHANNEL
# disagreement |c_hat - c_surf| as the per-segment uncertainty that donor spread failed to be.
# Reuses gt_SP-style samples (all 6 tops), gt_Q/gt_QW/gt_AZ, bl_chdd. ~2 min.
mg_TOPS = ["ANCC", "ASTNU", "ASTNL", "EGFDU", "EGFDL", "BUDA"]
mg_SP = []
for _fp, wd in zip(hw_files, sp_wells):
    _w = pd.read_csv(_fp, usecols=["X", "Y"] + mg_TOPS)
    _st = max(len(_w) // 120, 1)
    mg_SP.append(np.column_stack([_w["X"].to_numpy()[::_st], _w["Y"].to_numpy()[::_st]]
                                 + [_w[t].to_numpy()[::_st] for t in mg_TOPS]
                                 + [np.full(len(_w["X"][::_st]), wd["wi"])]))
mg_SP = np.vstack(mg_SP); mg_SP = mg_SP[np.isfinite(mg_SP[:, 2:8]).all(1)]
mg_cs = np.zeros(len(gt_Q)); mg_ok = np.zeros(len(gt_Q), bool)
for _q in range(len(gt_Q)):
    _d2 = (mg_SP[:, 0] - gt_Q[_q, 0]) ** 2 + (mg_SP[:, 1] - gt_Q[_q, 1]) ** 2
    _m = (_d2 < 3000.0 ** 2) & (mg_SP[:, 8] != gt_QW[_q])
    if _m.sum() < 30:
        continue
    _w = np.exp(-_d2[_m] / (2 * 750.0 ** 2))
    _x = mg_SP[_m, 0] - gt_Q[_q, 0]; _y = mg_SP[_m, 1] - gt_Q[_q, 1]
    _A = np.array([[np.sum(_w), np.sum(_w * _x), np.sum(_w * _y)],
                   [np.sum(_w * _x), np.sum(_w * _x * _x), np.sum(_w * _x * _y)],
                   [np.sum(_w * _y), np.sum(_w * _x * _y), np.sum(_w * _y * _y)]])
    _R = np.stack([np.array([np.sum(_w * z), np.sum(_w * _x * z), np.sum(_w * _y * z)])
                   for z in mg_SP[_m, 2:8].T])
    _B = np.linalg.solve(_A, _R.T)
    _g = _B[1:].mean(1)                                  # 6-top consensus gradient
    mg_cs[_q] = _g[0] * np.cos(gt_AZ[_q]) + _g[1] * np.sin(gt_AZ[_q]); mg_ok[_q] = True
mg_ct = np.concatenate([wd["seg"][16]["c"] for wd in sp_wells])
mg_ch = np.concatenate([bl_chdd[0][wd["wi"]][0] for wd in sp_wells])
print(f"surface drift estimator (6-top consensus, h=750, LOO): "
      f"corr(c_surf, c_true) = {np.corrcoef(mg_cs[mg_ok], mg_ct[mg_ok])[0, 1]:.3f}, "
      f"RMSE {np.sqrt(np.mean((mg_cs[mg_ok] - mg_ct[mg_ok]) ** 2)):.4f}")
print(f"donor drift field (reference):                         "
      f"corr = {np.corrcoef(mg_ch[mg_ok], mg_ct[mg_ok])[0, 1]:.3f}, "
      f"RMSE {np.sqrt(np.mean((mg_ch[mg_ok] - mg_ct[mg_ok]) ** 2)):.4f}")
print(f"two-channel disagreement as uncertainty: corr(|c_hat - c_surf|, |c_hat - c_true|) = "
      f"{np.corrcoef(np.abs(mg_ch - mg_cs)[mg_ok], np.abs(mg_ch - mg_ct)[mg_ok])[0, 1]:.3f}"
      f"   (donor-spread benchmark: 0.19 -- both useless)")

def mg_run(mode, folds=False):
    _lab = f"{mode:16s}" + ("holdout" if folds else "in-samp")
    for R in [0, 1500]:
        _Gs = {}; _qb = 0
        for wd in sp_wells:
            ch, dd = bl_chdd[R][wd["wi"]]
            _sg = wd["seg"][16]
            _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                          np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
            _ndz = np.diff(np.r_[0.0, wd["U"]])
            _gated = np.abs(_sg["proj"][_si]) < 0.35
            _g = np.where(_gated, 0.0, _ndz + ch[_si])
            _bs = np.digitize(dd, A_BINS[1:-1])[_si]
            _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
            _cols.append(np.cumsum(_g * np.sqrt((_si + 0.5) / 16)))
            if mode == "blend":
                _cols.append(np.cumsum(np.where(_gated, 0.0, (mg_cs[_qb:_qb + 16] - ch)[_si])))
            elif mode == "kappa x dis":
                _hi = (np.abs(ch - mg_cs[_qb:_qb + 16]) > np.median(np.abs(mg_ch - mg_cs)))[_si]
                _cols = [np.cumsum(np.where((_bs == b) & ~_hi, _g, 0.0)) for b in range(nB)] + \
                        [np.cumsum(np.where((_bs == b) & _hi, _g, 0.0)) for b in range(nB)] + \
                        [np.cumsum(_g * np.sqrt((_si + 0.5) / 16))]
            _qb += 16
            _Gs[wd["wi"]] = np.column_stack(_cols)
        def _fit(skip):
            _A = _y = None
            for wd in sp_wells:
                if skip is not None and wd["wi"] % 5 == skip:
                    continue
                G = _Gs[wd["wi"]]
                if _A is None:
                    _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
                _A += G.T @ G; _y += G.T @ wd["R0"]
            return np.linalg.lstsq(_A, _y, rcond=None)[0]
        _rw, _sq, _n = [], 0.0, 0
        for f in (range(5) if folds else [None]):
            _kb = _fit(f)
            for wd in sp_wells:
                if folds and wd["wi"] % 5 != f:
                    continue
                _e = _Gs[wd["wi"]] @ _kb - wd["R0"]
                _rw.append(np.sqrt(np.nanmean(_e ** 2))); _sq += np.nansum(_e ** 2); _n += int(np.isfinite(_e).sum())
        _lab += f"  R{R}: {np.mean(_rw):5.2f}/{np.sqrt(_sq / _n):5.2f}"
    print(_lab)
for _m in ["adopted", "blend", "kappa x dis"]:
    mg_run(_m)
for _m in ["adopted", "blend", "kappa x dis"]:
    mg_run(_m, folds=True)
print("""
VERDICT (negative): the surface gradient is a GOOD drift estimator (corr 0.93) but strictly
noisier than the donor field (0.947 / 0.0119), because it is NOT an independent channel -- same
wells, same interpretation, same rock knowledge, one more interpolation step. Consequently the
two-channel disagreement carries no uncertainty signal (corr 0.15 with actual error, below even
the useless donor-spread 0.19), the blend weight fits to ~0.04, and the in-sample gains of the
disagreement-kappa variants collapse under the 5-fold kappa holdout (13.3 pooled). The
wrong-magnitude tail wells move < 1 ft in every variant. CONCLUSION: the tops contribute
DIRECTION (the committee, adopted) and nothing for MAGNITUDE; the magnitude tails cannot be
tempered by any training-side field -- they are the well-local 58%. The remaining instrument for
them is the well's own log (GR), still parked.""")

# --- cell 74 ---
# === 896d15b9 resolved + the frame-consistency refinement (NEGATIVE, recorded) ===
# The committee excluded 896d15b9 (rot ~80). Was that a missed opportunity? Anatomy first, then
# the refinement candidate: deproject DONORS by theta_loc at their own positions too (pure
# local-frame field), instead of the current mixed frame (donors global, target local).
fr_wd = [w for w in sp_wells if w["wid"] == "896d15b9"][0]
_qb = fr_wd["wi"] * 16
_sg = fr_wd["seg"][16]
_cosL = np.cos(gt_AZ[_qb:_qb + 16] - gt_TH[_qb:_qb + 16])
print("896d15b9 per segment:  az  projG | th_loc rot | cosL | c_true  c_sub(mixed)")
for j in range(16):
    print(f"  {j:2d}: {np.degrees(gt_AZ[_qb+j])%360:4.0f} {_sg['proj'][j]:+.2f} | "
          f"{np.degrees(gt_TH[_qb+j])%360:4.0f} {gt_ROT[_qb+j]:3.0f} | {_cosL[j]:+.2f} | "
          f"{_sg['c'][j]:+.4f}  {gt_Dh[0][fr_wd['wi']][j]*_cosL[j]:+.4f}")
_U = fr_wd["U"]
print(f"=> theta_loc is STABLE at ~198 deg (a real ~80 deg rotation; in the local frame the well is"
      f"\n   dip-aligned, cosL ~ +0.9) and the substituted drift has the RIGHT SIGN. But donors carry"
      f"\n   only ~half its true magnitude, and the trajectory dives {_U[-1]:+.0f} ft while truth ends"
      f"\n   {fr_wd['R0'][-1]:+.0f} ft: an under-called drift predicts a plunge where hold is nearly exact."
      f"\n   Its failure is MAGNITUDE (the well-local 58%), wearing a direction costume: the rot<60"
      f"\n   fallback is right, albeit for a deeper reason than the rule knows.")

# refinement: pure local-frame donor field
fr_cosL = np.cos(gt_AZ - gt_TH)
fr_cs = np.concatenate([w["seg"][16]["c"] for w in sp_wells])
fr_FL = []
_q = 0
for w2 in sp_wells:
    for j in range(16):
        if abs(fr_cosL[_q]) > 0.3:
            fr_FL.append((gt_Q[_q, 0], gt_Q[_q, 1], fr_cs[_q] / fr_cosL[_q], w2["wi"]))
        _q += 1
fr_FL = np.array(fr_FL)
fr_CHL = {R: {} for R in [0, 1500]}
for wd in sp_wells:
    _keep = fr_FL[:, 3] != wd["wi"]
    _kx, _ky, _kD = fr_FL[_keep, 0], fr_FL[_keep, 1], fr_FL[_keep, 2]
    _qb = wd["wi"] * 16
    for R in [0, 1500]:
        ch = np.empty(16)
        for j in range(16):
            _d2 = (_kx - gt_Q[_qb + j, 0]) ** 2 + (_ky - gt_Q[_qb + j, 1]) ** 2
            _cand = np.where(_d2 >= R * R)[0] if R else np.arange(len(_d2))
            _sel = _cand[np.argpartition(_d2[_cand], 15)[:15]]
            _w = np.exp(np.maximum(-_d2[_sel] / 5e5, -700))
            ch[j] = (np.sum(_w * _kD[_sel]) / np.sum(_w)) * fr_cosL[_qb + j]
        fr_CHL[R][wd["wi"]] = ch

def fr_run(mode, folds=False):
    _lab = f"{mode:26s}" + ("holdout" if folds else "in-samp"); _pw = {}
    for R in [0, 1500]:
        _Gs = {}; _qb = 0
        for wd in sp_wells:
            ch, dd = bl_chdd[R][wd["wi"]]
            _sg = wd["seg"][16]
            _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                          np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
            _ndz = np.diff(np.r_[0.0, wd["U"]])
            _gated = np.abs(_sg["proj"][_si]) < 0.35
            _g = np.where(_gated, 0.0, _ndz + ch[_si])
            _bs = np.digitize(dd, A_BINS[1:-1])[_si]
            _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
            _cols.append(np.cumsum(_g * np.sqrt((_si + 0.5) / 16)))
            if mode == "committee (mixed, rot<60)":
                _chs = gt_Dh[R][wd["wi"]] * np.cos(gt_AZ[_qb:_qb + 16] - gt_TH[_qb:_qb + 16])
                _subm = _gated & (gt_ROT[_qb:_qb + 16] < 60)[_si]
                _cols.append(np.cumsum(np.where(_subm, _ndz + _chs[_si], 0.0)))
            elif mode == "pure local frame, all":
                _cols.append(np.cumsum(np.where(_gated, _ndz + fr_CHL[R][wd["wi"]][_si], 0.0)))
            _qb += 16
            _Gs[wd["wi"]] = np.column_stack(_cols)
        def _fit(skip):
            _A = _y = None
            for wd in sp_wells:
                if skip is not None and wd["wi"] % 5 == skip:
                    continue
                G = _Gs[wd["wi"]]
                if _A is None:
                    _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
                _A += G.T @ G; _y += G.T @ wd["R0"]
            return np.linalg.lstsq(_A, _y, rcond=None)[0]
        _rw, _sq, _n = [], 0.0, 0
        for f in (range(5) if folds else [None]):
            _kb = _fit(f)
            for wd in sp_wells:
                if folds and wd["wi"] % 5 != f:
                    continue
                _e = _Gs[wd["wi"]] @ _kb - wd["R0"]
                _rw.append(np.sqrt(np.nanmean(_e ** 2))); _sq += np.nansum(_e ** 2); _n += int(np.isfinite(_e).sum())
                if R == 0:
                    _pw[wd["wid"]] = np.sqrt(np.nanmean(_e ** 2))
        _lab += f"  R{R}: {np.mean(_rw):5.2f}/{np.sqrt(_sq / _n):5.2f}"
    print(_lab)
    return _pw
print()
fr_pw = {}
for _m in ["adopted", "committee (mixed, rot<60)", "pure local frame, all"]:
    fr_pw[_m] = fr_run(_m)
for _m in ["adopted", "committee (mixed, rot<60)", "pure local frame, all"]:
    fr_run(_m, folds=True)
print(f"\n{'well':10s}" + "".join(f"{m[:20]:>22s}" for m in fr_pw))
for _wid in ["43e16325", "896d15b9", "42c538a1", "eba6605e", "14ab73fb", "3a7dd95d"]:
    print(f"{_wid:10s}" + "".join(f"{fr_pw[m][_wid]:22.1f}" for m in fr_pw))
print("""
VERDICT (negative -- committee unchanged): the pure local frame loses on holdout (9.52 vs 9.45
pooled R0) because deprojecting DONORS by theta_loc injects direction noise at every donor -- the
same noise that made the global theta_loc swap a negative. The mixed frame is asymmetric BY
DESIGN: donors live in the stable global frame (low variance), only the target's reprojection
uses the local frame (unbiased direction exactly where the global frame predicts nothing). Even
under perfect frames 896d15b9 improves just 29.8 -> 28.2: donors know its direction but carry
half its magnitude -- no field can supply that; only the well's own log could.""")

# --- cell 76 ---
# === Neighbour-aggregation grid: 7 estimators x 3 kappa structures, in-sample AND holdout ===
# Scrutiny follow-up: precision weighting (donor variance from LS theory: Var(c_j) =
# sigma^2 diag((Phi'Phi)^-1), deprojection variance ~ 1/proj^2) and local-linear regression
# (order-1 kernel smoother, removes gradient bias), trialled across EVERY kappa structure and
# both donor regimes -- not just the best model. ~3 min.
for wd in sp_wells:                                      # per-segment coefficient variance
    _phi = wd["seg"][16]["phi"]
    _r = wd["R0"] - wd["U"] - _phi @ wd["seg"][16]["c"]
    _s2 = np.nansum(_r ** 2) / max(int(np.isfinite(_r).sum()) - 16, 1)
    wd["vc"] = np.maximum(_s2 * np.diag(np.linalg.inv(_phi.T @ _phi)), 1e-10)
ag_Q = np.vstack([wd["seg"][16]["mid"] for wd in sp_wells])
ag_FA = np.array([(wd["seg"][16]["mid"][j, 0], wd["seg"][16]["mid"][j, 1], wd["seg"][16]["c"][j],
                   wd["seg"][16]["proj"][j], wd["wi"], wd["vc"][j]) for wd in sp_wells for j in range(16)])
ag_CUT = np.abs(ag_FA[:, 3]) > 0.3
ag_top = {R: {} for R in [0, 1500]}
for wd in sp_wells:
    _keep = ag_FA[:, 4] != wd["wi"]
    _kx, _ky = ag_FA[_keep, 0], ag_FA[_keep, 1]
    _gi = np.where(_keep)[0]
    for R in [0, 1500]:
        _idx = np.empty((16, 150), dtype=np.int64); _ds = np.empty((16, 150))
        for j in range(16):
            _d2 = (_kx - wd["seg"][16]["mid"][j, 0]) ** 2 + (_ky - wd["seg"][16]["mid"][j, 1]) ** 2
            _cand = np.where(_d2 >= R * R)[0] if R else np.arange(len(_d2))
            _o = _cand[np.argpartition(_d2[_cand], 150)[:150]]
            _o = _o[np.argsort(_d2[_o])]
            _idx[j] = _gi[_o]; _ds[j] = np.sqrt(_d2[_o])
        ag_top[R][wd["wi"]] = (_idx, _ds)

def ag_kern(d, h=500.0):
    return np.exp(np.maximum(-d * d / (2 * h * h), -700))
def ag_A1(i, d, q):
    _m = ag_CUT[i]; i2, d2 = i[_m][:10], d[_m][:10]
    return np.mean(ag_FA[i2, 2] / ag_FA[i2, 3]), np.median(d2)
def ag_A2(i, d, q):
    _m = ag_CUT[i]; i2, d2 = i[_m][:15], d[_m][:15]
    _w = ag_kern(d2)
    return np.sum(_w * ag_FA[i2, 2] / ag_FA[i2, 3]) / np.sum(_w), np.median(d2)
def ag_A3(i, d, q):
    _m = ag_CUT[i]; i2, d2 = i[_m][:15], d[_m][:15]
    _w = ag_kern(d2) * ag_FA[i2, 3] ** 2 / ag_FA[i2, 5]
    return np.sum(_w * ag_FA[i2, 2] / ag_FA[i2, 3]) / np.sum(_w), np.median(d2)
def ag_A4(i, d, q):
    i2, d2 = i[:50], d[:50]
    _w = ag_kern(d2) / ag_FA[i2, 5]; _p = ag_FA[i2, 3]
    return np.sum(_w * _p * ag_FA[i2, 2]) / np.sum(_w * _p * _p), np.median(d2[:15])
def ag_A5(i, d, q):
    _m = ag_CUT[i]; i2, d2 = i[_m][:50], d[_m][:50]
    _w = ag_kern(d2)
    _dx = (ag_FA[i2, 0] - ag_Q[q, 0]) / 1000.0; _dy = (ag_FA[i2, 1] - ag_Q[q, 1]) / 1000.0
    _X = np.column_stack([np.ones(len(i2)), _dx, _dy])
    _A = (_X * _w[:, None]).T @ _X + np.sum(_w) * np.diag([0.0, 1.0, 1.0])
    return np.linalg.solve(_A, (_X * _w[:, None]).T @ (ag_FA[i2, 2] / ag_FA[i2, 3]))[0], np.median(d2[:15])
def ag_A6(i, d, q):
    i2, d2 = i[:50], d[:50]
    _w = ag_kern(d2) / ag_FA[i2, 5]; _p = ag_FA[i2, 3]
    _dx = (ag_FA[i2, 0] - ag_Q[q, 0]) / 1000.0; _dy = (ag_FA[i2, 1] - ag_Q[q, 1]) / 1000.0
    _X = np.column_stack([_p, _p * _dx, _p * _dy])
    _A = (_X * _w[:, None]).T @ _X + np.sum(_w * _p * _p) * np.diag([0.0, 1.0, 1.0])
    return np.linalg.solve(_A, (_X * _w[:, None]).T @ ag_FA[i2, 2])[0], np.median(d2[:15])
def ag_A7(i, d, q):
    _m = ag_CUT[i]; i2, d2 = i[_m][:15], d[_m][:15]
    _w = ag_kern(d2) / ag_FA[i2, 5]
    return np.sum(_w * ag_FA[i2, 2] / ag_FA[i2, 3]) / np.sum(_w), np.median(d2)

ag_ESTS = [("A1 unif k10 (original)", ag_A1), ("A2 kernel k15 (adopted)", ag_A2),
           ("A3 +precision proj2/vc", ag_A3), ("A4 GLS deproj (no cut)", ag_A4),
           ("A5 LOCAL-LINEAR ridge", ag_A5), ("A6 loclin GLS (no cut)", ag_A6),
           ("A7 +precision 1/vc", ag_A7)]
ag_CH = {}
for _name, _fn in ag_ESTS:
    ag_CH[_name] = {R: {} for R in [0, 1500]}
    for wd in sp_wells:
        for R in [0, 1500]:
            _idx, _ds = ag_top[R][wd["wi"]]
            ch = np.empty(16); dd = np.empty(16)
            for j in range(16):
                _Dh, dd[j] = _fn(_idx[j], _ds[j], wd["wi"] * 16 + j)
                ch[j] = _Dh * wd["seg"][16]["proj"][j]
            ag_CH[_name][R][wd["wi"]] = (ch, dd)

ag_RES = {}
ag_PW = {}
for _name, _ in ag_ESTS:
    for _st in ["S1 global kappa", "S2 kappa(d)", "S3 kappa(d)+sqrt(pos)"]:
        _Gs = {R: {} for R in [0, 1500]}
        for R in [0, 1500]:
            for wd in sp_wells:
                ch, dd = ag_CH[_name][R][wd["wi"]]
                _sg = wd["seg"][16]
                _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                              np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
                _g = np.where(np.abs(_sg["proj"][_si]) < 0.35, 0.0, np.diff(np.r_[0.0, wd["U"]]) + ch[_si])
                if _st.startswith("S1"):
                    _cols = [np.cumsum(_g)]
                else:
                    _bs = np.digitize(dd, A_BINS[1:-1])[_si]
                    _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
                    if _st.startswith("S3"):
                        _cols.append(np.cumsum(_g * np.sqrt((_si + 0.5) / 16)))
                _Gs[R][wd["wi"]] = np.column_stack(_cols)
        def _fit(skip):
            _A = _y = None
            for R in [0, 1500]:
                for wd in sp_wells:
                    if skip is not None and wd["wi"] % 5 == skip:
                        continue
                    G = _Gs[R][wd["wi"]]
                    if _A is None:
                        _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
                    _A += G.T @ G; _y += G.T @ wd["R0"]
            return np.linalg.lstsq(_A, _y, rcond=None)[0]
        _out = {}
        for _mode in ["in", "ho"]:
            for R in [0, 1500]:
                _rw, _sq, _n = [], 0.0, 0
                for f in (range(5) if _mode == "ho" else [None]):
                    _kb = _fit(f)
                    for wd in sp_wells:
                        if _mode == "ho" and wd["wi"] % 5 != f:
                            continue
                        _e = _Gs[R][wd["wi"]] @ _kb - wd["R0"]
                        _rww = np.sqrt(np.nanmean(_e ** 2))
                        _rw.append(_rww); _sq += np.nansum(_e ** 2); _n += int(np.isfinite(_e).sum())
                        if _mode == "in" and R == 0 and _st.startswith("S3"):
                            ag_PW.setdefault(_name, {})[wd["wid"]] = _rww
                _out[(_mode, R)] = (np.mean(_rw), np.sqrt(_sq / _n))
        ag_RES[(_name, _st)] = _out
        print(f"{_name:24s} {_st:22s} in R0 {_out[('in',0)][0]:5.2f}/{_out[('in',0)][1]:5.2f} "
              f"R1500 {_out[('in',1500)][0]:5.2f}/{_out[('in',1500)][1]:5.2f} | "
              f"ho R0 {_out[('ho',0)][0]:5.2f}/{_out[('ho',0)][1]:5.2f} "
              f"R1500 {_out[('ho',1500)][0]:5.2f}/{_out[('ho',1500)][1]:5.2f}")

fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
_snames = ["S1 global kappa", "S2 kappa(d)", "S3 kappa(d)+sqrt(pos)"]
for ax, R in zip(axes, [0, 1500]):
    _M = np.array([[ag_RES[(n, s)][("ho", R)][1] for s in _snames] for n, _ in ag_ESTS])
    _im = ax.imshow(_M, cmap="RdYlGn_r", aspect="auto")
    for _i in range(len(ag_ESTS)):
        for _j in range(3):
            ax.text(_j, _i, f"{_M[_i, _j]:.2f}", ha="center", va="center", fontsize=10,
                    weight="bold" if _M[_i, _j] == _M.min() else "normal")
    ax.set_xticks(range(3)); ax.set_xticklabels([s[:2] + "\n" + s[3:] for s in _snames], fontsize=8)
    ax.set_yticks(range(len(ag_ESTS))); ax.set_yticklabels([n for n, _ in ag_ESTS], fontsize=9)
    ax.set_title(f"HOLDOUT pooled RMSE, R={R}")
plt.suptitle("Aggregation grid: every estimator x every kappa structure (bold = column best)")
plt.tight_layout(); plt.show()
print("""
READ: (1) LOCAL-LINEAR (A5) wins at every kappa structure and both regimes -- the order-1
smoother removes regression-to-local-mean bias at field gradients, precisely the D2/D3 tail
mechanism. (2) PRECISION weighting (A3/A4/A7) loses everywhere, ~0.3 pooled: sigma^2_well
conflates measurement noise with geological roughness, so inverse-variance down-weights wells in
rough geology -- exactly the informative donors. A textbook assumption (heteroscedastic noise,
common signal) that this field violates. (3) The kappa-structure ordering (S1 < S2 < S3) is
preserved under every estimator: the trust architecture and the estimator improve independently.""")

# --- cell 77 ---
# === Local-linear adoption: sensitivity, K-robustness, committee composition, per-well impact ===
# Recorded sensitivity (bash sweeps): ridge alpha {0.3, 1, 3} -> holdout pooled {9.45, 9.49, 9.52}
# at R0 but {11.32, 11.24, 11.27} at R1500 -> alpha=1 best balance; donor depth {30, 50, 100}
# identical to 0.01 (plateau). K-robustness: A5 beats A2 at K=8 (9.67 vs 9.74) and K=32
# (9.63 vs 9.70, holdout pooled R0); K=16 remains optimal. Here: compose with the committee.
ag2_DH5 = {R: {} for R in [0, 1500]}                     # A5 D_hat (needed for committee column)
for wd in sp_wells:
    for R in [0, 1500]:
        _idx, _ds = ag_top[R][wd["wi"]]
        _Dh = np.empty(16)
        for j in range(16):
            _m = ag_CUT[_idx[j]]; i2, d2 = _idx[j][_m][:50], _ds[j][_m][:50]
            _w = ag_kern(d2)
            _dx = (ag_FA[i2, 0] - ag_Q[wd["wi"] * 16 + j, 0]) / 1000.0
            _dy = (ag_FA[i2, 1] - ag_Q[wd["wi"] * 16 + j, 1]) / 1000.0
            _X = np.column_stack([np.ones(len(i2)), _dx, _dy])
            _A = (_X * _w[:, None]).T @ _X + np.sum(_w) * np.diag([0.0, 1.0, 1.0])
            _Dh[j] = np.linalg.solve(_A, (_X * _w[:, None]).T @ (ag_FA[i2, 2] / ag_FA[i2, 3]))[0]
        ag2_DH5[R][wd["wi"]] = _Dh

def ag2_run(est, committee, folds=False):
    _Gs = {R: {} for R in [0, 1500]}
    for R in [0, 1500]:
        _qb = 0
        for wd in sp_wells:
            if est == "A2":
                ch, dd = bl_chdd[R][wd["wi"]]; _Dh = gt_Dh[R][wd["wi"]]
            else:
                ch, dd = ag_CH["A5 LOCAL-LINEAR ridge"][R][wd["wi"]]; _Dh = ag2_DH5[R][wd["wi"]]
            _sg = wd["seg"][16]
            _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                          np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
            _ndz = np.diff(np.r_[0.0, wd["U"]])
            _gated = np.abs(_sg["proj"][_si]) < 0.35
            _g = np.where(_gated, 0.0, _ndz + ch[_si])
            _bs = np.digitize(dd, A_BINS[1:-1])[_si]
            _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
            _cols.append(np.cumsum(_g * np.sqrt((_si + 0.5) / 16)))
            if committee:
                _chL = _Dh * np.cos(gt_AZ[_qb:_qb + 16] - gt_TH[_qb:_qb + 16])
                _subm = _gated & (gt_ROT[_qb:_qb + 16] < 60)[_si]
                _cols.append(np.cumsum(np.where(_subm, _ndz + _chL[_si], 0.0)))
            _qb += 16
            _Gs[R][wd["wi"]] = np.column_stack(_cols)
    def _fit(skip):
        _A = _y = None
        for R in [0, 1500]:
            for wd in sp_wells:
                if skip is not None and wd["wi"] % 5 == skip:
                    continue
                G = _Gs[R][wd["wi"]]
                if _A is None:
                    _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
                _A += G.T @ G; _y += G.T @ wd["R0"]
        return np.linalg.lstsq(_A, _y, rcond=None)[0]
    _pw = {}
    _lab = f"{est}{' + committee' if committee else '            '}" + ("  ho" if folds else "  in")
    for R in [0, 1500]:
        _rw, _sq, _n = [], 0.0, 0
        for f in (range(5) if folds else [None]):
            _kb = _fit(f)
            for wd in sp_wells:
                if folds and wd["wi"] % 5 != f:
                    continue
                _e = _Gs[R][wd["wi"]] @ _kb - wd["R0"]
                _rww = np.sqrt(np.nanmean(_e ** 2))
                _rw.append(_rww); _sq += np.nansum(_e ** 2); _n += int(np.isfinite(_e).sum())
                if R == 0:
                    _pw[wd["wid"]] = _rww
        _lab += f"  R{R}: {np.mean(_rw):5.2f}/{np.sqrt(_sq / _n):5.2f}"
    print(_lab)
    return _pw
ag2_old = ag2_run("A2", True)
_ = ag2_run("A2", True, folds=True)
ag2_new = ag2_run("A5", True)
_ = ag2_run("A5", True, folds=True)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
_o = np.array([ag2_old[wd["wid"]] for wd in sp_wells])
_n2 = np.array([ag2_new[wd["wid"]] for wd in sp_wells])
_dd0 = np.array([np.median(bl_chdd[0][wd["wi"]][1]) for wd in sp_wells])
_sc = axes[0].scatter(_o, _n2, c=np.clip(_dd0, 0, 3000), cmap="viridis", s=14, alpha=0.7)
_lim = [0.3, 90]
axes[0].plot(_lim, _lim, "k--", lw=1)
axes[0].set_xscale("log"); axes[0].set_yscale("log")
axes[0].set_xlim(_lim); axes[0].set_ylim(_lim)
axes[0].set_xlabel("rowwise RMSE, kernel-mean + committee (ft)")
axes[0].set_ylabel("rowwise RMSE, LOCAL-LINEAR + committee (ft)")
axes[0].set_title(f"773 wells: {int((_n2 < _o).sum())} improve / {int((_n2 > _o).sum())} degrade "
                  f"(below diagonal = better)")
fig.colorbar(_sc, ax=axes[0], label="median donor distance (ft)")
_tails = ["389ae58f", "fb03ae90", "9dfff011", "1b1eba53", "d924e971", "197f8a5a", "91b301ce"]
_xs = np.arange(len(_tails))
axes[1].bar(_xs - 0.2, [ag2_old[w] for w in _tails], 0.4, color="grey", label="kernel mean")
axes[1].bar(_xs + 0.2, [ag2_new[w] for w in _tails], 0.4, color="tab:green", label="local-linear")
axes[1].set_xticks(_xs); axes[1].set_xticklabels([w[:8] for w in _tails], fontsize=8)
axes[1].set_ylabel("rowwise RMSE (ft)")
axes[1].set_title("The magnitude-tail wells (both with committee)")
axes[1].legend(fontsize=9)
plt.tight_layout(); plt.show()
print("""
ADOPTED: local-linear kernel regression (k=50 donors, gaussian h=500 ft, slope-ridge alpha=1)
replaces the kernel-weighted mean, composed with kappa(d)+sqrt(pos), gate and theta_loc
committee. Wins all four holdout statistics at every kappa structure, every K in {8,16,32},
and tempers the magnitude tails it was theoretically aimed at. Reference model is now:
in-sample R0 7.43/9.24, R1500 9.07/11.05; holdout R0 7.48/9.34, R1500 9.10/11.11.
Cumulative LOO since the LB submission: 9.67 -> 9.24 pooled (-0.43, below the 0.5 resubmit bar).""")

# --- cell 78 ---
# === Aggregation closure: five remaining ideas x BOTH estimator families (ALL NEGATIVE/NEUTRAL) ===
# Ideas: (a) bandwidth re-tune (theory: local-linear tolerates larger h); (b) local-quadratic;
# (c) ordinary kriging (donor-redundancy weights -- registered prediction: loses, same-well
# segments are independently informative); (d) segment path-integration vs midpoint sampling;
# (e) heading-similarity kernel. Each run under kernel-mean (kNN family) AND local-linear where
# the idea exists in that family. Reuses ag_* from the grid cell. ~3 min.
ag3_AZ = np.empty(len(ag_FA)); ag3_P0 = np.empty((len(ag_FA), 2)); ag3_P1 = np.empty((len(ag_FA), 2))
_q = 0
for wd in sp_wells:
    _n = wd["n"]; _e = np.linspace(0, _n, 17)
    for j in range(16):
        _f0 = wd["s"] + 1 + int(_e[j]); _f1 = min(wd["s"] + 1 + max(int(_e[j + 1]) - 1, int(_e[j])), len(wd["X"]) - 1)
        ag3_AZ[_q] = np.arctan2(wd["Y"][_f1] - wd["Y"][_f0], wd["X"][_f1] - wd["X"][_f0])
        ag3_P0[_q] = (wd["X"][_f0], wd["Y"][_f0]); ag3_P1[_q] = (wd["X"][_f1], wd["Y"][_f1]); _q += 1
_rng = np.random.default_rng(0)
_ii = _rng.choice(np.where(ag_CUT)[0], 4000, replace=False)
_D = ag_FA[_ii, 2] / ag_FA[_ii, 3]; _Dc = _D - _D.mean()
_dist = np.sqrt((ag_FA[_ii, 0][:, None] - ag_FA[_ii, 0][None, :]) ** 2
                + (ag_FA[_ii, 1][:, None] - ag_FA[_ii, 1][None, :]) ** 2)
_prod = np.outer(_Dc, _Dc); _same = ag_FA[_ii, 4][:, None] == ag_FA[_ii, 4][None, :]
_cov = []
for _b0, _b1 in zip([0, 100, 300, 600, 1000, 1500, 2500], [100, 300, 600, 1000, 1500, 2500, 4000]):
    _m = (_dist >= _b0) & (_dist < _b1) & ~_same
    _cov.append(_prod[_m].mean())
_mids = np.array([50, 200, 450, 800, 1250, 2000, 3250]); _msk = np.array(_cov) > 0
_sl = np.polyfit(_mids[_msk], np.log(np.array(_cov)[_msk]), 1)
ag3_lam = -1 / _sl[0]; ag3_c0 = np.exp(_sl[1]); ag3_s2 = _Dc.var()
print(f"variogram of the drift field: C(d) = {ag3_c0:.6f} exp(-d/{ag3_lam:.0f} ft), total var "
      f"{ag3_s2:.6f} -> NUGGET = {1 - ag3_c0 / ag3_s2:.0%} of variance, white at zero distance")
print("(third independent measurement of the ~58% well-local share: correlogram, LOO resid var, nugget)\n")

def ag3_est(i, d, q, fam, h=500.0, quad=False, useaz=False, path=False, krig=False):
    _m = ag_CUT[i]; _iall = i[_m]
    _pts = [(ag_Q[q], 1.0)] if not path else [(ag3_P0[q], 0.25), (ag_Q[q], 0.5), (ag3_P1[q], 0.25)]
    _Dh = 0.0
    for _p, _wt in _pts:
        _dp = np.hypot(ag_FA[_iall, 0] - _p[0], ag_FA[_iall, 1] - _p[1])
        _kk = 30 if krig else (15 if fam == "knn" else 50)
        _o = np.argsort(_dp)[:_kk]
        i2, d2 = _iall[_o], _dp[_o]
        if krig:
            _C = ag3_c0 * np.exp(-np.sqrt((ag_FA[i2, 0][:, None] - ag_FA[i2, 0][None, :]) ** 2
                                          + (ag_FA[i2, 1][:, None] - ag_FA[i2, 1][None, :]) ** 2) / ag3_lam)
            _A = np.block([[_C + np.eye(_kk) * (ag3_s2 - ag3_c0 + 1e-8), np.ones((_kk, 1))],
                           [np.ones((1, _kk)), np.zeros((1, 1))]])
            _wv = np.linalg.solve(_A, np.r_[ag3_c0 * np.exp(-d2 / ag3_lam), 1.0])[:_kk]
            _Dh += _wt * np.sum(_wv * ag_FA[i2, 2] / ag_FA[i2, 3]); continue
        _w = ag_kern(d2, h)
        if useaz:
            _daz = np.arctan2(np.sin(ag3_AZ[i2] - ag3_AZ[q]), np.cos(ag3_AZ[i2] - ag3_AZ[q]))
            _w = _w * np.exp(-(np.degrees(np.abs(_daz)) / 60.0) ** 2)
        if fam == "knn":
            _Dh += _wt * np.sum(_w * ag_FA[i2, 2] / ag_FA[i2, 3]) / np.sum(_w)
        else:
            _dx = (ag_FA[i2, 0] - _p[0]) / 1000.0; _dy = (ag_FA[i2, 1] - _p[1]) / 1000.0
            _cols = [np.ones(len(i2)), _dx, _dy]; _pen = [0.0, 1.0, 1.0]
            if quad:
                _cols += [_dx * _dx, _dy * _dy, _dx * _dy]; _pen += [1.0, 1.0, 1.0]
            _X = np.column_stack(_cols)
            _A = (_X * _w[:, None]).T @ _X + np.sum(_w) * np.diag(_pen)
            _Dh += _wt * np.linalg.solve(_A, (_X * _w[:, None]).T @ (ag_FA[i2, 2] / ag_FA[i2, 3]))[0]
    return _Dh

def ag3_score(label, **kw):
    _Gs = {R: {} for R in [0, 1500]}
    for R in [0, 1500]:
        for wd in sp_wells:
            _idx, _ds = ag_top[R][wd["wi"]]
            ch = np.empty(16); dd = np.empty(16)
            for j in range(16):
                _q = wd["wi"] * 16 + j
                ch[j] = ag3_est(_idx[j], _ds[j], _q, **kw) * wd["seg"][16]["proj"][j]
                dd[j] = np.median(_ds[j][ag_CUT[_idx[j]]][:15])
            _sg = wd["seg"][16]
            _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                          np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
            _g = np.where(np.abs(_sg["proj"][_si]) < 0.35, 0.0, np.diff(np.r_[0.0, wd["U"]]) + ch[_si])
            _bs = np.digitize(dd, A_BINS[1:-1])[_si]
            _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
            _cols.append(np.cumsum(_g * np.sqrt((_si + 0.5) / 16)))
            _Gs[R][wd["wi"]] = np.column_stack(_cols)
    def _fit(skip):
        _A = _y = None
        for R in [0, 1500]:
            for wd in sp_wells:
                if skip is not None and wd["wi"] % 5 == skip:
                    continue
                G = _Gs[R][wd["wi"]]
                if _A is None:
                    _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
                _A += G.T @ G; _y += G.T @ wd["R0"]
        return np.linalg.lstsq(_A, _y, rcond=None)[0]
    _lab = f"{label:32s}"
    for _mode in ["in", "ho"]:
        for R in [0, 1500]:
            _rw, _sq, _n = [], 0.0, 0
            for f in (range(5) if _mode == "ho" else [None]):
                _kb = _fit(f)
                for wd in sp_wells:
                    if _mode == "ho" and wd["wi"] % 5 != f:
                        continue
                    _e = _Gs[R][wd["wi"]] @ _kb - wd["R0"]
                    _rw.append(np.sqrt(np.nanmean(_e ** 2))); _sq += np.nansum(_e ** 2); _n += int(np.isfinite(_e).sum())
            _lab += f" {_mode}R{R}: {np.mean(_rw):5.2f}/{np.sqrt(_sq / _n):5.2f}"
    print(_lab)
print("-- kNN family (kernel mean k=15) --")
ag3_score("A2 h=500 (reference)", fam="knn")
for _h in [300.0, 750.0, 1000.0]:
    ag3_score(f"A2 h={_h:.0f}", fam="knn", h=_h)
ag3_score("A2 path-integrated", fam="knn", path=True)
ag3_score("A2 x heading-similarity", fam="knn", useaz=True)
ag3_score("ordinary kriging k=30", fam="knn", krig=True)
print("-- local-linear family (k=50, ridge) --")
ag3_score("A5 h=500 (reference)", fam="ll")
for _h in [750.0, 1000.0]:
    ag3_score(f"A5 h={_h:.0f}", fam="ll", h=_h)
ag3_score("A5 local-QUADRATIC", fam="ll", quad=True)
ag3_score("A5 path-integrated", fam="ll", path=True)
ag3_score("A5 x heading-similarity", fam="ll", useaz=True)
print("""
CLOSURE (all negative/neutral in BOTH families -- adopted config stands):
(a) h=500 is optimal for kNN AND local-linear; local-linear degrades slower as h grows (it
    corrects the first-order bias larger h introduces) but never beats 500: the bandwidth is set
    by the GEOLOGY -- the same ~500 ft, fourth measurement -- not by estimator bias.
(b) quadratic terms: variance without signal (its order-0 analog IS the kernel mean).
(c) kriging loses as REGISTERED, worst in the buffered regime: with a ~56% nugget there is little
    structured covariance to exploit, and redundancy down-weighting fights the measured fact that
    same-well segments are independently informative.
(d) path-integration == midpoint sampling to 0.01 ft in both families (h >> segment length).
(e) heading-similarity hurts in both families: it discards cross-heading donors that the
    deprojection already transfers correctly.
The aggregation program is closed end to end; every idea has a recorded verdict in both families.""")

# --- cell 80 ---
# === Spline alternatives x both estimator families -- and the DUAL-FIELD synthesis (ADOPTED) ===
# V0 uniform K=16 | V1 fixed-length knots | V2 fused-ridge coefficients | V3 piecewise-linear
# drift | V4 joint global RBF surface | V5 adaptive change-point donor knots | V6 Fourier-smoothed.
# Each judged in-sample AND 5-fold kappa-holdout, both regimes, under kernel-mean and local-linear.
# The one winner is V2's REGIME structure: smoothed coefficients transfer farther, raw serve near
# donors -- completed as a DUAL field (raw + smoothed columns per distance bin). ~6 min.
def spl_fitc(wd, lam=0.0, edges=None):
    _e = np.linspace(0, wd["n"], 17) if edges is None else edges
    _K = len(_e) - 1
    _t = np.arange(1, wd["n"] + 1.0)
    _phi = np.column_stack([np.clip(_t - _e[j], 0, _e[j + 1] - _e[j]) for j in range(_K)])
    _A = _phi.T @ _phi
    if lam > 0:
        _D = np.diff(np.eye(_K), axis=0)
        _A = _A + lam * np.mean(np.diag(_phi.T @ _phi)) * _D.T @ _D
    return np.linalg.solve(_A, _phi.T @ (wd["R0"] - wd["U"]))

def spl_geo(wd, edges):
    _K = len(edges) - 1
    _mid = np.empty((_K, 2)); _proj = np.empty(_K)
    for j in range(_K):
        _f0 = wd["s"] + 1 + int(edges[j]); _f1 = min(wd["s"] + 1 + max(int(edges[j + 1]) - 1, int(edges[j])), len(wd["X"]) - 1)
        _mid[j] = ((wd["X"][_f0] + wd["X"][_f1]) / 2, (wd["Y"][_f0] + wd["Y"][_f1]) / 2)
        _proj[j] = np.cos(np.arctan2(wd["Y"][_f1] - wd["Y"][_f0], wd["X"][_f1] - wd["X"][_f0]) - np.radians(theta0))
    _si = np.clip(np.searchsorted(edges[1:], np.arange(1, wd["n"] + 1.0), side="left"), 0, _K - 1)
    return _mid, _proj, _si

def spl_est(kx, ky, kD, p, est, R, d2):
    _cand = np.where(d2 >= R * R)[0] if R else np.arange(len(d2))
    if est == "knn":
        _sel = _cand[np.argpartition(d2[_cand], 15)[:15]]
        _w = np.exp(np.maximum(-d2[_sel] / 5e5, -700))
        _Dh = np.sum(_w * kD[_sel]) / np.sum(_w)
    else:
        _sel = _cand[np.argpartition(d2[_cand], 50)[:50]]
        _w = np.exp(np.maximum(-d2[_sel] / 5e5, -700))
        _dx = (kx[_sel] - p[0]) / 1000.0; _dy = (ky[_sel] - p[1]) / 1000.0
        _X = np.column_stack([np.ones(len(_sel)), _dx, _dy])
        _A = (_X * _w[:, None]).T @ _X + np.sum(_w) * np.diag([0.0, 1.0, 1.0])
        _Dh = np.linalg.solve(_A, (_X * _w[:, None]).T @ kD[_sel])[0]
    return _Dh, np.sqrt(np.median(np.sort(d2[_sel])[:15]))

def spl_steps(field, est, geos):
    """field: (x,y,D,wi); geos[wi] = (mid, proj, segid, K); -> per-step (g, dd, pos) per regime."""
    OUT = {R: {} for R in [0, 1500]}
    for wd in sp_wells:
        _keep = field[:, 3] != wd["wi"]
        _kx, _ky, _kD = field[_keep, 0], field[_keep, 1], field[_keep, 2]
        _mid, _proj, _si, _K = geos[wd["wi"]]
        _ndz = np.diff(np.r_[0.0, wd["U"]])
        for R in [0, 1500]:
            ch = np.empty(_K); dd = np.empty(_K)
            for j in range(_K):
                _d2 = (_kx - _mid[j, 0]) ** 2 + (_ky - _mid[j, 1]) ** 2
                _Dh, dd[j] = spl_est(_kx, _ky, _kD, _mid[j], est, R, _d2)
                ch[j] = _Dh * _proj[j]
            _g = np.where(np.abs(_proj[_si]) < 0.35, 0.0, _ndz + ch[_si])
            OUT[R][wd["wi"]] = (_g, dd[_si], (_si + 0.5) / _K)
    return OUT

spl_rows = {}
def spl_score(STEPS, label, extra=None):
    _Gs = {R: {} for R in [0, 1500]}
    for R in [0, 1500]:
        for wd in sp_wells:
            _g, _dds, _pos = STEPS[R][wd["wi"]]
            _bs = np.digitize(_dds, A_BINS[1:-1])
            _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
            if extra is not None:
                _g2 = extra[R][wd["wi"]][0]
                _cols += [np.cumsum(np.where(_bs == b, _g2, 0.0)) for b in range(nB)]
                _cols.append(np.cumsum(0.5 * (_g + _g2) * np.sqrt(_pos)))
            else:
                _cols.append(np.cumsum(_g * np.sqrt(_pos)))
            _Gs[R][wd["wi"]] = np.column_stack(_cols)
    def _fit(skip):
        _A = _y = None
        for R in [0, 1500]:
            for wd in sp_wells:
                if skip is not None and wd["wi"] % 5 == skip:
                    continue
                G = _Gs[R][wd["wi"]]
                if _A is None:
                    _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
                _A += G.T @ G; _y += G.T @ wd["R0"]
        return np.linalg.lstsq(_A, _y, rcond=None)[0]
    _lab = f"{label:34s}"
    _vals = {}
    for _mode in ["in", "ho"]:
        for R in [0, 1500]:
            _rw, _sq, _n = [], 0.0, 0
            for f in (range(5) if _mode == "ho" else [None]):
                _kb = _fit(f)
                for wd in sp_wells:
                    if _mode == "ho" and wd["wi"] % 5 != f:
                        continue
                    _e = _Gs[R][wd["wi"]] @ _kb - wd["R0"]
                    _rw.append(np.sqrt(np.nanmean(_e ** 2))); _sq += np.nansum(_e ** 2); _n += int(np.isfinite(_e).sum())
            _vals[(_mode, R)] = np.sqrt(_sq / _n)
            _lab += f" {_mode}R{R}: {np.mean(_rw):5.2f}/{np.sqrt(_sq / _n):5.2f}"
    print(_lab)
    spl_rows[label] = _vals

spl_g16 = {wd["wi"]: (*spl_geo(wd, np.linspace(0, wd["n"], 17)), 16) for wd in sp_wells}
def spl_pack16(cs):
    _F = []
    for wd in sp_wells:
        _mid, _proj, _, _ = spl_g16[wd["wi"]]
        for j in range(16):
            if abs(_proj[j]) > 0.3:
                _F.append((_mid[j, 0], _mid[j, 1], cs[wd["wi"]][j] / _proj[j], wd["wi"]))
    return np.array(_F)
spl_cr = {wd["wi"]: wd["seg"][16]["c"] for wd in sp_wells}
spl_cs = {wd["wi"]: spl_fitc(wd, lam=10.0) for wd in sp_wells}
spl_cf = {}
for wd in sp_wells:
    _n = wd["n"]; _t = np.arange(1, _n + 1.0)
    _cols = [_t]
    for m in range(1, 9):
        _cols += [np.cumsum(np.cos(2 * np.pi * m * _t / _n)), np.cumsum(np.sin(2 * np.pi * m * _t / _n))]
    _b = np.linalg.lstsq(np.column_stack(_cols), wd["R0"] - wd["U"], rcond=None)[0]
    _tau = (np.arange(16) + 0.5) * _n / 16
    _dr = np.full(16, _b[0])
    for m in range(1, 9):
        _dr += _b[2 * m - 1] * np.cos(2 * np.pi * m * _tau / _n) + _b[2 * m] * np.sin(2 * np.pi * m * _tau / _n)
    spl_cf[wd["wi"]] = _dr
for est in ["knn", "ll"]:
    spl_score(spl_steps(spl_pack16(spl_cr), est, spl_g16), f"V0 uniform K=16 [{est}]")
    spl_score(spl_steps(spl_pack16(spl_cs), est, spl_g16), f"V2 fused-ridge rho=10 [{est}]")
    spl_score(spl_steps(spl_pack16(spl_cf), est, spl_g16), f"V6 Fourier M=8 [{est}]")
    _geo = {}
    _F = []
    for wd in sp_wells:
        _K1 = int(np.clip(round(wd["n"] / 300.0), 4, 48))
        _e = np.linspace(0, wd["n"], _K1 + 1)
        _c = spl_fitc(wd, edges=_e)
        _mid, _proj, _si = spl_geo(wd, _e)
        _geo[wd["wi"]] = (_mid, _proj, _si, _K1)
        for j in range(_K1):
            if abs(_proj[j]) > 0.3:
                _F.append((_mid[j, 0], _mid[j, 1], _c[j] / _proj[j], wd["wi"]))
    spl_score(spl_steps(np.array(_F), est, _geo), f"V1 fixed-length 300ft [{est}]")
    spl_score(spl_steps(spl_pack16(spl_cr), est, spl_g16, ), f"DUAL raw+smooth [{est}]",
              extra=spl_steps(spl_pack16(spl_cs), est, spl_g16))
print("""recorded from the full sweep (bash, same protocol): V3 piecewise-linear drift ho 9.78-9.82
(delocalized coefficients transfer poorly); V4 joint global RBF surface ho 15.5 (nothing global
survives a 56%-nugget field); V5 adaptive change-point donor knots ho 11.9 (knot positions are
per-well latent information); V1 at L=500 slightly worse than L=300~=K16 (~294 ft average).""")

fig, ax = plt.subplots(figsize=(12, 5))
_labels = [l for l in spl_rows]
_x = np.arange(len(_labels))
for _off, (_m, _R, _c, _n2) in enumerate([("ho", 0, "tab:green", "holdout R=0"), ("ho", 1500, "tab:red", "holdout R=1500")]):
    ax.plot(_x, [spl_rows[l][(_m, _R)] for l in _labels], "o-", color=_c, label=_n2)
ax.set_xticks(_x); ax.set_xticklabels([l.replace(" [", "\n[") for l in _labels], fontsize=7.5)
ax.set_ylabel("pooled RMSE (ft)"); ax.legend()
ax.set_title("Spline alternatives x estimator family (holdout). The DUAL field keeps the near-regime score\n"
             "and takes the far-regime gain: smoothed coefficients travel, raw coefficients stay local.")
ax.grid(alpha=0.25)
plt.tight_layout(); plt.show()
print("""
VERDICT: V1/V6 neutral, V3/V4/V5 negative (each for the predicted reason), V2 regime-dependent ->
completed as the DUAL FIELD: kappa gets separate raw / smoothed columns per distance bin and
DISCOVERS the structure itself (raw kappa ~[1.1, 1.0, 0.3, ...], smooth kappa ~[0, 0.1, 0.6, 0.8]):
trust raw detail from near donors, smoothed trend from far donors. ADOPTED under local-linear.""")

# --- cell 81 ---
# === BEST MODEL identification + the 12 worst wells, four models compared on TVT ===
# Contenders (all LOO, R=0 donors, kappa fit jointly over regimes as in the cells above):
#   M1 as-submitted config: kernel-mean kNN + kappa(d) + gate            (the LB 10.79 recipe)
#   M2 previous best:       local-linear + kappa(d)+sqrt(pos) + gate + theta_loc committee
#   M3 NEW BEST:            local-linear DUAL field (raw+smoothed) + kappa(d)x2 + sqrt(pos)
#                           + gate + committee
# Reuses bl_chdd, gt_*, ag_CH, spl_* from the cells above.
fin_CHs = {R: {} for R in [0, 1500]}                     # smoothed-field local-linear chdd
_Fs = spl_pack16(spl_cs)
for wd in sp_wells:
    _keep = _Fs[:, 3] != wd["wi"]
    _kx, _ky, _kD = _Fs[_keep, 0], _Fs[_keep, 1], _Fs[_keep, 2]
    _mid, _proj, _, _ = spl_g16[wd["wi"]]
    for R in [0, 1500]:
        ch = np.empty(16); dd = np.empty(16)
        for j in range(16):
            _d2 = (_kx - _mid[j, 0]) ** 2 + (_ky - _mid[j, 1]) ** 2
            _Dh, dd[j] = spl_est(_kx, _ky, _kD, _mid[j], "ll", R, _d2)
            ch[j] = _Dh * _proj[j]
        fin_CHs[R][wd["wi"]] = (ch, dd)

def fin_model(name):
    _Gs = {R: {} for R in [0, 1500]}
    for R in [0, 1500]:
        _qb = 0
        for wd in sp_wells:
            _sg = wd["seg"][16]
            _si = np.clip(np.searchsorted(np.linspace(0, wd["n"], 17)[1:],
                                          np.arange(1, wd["n"] + 1.0), side="left"), 0, 15)
            _ndz = np.diff(np.r_[0.0, wd["U"]])
            _gated = np.abs(_sg["proj"][_si]) < 0.35
            if name == "M1":
                ch, dd = bl_chdd[R][wd["wi"]]
                _g = np.where(_gated, 0.0, _ndz + ch[_si])
                _bs = np.digitize(dd, A_BINS[1:-1])[_si]
                _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
            elif name == "M2":
                ch, dd = ag_CH["A5 LOCAL-LINEAR ridge"][R][wd["wi"]]
                _g = np.where(_gated, 0.0, _ndz + ch[_si])
                _bs = np.digitize(dd, A_BINS[1:-1])[_si]
                _cols = [np.cumsum(np.where(_bs == b, _g, 0.0)) for b in range(nB)]
                _cols.append(np.cumsum(_g * np.sqrt((_si + 0.5) / 16)))
                _chL = gt_Dh[R][wd["wi"]] * np.cos(gt_AZ[_qb:_qb + 16] - gt_TH[_qb:_qb + 16])
                _subm = _gated & (gt_ROT[_qb:_qb + 16] < 60)[_si]
                _cols.append(np.cumsum(np.where(_subm, _ndz + _chL[_si], 0.0)))
            else:  # M3
                chr_, dd = ag_CH["A5 LOCAL-LINEAR ridge"][R][wd["wi"]]
                chs_, _ = fin_CHs[R][wd["wi"]]
                _gr = np.where(_gated, 0.0, _ndz + chr_[_si])
                _gsm = np.where(_gated, 0.0, _ndz + chs_[_si])
                _bs = np.digitize(dd, A_BINS[1:-1])[_si]
                _cols = [np.cumsum(np.where(_bs == b, _gr, 0.0)) for b in range(nB)]
                _cols += [np.cumsum(np.where(_bs == b, _gsm, 0.0)) for b in range(nB)]
                _cols.append(np.cumsum(0.5 * (_gr + _gsm) * np.sqrt((_si + 0.5) / 16)))
                _chL = gt_Dh[R][wd["wi"]] * np.cos(gt_AZ[_qb:_qb + 16] - gt_TH[_qb:_qb + 16])
                _subm = _gated & (gt_ROT[_qb:_qb + 16] < 60)[_si]
                _cols.append(np.cumsum(np.where(_subm, _ndz + _chL[_si], 0.0)))
            _qb += 16
            _Gs[R][wd["wi"]] = np.column_stack(_cols)
    _A = _y = None
    for R in [0, 1500]:
        for wd in sp_wells:
            G = _Gs[R][wd["wi"]]
            if _A is None:
                _A = np.zeros((G.shape[1], G.shape[1])); _y = np.zeros(G.shape[1])
            _A += G.T @ G; _y += G.T @ wd["R0"]
    _kb = np.linalg.lstsq(_A, _y, rcond=None)[0]
    _preds = {wd["wi"]: _Gs[0][wd["wi"]] @ _kb for wd in sp_wells}
    _rw = {wd["wid"]: np.sqrt(np.nanmean((_preds[wd["wi"]] - wd["R0"]) ** 2)) for wd in sp_wells}
    _sq = sum(np.nansum((_preds[wd["wi"]] - wd["R0"]) ** 2) for wd in sp_wells)
    _n = sum(int(np.isfinite(wd["R0"]).sum()) for wd in sp_wells)
    return _preds, _rw, np.sqrt(_sq / _n)

fin_out = {m: fin_model(m) for m in ["M1", "M2", "M3"]}
print(f"{'model':44s} {'rowwise':>8s} {'POOLED':>8s}")
for m, lbl in [("M1", "as-submitted: kernel kNN + kappa(d) [LB 10.79]"),
               ("M2", "prev best: local-linear + sqrt(pos) + committee"),
               ("M3", "NEW BEST: dual-field local-linear + committee")]:
    _p, _r, _pool = fin_out[m]
    print(f"{lbl:44s} {np.mean(list(_r.values())):8.2f} {_pool:8.2f}")
print(f"{'hold-at-anchor':44s} {np.mean([np.sqrt(np.nanmean(wd['R0'] ** 2)) for wd in sp_wells]):8.2f} "
      f"{np.sqrt(sum(np.nansum(wd['R0'] ** 2) for wd in sp_wells) / sum(int(np.isfinite(wd['R0']).sum()) for wd in sp_wells)):8.2f}")
print("""=> cumulative vs the LB submission: 9.67 -> 9.15 pooled = -0.52, ABOVE the 0.5 threshold:
   the submission script is updated to M3 and resubmitted (committee still never fires on the
   3 test wells; the dual field and local-linear DO change their predictions).""")

fin_worst = sorted(fin_out["M3"][1], key=lambda w: -fin_out["M3"][1][w])[:12]
fig, axes = plt.subplots(3, 4, figsize=(19, 12.5))
for ax, _wid in zip(axes.ravel(), fin_worst):
    wd = [w for w in sp_wells if w["wid"] == _wid][0]
    _anchor = wd["tvt"][wd["s"]]; _steps = np.arange(1, wd["n"] + 1)
    _sg = wd["seg"][16]
    ax.plot(_steps, _anchor + wd["R0"], color="tab:orange", lw=2.4, label="truth")
    ax.plot(_steps, np.full(wd["n"], _anchor), "--", color="grey", lw=1.0, label="hold")
    ax.plot(_steps, _anchor + fin_out["M1"][0][wd["wi"]], color="tab:blue", lw=1.2, label="submitted (LB 10.79)")
    ax.plot(_steps, _anchor + fin_out["M2"][0][wd["wi"]], color="tab:purple", lw=1.2, label="prev best")
    ax.plot(_steps, _anchor + fin_out["M3"][0][wd["wi"]], color="tab:green", lw=2.0, label="NEW BEST (dual-field LL)")
    ax.plot(_steps, _anchor + wd["U"] + _sg["phi"] @ _sg["c"], "k:", lw=1.0, label="oracle")
    ax.set_title(f"{_wid[:8]}:  M1 {fin_out['M1'][1][_wid]:.1f} | M2 {fin_out['M2'][1][_wid]:.1f} | "
                 f"M3 {fin_out['M3'][1][_wid]:.1f} ft", fontsize=9.5)
    ax.set_xlabel("lateral step")
for _r2 in range(3):
    axes[_r2, 0].set_ylabel("TVT (ft)")
axes[0, 0].legend(fontsize=8)
fig.suptitle("The 12 worst wells under the best model -- four generations compared "
             "(truth / hold / submitted / previous best / dual-field best / oracle)", y=0.995, fontsize=13)
plt.tight_layout()
plt.show()
