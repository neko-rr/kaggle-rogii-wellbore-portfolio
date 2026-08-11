# Literature & open data survey — ROGII wellbore (sources)

> Surveyed: 2026-07-23  
> Japanese analysis SSOT: `docs-ja/literature-survey.md`

## Papers / preprints (selected)

| ID | Title | Link | Why listed |
|---|---|---|---|
| P1a | High-Precision Geosteering via RL and Particle Filters | https://arxiv.org/abs/2402.06377 · journal DOI 10.1007/s10596-025-10352-y | PF on GR + type log; GWC2020 typelog; RL secondary for Kaggle |
| P1b | Bayesian Geosteering Using Sequential Monte Carlo | SPWLA Petrophysics 2020 (Veettil & Clark) | SMC/PF joint stratigraphy + tool location |
| P1c | Decision-Driven Geosteering Under Uncertainty | https://arxiv.org/abs/2606.17331 | PF belief + RL; GR–offset matching likelihood |
| P1d | Uncertainty-Aware Well Placement (Dual DRL + PF) | https://www.iccs-meeting.org/archive/iccs2025/papers/159070192.pdf | Open PDF; PF+DRL |
| P2 | Bayesian Approach… Automated Geosteering (Viterbi) | SPE-212544-MS | Multimodal correlation; not single MAP |
| P3a | DTW + Stratigraphic Constraints | https://doi.org/10.1029/2024PA005082 | Constrained DTW for logs |
| P3b | Stratigraphic Correlation… Geology-Informed DL | https://www.mdpi.com/2227-9717/13/5/1288 | Survey of DTW/xcorr/DL correlation |
| P4 | Real-Time Automated Geosteering… Log + 3D Horizon | https://doi.org/10.3390/geosciences14030071 | PF + DTW affine; needs seismic (N/A here) |
| P5 | DISTINGUISH Workflow (GAN + DDP) | https://arxiv.org/abs/2503.08509 | Decision workflow; low direct RMSE value |
| P6 | Continuous Surface Updates Using Gamma Log | SPE-227995-MS | GR→distance constraints; filter bad intervals |

## Open datasets

| ID | Name | Link | Use for this Kaggle? |
|---|---|---|---|
| D1 | GWC 2021 ~10k interpretations | https://zenodo.org/records/15190744 · https://github.com/geosteering-no/10000-geosteering-interpretations-and-decisions | Label-noise / human variance only — **do not mix into train features** |
| D2 | GWC 2020 typelog | https://doi.org/10.18710/20VIVT | Paper reproduction; not competition wells |
| D3 | Kaggle tidy GWC (Georgy) | Kaggle dataset via Georgy notebooks | Same as D1; already in license-ledger T015 |
| D4 | Well-log imputation benchmark (Teapot/Geolink/Taranaki) | https://zenodo.org/records/10987946 | Domain shift — avoid for submit models |
| D5 | USGS TX historical logs | https://doi.org/10.5066/P973SMX5 | Scans; not suitable |

## Community (competition-specific)

| Name | Link |
|---|---|
| mycarta rogii-geosteering-toolkit | https://github.com/mycarta/rogii-geosteering-toolkit |
| rogii-viewer | https://github.com/tom99763/rogii-viewer |
| geosteering-no org | https://github.com/geosteering-no |

## Disclaimer

Not legal advice. Prefer competition data + Host-approved assets. License: `docs-ja/license-ledger.md`.

## Team mapping (CHK)

Japanese SSOT: `docs-ja/literature-survey.md` §自チームへのアクション · `exp/experiment-checklist.md` §既存 CHK × 論文語彙.

- Existing CHKs backed by paper vocabulary (ruler/heel/hedge/PF/neighbor) — no new experiments from that alone.
- **New Active from literature only:** **CHK-040** (heel-anchored constrained DTW/NCC) · **CHK-041** (explicit multimodal posterior hedge). Do not add further lit-derived Active items.

Links and license notes were checked at survey time; **re-verify license before any download or submit use**. Paid commercial subsurface DBs remain out of scope until Host clarification.
