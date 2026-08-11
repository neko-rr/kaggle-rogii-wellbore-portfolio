Topic #707915: Are Public Notebooks Overfitting to the LB?
  Author: k256.dev
  Posted: 2026-06-12 15:17:00.227000
  Votes: 4  Comments: 6

Regarding the public notebooks that achieve high scores, do you think they are overfitting to the LB? Personally, I think they are.

In the previous competition I participated in, many notebooks appeared that were only slightly modified versions of the best public notebook, changing things like the random seed or the ensemble weights. As a result, many users ended up experiencing a shake-down.

It looks to me like something similar may be happening in this competition as well.

Strangely, I have not seen any discussion about this yet, so I thought I would raise the question.

I would be happy to hear your thoughts.

thx.

Comments:
笏懌楳 Georgy Mamarin (2026-06-27 08:39:48.027000) [+0]
笏・ Late to this, but there's a number on it now. pilkwang put one on the seed band: six byte-identical notebooks of his scored 7.201窶・.286 on the public board purely from particle-filter reseeding, no...
笏懌楳 hengck23 (2026-06-13 04:22:04.993000) [+4]
笏・ note that some public notebooks may give different results if you submit multiple times due to "random seeding".  This is already a warning sign that public/private score may be different
  笏懌楳 ImperfectKitto (2026-06-13 14:26:39.027000) [+1]
  笏・ That's true. One should fix seeds for experiments so noise doesn't get mistaken for genuine improvement
笏懌楳 ImperfectKitto (2026-06-12 16:46:58.103000) [+2]
笏・ For me, every LB improvement was prefaced by CV improvement. And I didn't rely on public notebooks much (or those public solutions blending ideas).
笏・ 
笏・ I would expect that's the case for other LB lead...
  笏懌楳 k256.dev (2026-06-12 17:35:10.503000) [+2]
  笏・ I can imagine that your score is not overfitted. I also agree that prioritizing CV is the most important thing.
  笏・ 
  笏・ I think the higher-ranking participants, especially those around the gold medal rang...
笏懌楳  (2026-06-23 14:33:23.607000) [+-3]
