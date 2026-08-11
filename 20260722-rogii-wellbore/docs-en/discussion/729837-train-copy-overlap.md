# Topic 729837 — Train copy override / hidden overlap (EN extract)

> fetched: 2026-07-27 via `kaggle competitions topics show`  
> JA: `docs-ja/discussion/729837-train-copy-overlap.md`

## Topic

**Train copy override in the public pipeline forks: does the hidden test set have overlap wells, and is this within the rules?**  
Author: Vaibhav_486 · Posted: 2026-07-26 18:54 UTC · Votes: 0 · Comments: 3

Several public notebooks contain a postprocessor that fills in a test well directly from the training copy when the well identifier appears in both sets. On wells where it triggers it essentially reproduces the label rather than predicting it. Could the organisers say whether the hidden test set actually contains any wells that overlap with training in this way, and whether using that path is considered acceptable? Asking because it is inherited by every fork of the popular baseline and it changes what a public score means.

## Comments (CLI; may truncate)

- **Tucker Arrants** (2026-07-26 19:07): No, there is no overlap. Probably a suggestion by a LLM that is confused about how the dummy test set works on Kaggle that has been inherited by every public notebook as they are all forks of each...
- **steubk** (2026-07-26 19:07): Points to Data page — visible `test/` contains only a few example instances...
- **PC Jimmmy** (2026-07-26 22:27): LLMs are apparently easily confused by the dummy test wells...
