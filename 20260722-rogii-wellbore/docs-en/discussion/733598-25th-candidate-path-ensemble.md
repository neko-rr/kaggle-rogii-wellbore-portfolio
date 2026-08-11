# 25th Place Solution - Candidate-Path Ensemble

**Source:** kaggle-cli-fetch  
**Topic ID:** 733598  
**URL:** https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733598  
**Fetched:** 2026/08/10 ~08:00 UTC  
**CLI version:** 2.2.3

---

## CLI raw output

```
Topic #733598: 25th Place Solution - Candidate-Path Ensemble with Residual Correction
  Author: Jin Niu
  Posted: 2026-08-07 15:32:08.434000
  Votes: 3  Comments: 0

Candidate-Path Ensemble with Residual Correction

Thanks to the hosts for organizing such an interesting competition. It was unlike any competition I had entered before. I mainly explored whether a 窶徇agic窶・physics-based idea could produce a large and reliable gain, but I did not find one. Physics was still valuable for generating plausible paths, anchors, and constraints, while learned models were needed to decide which signals to trust.

Code: Kaggle notebook

Overview

The competition target, TVT, describes the stratigraphic position of a horizontal well. Let \(s\) denote measured depth and let \(h(s)\) denote TVT. The paired Typewell provides a reference gamma-ray curve \(g_T(h)\), while the horizontal well provides the observed gamma-ray curve \(g_H(s)\). A simple observation model is

$$
g_H(s)\approx a_w g_T(h(s))+b_w+\epsilon(s).
$$

For well \(w\), \(a_w\) and \(b_w\) account for differences in gamma-ray scale and offset, while \(\epsilon(s)\) represents residual mismatch and measurement noise. The task can therefore be treated as sequence alignment: estimate a continuous \(h(s)\) that aligns the two curves while remaining consistent with the known prefix and the well trajectory.

The main difficulty is gamma-ray aliasing. Similar gamma-ray patterns may appear at several Typewell depths, so the best local match is not always the correct stratigraphic position. My solution generates several candidate TVT paths, models their uncertainty, and combines them at two levels: a fixed base ensemble followed by a multi-scale residual correction. It is a physics-guided machine-learning ensemble: physical and geometric models generate candidate paths and constraints, while learned models score or refine them.

Final Kaggle scores:



Public root mean squared error: 6.420

Private root mean squared error: 6.599


1. Base predictors

1.1 Candidate-path sequence model

This model generates 66 candidate TVT paths from particle filtering, gamma-ray alignment, trajectory geometry, structural projection, and several deterministic reconstruction methods.

The query well's own particle-filter path is used as the baseline. Cross-well candidates are shifted to meet this baseline at the first prediction node, preventing a neighboring well from transferring its absolute TVT offset directly. The sequence model then works with candidate displacements relative to the same baseline.

A one-dimensional convolutional network extracts along-well context and compares the candidates at every node. It predicts candidate scores, local drift, process scale, and the reliability of the transition penalty. A conditional random field and forward窶澱ackward inference produce marginal probabilities instead of selecting one complete path:

$$
\hat h_t^{\mathrm{candidate}}=\sum_k p(z_t=k\mid x)\,h_t^{(k)}.
$$

Here \(t\) indexes nodes along the horizontal well, \(k\) indexes candidate paths, \(h_t^{(k)}\) is the TVT proposed by candidate \(k\) at node \(t\), and \(x\) contains the visible input features. The latent state \(z_t\) identifies a candidate, and \(p(z_t=k\mid x)\) is its posterior probability. Thus, \(\hat h_t^{\mathrm{candidate}}\) is the posterior-weighted TVT prediction.

This predictor supplies the main absolute TVT estimate in the final ensemble.

1.2 Typewell-aligned physics ensemble

This component works in the structural coordinate \(S=TVT+Z\), where \(Z\) is the vertical trajectory coordinate. This separates changes caused by the well trajectory from changes in the interpreted formation surface. Every path is anchored to the last known prefix value and smoothed with a second-order structural penalty.

It averages four complete predictions:



an equal average of five gamma-ray and geometry paths;

a Cauchy-weighted average that downweights paths far from the pointwise median;

an ensemble of three Typewell-aligned structural branches;

a conservative Typewell projection whose correction is reduced when reliable matches are scarce.


The runtime combination is deterministic. However, these four paths were chosen using development out-of-fold results, so this is not an independently selected physics-only result.

1.3 Spatial trend model

A directional gradient field estimates local changes in \(S=TVT+Z\) from training wells as a function of spatial position and well direction. Integrating this field along a query trajectory gives a structural trend and a measure of spatial support.

LightGBM combines this information with gamma-ray alignment and candidate-posterior features to predict an initial correction on 256 nodes. A Huber-loss decoder then anchors the prediction at Prediction Start, smooths curvature, and constrains the slope in structural coordinates. This path provides the common center for the next two predictors.

1.4 Temporal convolutional phase correction

Six gamma-ray phase-response paths are constructed around the spatial trend prediction. A temporal convolutional network with dilation factors 1, 2, 4, 8, 16, and 32 estimates one non-negative strength for each response at every node.

The response strengths use sigmoid outputs rather than a softmax. They do not need to sum to one, so the model can suppress all phase corrections when the evidence is weak or combine several consistent corrections. The weighted response is added to the common center.

1.5 Bidirectional gamma-ray alignment

This predictor builds a gamma-ray-to-Typewell matching-cost volume over 61 offsets from 竏・0 to 30 feet. One response is obtained with a forward maximum-posterior recursion. Five additional responses use forward and backward messages to compute posterior means, allowing later gamma-ray observations to influence earlier positions.

Non-negative coefficients combine the six responses. They are stored separately for each cross-validation fold. At Kaggle inference time, all five fold-specific pipelines are run and their final predictions are averaged.

1.6 LightGBM correction around particle paths

This predictor starts from 48 particle-filter candidate paths. Robust gamma-ray matching and spatial support from training wells produce a local posterior over the candidates. The posterior mean, spread, entropy, highest probability, and disagreement statistics are retained as features.

Instead of predicting TVT from scratch, LightGBM predicts a bounded residual around an anchor formed by adding 75% of the local posterior-mean candidate displacement to a target-blind spatial baseline. Here, target-blind means that the baseline is computed without reading the query well's hidden TVT. This keeps the learned correction close to a physically plausible path while allowing local adjustment.

1.7 Geometry-aware particle filter

This predictor runs a geometry-aware particle filter in the structural coordinate \(S=TVT+Z\). Its transition model uses formation dip and directional gradients estimated from training wells, while the observation likelihood compares the horizontal-well gamma ray with the paired Typewell reference.

The deployed version uses 192 particles and 40 deterministic Monte Carlo runs whose random seeds are derived from visible input. Their likelihood-weighted average is combined with the last known prefix TVT, followed by a calibration fitted only on source wells, with separate behavior near and far from Prediction Start. Five fold-specific pipelines are averaged for an unseen query well.

2. Fixed base ensemble

The five complementary predictors described in Sections 1.2 and 1.4窶・.7 are combined as follows. The displayed weights are rounded to three decimals.

$$
\begin{aligned}
h^{\mathrm{complementary}}\approx{}&amp;0.483\,h^{\mathrm{structural}}
+0.312\,h^{\mathrm{phase}}\
&amp;+0.130\,h^{\mathrm{particle}}
+0.047\,h^{\mathrm{bidirectional}}\
&amp;+0.028\,h^{\mathrm{geometry}}.
\end{aligned}
$$

Here the superscripts denote, in order, the Typewell-aligned physics ensemble, temporal convolutional phase correction, LightGBM correction around particle paths, bidirectional gamma-ray alignment, and geometry-aware particle filter. The main base prediction is

$$
B=0.600\,h^{\mathrm{candidate}}+0.400\,h^{\mathrm{complementary}}.
$$

The five complementary weights were fitted from development out-of-fold predictions and then frozen. This base provides the absolute TVT level and the broadest-scale trend. The remaining paths are used only to correct its residual shape.

Development scores of the base paths

These are development out-of-fold scores, not independent confirmation results. Every value uses the development split, five-fold validation grouped by well, and root mean squared error pooled over all scored rows.




Complete prediction path
Role
Development-split error




Candidate-path sequence model
Main base path
5.805


Typewell-aligned physics ensemble
Complementary path
6.373


Spatial trend model
Shared intermediate center
6.455


Temporal convolutional phase correction
Complementary path
6.645


Bidirectional gamma-ray alignment
Complementary and long-range residual path
6.715


LightGBM correction around particle paths
Complementary path
7.461


Geometry-aware particle filter
Complementary path
8.090




On the same split, the five-model complementary blend scores 6.205, while combining it with the main candidate-path model improves the fixed base to 5.732. The spatial trend model is an intermediate complete prediction and is not added again as a separately weighted member.

3. Residual reference paths

Three additional predictions are compared with the same base:



The long-range alignment path is the complete bidirectional gamma-ray alignment prediction described in Section 1.5. It provides a smooth, long-range phase correction.

The state-graph path, exported before candidate-path inference, combines a 95-mode irreversible state graph, a directional gradient field built from training wells, multi-scale gamma-ray matching, reconstruction from the known prefix, and boundary constraints.

The 48-path physics posterior contains 12 path-family representatives, 32 high-likelihood seeded paths, and 4 deliberately diverse paths. Its initial prediction adds 75% of the local posterior-mean candidate displacement to a target-blind baseline. A separate 97-state geometry-aware cross-correlation search then considers phase offsets from 竏・4 to 24 feet. Fixed prefix perturbations of 竏・, 竏・, 3, and 6 feet estimate when this phase correction is reliable. This path contains no trainable machine-learning model.


Subtracting the base from each path gives:

$$
\Delta_{\mathrm{long}}=h^{\mathrm{long}}-B,\qquad
\Delta_{\mathrm{graph}}=h^{\mathrm{graph}}-B,\qquad
\Delta_{\mathrm{physics}}=h^{\mathrm{physics}}-B.
$$

Here \(h^{\mathrm{long}}\), \(h^{\mathrm{graph}}\), and \(h^{\mathrm{physics}}\) are the three complete reference predictions, \(B\) is the fixed base prediction from Section 2, and each \(\Delta\) is the corresponding pointwise residual relative to that base.

On the same development split, the long-range alignment path scores 6.715, the irreversible state-graph path scores 6.604, and the 48-path physics posterior scores 7.476. The first is the bidirectional alignment output already listed in Section 2, so it is not a separate fourth path.

4. Multi-scale residual fusion

The scored rows of each well are sorted by their numeric row index and interpolated to 256 equally spaced nodes. The spacing here is the scored-row index, not physical measured depth. An orthonormal type-II discrete cosine transform is applied to each residual. Let \(C_m(k)\) denote the resulting coefficient at cosine-basis index \(k\). These coefficient ranges represent relative along-well scales, not physical frequency bands or fixed geological wavelengths.

The frozen correction assigns the residual paths to different coefficient ranges:




Cosine-basis indices
Residual contribution




0窶・
No correction


4窶・5
0.20 long-range alignment + 0.20 state graph


16窶・3
Equal contributions from all three paths, with total scale 0.40


64窶・55
0.40 from the 48-path physics posterior




Setting the first four correction coefficients to zero preserves the offset and the broadest-scale trend. The long-range and state-graph paths handle coarser structure, while the 48-path physics posterior supplies the finest-scale detail.

This differs from assigning one global blending weight to each full prediction. Each model is used only at the along-well scales where its residual is most useful.

5. Endpoint protection

After the inverse transform, a smooth taper reduces the correction over the first and last 1/16 of the prediction interval. The final prediction is the base plus this tapered correction. The correction is exactly zero at the first and last scored samples, preserving the base prediction at both boundaries and reducing errors from unstable endpoint adjustments.

6. Validation

I used five-fold cross-validation grouped by well. For every fold, all target-dependent spatial information and fitted models were built from the other four folds. The held-out wells were used only as queries. Since I developed the model design and fusion rule on these splits, the results should be treated as development out-of-fold scores rather than an independent confirmation.




Well-level five-fold validation
Use
Base prediction
Final prediction
Improvement




Development split
Formula development
5.731803
5.713155
0.018649


Alternative well split
Frozen replay
5.631664
5.615535
0.016129




All five folds improved under both splits. The two splits contain the same 773 wells with different fold allocations. The final development-split score is 5.713. All values in this section were observed during model and fusion development and should not be interpreted as an unbiased estimate of leaderboard performance.

7. Kaggle inference

Validation and test inference use the same data flow:

validation: four training folds -&gt; held-out wells
Kaggle:     all training wells  -&gt; hidden test wells


The code reads the competition train, test, and sample-submission files at runtime. It does not assume fixed well identifiers, well counts, sequence lengths, or sample order. A separate test changed all of these properties and still produced complete id,tvt output with no duplicated or missing identifiers. Source and query wells remained disjoint, and hidden query TVT was never read.

For efficiency, the five-model complementary blend runs once and exports its bidirectional alignment path, the candidate-path model runs once and exports its state-graph path, and the 48-path physics posterior is the only additional full model run.

(ChatGPT assisted with the editing and organization of this writeup.)

No comments

```

---

## Notes

- CLI では埋め込み画像・Notebook カードが欠ける場合あり
