# %% [markdown]
# # The label is one geologist's drawing
# 
# This competition asks for `TVT` — where the geological layers sit along a horizontal well. The
# organisers' own evaluation slide defines the error as `manualTVT − predictedTVT`, and ROGII's Igor
# Kuvaev put it plainly in the forum: StarSteer "manually projects GR onto TVT scale based on human
# interpretation."
# 
# So the target is not a measurement. It is one professional's reading of ambiguous data.
# 
# That raises a question the leaderboard cannot answer: **how precisely can a manual interpretation be
# pinned down at all?** If two equally competent geologists would have drawn different lines, then
# below some error level a model stops learning geology and starts learning one person's habits.
# 
# Nobody can answer that from the competition data alone, because we only ever see one interpretation
# per well. But there is a public experiment where **176 specialists read simulated rock in cohorts of
# up to 161, each cohort working on one shared subsurface with the ground truth known** — the
# Geosteering World Cup 2021, run by ROGII and published by NORCE/University of Stavanger under
# CC BY 4.0. I reshaped it into tidy tables and attached it here.
# 
# Two data sources, one question. Let me be upfront about what this will not do: **it will not improve
# your score.** There is no gamma-ray-versus-typewell signal in the GWC data. What it gives you is a
# measured sense of what you are fitting, and one aggregation result that does transfer.
# 
# *By [Georgy Mamarin](https://www.kaggle.com/georgymamarin) · attached to
# [ROGII — Wellbore Geology Prediction](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction)*

# %% [markdown]
# **What you'll take away**
# 
# - **What the ROGII target actually is** — measured evidence that the label is a piecewise-linear figure
#   with a human's signature on it, plus the control that shows how far that evidence really goes.
# - **How far trained specialists disagree** when they see the same subsurface with truth known — the
#   spread the leaderboard can never show you.
# - **One check that transfers to your pipeline:** median aggregation beats the mean by 35–38% here, and
#   the crowd beats the median individual by 2.15–2.35× — but the edge lives in the tail, so check your
#   own pool for one first.
# - **What this does *not* license you to claim** — an explicit limits section, because the numbers do not
#   port across as a label-noise figure.
# 
# **Contents**
# 
# 1. [What the ROGII label actually is](#part1)
# 2. [One subsurface, 107 readings of it, known truth](#part2)
# 3. [The one result that transfers](#part3)
# 4. [Design choices and limitations](#limits)
# 5. [Related work, credits and citation](#related)

# %% [markdown]
# ### The attached dataset, in one table
# 
# The Geosteering World Cup 2021 release reshaped into five tidy tables. Everything below runs on these
# plus the competition's own `train/` files.
# 
# | file | one row is | key columns | why it matters here |
# |---|---|---|---|
# | `players.csv` | one participant in one round | `player`, `round`, `scenario`, `peers_in_scenario`, `final_rmse_vs_truth_m` | who interpreted what; **always group by `round` + `scenario`** before comparing |
# | `interpretations.csv` | one interpretation state in time | `player`, `step`, `md_m`, `tvd_shift_m`, `bit_md_m` | the raw record of a specialist changing their mind as logs arrive |
# | `interpretations_final_gridded.csv` | one participant's **final** answer, on a common depth grid | `round`, `scenario`, `player`, `md_m`, `tvd_shift_m`, `truth_tvd_shift_m` | the comparable form — this is what Parts 2 and 3 use |
# | `truth.csv` | the real subsurface per scenario | `round`, `scenario`, `md_m`, `tvd_shift_m` | ground truth; the experiment's whole point |
# | `trajectories.csv` | the well path each player steered | `player`, `md_m`, `tvd_m`, `incl_deg` | steering decisions, kept for reuse (not needed for this notebook's question) |
# 
# The `_m` suffix marks metres, the source unit. The competition works in feet, so anything compared
# across the two is converted (`M2FT`) at the point of use.

# %% cell 3
import glob, os, random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

SEED = 42
random.seed(SEED); np.random.seed(SEED); os.environ["PYTHONHASHSEED"] = str(SEED)
rng = np.random.default_rng(SEED)
M2FT = 3.28084  # the GWC tables are in metres

plt.rcParams.update({
    "figure.dpi": 90, "font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11,
    "axes.grid": True, "grid.alpha": 0.25, "axes.spines.top": False, "axes.spines.right": False,
})
C_TRUTH, C_CROWD, C_EXPERT, C_BEST = "#000000", "#D55E00", "#7F7F7F", "#0072B2"

def find_file(pattern):
    """Kaggle mounts attached sources at different paths, so search recursively."""
    hits = glob.glob(f"/kaggle/input/**/{pattern}", recursive=True)
    if not hits:
        hits = glob.glob(f"**/{pattern}", recursive=True)
    if not hits:
        raise FileNotFoundError(f"{pattern} not found; available: {glob.glob('/kaggle/input/*')}")
    return hits[0]

# ROGII needs the directory CONTAINING train/, not train/ itself
ROGII = os.path.dirname(os.path.dirname(find_file("train/*__horizontal_well.csv")))
GWC = os.path.dirname(find_file("players.csv"))
print("ROGII:", ROGII, "\nGWC  :", GWC)

# %% [markdown]
# <a id="part1"></a>
# ## Part 1 — what the ROGII label actually is
# 
# The organisers have already told us a person draws this line. What Part 1 asks is what that drawing
# looks like as a signal.
# `ANCC` is the depth of a formation top along the well; `TVT = ANCC − Z + b`, so whatever structure
# `ANCC` has, the target inherits.
# 
# These wells drill down, turn, and then run sideways for about a mile. That last stretch is the
# **lateral**, and everything in Part 1 is restricted to it (inclination above 85°, typically the final
# ~5,000 ft of hole). The restriction matters: the slope of `ANCC` against measured depth only reads as
# a geological dip where the hole is horizontal. Through the vertical and build sections the trace bends
# because the *hole* is turning, not because anyone drew a bend there.

# %% cell 5
files = sorted(glob.glob(f"{ROGII}/train/*__horizontal_well.csv"))[:60]

# how quantised is each column? a drawn line reuses a few slopes; an instrument does not.
COLS = ["ANCC", "Z", "X", "GR"]
uniq = {c: [] for c in COLS}
dips, n_segments = [], []
for f in files:
    df = pd.read_csv(f).dropna(subset=["ANCC"])
    if len(df) < 1500:
        continue
    for c in COLS:
        if c in df:
            uniq[c].append(len(np.unique(np.round(np.diff(df[c].values), 4))))

    coarse = df["ANCC"].values[::50]                        # slope on a 50 ft base
    slope = np.diff(coarse) / 50
    Zc, MDc = df["Z"].values[::50], df["MD"].values[::50]
    inc = np.degrees(np.arccos(np.clip(-np.diff(Zc) / np.diff(MDc), -1, 1)))
    lat = inc > 85                     # only in the lateral is MD ~ horizontal displacement,
    dips += list(np.degrees(np.arctan(slope[lat])))        # so only there is this an apparent dip
    sl = slope[lat]
    n_segments.append(int((np.abs(np.diff(sl)) > 0.006).sum()) + 1 if len(sl) > 2 else 0)

dips = np.abs(np.array(dips))
print(f"wells inspected                                 {len(n_segments)}")
print(f"straight segments per well, lateral (median)    {np.median(n_segments):.0f}")
print(f"apparent dip, lateral: median {np.median(dips):.2f} deg, p90 {np.percentile(dips, 90):.2f} deg, "
      f"share below 4 deg {np.mean(dips < 4):.3f}")
print()
print("distinct step values per well (median) - the control:")
for c in COLS:
    if uniq[c]:
        role = {"ANCC": "the label (drawn?)", "Z": "surveyed depth", "X": "surveyed easting",
                "GR": "gamma-ray, a real instrument reading"}[c]
        print(f"   {c:5s} {np.median(uniq[c]):5.0f}   {role}")

# %% cell 6
# two panels, sized for Kaggle page width
demo = pd.read_csv(files[0]).dropna(subset=["ANCC"]).reset_index(drop=True)
inc_demo = np.degrees(np.arccos(np.clip(-np.gradient(demo["Z"].values, demo["MD"].values), -1, 1)))
w = demo.iloc[int(np.argmax(inc_demo > 85)):]   # the lateral only, by the same inc>85 test panel (b)
                                                # uses: while the hole is still building, the trace
                                                # bends for geometric rather than drawn reasons

fig, ax = plt.subplots(1, 2, figsize=(8.2, 3.4))

# (a) the drawing itself: straight segments meeting at control points
ax[0].plot(w["MD"], w["ANCC"], color=C_BEST, lw=1.8)
brk = np.where(np.abs(np.diff(np.diff(w["ANCC"].values[::25]) / 25)) > 0.006)[0]
ax[0].scatter(w["MD"].values[::25][brk + 1], w["ANCC"].values[::25][brk + 1],
              s=26, color=C_CROWD, zorder=5, label="slope changes")
ax[0].set_xlabel("MD (ft)"); ax[0].set_ylabel("ANCC (ft)")
ax[0].set_title("One well, lateral: straight segments, few joints")
ax[0].legend(fontsize=9, loc="best")

# (b) dips: a dense, unremarkable distribution, which is the point
ax[1].hist(dips, bins=np.linspace(0, 8, 40), color=C_EXPERT, edgecolor="white")
ax[1].axvline(4, color=C_CROWD, lw=1.6, ls="--")
ax[1].text(4.15, ax[1].get_ylim()[1] * 0.82,
           f"{np.mean(dips < 4):.0%}\nbelow 4°", fontsize=10, color=C_CROWD, va="top")
ax[1].text(0.98, 0.60, f"tail clipped:\n{np.mean(dips > 8):.1%} past 8°,\nmax {dips.max():.0f}°",
           transform=ax[1].transAxes, ha="right", va="top", fontsize=9, color="#555555")
ax[1].set_xlabel("apparent dip (degrees)")
ax[1].set_ylabel("50 ft segments")
ax[1].set_title("Dips along the lateral stay gentle")
plt.tight_layout(); plt.show()

# %% [markdown]
# **The label behaves like a drawing.** Left: along the lateral it walks in straight segments meeting at
# a handful of joints — 14 in this well, one of the quieter ones; across the 59 wells the median is 24. Right: those segments dip gently, 98% of them under 4°. Roughly 30 distinct
# slope values carry a whole well. That is what a piecewise-linear figure built from a few dozen control
# points looks like.
# 
# **How strongly does that prove a human drew it? Run the control.** The printed table above applies the
# same quantisation test to columns that are *not* interpretations. `ANCC` reuses about 30 distinct step
# values per well — but the surveyed depth `Z` reuses only about 106, and the easting `X` about 62. Those
# are the recorded well path, nobody's reading of anything, and they come out quantised too, because a
# trajectory is itself interpolated between sparse survey stations. The genuine instrument channel, `GR`,
# sits at about 861.
# 
# So `ANCC` is the most quantised column in the file, two to three and a half times more so than the surveyed
# geometry — a signature consistent with a drawn line, not a proof of one. Read it that way.
# 
# *An earlier version of this notebook claimed more.* &nbsp; It reported that every step of `ANCC` lands
# exactly on a 0.01 ft grid, 100% of steps, and argued a physical surface could never do that. The number
# is real. The inference was wrong: `X`, `Y` and `Z` pass the identical test at 1.000, because the CSV
# stores those columns at two decimals. It was measuring the export format, not the cursor. A test that
# fires on the control is not evidence, and this one is left here as the worked example.
# 
# That is worth knowing on its own: predictions shaped like the labels (piecewise-smooth, gently
# dipping) match the process that generated them. But it also sets up the real question — if a person
# drew this line, how differently might another person have drawn it?

# %% [markdown]
# <a id="part2"></a>
# ## Part 2 — one subsurface, 107 readings of it, known truth
# 
# The Geosteering World Cup put specialists in a real-time drilling simulation. Every couple of
# minutes they saw new logs, updated their interpretation, and steered. Everything was recorded, and
# the true geology is known.
# 
# Group by scenario before comparing anything — the two rounds are different geology, and each scenario
# stops at its own depth, so pooling misaligns the shared grid. One structural gift: `cd117866` and
# `d3434a51` are two *disjoint* groups of specialists who read the *same* round-1 subsurface — a
# replication by people, not just by rock.
# 
# The table below counts everyone who took part. Parts 2 and 3 use the slightly smaller subset that
# covered the full shared depth grid — 107 of the 108 in `cd117866`, 56 of 57, 159 of 161 — because a
# partial interpretation cannot be compared position by position.

# %% cell 9
players = pd.read_csv(f"{GWC}/players.csv")
gridded = pd.read_csv(f"{GWC}/interpretations_final_gridded.csv")

(players.groupby(["round", "scenario"])
 .agg(experts=("player", "nunique"),
      median_err_ft=("final_rmse_vs_truth_m", lambda s: s.median() * M2FT))
 .query("experts >= 20").round(1))

# %% cell 10
def scenario_matrix(rnd, scen):
    """One scenario's final interpretations -> (expert x MD) matrix in feet, plus the truth.

    Every participant who covered the shared grid is kept, including the ones who did badly:
    trimming a tail would flatter the crowd and would not match the numbers published on the
    dataset page.
    """
    g = gridded[(gridded["round"] == rnd) & (gridded.scenario == scen)]
    piv = g.pivot_table(index="player", columns="md_m", values="tvd_shift_m")
    cols = piv.columns[piv.notna().mean(axis=0) >= 0.90]
    piv = piv[cols].dropna(axis=0)
    tru = g.groupby("md_m").truth_tvd_shift_m.first().reindex(cols).values * M2FT
    mat = piv.values * M2FT
    err = np.sqrt(np.mean((mat - tru) ** 2, axis=1))
    return cols.values, mat, tru, err

md_grid, experts, tru, err = scenario_matrix(1, "cd117866")
print(f"{experts.shape[0]} experts x {experts.shape[1]} depth positions")
print(f"vs truth (ft): median {np.median(err):.1f} | best {err.min():.1f} | p90 {np.percentile(err, 90):.1f}")

# %% cell 11
fig, ax = plt.subplots(figsize=(8.2, 4.2))
for row in experts:
    ax.plot(md_grid, row, color=C_EXPERT, alpha=0.18, lw=0.8)

crowd = np.median(experts, axis=0)
best = experts[np.argmin(err)]
ax.plot(md_grid, best, color=C_BEST, lw=1.6, ls="--", label=f"best single expert ({err.min():.1f} ft)")
ax.plot(md_grid, crowd, color=C_CROWD, lw=2.2,
        label=f"crowd median ({np.sqrt(np.mean((crowd - tru) ** 2)):.1f} ft)")
ax.plot(md_grid, tru, color=C_TRUTH, lw=2.2, label="ground truth")
ax.plot([], [], color=C_EXPERT, lw=1, label=f"{len(experts)} individual experts")

lo, hi = tru.min() - 130, tru.max() + 130
off = int((experts.min(axis=1) < lo).sum() + (experts.max(axis=1) > hi).sum())
ax.set_ylim(lo, hi)
ax.set_xlabel("measured depth along well, m")
ax.set_ylabel("geology position (TVD shift), ft")
ax.set_title(f"One subsurface, {len(experts)} final interpretations of it")
ax.legend(loc="lower left", fontsize=9, framealpha=0.9, ncol=2)
if off:
    ax.text(0.99, 0.02, f"{off} experts run off-scale", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=9, color=C_EXPERT)
plt.tight_layout(); plt.show()

# %% [markdown]
# Every grey line is a trained specialist's final answer on data they saw in full. They diverge by tens
# of feet, and the disagreement is structured rather than random — people commit to a reading and carry
# it along the well. Ten of them run so far off the chart they are counted in the corner rather than drawn.
# 
# The orange line is simply the median of the grey ones at each position. It beats all but ten of the
# 107 individuals who drew the grey ones.
# 
# With one exception, and it is the interesting one. The fault at 4,650 m, where the geology jumps, is
# exactly where the crowd median fails worst — it misses by 43 ft there, against a median miss of under
# 2 ft along the rest of the well. Averaging opinions smooths a discontinuity that a single decisive
# reader could have called correctly. Consensus buys you accuracy in the ordinary stretches and costs
# you at the break.

# %% [markdown]
# <a id="part3"></a>
# ## Part 3 — the one result that transfers
# 
# Sample *k* experts at random, take their median, measure against truth, repeat.

# %% cell 14
def consensus_curve(mat, tru, ks=(1, 2, 3, 5, 10, 20, 40), draws=300):
    out = []
    for k in ks:
        if k > len(mat):
            break
        vals = [np.sqrt(np.mean((np.median(mat[rng.choice(len(mat), k, replace=False)], axis=0) - tru) ** 2))
                for _ in range(draws)]
        out.append((k, float(np.mean(vals))))
    return out

curves = {}
for rnd, scen in [(1, "cd117866"), (1, "d3434a51"), (2, "7d08e523")]:
    _, mat, t, e = scenario_matrix(rnd, scen)
    curves[f"round{rnd}/{scen}"] = dict(
        curve=consensus_curve(mat, t), median_expert=float(np.median(e)),
        crowd_median=float(np.sqrt(np.mean((np.median(mat, axis=0) - t) ** 2))),
        crowd_mean=float(np.sqrt(np.mean((mat.mean(axis=0) - t) ** 2))),
    )

summary = pd.DataFrame([
    {"scenario": k,
     "median expert, ft": round(v["median_expert"], 1),
     "crowd MEDIAN, ft": round(v["crowd_median"], 2),
     "crowd mean, ft": round(v["crowd_mean"], 2),
     "crowd gain": f"{v['median_expert'] / v['crowd_median']:.2f}x",
     "median beats mean by": f"{100 * (1 - v['crowd_median'] / v['crowd_mean']):.0f}%"}
    for k, v in curves.items()
])
# Kaggle renders tables smaller than body text, so set the size explicitly
summary.style.hide(axis="index").set_properties(**{"font-size": "13px"}).set_table_styles(
    [{"selector": "th", "props": [("font-size", "13px"), ("text-align", "left")]}]
)

# %% [markdown]
# **Both columns on the right are the finding.** The crowd gain holds at ~2.2× across three different
# subsurfaces with different participant counts — aggregation buys a fixed multiple, not something that
# scales with how hard the problem is. And the median beats the mean every time: outlier interpreters are
# always present, and a mean walks toward them.
# 
# That second column is the one line of this notebook that transfers directly to a modelling pipeline.
# If you combine diverse estimators with a plain weighted average — which most blending code does —
# switching to a median is the cheapest available change. One boundary, measured here: the median's
# edge is the tail's doing. Trim these cohorts to their eleven most closely agreeing members and the
# mean wins two of three — so check whether your pool has a tail before you switch. A handful of
# comparably tuned models usually doesn't.

# %% cell 16
fig, ax = plt.subplots(figsize=(8.2, 4.0))
for (name, v), m in zip(curves.items(), ["o", "s", "^"]):
    ks = [k for k, _ in v["curve"]]
    ax.plot(ks, [x for _, x in v["curve"]], marker=m, lw=1.8, label=name)

ax.set_xscale("log"); ax.set_xticks([1, 2, 3, 5, 10, 20, 40])
ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
ax.set_xlabel("number of experts aggregated (log scale)")
ax.set_ylabel("RMSE of the consensus vs truth, ft")
ax.set_title("Returns to ensemble size decay, but never flatten")
ax.legend(fontsize=9)
plt.tight_layout(); plt.show()

# %% [markdown]
# Around 90% of the achievable gain arrives by ten members; the remainder costs four times as many people.
# The curve bends hard but does not go flat.
# 
# I first read this as full saturation around ten to twenty, on a narrower depth window, and it did not
# survive a wider one. Worth re-checking on your own slice before designing around it.

# %% [markdown]
# <a id="limits"></a>
# ## Design choices and limitations
# 
# **Read this before quoting any number from here.** The GWC figures are an *upper bound* on
# interpretation noise, not this competition's label noise. Anyone quoting "the label noise here is
# 9.5 feet" from this notebook is over-reading it.
# 
# | what you might take from this | does it transfer to ROGII? | why |
# |---|---|---|
# | the **feet** — "labels are ±9.5 ft noisy" | **No** | GWC has ~177 ft of relief over kilometres; the ROGII evaluation zone is a much narrower band, and GWC was timed at ~2 min per decision against unhurried interpretation here |
# | **the target is a human drawing** | **Yes, from the organisers** | ROGII say so outright; Part 1 adds only the *shape* — a piecewise-linear line of a few dozen segments, the most quantised column in the file. So an irreducible floor exists — wherever it sits. Past it you are learning one interpreter's habits, and the private wells may not share them |
# | **median beats mean** by 35–38% | **Yes, when the pool has a tail** | held for two disjoint groups on one subsurface and again on a second, easier one; but the edge comes from a 579 ft worst reading — trim to the eleven most-agreeing members and the mean wins two of three. Check for a tail before switching |
# | **more members keep helping** | **Yes, weakly** | the curve bends hard but never flattens — worth knowing before you cap an ensemble at ten |
# 
# **The honest summary:** this dataset will not move your score. It tells you what you are fitting, and
# suggests one change to how you combine estimators.

# %% [markdown]
# <a id="related"></a>
# ## Related work
# 
# *The competition this is attached to* — [ROGII — Wellbore Geology
# Prediction](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction).
# 
# *The same researchers, a sharper design* — the [Geology Forecast
# Challenge](https://www.kaggle.com/competitions/geology-forecast-challenge-open) comes from the NORCE
# group who published the GWC data. It asks for the layer sequence ahead of the bit and requires **ten
# realisations** rather than one prediction, scored by a Gaussian-mixture likelihood. That choice, by the
# people who study this problem for a living, is its own argument for treating the answer as a
# distribution.
# 
# *Where the public methods plateau here* — I mapped that in [Fork the ruler, not the
# model](https://www.kaggle.com/code/georgymamarin/fork-the-ruler-not-the-model): same instinct, applied
# to the competition's own data instead of a controlled experiment.
# 
# ## Credits
# 
# **The experiment and the data are not mine.** They belong to S. Alyaev, Y. Cheraghi, I. Kuvaev,
# S. Clark and A. Zhuravlev at NORCE / University of Stavanger, who ran the Geosteering World Cup and
# published the record openly. My contribution is reshaping it into tidy tables and asking one question
# of it. Thanks also to ROGII for running the competition, and to Igor Kuvaev, whose forum answer about
# how `TVT` is produced is what started this.
# 
# **If you take one thing:** check your pool for a tail, then try the median instead of the mean the
# next time you blend, and tell me whether it moved anything. If you find a scenario where it does
# not, I would like to see it — the comments are open, and I will run it.

# %% [markdown]
# ## Citation
# 
# GWC data: © 2025 S. Alyaev, Y. Cheraghi, I. Kuvaev, S. Clark, A. Zhuravlev, **CC BY 4.0** —
# [Zenodo 10.5281/zenodo.15190734](https://doi.org/10.5281/zenodo.15190734),
# [source repository](https://github.com/geosteering-no/10000-geosteering-interpretations-and-decisions).
# 
# Paper: Cheraghi Y., Alyaev S., Bratvold R.B., Hong A., Kuvaev I., Clark S., Zhuravlev A. (2025).
# *Analyzing expert decision-making in geosteering: statistical insights from a large-scale controlled
# experiment.* Applied Computing and Geosciences.
# [doi:10.1016/j.acags.2025.100237](https://doi.org/10.1016/j.acags.2025.100237)
# 
# Please cite the original authors — that is the licence condition. The experiment and the data are
# theirs; I reshaped it into tidy tables.
