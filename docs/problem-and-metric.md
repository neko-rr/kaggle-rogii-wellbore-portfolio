# Problem and metric

## Competition

- **Name:** ROGII - Wellbore Geology Prediction  
- **URL:** https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction  
- **Type:** Featured Code Competition (tabular / well-structured, notebook submit)  
- **Close:** final submission **2026-08-05 23:59 UTC**

## Task

Given horizontal-well measurements (trajectory, GR-style curves, etc.) and vertical **typewell** references, estimate **TVT (True Vertical Thickness)** on evaluation intervals.  
Use case: support **geosteering** automation.

## Metric and deliverable

| Item | Spec |
|---|---|
| Metric | **RMSE** on row-level `tvt` |
| Submission | `submission.csv` columns `id,tvt` |
| Runtime | Code Competition notebook pipeline |

## Public vs Private leaderboard

Host note (paraphrased): Public score uses about **26%** of the test data; final ranking uses the other **~74%**.

Implications used in this project:

- Public is a **fixed slice**, not a private score estimator.  
- Strategies that overfit Public tip-heads can jump in Private RMSE.  
- Final planning must keep a **Trust** surface, not only Public-best.

## Data (not redistributed)

Raw competition files stay on Kaggle. This portfolio does **not** ship `dataset/` bodies.  
Accept competition rules and download if you re-run kernels.
