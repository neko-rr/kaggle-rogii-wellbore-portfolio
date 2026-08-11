# Competition Conditions — ROGII Wellbore Geology Prediction (source notes)

> Source: Overview / Evaluation / Code Requirements (user paste) · 2026-07-23  
> Japanese SSOT: `docs-ja/conditions.md`

## Background

~10,000 horizontal wells drilled yearly; much interpretation is still manual. Limited measurements and faulted geology make it hard to know bit position in the formation.

## Task

Build ML models to predict geology along a horizontal wellbore (favorable layers / placement) — specifically **TVT** for the evaluation zone.

## Evaluation

- Metric: **RMSE**
- Submission: `submission.csv` with header `id,tvt`

## Working Note Award (optional)

- Eligibility: Medal Zone on public LB
- Criteria: breadth/depth of exploration, data/well insights, physical meaningfulness, contribution of ideas, uncertainty estimation
- Deadline: **2026-07-06 23:59 UTC** (passed)

## Timeline (UTC 23:59 unless noted)

| Event | Date |
|---|---|
| Start | 2026-05-05 |
| Working Note | 2026-07-06 |
| Entry | 2026-07-29 |
| Team Merger | 2026-07-29 |
| Final Submission | 2026-08-05 |

## Code Requirements

- Notebook submissions only
- CPU/GPU ≤ 9 hours
- Internet disabled
- Freely & publicly available external data / pretrained models allowed
- Output must be named **`submission.csv`**

## Prizes

| Place | Amount |
|---|---|
| 1st | $25,000 |
| 2nd | $13,000 |
| 3rd | $7,000 |
| 4th | $5,000 |
| Working Note ×2 | $2,500 each |
| **Total** | **$50,000** |

## Participation (at paste time)

15,538 Entrants · 6,025 Participants · 5,481 Teams · 112,936 Submissions

## Citation

Igor Kuvaev, Rafael Aguilar, John Granmayeh, Ryan Holbrook, María Cruz, and Ashley Oldacre. ROGII - Wellbore Geology Prediction. https://kaggle.com/competitions/rogii-wellbore-geology-prediction, 2026. Kaggle.

URL: https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction

---

## Rules (user paste · 2026-07-23) — key extracts

- Max team size: **5**
- Submissions: **5 per day**; select up to **2 Final Submissions**
- Competition Data: **Competition use only** (no redistribution)
- Winner License: **Non-exclusive** grant to Sponsor (perpetual, royalty-free, etc.)
- External data/models: public & equally accessible at no cost, or Reasonableness
- AMLT allowed with appropriate license + Winner Obligations
- Private sharing outside teams forbidden; public forum sharing under OSI (no commercial restriction)
- Winner must deliver train + infer code, docs, environment; may join sponsor call
- Governing law: Texas / Harris County, Houston
- Participant has **accepted** the rules
