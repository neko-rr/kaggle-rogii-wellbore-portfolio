# %% cell 0
import pandas as pd
import numpy as np
import glob
import os

from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_squared_error
from catboost import CatBoostRegressor

# =====================================================
# LOAD ALL WELLS
# =====================================================

TRAIN_PATH = "/kaggle/input/competitions/rogii-wellbore-geology-prediction/train"

all_rows = []

for hfile in glob.glob(
    f"{TRAIN_PATH}/*__horizontal_well.csv"
):

    well_id = (
        os.path.basename(hfile)
        .replace("__horizontal_well.csv", "")
    )

    df = pd.read_csv(hfile)

    ps_idx = df["TVT_input"].last_valid_index()

    if ps_idx is None:
        continue

    last_tvt = df.loc[ps_idx, "TVT_input"]

    df["well_id"] = well_id

    df["LAST_KNOWN_TVT"] = last_tvt

    df["DIST_FROM_PS"] = (
        np.arange(len(df)) - ps_idx
    )

    df["TVT_REL"] = (
        df["TVT"] - last_tvt
    )

    all_rows.append(df)

train_df = pd.concat(
    all_rows,
    ignore_index=True
)

print("Train shape:", train_df.shape)

# =====================================================
# FEATURE ENGINEERING
# =====================================================

train_df["REL_ANCC"] = train_df["Z"] - train_df["ANCC"]
train_df["REL_ASTNU"] = train_df["Z"] - train_df["ASTNU"]
train_df["REL_ASTNL"] = train_df["Z"] - train_df["ASTNL"]
train_df["REL_EGFDU"] = train_df["Z"] - train_df["EGFDU"]
train_df["REL_EGFDL"] = train_df["Z"] - train_df["EGFDL"]
train_df["REL_BUDA"] = train_df["Z"] - train_df["BUDA"]

train_df["ANCC_MISSING"] = (
    train_df["ANCC"].isna().astype(int)
)

train_df["EGFDL_MISSING"] = (
    train_df["EGFDL"].isna().astype(int)
)

train_df["DIST_FROM_PS_SQ"] = (
    train_df["DIST_FROM_PS"] ** 2
)

train_df["GR_X_DIST"] = (
    train_df["GR"].fillna(0)
    * train_df["DIST_FROM_PS"]
)

train_df["LAST_TVT_X_DIST"] = (
    train_df["LAST_KNOWN_TVT"]
    * train_df["DIST_FROM_PS"]
)

# =====================================================
# SAMPLE
# =====================================================

sample_df = train_df.sample(
    500000,
    random_state=42
)

# =====================================================
# FEATURES
# =====================================================

FEATURES = [

    "LAST_KNOWN_TVT",
    "DIST_FROM_PS",
    "DIST_FROM_PS_SQ",

    "MD",
    "X",
    "Y",
    "Z",

    "GR",
    "GR_X_DIST",

    "REL_ANCC",
    "REL_ASTNU",
    "REL_ASTNL",
    "REL_EGFDU",
    "REL_EGFDL",
    "REL_BUDA",

    "ANCC",
    "ASTNU",
    "ASTNL",
    "EGFDU",
    "EGFDL",
    "BUDA",

    "ANCC_MISSING",
    "EGFDL_MISSING",

    "LAST_TVT_X_DIST"
]

X = sample_df[FEATURES].fillna(-999)

y = sample_df["TVT_REL"]

groups = sample_df["well_id"]

# =====================================================
# SPLIT
# =====================================================

gss = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

tr, va = next(
    gss.split(
        X,
        y,
        groups
    )
)

# =====================================================
# MODEL
# =====================================================

model = CatBoostRegressor(
    iterations=1000,
    depth=8,
    learning_rate=0.05,
    loss_function="RMSE",
    eval_metric="RMSE",
    random_seed=42,
    verbose=100
)

model.fit(
    X.iloc[tr],
    y.iloc[tr]
)

# =====================================================
# EVALUATE
# =====================================================

pred = model.predict(
    X.iloc[va]
)

rmse = np.sqrt(
    mean_squared_error(
        y.iloc[va],
        pred
    )
)

print("\nRMSE =", rmse)

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

imp = pd.DataFrame({
    "feature": FEATURES,
    "importance": model.feature_importances_
})

imp = imp.sort_values(
    "importance",
    ascending=False
)

print("\nTop Features")
print(imp.head(20))

# %% cell 1
import pandas as pd
import numpy as np
import glob
import os

TRAIN_PATH = "/kaggle/input/competitions/rogii-wellbore-geology-prediction/train"

all_rows = []

for hfile in glob.glob(f"{TRAIN_PATH}/*__horizontal_well.csv"):

    well_id = os.path.basename(hfile).replace(
        "__horizontal_well.csv", ""
    )

    df = pd.read_csv(hfile)

    ps_idx = df["TVT_input"].last_valid_index()

    if ps_idx is None:
        continue

    last_tvt = df.loc[ps_idx, "TVT_input"]

    df["well_id"] = well_id
    df["LAST_KNOWN_TVT"] = last_tvt
    df["DIST_FROM_PS"] = np.arange(len(df)) - ps_idx

    df["TVT_REL"] = (
        df["TVT"] - last_tvt
    )

    all_rows.append(df)

train_df = pd.concat(
    all_rows,
    ignore_index=True
)

print(train_df.shape)

# %% cell 2
train_df["DIST_FROM_PS_SQ"] = (
    train_df["DIST_FROM_PS"] ** 2
)

train_df["GR_X_DIST"] = (
    train_df["GR"].fillna(0)
    * train_df["DIST_FROM_PS"]
)

train_df["LAST_TVT_X_DIST"] = (
    train_df["LAST_KNOWN_TVT"]
    * train_df["DIST_FROM_PS"]
)

# %% cell 3
from catboost import CatBoostRegressor

FEATURES = [
    "LAST_KNOWN_TVT",
    "DIST_FROM_PS",
    "DIST_FROM_PS_SQ",
    "MD",
    "X",
    "Y",
    "Z",
    "GR",
    "GR_X_DIST",
    "LAST_TVT_X_DIST"
]

X = train_df[FEATURES].fillna(-999)

y = train_df["TVT_REL"]

model = CatBoostRegressor(
    iterations=1000,
    depth=8,
    learning_rate=0.05,
    loss_function="RMSE",
    verbose=100
)

model.fit(X, y)

# %% cell 4
TEST_PATH = "/kaggle/input/competitions/rogii-wellbore-geology-prediction/test"

# %% cell 5
test_rows = []

for hfile in glob.glob(
    f"{TEST_PATH}/*__horizontal_well.csv"
):

    well_id = os.path.basename(hfile).replace(
        "__horizontal_well.csv",
        ""
    )

    df = pd.read_csv(hfile)

    df["row_idx"] = np.arange(len(df))

    ps_idx = df["TVT_input"].last_valid_index()

    last_tvt = df.loc[
        ps_idx,
        "TVT_input"
    ]

    df["well_id"] = well_id

    df["LAST_KNOWN_TVT"] = last_tvt

    df["DIST_FROM_PS"] = (
        np.arange(len(df)) - ps_idx
    )

    test_rows.append(df)

test_df = pd.concat(
    test_rows,
    ignore_index=True
)

# %% cell 6
# Create engineered features in test data

test_df["DIST_FROM_PS_SQ"] = (
    test_df["DIST_FROM_PS"] ** 2
)

test_df["GR_X_DIST"] = (
    test_df["GR"].fillna(0)
    * test_df["DIST_FROM_PS"]
)

test_df["LAST_TVT_X_DIST"] = (
    test_df["LAST_KNOWN_TVT"]
    * test_df["DIST_FROM_PS"]
)

print(test_df.columns.tolist())

# %% cell 7
missing = [
    c for c in FEATURES
    if c not in test_df.columns
]

print("Missing:", missing)

# %% cell 8
X_test = test_df[
    FEATURES
].fillna(-999)

pred_rel = model.predict(X_test)

test_df["TVT_PRED"] = (
    pred_rel +
    test_df["LAST_KNOWN_TVT"]
)

# %% cell 9
test_df["DIST_FROM_PS_SQ"] = (
    test_df["DIST_FROM_PS"] ** 2
)

test_df["GR_X_DIST"] = (
    test_df["GR"].fillna(0)
    * test_df["DIST_FROM_PS"]
)

test_df["LAST_TVT_X_DIST"] = (
    test_df["LAST_KNOWN_TVT"]
    * test_df["DIST_FROM_PS"]
)

# %% cell 10
X_test = test_df[
    FEATURES
].fillna(-999)

pred_rel = model.predict(
    X_test
)

test_df["TVT_PRED"] = (
    pred_rel
    + test_df["LAST_KNOWN_TVT"]
)

# %% cell 11
# =====================================================
# ROGII - Supercharged Relative TVT Predictor (GPU)
# Target RMSE: < 4.0
# =====================================================

import pandas as pd
import numpy as np
import glob
import os
from tqdm.auto import tqdm

from sklearn.model_selection import GroupKFold
from sklearn.metrics import mean_squared_error
from catboost import CatBoostRegressor

TRAIN_PATH = "/kaggle/input/competitions/rogii-wellbore-geology-prediction/train"
TEST_PATH = "/kaggle/input/competitions/rogii-wellbore-geology-prediction/test"

# =====================================================
# 1. LOAD & ENGINEER TRAIN DATA
# =====================================================
all_rows = []

print("Loading and Engineering Train Data...")
for hfile in tqdm(glob.glob(f"{TRAIN_PATH}/*__horizontal_well.csv")):
    well_id = os.path.basename(hfile).replace("__horizontal_well.csv", "")
    df = pd.read_csv(hfile)

    df["well_id"] = well_id
    
    # MULTI-ANCHOR TRACKING (Fixes the last_valid_index issue)
    df["LAST_KNOWN_TVT"] = df["TVT_input"].ffill()
    df["LAST_KNOWN_Z"] = df["Z"].where(df["TVT_input"].notna()).ffill()
    
    last_idx = np.where(df["TVT_input"].notna(), np.arange(len(df)), np.nan)
    df["LAST_ANCHOR_IDX"] = pd.Series(last_idx).ffill()
    
    # Drop rows before the first anchor (cannot predict without a starting point)
    df = df.dropna(subset=["LAST_KNOWN_TVT"]).copy()
    
    # RELATIVE DRIFT FEATURES
    df["DIST_FROM_PS"] = np.arange(len(df)) - df["LAST_ANCHOR_IDX"]
    df["DIST_FROM_PS_SQ"] = df["DIST_FROM_PS"] ** 2
    df["Z_DRIFT"] = df["Z"] - df["LAST_KNOWN_Z"]
    
    # TARGET
    df["TVT_REL"] = df["TVT"] - df["LAST_KNOWN_TVT"]

    # SURFACE DISTANCES
    for surf in ["ANCC", "ASTNU", "ASTNL", "EGFDU", "EGFDL", "BUDA"]:
        if surf in df.columns:
            df[f"REL_{surf}"] = df["Z"] - df[surf]
            df[f"{surf}_MISSING"] = df[surf].isna().astype(int)

    # SIGNAL FEATURES
    df["GR_X_DIST"] = df["GR"].fillna(0) * df["DIST_FROM_PS"]
    df["LAST_TVT_X_DIST"] = df["LAST_KNOWN_TVT"] * df["DIST_FROM_PS"]
    
    # ROLLING CONTEXT
    df["GR_ROLL_MEAN_11"] = df["GR"].rolling(11, center=True, min_periods=1).mean()
    df["GR_ROLL_STD_11"] = df["GR"].rolling(11, center=True, min_periods=1).std()

    all_rows.append(df)

train_df = pd.concat(all_rows, ignore_index=True)
print(f"Full Train shape (No sampling): {train_df.shape}")

# =====================================================
# 2. DEFINE FEATURES & SPLIT
# =====================================================
FEATURES = [
    "LAST_KNOWN_TVT", "LAST_KNOWN_Z", "DIST_FROM_PS", "DIST_FROM_PS_SQ", "Z_DRIFT",
    "MD", "X", "Y", "Z", "GR", "GR_X_DIST", "LAST_TVT_X_DIST",
    "GR_ROLL_MEAN_11", "GR_ROLL_STD_11",
    "REL_ANCC", "REL_ASTNU", "REL_ASTNL", "REL_EGFDU", "REL_EGFDL", "REL_BUDA",
    "ANCC", "ASTNU", "ASTNL", "EGFDU", "EGFDL", "BUDA",
    "ANCC_MISSING", "EGFDL_MISSING"
]

X = train_df[FEATURES].fillna(-999)
y = train_df["TVT_REL"]
groups = train_df["well_id"]

# Use 5-Fold CV instead of a single GroupShuffleSplit
gkf = GroupKFold(n_splits=5)
folds = list(gkf.split(X, y, groups))

# =====================================================
# 3. TRAIN ENSEMBLE (GPU)
# =====================================================
models = []
oof_preds = np.zeros(len(X))
scores = []

print("\nStarting GPU Training...")
for fold, (tr, va) in enumerate(folds):
    print(f"\n--- Fold {fold} ---")
    
    model = CatBoostRegressor(
        iterations=2000, 
        depth=8,
        learning_rate=0.03,
        loss_function="RMSE",
        eval_metric="RMSE",
        random_seed=42,
        task_type="GPU", # Utilize hardware to train on all 5M rows fast
        verbose=250
    )
    
    model.fit(X.iloc[tr], y.iloc[tr], eval_set=(X.iloc[va], y.iloc[va]))
    
    pred = model.predict(X.iloc[va])
    oof_preds[va] = pred
    rmse = np.sqrt(mean_squared_error(y.iloc[va], pred))
    scores.append(rmse)
    models.append(model)
    print(f"Fold {fold} RMSE: {rmse:.4f}")

print(f"\nMean OOF RMSE: {np.mean(scores):.4f}")

# =====================================================
# 4. PREPARE TEST DATA & PREDICT
# =====================================================
test_rows = []
print("\nPreparing Test Data...")
for hfile in tqdm(glob.glob(f"{TEST_PATH}/*__horizontal_well.csv")):
    well_id = os.path.basename(hfile).replace("__horizontal_well.csv", "")
    df = pd.read_csv(hfile)
    
    df["well_id"] = well_id
    df["row_idx"] = np.arange(len(df))
    
    # Apply identical feature engineering
    df["LAST_KNOWN_TVT"] = df["TVT_input"].ffill()
    df["LAST_KNOWN_Z"] = df["Z"].where(df["TVT_input"].notna()).ffill()
    last_idx = np.where(df["TVT_input"].notna(), np.arange(len(df)), np.nan)
    df["LAST_ANCHOR_IDX"] = pd.Series(last_idx).ffill()
    
    df["DIST_FROM_PS"] = np.arange(len(df)) - df["LAST_ANCHOR_IDX"]
    df["DIST_FROM_PS_SQ"] = df["DIST_FROM_PS"] ** 2
    df["Z_DRIFT"] = df["Z"] - df["LAST_KNOWN_Z"]
    
    for surf in ["ANCC", "ASTNU", "ASTNL", "EGFDU", "EGFDL", "BUDA"]:
        if surf in df.columns:
            df[f"REL_{surf}"] = df["Z"] - df[surf]
            df[f"{surf}_MISSING"] = df[surf].isna().astype(int)
        else:
            df[f"REL_{surf}"] = -999
            df[f"{surf}_MISSING"] = 1
            
    df["GR_X_DIST"] = df["GR"].fillna(0) * df["DIST_FROM_PS"]
    df["LAST_TVT_X_DIST"] = df["LAST_KNOWN_TVT"] * df["DIST_FROM_PS"]
    df["GR_ROLL_MEAN_11"] = df["GR"].rolling(11, center=True, min_periods=1).mean()
    df["GR_ROLL_STD_11"] = df["GR"].rolling(11, center=True, min_periods=1).std()

    test_rows.append(df)

test_df = pd.concat(test_rows, ignore_index=True)

# Ensure all features exist in test
for col in FEATURES:
    if col not in test_df.columns:
        test_df[col] = -999

X_test = test_df[FEATURES].fillna(-999)

print("\nGenerating Ensembled Predictions...")
test_preds = np.zeros(len(X_test))
for model in models:
    test_preds += model.predict(X_test) / len(models)

test_df["TVT_PRED"] = test_preds + test_df["LAST_KNOWN_TVT"]

# =====================================================
# 5. FORMAT & SAVE SUBMISSION
# =====================================================
submission_rows = []
for _, row in test_df.iterrows():
    if pd.isna(row["TVT_input"]): # Only predict for missing anchors
        submission_rows.append({
            "id": f"{row['well_id']}_{int(row['row_idx'])}",
            "tvt": row["TVT_PRED"]
        })

submission_all = pd.DataFrame(submission_rows)

# Align exactly with sample_submission structure
sample_sub = pd.read_csv("/kaggle/input/competitions/rogii-wellbore-geology-prediction/sample_submission.csv")
submission = sample_sub[["id"]].merge(submission_all, on="id", how="left")

submission.to_csv("submission.csv", index=False)
print(f"\nSaved submission.csv with {len(submission)} rows. Ready for scoring.")

# %% cell 12
sample_sub = pd.read_csv(
    "/kaggle/input/competitions/rogii-wellbore-geology-prediction/sample_submission.csv"
)

print(sample_sub.head())
print(sample_sub.columns)
print(sample_sub.shape)

# %% cell 13
# =====================================
# CREATE SUBMISSION IDS
# =====================================

submission_rows = []

for _, row in test_df.iterrows():

    # Only hidden rows need prediction
    if pd.isna(row["TVT_input"]):

        row_idx = row.name

        submission_rows.append({
            "id": f"{row['well_id']}_{row_idx}",
            "tvt": row["TVT_PRED"]
        })

submission = pd.DataFrame(submission_rows)

print(submission.head())
print(submission.shape)

# =====================================
# MATCH SAMPLE SUBMISSION ORDER
# =====================================

sample_sub = pd.read_csv(
    "/kaggle/input/competitions/rogii-wellbore-geology-prediction/sample_submission.csv"
)

submission = (
    sample_sub[["id"]]
    .merge(
        submission,
        on="id",
        how="left"
    )
)

print(submission.head())
print(submission.shape)

# =====================================
# SAVE
# =====================================

submission.to_csv(
    "submission.csv",
    index=False
)

print("Saved submission.csv")

# %% cell 14
submission.shape

# %% cell 15
submission.isna().sum()

# %% cell 16
print(sample_sub.head(20))

# %% cell 17
print(submission.head(20))

# %% cell 18
print(len(sample_sub))
print(len(submission))
print(submission["tvt"].isna().sum())

# %% cell 19
missing_ids = submission[
    submission["tvt"].isna()
]

print(missing_ids.head(20))
print(len(missing_ids))

# %% cell 20
print(
    missing_ids["id"]
    .str.split("_")
    .str[0]
    .value_counts()
    .head(20)
)

# %% cell 21
submission_rows_df = pd.DataFrame(submission_rows)

# %% cell 22
pred_ids = set(
    submission_rows_df["id"]
)

sample_ids = set(
    sample_sub["id"]
)

print(
    "Missing IDs:",
    len(sample_ids - pred_ids)
)

print(
    list(sample_ids - pred_ids)[:20]
)

# %% cell 23
print(submission.shape)
print(submission.isna().sum())

missing = submission[submission["tvt"].isna()]
print("Missing rows:", len(missing))

if len(missing) > 0:
    print(missing.head(20))

# %% cell 24
import pandas as pd

sub = pd.read_csv("submission.csv")

print(sub.head())
print(sub.shape)
print(sub.isna().sum())
