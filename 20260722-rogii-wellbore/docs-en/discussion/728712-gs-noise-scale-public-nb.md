# Observation: a small `gs` (GR noise scale) tweak in a public notebook

**Source:** kaggle-cli-fetch  
**Topic ID:** 728712  
**URL:** https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/728712  
**Fetched:** 2026/07/25 03:50 UTC  
**CLI version:** Kaggle CLI 2.2.3

---

## Meta

- Author: suzu10
- Posted: 2026-07-24 09:11:03 UTC
- Votes: 3 · Comments: 0

## Original post

Sharing an observation from a publicly available notebook in case it's useful to others still iterating.

In hjyact's "Ultimate PF-Config Strategy" notebook
(https://www.kaggle.com/code/hjyact/ultimate-pf-config-strategy-a-reproducible-score),
a single-line change — scaling the GR noise estimate (`gs`) by roughly **1.3x** —
produced a noticeably better score compared to the unmodified version. Both the
notebook and the parameter are public, so I wanted to flag it here on the forum
as well (not just on social media), for equal visibility to everyone.

We also posted about this on our own X/Twitter account earlier, and a fellow
competitor rightly pointed out that useful observations about public notebooks
should be shared on Kaggle's own discussion board too, for fairness — hence
this post.

Hope it helps someone's iteration. Good luck all!

## Comments

None as of fetch.

---

## Notes

- This `gs` is **PF / GR noise scale** inside a public PF-config notebook — not the same as Typewell-free heel affine `gs` (own F001).
- Tip / dual-track / PF family: possible micro-tweak for 枠1 exploration only; **not Final2 diversity**.
- Host did not comment.
