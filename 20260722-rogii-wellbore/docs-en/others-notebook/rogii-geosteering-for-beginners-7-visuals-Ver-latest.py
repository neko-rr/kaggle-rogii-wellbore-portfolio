# %% [markdown]
# # 🛢️ ROGII Geosteering, Explained — TVT, GR Correlation & a Clean Baseline
# 
# > **New to this competition and wondering what on earth a "TVT" is?** This notebook is for you.
# 
# Most notebooks here jump straight to models. This one first **explains the drilling problem in plain language**, then shows the **pictures** that make geosteering click — starting from the official cross-section the organizers hand you — and finally gives a **clean, reproducible baseline** you can fork and build on.
# 
# **What we are actually doing:** a drilling company steers a well *horizontally* through a thin, valuable rock layer (the "pay zone"). To stay inside it, they need to know the bit's **vertical position inside the geology** at every step. That vertical position is the **TVT (True Vertical Thickness)** — and that is exactly what we predict.
# 
# The only sensor we have along the horizontal is the **GR (Gamma Ray)** log. Each rock layer has its own GR "fingerprint", recorded once in a vertical reference well (the **type well**). Geosteering = *matching* the horizontal GR against that fingerprint to figure out where we are.
# 
# ---
# **Roadmap**
# 1. 🗺️ The whole problem in one picture — the official cross-section
# 2. The data — horizontal wells vs type wells
# 3. 🎯 Picture 1 — the type-well GR *signature*
# 4. 🧭 Picture 2 — the drill path through the earth
# 5. 💡 Picture 3 — the geosteering intuition (the "aha")
# 6. 📊 Picture 4 — the target & what we actually predict
# 7. 🪨 Picture 5 — the geological layers a well crosses
# 8. 🎨 GR fingerprint by formation
# 9. 🤖 A humble baseline — and an honest look at what *fails*
# 

# %% cell 1
import os, glob, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
warnings.filterwarnings("ignore")

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.grid": True, "grid.alpha": 0.25, "axes.edgecolor": "#888",
    "font.size": 11, "axes.titlesize": 13, "axes.titleweight": "bold",
})

# --- auto-detect data root (Kaggle input or local mirror) ---
CANDIDATES = [
    "/kaggle/input/competitions/rogii-wellbore-geology-prediction",
    "/kaggle/input/rogii-wellbore-geology-prediction",
    "data/rogii", "../data/rogii", "./rogii",
]
ROOT = next((p for p in CANDIDATES if os.path.isdir(os.path.join(p, "train"))), None)
assert ROOT, "data root not found"
TRAIN, TEST = os.path.join(ROOT, "train"), os.path.join(ROOT, "test")

def well_ids(folder):
    return sorted({os.path.basename(f).split("__")[0]
                   for f in glob.glob(os.path.join(folder, "*__horizontal_well.csv"))})

train_ids, test_ids = well_ids(TRAIN), well_ids(TEST)
print(f"data root : {ROOT}")
print(f"train wells: {len(train_ids)}   test wells: {len(test_ids)}")

def load_h(folder, wid):  # horizontal well
    return pd.read_csv(os.path.join(folder, f"{wid}__horizontal_well.csv"))
def load_t(folder, wid):  # type well (vertical reference)
    return pd.read_csv(os.path.join(folder, f"{wid}__typewell.csv"))

ex = train_ids[0]   # one reference well, reused throughout the notebook


# %% [markdown]
# ## 1. 🗺️ The whole problem in one picture
# 
# The competition ships a **cross-section image for every training well** (`<id>.png`) — and almost nobody opens them. It is the single most useful artifact in the dataset and the fastest way to *see* what geosteering means. Here is one, and how to read its four panels.
# 

# %% cell 3
import matplotlib.image as mpimg
png = os.path.join(TRAIN, f"{ex}.png")
if os.path.exists(png):
    fig, ax = plt.subplots(figsize=(13, 7.2))
    ax.imshow(mpimg.imread(png)); ax.axis("off")
    ax.set_title(f"Official ROGII cross-section — well {ex[:8]}", pad=6)
    plt.tight_layout(); plt.show()
else:
    print("cross-section image not found for", ex)


# %% [markdown]
# **Reading the four panels** (top-left → right):
# 
# - **Gamma Ray Log** — GR along the bore (`MD`). The only sensor we get on the horizontal.
# - **Well Path Projection** — the bit's path (thick blue) sinking then running flat, drawn against the **formation surfaces** (`ANCC, ASTNU, ASTNL, EGFDU, EGFDL, BUDA`). The red dot is the **prediction start**: everything to its right is what we estimate.
# - **TVT plot** — the horizontal-well GR (black) laid over the **type-well GR** (red) against `TVT`. When the two curves line up, we have located the bit vertically. Dashed lines are formation tops.
# - **TVT plot (last 200 ft)** — a zoom on the same match near the toe.
# 
# Every plot that follows is just one of these panels, pulled apart so you can rebuild it yourself.
# 

# %% [markdown]
# ## 2. The data: two files per well
# 
# Every well ships with **two** tables:
# 
# | File | What it is | Key columns |
# |---|---|---|
# | `*__horizontal_well.csv` | the steered well, measured **along** the bore | `MD` (measured depth), `X,Y,Z` (3-D position), `GR` (gamma ray), `TVT` (target), `TVT_input` (the *known* heel section) |
# | `*__typewell.csv` | a nearby **vertical** reference well | `TVT`, `GR`, `Geology` (formation label) |
# 
# The horizontal well is what we steer; the type well is the **"map"** of GR against depth that we steer *by*.
# 

# %% cell 6
h = load_h(TRAIN, ex); t = load_t(TRAIN, ex)
print("horizontal_well:", h.shape, "->", list(h.columns))
display(h.head(3))
print("\ntype_well:", t.shape, "->", list(t.columns))
display(t.head(3))


# %% [markdown]
# ## 3. 🎯 Picture 1 — the type-well *signature*
# 
# The type well records **GR as a function of vertical depth (TVT)**. Read it bottom-to-top and you get each formation's gamma-ray fingerprint: shales are "hot" (high GR), clean sands are "cold" (low GR).
# 
# **This curve is the reference the driller matches against.** Learn to read it and geosteering stops being magic.
# 

# %% cell 8
t = load_t(TRAIN, ex).dropna(subset=["GR", "TVT"])
fig, ax = plt.subplots(figsize=(4.8, 8))
ax.plot(t["GR"], t["TVT"], color="#1f77b4", lw=1.2)
ax.fill_betweenx(t["TVT"], t["GR"], t["GR"].min(), alpha=0.12, color="#1f77b4")
ax.invert_yaxis()  # depth increases downward
ax.set_xlabel("GR  (gamma ray, API)"); ax.set_ylabel("TVT  (true vertical thickness)")
ax.set_title(f"Type-well GR signature — well {ex[:8]}")
# shade a 'hot' (shale) band as an illustration
hi = t["GR"].quantile(0.80)
ax.axvline(hi, color="#d62728", ls="--", lw=1, alpha=0.7)
ax.text(hi, t["TVT"].min(), "  high GR = shale", color="#d62728", va="top", fontsize=9)
plt.tight_layout(); plt.show()


# %% [markdown]
# ## 4. 🧭 Picture 2 — the drill path through the earth
# 
# Here is the actual **trajectory** of a horizontal well: it drops from vertical, then turns and runs sideways through the target layer. We colour the path by its GR reading — watch how the gamma ray shifts as the bit wanders up and down inside the geology.
# 

# %% cell 10
h = load_h(TRAIN, ex)
fig, ax = plt.subplots(figsize=(10, 4.2))
sc = ax.scatter(h["MD"], h["Z"], c=h["GR"], cmap="viridis", s=6)
ax.set_xlabel("MD  (measured depth along the bore)")
ax.set_ylabel("Z  (true vertical depth)")
ax.set_title(f"Well {ex[:8]} — drill path coloured by GR")
cb = plt.colorbar(sc, ax=ax); cb.set_label("GR")
plt.tight_layout(); plt.show()


# %% [markdown]
# ## 5. 💡 Picture 3 — the geosteering intuition (the "aha")
# 
# Here is the whole game in one plot. On the left, the **type-well GR-vs-TVT signature**. On the right, the **horizontal well's GR** as it is drilled.
# 
# When the horizontal GR rises and falls, it is re-tracing pieces of that signature at whatever TVT the bit currently sits. **Predicting TVT = finding, at each step, which slice of the signature the current GR belongs to** — constrained by the fact that the bit moves smoothly.
# 

# %% cell 12
t = load_t(TRAIN, ex).dropna(subset=["GR","TVT"])
h = load_h(TRAIN, ex).dropna(subset=["GR"])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5), gridspec_kw={"width_ratios":[1,2.2]})
a1.plot(t["GR"], t["TVT"], color="#1f77b4", lw=1.2); a1.invert_yaxis()
a1.set_title("Type-well signature\n(GR vs TVT)"); a1.set_xlabel("GR"); a1.set_ylabel("TVT")
a2.plot(h["MD"], h["GR"], color="#2ca02c", lw=0.9)
a2.set_title("Horizontal GR as drilled (MD)"); a2.set_xlabel("MD"); a2.set_ylabel("GR")
a2.axhline(h["GR"].median(), color="#888", ls=":", lw=1)
fig.suptitle("Same rock, two views — geosteering matches one onto the other", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.show()


# %% [markdown]
# ## 6. 📊 Picture 4 — the target, and what we actually predict
# 
# In the horizontal file, `TVT_input` is filled in for the **heel** (the early, near-vertical part where position is certain) and blank for the rest. **We predict TVT for the blank region** — the long horizontal run.
# 
# Left: for one test well, the known heel vs the region to predict. Right: how TVT is distributed across many training wells.
# 

# %% cell 14
# left: known vs predict region on a test well
tw = test_ids[0]
ht = load_h(TEST, tw)
known = ht["TVT_input"].notna()
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
a1.plot(ht.loc[known, "MD"], ht.loc[known, "TVT_input"], color="#1f77b4", lw=1.6, label="known heel (TVT_input)")
a1.axvspan(ht.loc[~known, "MD"].min(), ht["MD"].max(), color="#d62728", alpha=0.08)
a1.text(ht.loc[~known,"MD"].min(), ht["TVT_input"].min(), "  <- predict this region", color="#d62728", fontsize=9)
a1.set_title(f"Test well {tw[:8]} — known vs to-predict"); a1.set_xlabel("MD"); a1.set_ylabel("TVT"); a1.legend(fontsize=9)

# right: TVT spread across a sample of train wells
vals = []
for wid in train_ids[:120]:
    d = load_h(TRAIN, wid)
    if "TVT" in d: vals.append(d["TVT"].dropna().values)
allv = np.concatenate(vals) if vals else np.array([0])
a2.hist(allv, bins=60, color="#9467bd", alpha=0.85)
a2.set_title("TVT distribution (120 train wells)"); a2.set_xlabel("TVT"); a2.set_ylabel("count")
plt.tight_layout(); plt.show()


# %% [markdown]
# ## 7. 🪨 Picture 5 — the geological layers a well crosses
# 
# Training horizontal wells also carry the modelled **formation surfaces** (`ANCC, ASTNU, ASTNL, EGFDU, EGFDL, BUDA`). Plotting them against MD shows the stack of layers the bit travels through — the structural context behind the GR wiggles.
# 

# %% cell 16
h = load_h(TRAIN, ex)
surf = [c for c in ["ANCC","ASTNU","ASTNL","EGFDU","EGFDL","BUDA"] if c in h]
fig, ax = plt.subplots(figsize=(10, 4.6))
colors = cm.tab10(np.linspace(0, 1, len(surf)))
for c, col in zip(surf, colors):
    ax.plot(h["MD"], h[c], lw=1.3, label=c, color=col)
ax.plot(h["MD"], h["Z"], color="black", lw=1.6, ls="--", label="bit (Z)")
ax.set_xlabel("MD"); ax.set_ylabel("depth"); ax.set_title(f"Well {ex[:8]} — formation surfaces vs the bit path")
ax.legend(ncol=4, fontsize=9)
plt.tight_layout(); plt.show()


# %% [markdown]
# ## 8. 🎨 GR fingerprint by formation
# 
# Why does GR matching work at all? Because each formation sits in a **different GR band**. Pulling the type-well `Geology` labels across many wells, the **distributions differ but substantially overlap** — that *partial* separation is the signal every geosteering method leans on, and also why a single GR reading is never enough to place the bit on its own.
# 

# %% cell 18
from collections import defaultdict
buckets = defaultdict(list)
for wid in train_ids[:150]:
    g = load_t(TRAIN, wid)
    if "Geology" not in g: continue
    g = g.dropna(subset=["GR", "Geology"])
    for name, part in g.groupby("Geology"):
        buckets[name].append(part["GR"].values)

MAIN = ["ANCC", "ASTNU", "ASTNL", "EGFDU", "EGFDL", "BUDA", "OLMOS"]
labels = [f for f in MAIN if f in buckets]
data = [np.concatenate(buckets[f]) for f in labels]

fig, ax = plt.subplots(figsize=(10, 4.6))
bp = ax.boxplot(data, tick_labels=labels, patch_artist=True, showfliers=False,
                medianprops=dict(color="black"))
for patch, c in zip(bp["boxes"], cm.viridis(np.linspace(0.1, 0.9, len(labels)))):
    patch.set_facecolor(c); patch.set_alpha(0.75)
ax.set_ylabel("GR  (gamma ray, API)")
ax.set_title("GR distribution by formation (type wells)")
plt.tight_layout(); plt.show()


# %% [markdown]
# ## 9. 🤖 A strong, humble baseline — and an honest look at what *fails*
# 
# Here is the twist most newcomers miss. The dumbest possible model — **"the bit stays where it last was"** (predict TVT = the last known heel value, and hold it flat across the whole horizontal) — is *surprisingly hard to beat*.
# 
# Let's measure it, then honestly try to beat it. We validate everything with **GroupKFold over wells** (no well leaks across folds), and the metric is RMSE on TVT.
# 

# %% cell 20
from sklearn.model_selection import GroupKFold

def anchored(df):
    d = df.copy().sort_values("MD").reset_index(drop=True)
    k = d["TVT_input"].notna()
    i = d.index[k][-1]                      # last known heel row
    d["anchor"] = d.loc[i, "TVT_input"]     # the value we 'hold'
    d["md_since"] = d["MD"] - d.loc[i, "MD"]
    return d

# collect the horizontal region we would predict, across a sample of wells
N = 250
rows = []
for wid in train_ids[:N]:
    d = load_h(TRAIN, wid)
    if "TVT" not in d: continue
    d = anchored(d)
    m = d["TVT"].notna() & d["TVT_input"].isna()
    if m.sum() < 10: continue
    s = d.loc[m, ["MD","X","Y","Z","GR","TVT","anchor","md_since"]].copy()
    s["well"] = wid
    rows.append(s)
tr = pd.concat(rows, ignore_index=True)

# Baseline 0 -- anchor-hold: predict TVT = anchor (flat)
rmse_hold = float(np.sqrt(np.mean((tr["anchor"] - tr["TVT"]) ** 2)))
print(f"rows {len(tr):,} from {tr['well'].nunique()} wells")
print(f"Baseline 0  anchor-hold   RMSE: {rmse_hold:.3f}")


# %% [markdown]
# ### Does throwing ML at it actually help? (an honest experiment)
# 
# The natural reflex is "just feed GR + geometry to LightGBM." So let's do exactly that — predict the *wander* `TVT − anchor` from local GR shape and trajectory features — and see whether it beats the flat baseline.
# 

# %% cell 22
import lightgbm as lgb

def add_feats(g):
    g = g.sort_values("MD").copy()
    g["gr_rm"]   = g["GR"].rolling(51, min_periods=1, center=True).mean()
    g["gr_rs"]   = g["GR"].rolling(51, min_periods=1, center=True).std().fillna(0)
    g["gr_grad"] = g["GR"].diff().fillna(0)
    g["dz_since"]= g["Z"] - g["Z"].iloc[0]
    return g

trf = pd.concat([add_feats(g).assign(well=wid) for wid, g in tr.groupby("well")],
                ignore_index=True)
trf["y"] = trf["TVT"] - trf["anchor"]
FEATS = ["md_since","dz_since","GR","gr_rm","gr_rs","gr_grad","X","Y","Z"]

gkf = GroupKFold(n_splits=5); oof = np.zeros(len(trf))
for tri, vai in gkf.split(trf, groups=trf["well"]):
    m = lgb.LGBMRegressor(n_estimators=300, learning_rate=0.03, num_leaves=31,
                          min_child_samples=200, subsample=0.8, colsample_bytree=0.8,
                          random_state=42, verbose=-1)
    m.fit(trf.iloc[tri][FEATS], trf.iloc[tri]["y"])
    oof[vai] = m.predict(trf.iloc[vai][FEATS])
rmse_ml = float(np.sqrt(np.mean(((oof + trf["anchor"].values) - trf["TVT"].values) ** 2)))
print(f"Baseline 0  anchor-hold        RMSE: {rmse_hold:.3f}")
print(f"Row-wise LightGBM on GR+geom   RMSE: {rmse_ml:.3f}")
print("-> row-wise ML BEATS anchor-hold:", rmse_ml < rmse_hold)


# %% [markdown]
# **It doesn't beat it.** And that is the single most useful thing to learn about this competition.
# 
# The wander of the bit inside its layer is a **sequential, mean-reverting process**: at any single row, GR alone barely says whether we are 3 ft high or 3 ft low. The information lives in the *sequence* and in the *type-well signature* — not in independent rows. Momentum extrapolation and depth-tracking fail the same way (try them!).
# 
# So we ship the honest baseline — **anchor-hold** — and generate the submission from it.
# 

# %% cell 24
out = []
for wid in test_ids:
    raw = load_h(TEST, wid).copy()
    raw["_row_id"] = np.arange(len(raw))            # original 0-based row index == the submission id suffix
    d = anchored(raw)
    m = d["TVT_input"].isna()                       # predict the blank horizontal region
    if m.sum() == 0: continue
    ids  = [f"{wid}_{int(i)}" for i in d.loc[m, "_row_id"]]
    yhat = d.loc[m, "anchor"].values                # hold the last known TVT
    out.append(pd.DataFrame({"id": ids, "tvt": yhat}))

sub = pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=["id", "tvt"])
ss = pd.read_csv(os.path.join(ROOT, "sample_submission.csv"))
sub = ss[["id"]].merge(sub, on="id", how="left")

# fail loudly instead of masking a broken merge with zeros
assert sub["id"].tolist() == ss["id"].tolist(), "id set/order mismatch vs sample_submission"
assert sub["tvt"].notna().all(), "missing predictions after merge"
assert np.isfinite(sub["tvt"]).all(), "non-finite predictions"

sub.to_csv("submission.csv", index=False)
print("submission.csv:", sub.shape,
      "| tvt range:", round(float(sub["tvt"].min()), 1), "->", round(float(sub["tvt"].max()), 1))
display(sub.head())


# %% [markdown]
# ## Where the real gains are
# 
# The public leaderboard leaders score far below this anchor-hold number — bearing in mind our `16.088` is *out-of-fold on training wells*, not the public test set, so the two are not a like-for-like comparison. What is clear from the experiment above is that **this simple row-wise LightGBM does not capture the gain**. If you want to climb, this is the map:
# 
# - **Align to the type well.** Match the horizontal GR *sequence* to the type-well GR-vs-TVT signature (dynamic-programming / warping alignment). This is the actual geosteering step, and it is where the signal lives.
# - **Model the sequence.** State-space filters, HMM/Viterbi decoding, or TCN/recurrent nets respect the smooth, ordered nature of TVT — unlike independent-row regression.
# - **Per-well calibration.** GR baselines and layer dips vary well to well; normalise before matching.
# - **Ensemble diverse views.** Different alignment/sequence models make different mistakes.
# 
# **Key takeaway:** don't trust a per-row model here — measure against anchor-hold first, and make sure you actually beat it.
# 
# If this saved you a few hours or made geosteering click, **an upvote keeps it visible for the next person** 🙏. Questions very welcome in the comments.
# 
