# %% [markdown]
# # ROGII Wellbore Geology - a visual EDA
# 
# Drilling a horizontal well is navigating underground without a map. This competition asks us to
# predict **TVT** (True Vertical Thickness = the geological position of the bit) along the lateral
# section of a well, in the **evaluation zone** where it is unknown.
# 
# This notebook makes the problem concrete and visual:
# 1. What a single well actually looks like (trajectory, gamma-ray log, TVT).
# 2. What the **evaluation zone** is and exactly which rows we must predict.
# 3. The **typewell** - the vertical reference log used for geological correlation.
# 4. Dataset-level structure (well lengths, eval-zone sizes, geology labels).
# 5. An honest note on the train/test overlap that the leaderboard is exploiting.
# 
# If it helps you get started, an upvote is appreciated.

# %% cell 1
import os, glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")

CANDIDATES = ["/kaggle/input/competitions/rogii-wellbore-geology-prediction",
              "/kaggle/input/rogii-wellbore-geology-prediction", "data/rogii"]
BASE = next((p for p in CANDIDATES if os.path.isdir(os.path.join(p, "train"))), None)
if BASE is None:
    hits = glob.glob("/kaggle/input/**/train/", recursive=True)
    BASE = os.path.dirname(hits[0].rstrip("/")) if hits else CANDIDATES[0]
TRAIN = os.path.join(BASE, "train")

def well_ids(folder):
    return sorted({os.path.basename(f).split("__")[0]
                   for f in glob.glob(os.path.join(folder, "*__horizontal_well.csv"))})

train_ids = well_ids(TRAIN)
print("train wells:", len(train_ids))

WELL = train_ids[0]
hw = pd.read_csv(os.path.join(TRAIN, f"{WELL}__horizontal_well.csv"))
tw = pd.read_csv(os.path.join(TRAIN, f"{WELL}__typewell.csv"))
print("horizontal_well columns:", list(hw.columns))
print("typewell columns      :", list(tw.columns))
hw.head(3)

# %% [markdown]
# ## 1. The well trajectory and the evaluation zone
# 
# A horizontal well starts vertical, then bends and runs laterally through the target formation.
# `Z` is true vertical depth (below sea level); `MD` is measured depth along the hole. The
# **evaluation zone** is exactly the set of rows where `TVT_input` is `NaN` - that is what we predict.
# Here it is a single contiguous segment along the lateral.

# %% cell 3
eval_mask = hw["TVT_input"].isna()
print(f"well {WELL}: {len(hw)} rows | eval-zone rows: {int(eval_mask.sum())} "
      f"({eval_mask.mean()*100:.1f}%)")

fig, ax = plt.subplots(figsize=(13, 6))
ax.plot(hw["MD"], hw["Z"], color="#333333", lw=2, label="well path (TVD)")
ax.scatter(hw.loc[eval_mask, "MD"], hw.loc[eval_mask, "Z"], s=8, color="#E4572E",
           label="evaluation zone", zorder=3)
ax.set_xlabel("Measured Depth MD (ft)")
ax.set_ylabel("True Vertical Depth Z (ft)")
ax.set_title(f"Well {WELL} - trajectory, evaluation zone highlighted")
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 2. The gamma-ray log along the well
# 
# Gamma ray (`GR`) measures natural radioactivity and is the main signal for telling rock layers
# apart. This is the curve geologists read to steer the bit. The shaded band is the evaluation zone.

# %% cell 5
eval_md = hw.loc[eval_mask, "MD"]
fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(hw["MD"], hw["GR"], color="#2E86AB", lw=1)
if len(eval_md):
    ax.axvspan(eval_md.min(), eval_md.max(), color="#E4572E", alpha=0.12, label="evaluation zone")
ax.set_xlabel("Measured Depth MD (ft)")
ax.set_ylabel("Gamma Ray (API)")
ax.set_title(f"Well {WELL} - gamma-ray log")
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 3. The target: TVT (geological position)
# 
# `TVT` is the manually interpreted geological position for each foot of the lateral. In training it
# is fully known; in test it is hidden in the evaluation zone. Note how TVT is smooth and structured -
# it is not noise, it follows the geology. That is what makes a physically-meaningful model possible.

# %% cell 7
fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(hw["MD"], hw["TVT"], color="#43AA8B", lw=2, label="TVT (known in train)")
if len(eval_md):
    ax.axvspan(eval_md.min(), eval_md.max(), color="#E4572E", alpha=0.12,
               label="eval zone (hidden in test)")
ax.set_xlabel("Measured Depth MD (ft)")
ax.set_ylabel("TVT (ft)")
ax.set_title(f"Well {WELL} - target TVT along the well")
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 4. The typewell - vertical reference log
# 
# The typewell is a vertical GR profile indexed by TVT, with a `Geology` label per depth. Correlating
# the horizontal GR against this reference is how you place the bit in the right layer. Colored bands
# are geological units.

# %% cell 9
tw_valid = tw.dropna(subset=["GR"]).copy()
geols = [g for g in tw["Geology"].dropna().unique()]
cmap = {g: cm.tab10(i % 10) for i, g in enumerate(geols)}

fig, ax = plt.subplots(figsize=(6, 9))
ax.plot(tw_valid["GR"], tw_valid["TVT"], color="#2E86AB", lw=1)
for g in geols:
    seg = tw[tw["Geology"] == g]
    if len(seg):
        ax.axhspan(seg["TVT"].min(), seg["TVT"].max(), color=cmap[g], alpha=0.20)
ax.invert_yaxis()
ax.set_xlabel("Gamma Ray (API)")
ax.set_ylabel("TVT (ft)")
ax.set_title(f"Typewell {WELL}\n({len(geols)} geology units)")
handles = [plt.Rectangle((0, 0), 1, 1, color=cmap[g], alpha=0.5) for g in geols]
ax.legend(handles, geols, fontsize=9, loc="upper right", title="Geology")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 5. Dataset-level structure
# 
# How long are wells, how big is the evaluation zone, and how many geology units appear? Computed on a
# random sample of wells for speed (stated so the numbers are honest).

# %% cell 11
rng = np.random.default_rng(42)
sample_ids = list(rng.choice(train_ids, size=min(200, len(train_ids)), replace=False))
lengths, eval_frac, n_geol = [], [], []
for wid in sample_ids:
    h = pd.read_csv(os.path.join(TRAIN, f"{wid}__horizontal_well.csv"), usecols=["TVT_input"])
    lengths.append(len(h))
    eval_frac.append(h["TVT_input"].isna().mean())
    t = pd.read_csv(os.path.join(TRAIN, f"{wid}__typewell.csv"), usecols=["Geology"])
    n_geol.append(t["Geology"].dropna().nunique())

fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
sns.histplot(lengths, bins=30, color="#2E86AB", ax=axes[0]); axes[0].set_title("Well length (rows)")
sns.histplot(np.array(eval_frac) * 100, bins=30, color="#E4572E", ax=axes[1]); axes[1].set_title("Eval-zone size (% of well)")
sns.histplot(n_geol, bins=range(1, max(n_geol) + 2), color="#43AA8B", ax=axes[2]); axes[2].set_title("Geology units per typewell")
plt.suptitle(f"Dataset structure (sample of {len(sample_ids)} wells)", y=1.03)
plt.tight_layout()
plt.show()

print(f"median well length : {int(np.median(lengths))} rows")
print(f"median eval-zone   : {np.median(eval_frac)*100:.1f}% of the well")
print(f"median geology units: {int(np.median(n_geol))}")

# %% [markdown]
# ## 6. Honest note on train/test overlap
# 
# The public example `test/` wells share their identifiers and logs with training wells, and the
# public leaderboard scores dropped sharply (roughly 7 -> ~5.3) once people matched a test well to its
# training twin by the GR signature and copied the known TVT. That matching is allowed (the data is
# provided), but it is a data-overlap effect, not a geological model - and the ROGII Working-Note award
# explicitly rewards physically-meaningful solutions. A robust approach therefore combines:
# 
# - **correlation / matching** where a reliable twin exists, and
# - **a genuine model** of TVT from MD, Z and GR for everything else.
# 
# The next notebook builds an honest, cross-validated baseline for the modelling part. If this EDA
# helped you understand the data, an upvote is appreciated.
