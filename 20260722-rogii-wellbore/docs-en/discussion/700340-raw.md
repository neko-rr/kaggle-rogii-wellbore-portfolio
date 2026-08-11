Topic #700340: OOF vs LB: should we track worst-well improvements instead of only global RMSE?
  Author: Zhenyu Zhang
  Posted: 2026-05-17 09:20:41.450000
  Votes: 6  Comments: 0

I窶冦 trying to understand how to evaluate real progress in this competition.

In our experiments, lower OOF RMSE does not always seem to imply a better LB score. That
  makes me wonder: how should we know whether a model change is actually better?

One idea is to look not only at the overall OOF, but also at the hardest wells. In our
  EDA, some consistently difficult wells are:




86454a6f


fb03ae90


1b1eba53


389ae58f


896d15b9

These wells tend to have very large signed-bias errors across the whole well. So maybe a
model with slightly better OOF is not really better if it does not improve these failure
cases.

For model comparison, would you focus on overall OOF, fold consistency, worst-well
improvement, bias reduction, or another validation signal?

I窶囘 be interested to hear how others judge whether an OOF gain is likely to transfer to
LB.

No comments
