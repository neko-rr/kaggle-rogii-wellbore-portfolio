Topic #719389: Does CV correlates with LB・・
  Author: yuanzhe zhou
  Posted: 2026-07-04 23:17:13.797000
  Votes: 20  Comments: 15

It seems that the CV for public high scoring notebook is around 10 RMSE, but the LB for that notebook is 7. Does your CV correlates with LB? 

LLM helped me to build a model and the CV/LB are both around 10. 

Edit : From the discussions, I believe CV is what we should aim for firstly.

Comments:
笏懌楳 yu4u (2026-07-07 15:41:11.643000) [+18]
笏・ It seems that the conclusion has already been reached, but this competition is clearly a trust-your-CV competition.
笏・ I compute my CV as the average over 5 folds ﾃ・5 seeds, and only adopt changes tha...
  笏懌楳 SpeedSci (2026-07-07 15:46:19.487000) [+0]
  笏・ wow・“ood・ゝhis looks quite stable.
  笏懌楳 Jeevan Jolly (2026-07-07 17:11:23.457000) [+0]
  笏・ What is your single model best CV, if you don't mind me asking.
  笏懌楳 tennogh (2026-07-08 12:45:48.227000) [+2]
  笏・ Interesting that your CV is consistently below your LB. For me it's the opposite. Maybe my CV scheme is too hard.
笏懌楳 k256.dev (2026-07-05 03:04:23.737000) [+8]
笏・ I think that only part of the CV data is truly correlated with the LB.
笏・ 
笏・ The 773 CV wells can be divided into two groups based on a certain rule. From what I've observed, the LB correlates well with...
  笏懌楳 SpeedSci (2026-07-05 07:14:54.657000) [+0]
  笏・ Wouldn't this kind of split cause a lot of fluctuation in the LB score?
    笏懌楳 k256.dev (2026-07-05 08:00:41.647000) [+1]
    笏・ It depends on the current RMSE, but simply changing the random seed at one point in the algorithm can already cause fluctuations of around 0.2窶・.3. I consider that to be a fairly large amount of va...
笏懌楳 Tucker Arrants (2026-07-05 00:08:13.287000) [+4]
笏・ I lost basically all correlation between CV and LB once CV starting getting below 6. Before that, it was decently correlated.
  笏懌楳 yuanzhe zhou (2026-07-05 08:23:29.420000) [+3]
  笏・ Thanks for the info. From the information above (from different kagglers), I believe CV is very important in this competition. But LB also matters (high LB means that you have done something correc...
  笏懌楳 SpeedSci (2026-07-05 08:31:58.687000) [+0]
  笏・ Do you think we should deliberately handle those bad wells? And do you think Unet is worth using?
  笏懌楳 Rishikesh Jani (2026-07-08 04:40:26.960000) [+1]
  笏・ Same here. Around the 5.8 mark.
笏懌楳 ImperfectKitto (2026-07-05 00:21:02.577000) [+1]
笏・ correlation isn't "="
笏・ 
笏・ if with lower CV you get lower LB, you're chilling. that said, I had many inversions (lower CV but higher LB, not other way around though)
笏懌楳 tennogh (2026-07-04 23:21:37.003000) [+1]
笏・ It correlates to some extent, there is a previous thread where people have shared their figures. But LB is very noisy (only ~50 wells vs 773 wells for CV). The public notebooks are probably relying...
笏懌楳 Sasha Turutin (2026-07-04 23:20:03.953000) [+1]
笏・ In my case not very much, but maybe I'm doing something wrong. Never reached CV less than 8 so far.
笏懌楳 Georgy Mamarin (2026-07-05 17:41:08.040000) [+-14]
笏・ Short version: your CV and the public LB are scored on different sets of wells, so they won't line up cleanly. The public LB is only ~50 wells (a friendlier slice of the ~200 hidden), scored with r...
