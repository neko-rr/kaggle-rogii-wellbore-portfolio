Topic #726465: Where does the top-team signal come from below the per-well line-oracle?
  Author: stevenleehans
  Posted: 2026-07-15 11:06:09.466000
  Votes: 14  Comments: 19

I've built a from-scratch stack for ROGII (predict TVT along horizontal-well eval zones from trajectory + gamma-ray + vertical typewell): typewell master-frame clustering, marker-surface T=Z+TVT transfer from offset wells via anisotropic IDW, a momentum particle filter in marker-space with a two-pass smoother, and a GBM ensemble over ~60 features. Grouped-by-well pooled CV 竕・8.8 (773 wells).

Diagnostics on where my error lives:



Per-well oracle ceilings: best constant 9.04, best line 6.70, quadratic 5.34, smooth 2.90. My model (8.8) sits between constant and line.
Error splits sharply by nearest same-frame neighbor distance: wells with a neighbor &lt;150 ft are already at RMSE 6.70 (the line-oracle); wells with no neighbor within 600 ft are at 10.15 (worse than their own per-well constant) and dominate the error.

Far-neighbor dip has no transferable signal: a frame-average drift-vs-distance prior scores 17.5 (dip does not transfer within a master frame).

GR fine-structure matching is dead: high-passed lateral-vs-typewell shape-cost minimizes ~20 ft from the true TVT (SNR&lt;1 in the narrow ﾂｱ20 ft eval band); the true position isn't even a low-cost point.


Top teams report CV 5.7窶・.0 窶・below my 8.8 and below the per-well line-oracle, i.e. they're capturing curvature. Given GR fine-structure matching provably fails here:



Is the signal full-curve transfer of offset wells' interpreted TVT profiles (not just a smooth structure surface) for wells with close neighbors 窶・borrowing the stratigraphic wiggle?

Is there a GR/DTW formulation that works where naive high-passed shape-matching fails (multi-scale, self-log reference, warp constraints)?

One competitor hinted the 773 wells split into two groups by a rule, with the LB correlating with only one 窶・what is that split, and does it imply a different method per group?

For far-neighbor wells with no offset control, is there any exploitable dip signal, or do top teams simply accept ~10 there and win on the covered wells?

Comments:
笏懌楳 De DQ (2026-07-15 11:54:53.293000) [+10]
笏・ Hi stevenleehans,
笏・ 
笏・ Great analysis on the error splits! Since you are new to Kaggle, here is the simple intuition behind the top teams' "magic" scores (CV ~5.7) without the complex math:
笏・ 
笏・ 
笏・ 
笏・ The "Sig...
  笏懌楳 stevenleehans (2026-07-15 12:01:40.630000) [+0]
  笏・ Oh my God thank you so much for detailed explanation. Best of luck for this competition!
  笏・ I will try to digest this!
    笏懌楳  (2026-07-15 12:06:36.640000) [+0]
  笏懌楳 Tucker Arrants (2026-07-15 14:30:21.410000) [+8]
  笏・ To add, you can get your single model CV score below 5ft without using any neighbor well data, so you can take GR matching quite far here.
    笏懌楳 Jeevan Jolly (2026-07-16 06:56:26.813000) [+4]
    笏・ Honestly lost. Still haven't achieved this ｫ､. is the score below 5ft mean-per-well or pooled? cuz I can get to mean-per-well 5.22ft, but pooled is at 7ft
    笏懌楳 stevenleehans (2026-07-16 08:21:41.860000) [+1]
    笏・ Same as me though, the more you know the more you don't know
    笏・ I'm on the peak of mount stupid I suppose
    笏懌楳 GG Ayo (AyoGG) (2026-07-16 08:38:33.937000) [+0]
    笏・ mean-per-well 5.391ft, pooled 7.941ft ,median 3.331ft qq
    笏懌楳 Tucker Arrants (2026-07-16 09:10:17.130000) [+1]
    笏・ Pooled, like the competition metric. I haven窶冲 checked the mean per well.
    笏懌楳 Andrey Chankin (2026-07-16 10:34:09.767000) [+3]
    笏・ so, you dont have heavy outlier wells to treat them differently?
    笏懌楳 stevenleehans (2026-07-16 10:46:41.500000) [+1]
    笏・ For your 5.x tabular model, is each training sample a station, a complete-well candidate path, or a segment? Are GR/typewell features computed in TVT coordinates, MD coordinates, or from candidate ...
    笏懌楳 James Day (2026-07-16 12:21:13.203000) [+2]
    笏・ @tuckerarrants, was your pooled 4.x from a single CV fold, or was it k-fold?
    笏・ 
    笏・ I have 5.77 pooled 5-fold and have some individual folds in the 4.x range, but have yet to see any 5-fold averages belo...
    笏懌楳 Andrey Chankin (2026-07-16 12:53:48.720000) [+0]
    笏・ @tuckerarrants, was your pooled 4.x from a single CV fold, or was it k-fold?
    笏・   
    笏・ I have 5.77 pooled 5-fold and have some individual folds in the 4.x range, but have yet to see any 5-fold averages be...
    笏懌楳 Tucker Arrants (2026-07-16 13:08:08.993000) [+1]
    笏・ @jsday96 Yessir 5 folds. Best fold is around 4.5ft, worst fold is 5.3ft.
    笏・ 
    笏・ @bluepill Yes I have outlier wells, about 25 wells above 12ft of error, but I do not handle them specially. 
    笏・ 
    笏・ @stevenleehan...
    笏懌楳 James Day (2026-07-16 22:23:09.640000) [+2]
    笏・ @bluepill - Random group by well, no special geographic groupings or stratification.
    笏懌楳 Poobear (2026-07-17 23:41:10.953000) [+0]
    笏・ One validation detail would help calibrate that claim: is the below-5ft CV grouped by whole well, and does each validation well recreate the organizer's TVT_input visible-prefix/hidden-suffix mask?...
    笏懌楳 Tucker Arrants (2026-07-18 00:17:27.997000) [+0]
    笏・ Yes CV is grouped by well. Validation is performed with same inputs available at test time. I am sure there are others with CV in the 4.x range at this point in the competition.
    笏懌楳 stevenleehans (2026-07-18 17:24:38.157000) [+1]
    笏・ Thank you Tucker for the pointers. I will keep pushing!
  笏懌楳 stevenleehans (2026-07-18 17:25:34.460000) [+0]
  笏・ Thank you @dedquoc for extraordinary explanation. It made me clear about these methods instead of just using it blindly and feeding it to LLM
笏懌楳 victor (2026-07-17 18:07:20.510000) [+0]
笏・ the neighbor distance split lining up with the line oracle is the part that stuck. far wells worse than a constant is rough
