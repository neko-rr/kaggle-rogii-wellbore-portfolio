# %% [markdown]
# # ROGII - Wellbore Geology Prediction EDA
# 
# This notebook is a starter exploration for the **ROGII - Wellbore Geology Prediction** Kaggle competition.
# 
# The competition asks us to predict **TVT** (`True Vertical Thickness`) for the hidden/evaluation part of each horizontal well. Each well is a sequence along measured depth (`MD`). Before the prediction start, Kaggle provides `TVT_input`, which is a copy of the known target. After the prediction start, `TVT_input` becomes missing and the model must infer the missing geological position.
# 
# The main data sources are:
# 
# - Horizontal well trajectory and log data: `MD`, `X`, `Y`, `Z`, `GR`, `TVT_input`, and in training also `TVT` plus geological surface columns.
# - A paired vertical reference log, called a **Typewell**, with `TVT` and `GR` that helps correlate gamma ray signatures.
# - Optional PNG visualizations for training wells.
# 
# The evaluation metric is RMSE on predicted `tvt` values.

# %% [markdown]
# ## 1. Setup
# 
# The path helper below works both in a Kaggle Notebook and in a local extracted copy of the competition data. It expects the competition files to contain `train/`, `test/`, and `sample_submission.csv`.

# %% cell 2
from pathlib import Path
from collections import Counter
import math
import os
import re
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, Markdown

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", 100)
pd.set_option("display.max_colwidth", 120)

try:
    import seaborn as sns
    sns.set_theme(style="whitegrid")
    HAS_SEABORN = True
except Exception:
    HAS_SEABORN = False
    plt.style.use("ggplot")

RANDOM_STATE = 42

# %% cell 3
def find_data_root():
    candidates = [
        Path("/kaggle/input/competitions/rogii-wellbore-geology-prediction"),
        Path.cwd(),
    ]

    # Also check parents of the current working directory.
    candidates.extend(Path.cwd().parents)

    for root in candidates:
        if (root / "train").is_dir() and (root / "sample_submission.csv").is_file():
            return root.resolve()

    raise FileNotFoundError(
        "Could not find competition data. Expected train/, test/, and sample_submission.csv."
    )

DATA_ROOT = find_data_root()
TRAIN_DIR = DATA_ROOT / "train"
TEST_DIR = DATA_ROOT / "test"
SAMPLE_SUB_PATH = DATA_ROOT / "sample_submission.csv"

print(f"DATA_ROOT = {DATA_ROOT}")
print(f"TRAIN_DIR = {TRAIN_DIR}")
print(f"TEST_DIR  = {TEST_DIR}")

# %% [markdown]
# ## 2. Task Deck Notes
# 
# The competition includes `AI_wellbore_geology_prediction_task_en.pptx`, which is worth reading before modeling. The key points from the deck are:
# 
# - The goal is to calculate `TVT` beyond the prediction start using horizontal-well `XYZ` and `GR`, plus Typewell `TVT` and `GR`.
# - Horizontal `GR` should be correlated against Typewell `GR` on the TVT scale.
# - `TVT` is not guaranteed to move in one direction. It can increase, decrease, or stay nearly constant along the horizontal well.
# - The horizontal well's known segment before prediction start can be very valuable, because its `GR` may align better with the later lateral than the Typewell alone.
# - Neighboring wells can help because geological dip often behaves similarly in nearby wells.
# - Prediction quality is measured by RMSE of manual `TVT` minus predicted `TVT` over the hidden points.
# 
# The next cell extracts the deck text so the notebook remains self-contained.

# %% cell 5
from zipfile import ZipFile
import xml.etree.ElementTree as ET

PPTX_PATH = DATA_ROOT / "AI_wellbore_geology_prediction_task_en.pptx"

def extract_pptx_text(pptx_path):
    if not pptx_path.exists():
        return pd.DataFrame(columns=["slide", "text"])

    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    rows = []
    with ZipFile(pptx_path) as zf:
        slide_files = sorted(
            [name for name in zf.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")],
            key=lambda name: int(name.rsplit("slide", 1)[1].split(".xml")[0]),
        )
        for slide_number, name in enumerate(slide_files, start=1):
            root = ET.fromstring(zf.read(name))
            pieces = []
            for node in root.findall(".//a:t", ns):
                text = " ".join((node.text or "").split())
                if text and (not pieces or pieces[-1] != text):
                    pieces.append(text)
            rows.append({"slide": slide_number, "text": " | ".join(pieces)})
    return pd.DataFrame(rows)

pptx_text = extract_pptx_text(PPTX_PATH)
print(f"PPTX path: {PPTX_PATH}")
print(f"Slides extracted: {len(pptx_text)}")

important_slides = [2, 3, 4, 5, 6, 7, 9, 12, 13, 14]
display(pptx_text[pptx_text["slide"].isin(important_slides)])

# %% [markdown]
# ## 3. Data Layout
# 
# Each well is identified by an 8-character hash, for example `000d7d20`.
# 
# Training files:
# 
# - `{WELLNAME}__horizontal_well.csv`: trajectory, logs, training target, known `TVT_input`, and formation-surface columns.
# - `{WELLNAME}__typewell.csv`: vertical reference log for correlation.
# - `{WELLNAME}.png`: visualization of the well path and geological cross-section.
# 
# Test files:
# 
# - `{WELLNAME}__horizontal_well.csv`: trajectory/log data and `TVT_input`; the target zone is hidden.
# - `{WELLNAME}__typewell.csv`: paired vertical reference log.
# 
# The visible `test/` folder contains example data. In the official scoring run, Kaggle replaces it with the hidden test set.

# %% cell 7
def well_id_from_path(path):
    name = Path(path).name
    if "__" in name:
        return name.split("__", 1)[0]
    return name.split(".", 1)[0]

train_horizontal_paths = sorted(TRAIN_DIR.glob("*__horizontal_well.csv"))
train_typewell_paths = sorted(TRAIN_DIR.glob("*__typewell.csv"))
train_png_paths = sorted(TRAIN_DIR.glob("*.png"))
test_horizontal_paths = sorted(TEST_DIR.glob("*__horizontal_well.csv")) if TEST_DIR.exists() else []
test_typewell_paths = sorted(TEST_DIR.glob("*__typewell.csv")) if TEST_DIR.exists() else []

file_summary = pd.DataFrame([
    {"split": "train", "kind": "horizontal_well.csv", "files": len(train_horizontal_paths)},
    {"split": "train", "kind": "typewell.csv", "files": len(train_typewell_paths)},
    {"split": "train", "kind": "png", "files": len(train_png_paths)},
    {"split": "test", "kind": "horizontal_well.csv", "files": len(test_horizontal_paths)},
    {"split": "test", "kind": "typewell.csv", "files": len(test_typewell_paths)},
    {"split": "root", "kind": "sample_submission.csv", "files": int(SAMPLE_SUB_PATH.exists())},
])
display(file_summary)

print("First few training horizontal files:")
for path in train_horizontal_paths[:5]:
    print(" ", path.relative_to(DATA_ROOT))

# %% [markdown]
# ## 4. Load a Few Wells
# 
# The next helpers load a horizontal well and its paired Typewell. For a training well, the horizontal file contains the true `TVT`. In test, the hidden target is not available.

# %% cell 9
def horizontal_path(well_id, split="train"):
    base = TRAIN_DIR if split == "train" else TEST_DIR
    return base / f"{well_id}__horizontal_well.csv"

def typewell_path(well_id, split="train"):
    base = TRAIN_DIR if split == "train" else TEST_DIR
    return base / f"{well_id}__typewell.csv"

def png_path(well_id):
    return TRAIN_DIR / f"{well_id}.png"

def load_horizontal(well_id, split="train"):
    return pd.read_csv(horizontal_path(well_id, split))

def load_typewell(well_id, split="train"):
    return pd.read_csv(typewell_path(well_id, split))

available_train_wells = sorted(well_id_from_path(p) for p in train_horizontal_paths)
preferred_wells = ["000d7d20", "00bbac68", "00e12e8b", "015fe0d2", "01869cd4"]
sample_wells = [w for w in preferred_wells if w in available_train_wells]

if len(sample_wells) < 3:
    sample_wells += [w for w in available_train_wells if w not in sample_wells][: 3 - len(sample_wells)]

sample_wells = sample_wells[:3]
print("Sample wells:", sample_wells)

# %% cell 10
for well_id in sample_wells:
    horizontal = load_horizontal(well_id, split="train")
    typewell = load_typewell(well_id, split="train")

    display(Markdown(f"### Well `{well_id}`"))
    print(f"Horizontal shape: {horizontal.shape}")
    print(f"Typewell shape:   {typewell.shape}")
    print("Horizontal columns:", list(horizontal.columns))
    print("Typewell columns:  ", list(typewell.columns))

    display(Markdown("Horizontal well head:"))
    display(horizontal.head())
    display(Markdown("Typewell head:"))
    display(typewell.head())

# %% [markdown]
# ## 5. Training Visualizations
# 
# The PNGs are useful for building intuition. They show a visual summary of the well path and geological cross-section for training examples.

# %% cell 12
if train_png_paths:
    fig, axes = plt.subplots(1, len(sample_wells), figsize=(5.5 * len(sample_wells), 4), constrained_layout=True)
    if len(sample_wells) == 1:
        axes = [axes]

    for ax, well_id in zip(axes, sample_wells):
        path = png_path(well_id)
        if path.exists():
            img = plt.imread(path)
            ax.imshow(img)
            ax.set_title(well_id)
            ax.axis("off")
        else:
            ax.text(0.5, 0.5, f"No PNG for {well_id}", ha="center", va="center")
            ax.axis("off")
    plt.show()
else:
    print("No training PNG files found.")

# %% [markdown]
# ## 6. How `TVT_input` Defines the Prediction Start
# 
# `TVT_input` is known before the prediction start and missing after it. In training, the true `TVT` remains available, so we can inspect the hidden/evaluation zone directly.
# 
# A good model should use the known TVT path, the horizontal well gamma ray (`GR`), the Typewell gamma ray, and spatial trajectory to infer the missing continuation.

# %% cell 14
def first_missing_index(series):
    mask = series.isna()
    if not mask.any():
        return None
    return int(np.flatnonzero(mask.to_numpy())[0])

def plot_well_overview(well_id, split="train"):
    horizontal = load_horizontal(well_id, split=split)
    typewell = load_typewell(well_id, split=split)

    fig, axes = plt.subplots(1, 3, figsize=(18, 4.5), constrained_layout=True)

    # 1. Target path and provided input target.
    ax = axes[0]
    if "TVT" in horizontal.columns:
        ax.plot(horizontal["MD"], horizontal["TVT"], label="TVT target", lw=1.4)
    if "TVT_input" in horizontal.columns:
        ax.plot(horizontal["MD"], horizontal["TVT_input"], label="TVT_input", lw=1.1, alpha=0.9)
        ps_idx = first_missing_index(horizontal["TVT_input"])
        if ps_idx is not None:
            ax.axvline(horizontal.loc[ps_idx, "MD"], color="crimson", ls="--", lw=1.2, label="Prediction start")
    ax.set_title(f"{well_id}: TVT along horizontal well")
    ax.set_xlabel("MD (ft)")
    ax.set_ylabel("TVT (ft)")
    ax.legend(loc="best")

    # 2. Horizontal well gamma ray along measured depth.
    ax = axes[1]
    if "GR" in horizontal.columns:
        ax.plot(horizontal["MD"], horizontal["GR"], color="tab:green", lw=0.8)
    if "TVT_input" in horizontal.columns:
        ps_idx = first_missing_index(horizontal["TVT_input"])
        if ps_idx is not None:
            ax.axvline(horizontal.loc[ps_idx, "MD"], color="crimson", ls="--", lw=1.2)
    ax.set_title("Horizontal GR log")
    ax.set_xlabel("MD (ft)")
    ax.set_ylabel("GR (API)")

    # 3. Typewell GR vs TVT with known horizontal GR projected to TVT_input.
    ax = axes[2]
    if {"GR", "TVT"}.issubset(typewell.columns):
        ax.plot(typewell["GR"], typewell["TVT"], color="black", lw=1.1, label="Typewell GR")
    if {"GR", "TVT_input"}.issubset(horizontal.columns):
        known = horizontal[horizontal["TVT_input"].notna() & horizontal["GR"].notna()]
        ax.scatter(known["GR"], known["TVT_input"], s=8, alpha=0.35, color="tab:green", label="Known horizontal GR")
    ax.invert_yaxis()
    ax.set_title("GR signatures on TVT scale")
    ax.set_xlabel("GR (API)")
    ax.set_ylabel("TVT (ft, inverted)")
    ax.legend(loc="best")

    plt.show()

for well_id in sample_wells:
    plot_well_overview(well_id, split="train")

# %% [markdown]
# ## 7. TVT Direction: Increasing, Decreasing, and Flat Segments
# 
# The task deck emphasizes that the same horizontal well can move up, down, or remain nearly flat in TVT. This matters because a model that assumes TVT always increases with `MD` will fail on wells where the lateral crosses dipping geology in the opposite direction.
# 
# The next cell samples training wells and looks at `dTVT / dMD` to show how often the target is increasing, decreasing, or nearly flat.

# %% cell 16
slope_rows = []

for i, path in enumerate(train_horizontal_paths):
    df = pd.read_csv(path, usecols=["MD", "TVT"])
    dmd = df["MD"].diff()
    dtvt = df["TVT"].diff()
    slope = (dtvt / dmd).replace([np.inf, -np.inf], np.nan).dropna()

    if len(slope) > 500:
        slope = slope.sample(500, random_state=RANDOM_STATE + i)

    slope_rows.append(pd.DataFrame({"well_id": well_id_from_path(path), "dTVT_dMD": slope}))

slope_df = pd.concat(slope_rows, ignore_index=True)
flat_eps = 0.02
slope_df["direction"] = np.select(
    [slope_df["dTVT_dMD"] > flat_eps, slope_df["dTVT_dMD"] < -flat_eps],
    ["increasing", "decreasing"],
    default="nearly flat",
)

display(slope_df["direction"].value_counts(normalize=True).mul(100).rename("percent").reset_index())

fig, axes = plt.subplots(1, 2, figsize=(13, 4), constrained_layout=True)
axes[0].hist(slope_df["dTVT_dMD"].clip(-2, 2), bins=80, color="teal", edgecolor="white")
axes[0].axvline(0, color="black", lw=1)
axes[0].set_title("Sampled dTVT / dMD distribution, clipped to [-2, 2]")
axes[0].set_xlabel("dTVT / dMD")
axes[0].set_ylabel("Sampled row count")

slope_df["direction"].value_counts().reindex(["increasing", "nearly flat", "decreasing"]).plot(
    kind="bar", ax=axes[1], color=["seagreen", "gray", "crimson"]
)
axes[1].set_title("Direction classes")
axes[1].set_xlabel("")
axes[1].set_ylabel("Sampled row count")
axes[1].tick_params(axis="x", rotation=0)
plt.show()

# %% [markdown]
# ## 8. Dataset-Level Well Summary
# 
# The next cells summarize all training horizontal wells without concatenating the full dataset into one huge table. Each row of `train_summary` corresponds to one well.

# %% cell 18
def summarize_horizontal_file(path):
    df = pd.read_csv(path)
    well_id = well_id_from_path(path)

    result = {
        "well_id": well_id,
        "rows": len(df),
        "columns": len(df.columns),
    }

    for col in ["MD", "X", "Y", "Z", "TVT", "GR"]:
        if col in df.columns:
            result[f"{col}_min"] = df[col].min(skipna=True)
            result[f"{col}_max"] = df[col].max(skipna=True)
            result[f"{col}_range"] = result[f"{col}_max"] - result[f"{col}_min"]
            result[f"{col}_mean"] = df[col].mean(skipna=True)
            result[f"{col}_missing_pct"] = 100 * df[col].isna().mean()

    if "TVT_input" in df.columns:
        result["tvt_input_known_rows"] = int(df["TVT_input"].notna().sum())
        result["evaluation_rows"] = int(df["TVT_input"].isna().sum())
        result["evaluation_pct"] = 100 * df["TVT_input"].isna().mean()
        ps_idx = first_missing_index(df["TVT_input"])
        result["prediction_start_index"] = ps_idx
        result["prediction_start_md"] = np.nan if ps_idx is None else df.loc[ps_idx, "MD"]

    return result

train_summary = pd.DataFrame([summarize_horizontal_file(path) for path in train_horizontal_paths])
print(train_summary.shape)
display(train_summary.head())

# %% cell 19
summary_cols = [
    "rows",
    "MD_range",
    "TVT_range",
    "GR_missing_pct",
    "tvt_input_known_rows",
    "evaluation_rows",
    "evaluation_pct",
]
summary_cols = [c for c in summary_cols if c in train_summary.columns]

display(train_summary[summary_cols].describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).T)

# %% cell 20
fig, axes = plt.subplots(2, 2, figsize=(14, 9), constrained_layout=True)
axes = axes.ravel()

plots = [
    ("rows", "Rows per horizontal well", "rows"),
    ("evaluation_rows", "Rows to predict per training well", "rows"),
    ("GR_missing_pct", "Horizontal GR missing rate", "% missing"),
    ("TVT_range", "TVT range per well", "ft"),
]

for ax, (col, title, xlabel) in zip(axes, plots):
    if col in train_summary.columns:
        ax.hist(train_summary[col].dropna(), bins=40, color="steelblue", edgecolor="white")
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Well count")
    else:
        ax.axis("off")

plt.show()

# %% [markdown]
# ## 9. Map View: Offset-Well Context
# 
# The task deck also notes that neighboring wells can be useful because geological dip often behaves similarly over short distances. A simple first check is to plot well trajectories in `X`/`Y` space and identify nearby offsets.

# %% cell 22
MAX_MAP_WELLS = 250
map_paths = train_horizontal_paths[:MAX_MAP_WELLS]

fig, ax = plt.subplots(figsize=(8, 8))

for path in map_paths:
    df = pd.read_csv(path, usecols=["X", "Y"])
    step = max(1, len(df) // 300)
    df = df.iloc[::step]
    ax.plot(df["X"], df["Y"], color="lightgray", lw=0.6, alpha=0.45)

for well_id in sample_wells:
    df = pd.read_csv(horizontal_path(well_id, "train"), usecols=["X", "Y"])
    ax.plot(df["X"], df["Y"], lw=2.2, label=well_id)
    ax.scatter(df["X"].iloc[0], df["Y"].iloc[0], s=20)

if test_horizontal_paths:
    for path in test_horizontal_paths:
        df = pd.read_csv(path, usecols=["X", "Y"])
        ax.plot(df["X"], df["Y"], color="dodgerblue", lw=1.2, ls="--", alpha=0.8)

ax.set_title(f"Map view of {len(map_paths)} training trajectories plus visible test examples")
ax.set_xlabel("X / Easting (ft)")
ax.set_ylabel("Y / Northing (ft)")
ax.set_aspect("equal", adjustable="box")
ax.legend(loc="best")
plt.show()

# %% [markdown]
# ## 10. Missingness by Feature
# 
# Gamma ray can contain missing values. `TVT_input` is intentionally missing in the evaluation zone. In training, `TVT` is complete and can be used for validation experiments.

# %% cell 24
missing_counts = Counter()
nonmissing_counts = Counter()
column_totals = Counter()

for path in train_horizontal_paths:
    df = pd.read_csv(path)
    for col in df.columns:
        miss = int(df[col].isna().sum())
        missing_counts[col] += miss
        nonmissing_counts[col] += int(df[col].notna().sum())
        column_totals[col] += len(df)

missing_df = pd.DataFrame({
    "column": sorted(column_totals),
    "missing": [missing_counts[c] for c in sorted(column_totals)],
    "non_missing": [nonmissing_counts[c] for c in sorted(column_totals)],
    "total_rows_with_column": [column_totals[c] for c in sorted(column_totals)],
})
missing_df["missing_pct"] = 100 * missing_df["missing"] / missing_df["total_rows_with_column"]
missing_df = missing_df.sort_values("missing_pct", ascending=False)

display(missing_df)

# %% cell 25
fig, ax = plt.subplots(figsize=(10, 5))
plot_df = missing_df.sort_values("missing_pct")
ax.barh(plot_df["column"], plot_df["missing_pct"], color="tomato")
ax.set_xlabel("Missing values (%)")
ax.set_title("Training horizontal well missingness by column")
plt.show()

# %% [markdown]
# ## 11. Numeric Feature Correlations
# 
# This samples a small number of rows from each training well to inspect broad numeric relationships. Correlations are only a rough view here because the rows are sequential and wells are not independent IID rows.

# %% cell 27
numeric_cols = ["MD", "X", "Y", "Z", "ANCC", "ASTNU", "ASTNL", "EGFDU", "EGFDL", "BUDA", "TVT", "GR", "TVT_input"]
existing_numeric_cols = None
sampled_frames = []

for i, path in enumerate(train_horizontal_paths):
    df = pd.read_csv(path)
    cols = [c for c in numeric_cols if c in df.columns]
    df = df[cols]
    if len(df) > 200:
        df = df.sample(200, random_state=RANDOM_STATE + i)
    sampled_frames.append(df)

sampled_train = pd.concat(sampled_frames, ignore_index=True)
print(sampled_train.shape)
display(sampled_train.head())

# %% cell 28
corr = sampled_train.corr(numeric_only=True)

fig, ax = plt.subplots(figsize=(10, 8))
if HAS_SEABORN:
    sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-1, vmax=1, square=True, ax=ax)
else:
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticks(range(len(corr.index)))
    ax.set_yticklabels(corr.index)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
ax.set_title("Sampled training numeric feature correlation")
plt.show()

# %% [markdown]
# ## 12. Typewell Exploration
# 
# Typewells are vertical reference logs. Their `GR` signatures can be matched against horizontal-well `GR` to infer where the horizontal well sits on the TVT/geology scale.

# %% cell 30
def summarize_typewell_file(path):
    df = pd.read_csv(path)
    result = {
        "well_id": well_id_from_path(path),
        "rows": len(df),
    }
    for col in ["TVT", "GR"]:
        if col in df.columns:
            result[f"{col}_min"] = df[col].min(skipna=True)
            result[f"{col}_max"] = df[col].max(skipna=True)
            result[f"{col}_range"] = result[f"{col}_max"] - result[f"{col}_min"]
            result[f"{col}_missing_pct"] = 100 * df[col].isna().mean()
    if "Geology" in df.columns:
        result["geology_missing_pct"] = 100 * df["Geology"].isna().mean()
        result["n_geology_labels"] = df["Geology"].dropna().nunique()
    return result

typewell_summary = pd.DataFrame([summarize_typewell_file(path) for path in train_typewell_paths])
print(typewell_summary.shape)
display(typewell_summary.head())

display(typewell_summary.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).T)

# %% cell 31
geology_counter = Counter()

for path in train_typewell_paths:
    df = pd.read_csv(path)
    if "Geology" in df.columns:
        geology_counter.update(df["Geology"].dropna().astype(str))

geology_counts = pd.DataFrame(geology_counter.most_common(), columns=["Geology", "rows"])
display(geology_counts)

if not geology_counts.empty:
    fig, ax = plt.subplots(figsize=(8, 4))
    top = geology_counts.head(15).sort_values("rows")
    ax.barh(top["Geology"], top["rows"], color="slateblue")
    ax.set_title("Most common Typewell geology labels")
    ax.set_xlabel("Rows")
    plt.show()

# %% [markdown]
# ## 13. Sample Submission and Test Anatomy
# 
# The sample submission tells us exactly which rows need `tvt` predictions in the visible test folder. The `id` column uses `{well_id}_{row_index}`.

# %% cell 33
sub = pd.read_csv(SAMPLE_SUB_PATH)
sub["well_id"] = sub["id"].str.rsplit("_", n=1).str[0]
sub["row_index"] = sub["id"].str.rsplit("_", n=1).str[1].astype(int)

print(sub.shape)
display(sub.head())
display(sub.groupby("well_id").size().rename("submission_rows").reset_index())

# %% cell 34
test_rows = []
for path in test_horizontal_paths:
    well_id = well_id_from_path(path)
    df = pd.read_csv(path)
    row = {
        "well_id": well_id,
        "rows": len(df),
        "missing_TVT_input_rows": int(df["TVT_input"].isna().sum()) if "TVT_input" in df.columns else np.nan,
        "first_missing_index": first_missing_index(df["TVT_input"]) if "TVT_input" in df.columns else None,
        "has_target_TVT_column": "TVT" in df.columns,
    }
    test_rows.append(row)

test_summary = pd.DataFrame(test_rows)
display(test_summary)

# %% [markdown]
# ## 14. Practical Modeling Notes
# 
# A useful validation setup is to mimic test behavior on training wells: keep the known `TVT_input` segment, hide the evaluation zone, and score predictions against the training `TVT`.
# 
# Ideas worth exploring:
# 
# - Treat each well as a sequence, not as independent rows.
# - Use `TVT_input` to estimate local TVT trend before the prediction start.
# - Align horizontal `GR` to Typewell `GR` on the TVT scale, especially around the known segment.
# - Use neighboring wells and spatial coordinates (`X`, `Y`, `Z`) to estimate dip and local geology trends.
# - Handle missing `GR` explicitly; missingness itself may vary by well and segment.
# - Validate by well, not by random row split, to avoid leakage across sequential rows from the same well.
# 
# This notebook is only an EDA starter. A strong solution will likely combine sequence alignment, spatial geology features, and well-level validation.
