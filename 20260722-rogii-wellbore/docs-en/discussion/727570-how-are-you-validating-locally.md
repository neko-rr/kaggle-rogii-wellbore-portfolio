# How are you validating locally?

**Source:** kaggle-cli-fetch  
**Topic ID:** 727570  
**URL:** https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/727570  
**Fetched:** 2026/07/24 06:00 UTC  
**CLI version:** Kaggle CLI 2.2.3

---

## Meta

- Author: IamDiganta.7
- Posted: 2026-07-19 15:59:12 UTC
- Votes: 1 · Comments: 5
- Latest comment: 2026/07/23 15:29 UTC (souldrive)

## Original post

I’m struggling to build a CV setup that correlates well with the leaderboard. How are you splitting the wells and handling duplicate typewells or nearby wells? It would also be really helpful if people could share their approximate local CV score vs leaderboard score.

## Comments

### souldrive — 2026/07/23 15:29 UTC [+1]

I split at two levels and always report both, because they answer different questions:

- **By well** — the minimum bar. Anything finer leaks: neighbouring rows in one wellbore are nearly identical, so row-level CV mostly measures interpolation.
- **By field** — wells grouped by location (k-means on each well's median X/Y, k=5). Holding out a whole group is the honest analogue of the real task, since the hidden wells come from places the model has not seen.

The gap between the two is the useful part. Measured over all 773 training wells on two deliberately simple baselines:

| | well-CV | field-CV | worst field |
|---|---|---|---|
| flat anchor | 15.799 | 16.085 | 19.208 |
| anchor + 0.02 x local slope | 15.497 | 15.884 | 19.137 |

Field-CV is consistently ~0.3 ft worse than well-CV. That difference is the part of a well-CV score that comes from having already seen the neighbourhood — which the hidden test will not hand you. I also watch the worst field rather than only the average, since a model that is fine on average and bad in one region is the one that hurts when the hidden wells land there.

One caveat: the worst-field number moves depending on how the split came out (k-means seed / implementation), so read it next to the pooled number rather than on its own.

On sharing CV-vs-LB numbers — gaps people have posted are not the same size (~+0.32 to +0.72 to +1.35 depending on model). Each person's own gap looks quite stable, but borrowing someone else's to calibrate your own does not seem safe.

**The `test/` folder cannot validate anything.** It has three wells, and all three are exact copies of training wells — same row counts, known prefix matching the training TVT at RMSE 0.0000. They are placeholders, swapped for the real hidden wells at submission time. Any score you compute on them is a model scored on its own training data.

Notebook: https://www.kaggle.com/code/souldrive/rogii-tvt-identity-and-honest-cv-design

### Tucker Arrants — 2026/07/19 16:35 UTC [+3]

I group by well but only use per-well data, if you use spatial/neighboring well data, you may need a different splitting.

CV is 4.98, 5 fold x 5 seeds, scores 5.7 on the LB. LB is just noisy, you can do some simulations depending on your model to estimate a noise range.

#### OpPrime (reply) — 2026/07/21 17:56 UTC [+0]

some elements of noise can be attributes to stochastic features

#### Tucker Arrants (reply) — 2026/07/21 18:21 UTC [+0]

There is even noise when training with different GPUs, with the exact same model, fold split, and fixed seeds.

### OpPrime — 2026/07/21 18:05 UTC [+0]

Mine is much worse. My numbers are more like 6-7-8 on CV (5 folds, 5 seeds) and then 8-9-10 on LB.

It fully depends on model and framework.

Some models seem to learn to memorise fantastically well in CV but then do not transfer at all to LB. Example: GRU about 6 on CV and 7.35 on LB.

Interesting problem with ensembles without source (e.g. Fleongg's model) — CV-LB relationship suffers when fold/seed are not aligned across components. Simple models have a cleaner relationship; multipart ensembles differ significantly.

---

## Notes

- Prior local fetch had Comments: 4 and truncated bodies (UTF-16). Refreshed from `--format json` on 2026/07/24.
- souldrive addition (2026/07/23) is the main delta: well-CV vs field-CV gap ~0.3, worst-field monitoring, test/ is identity leak.
