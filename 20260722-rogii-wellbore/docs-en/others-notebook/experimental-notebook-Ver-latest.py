# %% [markdown]
# ## Experiment 1: Heel/Affine GR Calibration + Robust `gs` Fix
# 
# **Base notebook:** [ROGII LB7295 Public Rebuild](https://www.kaggle.com/code/bernubritz/rogii-lb7295-public-rebuild?scriptVersionId=328608078)  
# **My experimental notebook:** [ROGII Experimental Notebook](https://www.kaggle.com/code/foysalemonshanto/rogii-experimental-notebook?scriptVersionId=331362354)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.153** |
# | Experiment LB | **9.615** |
# | Status | **Not Improved** |
# 
# ### Motivation
# 
# The EDA showed that horizontal GR and typewell GR usually have a real physical relationship, but their amplitude and offset can drift from well to well. A PF/beam tracker that compares raw horizontal GR directly against raw typewell GR may therefore become over-confident in the wrong alignment, especially when the visible prefix indicates a clear GR scale or offset shift.
# 
# This experiment tested whether a simple per-well affine GR calibration could make the GR likelihood more physically consistent before PF/beam matching.
# 
# ### Core Mechanism
# 
# For each well, using only the visible `TVT_input` prefix:
# 
# - Fit an affine relationship:
# 
#   `horizontal_GR ≈ a * typewell_GR + b`
# 
# - Apply the inverse correction to the hidden/evaluation GR before likelihood matching:
# 
#   `corrected_GR = (horizontal_GR - b) / a`
# 
# - Use the corrected GR inside both:
# 
#   - `run_particle_filter`
#   - `run_beam_ensemble`
# 
# - Guard against unstable fits:
# 
#   - `a` bounded to `[0.25, 4.0]`
#   - `|b| <= 500`
#   - fallback to identity correction when the fit is degenerate
# 
# ### Robust `gs` Fix
# 
# The experiment also fixed a GR noise-estimation issue inside the PF likelihood.
# 
# Instead of using:
# 
# ```python
# np.nan_to_num(gr, nan=0.0)

# %% [markdown]
# ## Experiment 2: Multi-Reference Contact Override
# 
# **Base notebook:** [ROGII LB7295 Public Rebuild](https://www.kaggle.com/code/bernubritz/rogii-lb7295-public-rebuild?scriptVersionId=328608078)  
# **My experimental notebook:** [ROGII Experimental Notebook - Experiment 2](https://www.kaggle.com/code/foysalemonshanto/rogii-experimental-notebook?scriptVersionId=331364540)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.153** |
# | Experiment LB | **7.256** |
# | Status | **No improvement** |
# 
# ### Motivation
# 
# The base notebook used a guarded same-well contact override based on a fixed formation reference, mainly `EGFDU`. Because the training files contain multiple interpreted formation surfaces (`ANCC`, `ASTNU`, `ASTNL`, `EGFDU`, `EGFDL`, `BUDA`), this experiment tested whether choosing the best available contact reference per overlapping well could improve the final override.
# 
# The idea was physically reasonable: different wells may align better to different formation contacts, and the visible prefix can be used as a local sanity check before applying any override.
# 
# ### Core Change
# 
# For each overlapping test well, the override step was changed from a fixed-reference strategy to a multi-reference search.
# 
# The candidate references were:
# 
# - `ANCC`
# - `ASTNU`
# - `ASTNL`
# - `EGFDU`
# - `EGFDL`
# - `BUDA`
# 
# For each candidate formation reference:
# 
# - reconstruct a TVT-from-contact path
# - interpolate it onto the test well MD grid
# - compare it against the known visible prefix, `TVT_input`
# - compute prefix RMSE
# - select the reference with the lowest prefix RMSE
# 
# The original safety guard was kept unchanged:
# 
# - apply the override only if the selected contact path has prefix RMSE `< 1 ft`
# - require enough valid rows
# - otherwise fall back to the original prediction
# 
# ### Expected Impact
# 
# This was expected to be a low-risk improvement because `EGFDU` remained inside the candidate set. In theory, the method could tie the original behavior when `EGFDU` was best, and improve when another contact reference better matched the visible prefix.
# 
# The expected gain was marginal and limited mostly to overlapping/public-style wells where same-well contact information was available.
# 
# ### Result and Lesson
# 
# This experiment **failed to improve public LB**: the score changed from **7.153** to **7.256**.
# 
# The main lesson was that contact overrides are powerful but fragile. Even when a contact path looks better on the visible prefix, that does not guarantee better behavior across the hidden tail. A broader contact search can introduce subtle overfitting to the prefix unless the guard is extremely strict.
# 
# This reinforced one of the main solution principles: use formation/contact information only as a highly guarded correction, not as an aggressive replacement for the conservative TVT anchor.

# %% [markdown]
# ## Experiment 3: Bayesian Forward-Backward Smoother - NaN Leak Fix and Validation
# 
# **Base notebook:** [rogii [lb: 7.191] (Copy n Upgrade)](https://www.kaggle.com/code/tamerlanomralinov/rogii-lb-7-191-copy-n-upgrade)  
# **My experimental notebook:** [ROGII Experimental Notebook 2](https://www.kaggle.com/code/foysalemonshanto/rogii-experimental-notebook-2)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.191** |
# | Validation sample | **50 wells** |
# | Best smoother CV RMSE | **21.39 ft** |
# | Last-known baseline CV RMSE | **12.49 ft** |
# | Status | **No improvement, but bug fixed** |
# 
# ### Objective
# 
# This experiment tested whether a full-sequence Bayesian forward-backward smoother could improve TVT tracking by using future GR constraints, instead of relying only on forward-only PF/beam-style tracking.
# 
# The idea was attractive because the hidden evaluation zone is one long contiguous tail. A smoother can, in theory, use information from both directions and produce a more globally consistent TVT path.
# 
# ### Bug Identified
# 
# A critical NaN leak was found inside `bayes_smoother_well()`.
# 
# When a well had too few known prefix rows:
# 
# known.sum() < 5
# 
# but still had evaluation rows:
# ev.sum() > 0
# the function returned:
# ti.copy()
# However, ti still contained NaN values in the evaluation zone. Those NaNs then entered the CV error calculation:
# se_sm += np.sum(e_sm ** 2)
# As a result, the smoother RMSE became nan, making the validation result unusable.
# Fix
# The edge cases were separated cleanly:
# If ev.sum() == 0, return ti.copy() because there is nothing to predict.
# If known.sum() < 5, return None and skip that well in CV.
# Add a final safety fallback so any remaining NaN in the evaluation zone is replaced by the linear prior or last-known TVT.
# 
# ### Add a validation guard:
# 
# assert np.isfinite(_rmse_sm)
# This prevents future silent NaN leakage.
# CV Results
# Model / Prior Blend	Pooled RMSE (ft)	Last-Known Baseline
# Linear Prior (w_struct=0.0)	36.24	12.49
# Mixed Prior (w_struct=0.5)	21.39	12.49
# Structural Prior (w_struct=1.0)	24.09	12.49
# 
# ### Result and Lesson
# 
# The bug fix worked: CV produced finite, reliable numbers.
# However, the method failed as a model improvement. Even the best smoother setting, w_struct=0.5, scored 21.39 ft RMSE, much worse than the simple last-known TVT baseline at 12.49 ft RMSE.
# The main lesson was that the GR/typewell matching signal is not strong enough to support an aggressive full-sequence smoother in this dataset. The smoother introduced too much random-walk freedom and overfit noisy GR residual patterns.
# This experiment strengthened one of the central conclusions of the project: the known TVT_input prefix is an extremely strong anchor, and any method that moves too far away from it needs very strong evidence and strict uncertainty control.

# %% [markdown]
# ## Experiment 4: Gold `conservative_plus` Profile
# 
# **Base notebook:** [ROGII : PF + Contact + Gold Calibration Stack](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack)  
# **My experimental notebook:** [ROGII Experimental Notebook 6](https://www.kaggle.com/code/foysalemonshanto/experimental-notebook-6)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.209** |
# | Experiment LB | **7.296** |
# | Status | **No Improvement** |
# 
# ### Objective
# 
# This experiment tested whether a slightly more permissive version of the final Gold visible-prefix calibration overlay could recover extra signal beyond the conservative profile.
# 
# The base notebook already uses a conservative Gold profile as the final correction layer. That profile is intentionally strict and only moves the public anchor when the visible-prefix backtest gives enough evidence that a calibration candidate is better than the current prediction.
# 
# ### Change
# 
# Only the final Gold profile was changed:
# 
# os.environ["ROGII_GOLD_PROFILE"] = "conservative_plus"
# 
# A new conservative_plus profile was added between conservative and balanced. It slightly relaxed the gain and consistency thresholds and allowed a slightly larger capped move. The profile loop was also updated so the notebook writes:
# submission_gold_prefix_conservative_plus.csv
# 
# ### Result
# 
# The experiment worsened the public leaderboard score:
# Metric	Value
# Base LB	7.209
# Experiment LB	7.296
# 
# ### Result and Lesson
# 
# The relaxed Gold gate did not improve generalization. It moved the solution too far from the safer conservative anchor, and the extra visible-prefix correction did not transfer well to the hidden evaluation set.
# This experiment failed, but it was still useful because it confirmed an important project-level lesson: for this pipeline, the original conservative Gold profile is safer than a more permissive variant. Slightly relaxing the final calibration gate can overfit the visible prefix without improving hidden-test performance.
# 

# %% [markdown]
# ## Experiment 5: Model-Package Tiny Blend
# 
# **Base notebook:** [ROGII v3: Heel-Calibrated Contact Geosteering](https://www.kaggle.com/code/pilkwang/rogii-v3-heel-calibrated-contact-geosteering?scriptVersionId=330296706)  
# **My experimental notebook:** [ROGII Experimental Notebook 4](https://www.kaggle.com/code/rokaiyasomapti/rogii-experimental-notebook-4?scriptVersionId=331382658)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.245** |
# | Experiment LB | **7.218** |
# | Status | **Successful** |
# 
# ### Objective
# 
# This experiment tested whether an external model-package prediction could add a very small but useful correction on top of the `contact_verified` base.
# 
# The goal was not to replace the physical/geosteering solution. Instead, the model package was treated as a weak secondary signal that might capture residual structure missed by the main trajectory/contact pipeline.
# 
# ### Change
# 
# The base profile was kept unchanged:
# 
# 
# SUBMISSION_PROFILE = "contact_verified"
# 
# Only the model-package correction was enabled:
# RUN_MODEL_PACKAGE_CORRECTION = True
# MODEL_PACKAGE_GATED_MAX_WEIGHT = 0.005
# MODEL_PACKAGE_GATED_CANDIDATES = (0.005,)
# MODEL_PACKAGE_DIFF_P95_DISABLE = None
# 
# ### Mechanism
# 
# The notebook first builds the normal base submission.csv. Then it generates a model-package prediction and applies a tiny gated blend:
# final = (1 - gate) * base + gate * model_package
# The maximum gate was only:
# 0.005
# So even when the correction was active, the final movement was intentionally very small.
# 
# ### Motivation
# 
# A previous diagnostic showed that the model-package prediction differed from the base by about:
# mean absolute difference: around 15 ft
# p95 absolute difference: around 26.7 ft
# That meant the package was meaningfully different from the base and might contain new signal. However, because the difference was large, the experiment used only the smallest safe movement.
# 
# ### Risk
# 
# The old guard had disabled this correction because the model-package prediction disagreed strongly with the base. That made the experiment risky: if the base solution was already stronger, even a tiny movement toward the model package could hurt.
# The design therefore used a deliberately tiny weight instead of a normal blend.
# 
# ### Result and Lesson
# 
# This experiment improved public LB from 7.245 to 7.218.
# This was one of the few successful experiments. The result suggests that the external model-package prediction contained a small amount of complementary signal, but only when used as a very weak correction.
# The main lesson was that model diversity can help, but the correction must be heavily constrained. A large model-package blend would likely be unsafe; the useful contribution came from a tiny, gated residual adjustment rather than from replacing the main geosteering/contact solution.

# %% [markdown]
# ## Experiment 6: Gold Profile Balanced
# 
# **Base notebook:** [ROGII v3: Heel-Calibrated Contact Geosteering](https://www.kaggle.com/code/pilkwang/rogii-v3-heel-calibrated-contact-geosteering)  
# **My experimental notebook:** [ROGII Experimental Notebook 4-5](https://www.kaggle.com/code/foysalemonshanto/rogii-experimental-notebook-4-5?scriptVersionId=331384758)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.261** |
# | Experiment LB | **7.582** |
# | Status | **Failed** |
# 
# ### Objective
# 
# This experiment tested whether the visible-prefix Gold calibration could benefit from a slightly less conservative profile.
# 
# The base setup kept the main submission path unchanged and only relaxed the final Gold calibration gate by switching the visible-prefix profile from `conservative` to `balanced`.
# 
# ### Change
# 
# Only the Gold profile was changed:
# 
# 
# VISIBLE_PREFIX_PROFILE = "balanced"
# 
# he notebook still used the same base path:
# SUBMISSION_PROFILE = "contact_verified"
# RUN_MODEL_PACKAGE_CORRECTION = False
# RUN_FULL_STACK_CV_ABLATION = False
# The balanced profile lowers the commit threshold and allows a larger move than conservative.
# 
# ### Result
# 
# The experiment made the public LB worse:
# Metric	Value
# Base LB	7.261
# Experiment LB	7.582
# 
# ### Result and Lesson
# 
# This experiment failed. The more permissive Gold profile overcommitted on the visible prefix and moved the final predictions too far away from the safer conservative anchor.
# The result suggests that, for this pipeline, the original conservative Gold profile is better at protecting hidden-tail generalization than the balanced variant.

# %% [markdown]
# ## Experiment 7: `PP.w_sub1 = 0.64`
# 
# **Base notebook:** [ROGII v3: Heel-Calibrated Contact Geosteering](https://www.kaggle.com/code/pilkwang/rogii-v3-heel-calibrated-contact-geosteering)  
# **My experimental notebook:** [ROGII Experimental Notebook 4-5](https://www.kaggle.com/code/foysalemonshanto/rogii-experimental-notebook-4-5)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.261** |
# | Experiment LB | **7.316** |
# | Status | **Failed** |
# 
# ### Objective
# 
# This experiment tested a slightly more learned-model-heavy blend inside the learned trajectory branch.
# 
# The goal was to check whether increasing the learned model contribution could improve hidden-tail prediction while keeping the rest of the submission pipeline unchanged.
# 
# ### Change
# 
# The base setup was kept unchanged:
# 
# python
# SUBMISSION_PROFILE = "contact_verified"
# RUN_MODEL_PACKAGE_CORRECTION = False
# RUN_FULL_STACK_CV_ABLATION = False
# 
# Only one parameter was changed:
# PP.w_sub1 = 0.64
# The base value was:
# PP.w_sub1 = 0.60
# Mechanism
# PP.w_sub1 controls the internal learned-trajectory branch blend:
# delta = w_sub1 * learned_model_delta + (1 - w_sub1) * likPF_delta
# This is not the final SP45/Fleongg blend weight. It only changes the balance inside one learned trajectory component.
# ### Motivation
# 
# Notebook comments suggested that a useful range might be around 0.55 to 0.68. This experiment tested a moderate move from 0.60 toward the model-heavy side.
# The reasoning was that if the learned model captured useful hidden-tail structure better than the likelihood/PF component, a slightly higher w_sub1 could improve the final result.
# Risk
# ### The main risk was overfitting.
# 
# The EDA showed that the last-known TVT anchor is very strong, while more aggressive extrapolation can fail badly. Increasing the learned model weight can hurt if the learned delta overreacts to noisy tail patterns or spurious correlations.
# 
# ### Result and Lesson
# 
# This experiment failed on public LB: the score worsened from 7.261 to 7.316.
# The result suggests that simply making the learned branch more model-heavy was not a robust improvement. The base balance was already close to a safer region, and pushing more weight onto the learned delta reduced robustness.
# The lesson was that blend-weight tuning alone is not enough. Improvements need to come from better confidence, better well selection, or physically meaningful corrections rather than a uniform increase in model aggressiveness.

# %% [markdown]
# ## Experiment 8: Calibration-Gated Selector Hold
# 
# **Base notebook:** [ROGII v3: Heel-Calibrated Contact Geosteering](https://www.kaggle.com/code/pilkwang/rogii-v3-heel-calibrated-contact-geosteering?scriptVersionId=330296706)  
# **My experimental notebook:** [ROGII Experimental Notebook 4 - Experiment 8](https://www.kaggle.com/code/rokaiyasomapti/rogii-experimental-notebook-4?scriptVersionId=331390635)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.245** |
# | Experiment LB | **7.243** |
# | Status | **Small improvement** |
# 
# ### Objective
# 
# This experiment tested whether prefix GR/typewell calibration quality could be used as a confidence gate for the selector path.
# 
# The motivation came from EDA: GR alignment is physically real, but it is not uniformly reliable across wells. Some wells have strong prefix correlation and stable calibration behavior, while others have noisy or missing GR. A selector that treats all wells equally can therefore become too aggressive.
# 
# ### Core Idea
# 
# Instead of always allowing the selector path to move the prediction, this experiment adds a calibration-aware hold rule.
# 
# The selector is allowed to act only when the visible prefix suggests that the GR/typewell relationship is trustworthy enough. Otherwise, the prediction is held closer to the safer base trajectory.
# 
# ### Change
# 
# The base setup was kept clean and unchanged. The experiment only added a confidence gate based on calibration diagnostics such as:
# 
# - prefix GR/typewell correlation
# - calibration quality
# - prefix fit error
# - GR missingness / weak alignment indicators
# 
# The goal was not to create a new trajectory model, but to reduce risky selector moves on wells where the prefix evidence was weak.
# 
# ### Expected Impact
# 
# This was expected to help wells where the selector was likely to overreact to unreliable GR evidence.
# 
# The expected gain was small because the change is conservative: it does not create a new signal, it only blocks or reduces low-confidence moves.
# 
# ### Result and Lesson
# 
# This experiment gave a small public LB improvement: **7.245** to **7.243**.
# 
# The gain was modest, but the direction was useful. It supported the broader conclusion that confidence estimation matters more than aggressive modeling in this competition.
# 
# The main lesson was that calibration diagnostics are useful as uncertainty features. They may not be strong enough to select all winning wells by themselves, but they can help identify when a model path should be trusted less.

# %% [markdown]
# ## Experiment 9: Tool-Coherence-Gated Bimodal Midpoint Hedge
# 
# **Base notebook:** [ROGII : PF + Contact + Gold Calibration Stack](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack)  
# **My experimental notebook:** [ROGII PF Contact Gold Calibration Stack Base](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack-base/notebook?scriptVersionId=332959039)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.189** |
# | Experiment LB | **7.185** |
# | LB change | **-0.004** |
# | Status | **Small improvement** |
# 
# ### Objective
# 
# This experiment tested whether a bimodal midpoint hedge becomes safer when it is applied only when multiple tools agree that the well is ambiguous.
# 
# The earlier bimodal hedge was too easy to trigger and damaged some wells. This version adds a tool-coherence gate before allowing any midpoint-style move.
# 
# ### Change
# 
# The base PF/contact/gold pipeline was kept unchanged except for the bimodal hedge decision layer.
# 
# Instead of applying the hedge from a single GR/PF signal, the experiment requires stronger agreement between candidate tools before moving away from the anchor. The hedge is only allowed when the ambiguity signal is coherent enough to suggest a real second plausible datum rather than random PF/beam disagreement.
# 
# The correction remains conservative:
# - no broad replacement of the base prediction;
# - only a small move is allowed;
# - ambiguous wells are targeted;
# - the last-known/anchor behavior remains the default.
# 
# ### Result
# 
# The public LB improved from **7.189** to **7.185**, a small but positive movement.
# 
# The gain is marginal, but it supports the main lesson from the failed bimodal experiments: the bimodal idea is only useful when the trigger is heavily guarded.
# 
# ### Lesson
# 
# Bimodal hedging should not be treated as a general correction. Most wells should stay anchored. The useful signal appears only when independent tools agree that the well may have a second plausible stratigraphic datum.
# 
# This experiment suggests that coherence gating is safer than a raw midpoint hedge, but the effect size is still small and should be treated as a narrow post-processing improvement rather than a core model replacement.

# %% [markdown]
# ## Experiment 10: Heel-Calibrated Two-Minima Posterior Hedge
# 
# **Base notebook:** [ROGII : PF + Contact + Gold Calibration Stack](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack)  
# **My experimental notebook:** [ROGII PF Contact Gold Calibration Stack 3](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack-3?scriptVersionId=332867643)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.189** |
# | Experiment LB | **7.186** |
# | LB change | **-0.003** |
# | Status | **Small improvement** |
# 
# ### Objective
# 
# This experiment tested a safer version of the bimodal hedge idea.
# 
# The previous bimodal midpoint hedge was too weakly guarded and hurt the leaderboard. The updated idea was inspired by the observation that repeated GR patterns can create two plausible stratigraphic datums. Instead of committing to one mode or using a fixed midpoint, this version tries to estimate a small posterior-style correction from two near-tied GR-misfit minima.
# 
# ### Change
# 
# The base PF/contact/gold pipeline was kept unchanged except for the selector prediction step.
# 
# For each well, the known heel/prefix was used to fit an affine GR calibration:
# 
# 
# typewell_GR(TVT_input) ~= a * horizontal_GR + b
# 
# Then the calibrated horizontal GR was compared against the typewell GR while scanning bounded vertical shifts around the current base path.
# If two near-tied minima appeared at a plausible bundle-gap distance, the method computed a small posterior correction instead of committing to one minimum.
# 
# ### The correction was heavily guarded:
# 
# enough finite GR rows required;
# enough known heel/prefix rows required;
# minimum heel calibration quality required;
# two minima must be separated by a plausible distance;
# minima must be near-tied;
# final move is downweighted and capped.
# 
# ### Result
# 
# The public LB moved from 7.189 to 7.186, a small improvement.
# The gain is marginal, but directionally useful because the previous midpoint hedge was harmful. This suggests that the bimodal idea can help only when it is tied to heel-calibrated GR evidence and kept very conservative.
# 
# ### Lesson
# 
# Bimodal correction is not a broad replacement for the anchor. It is a tiny, high-risk adjustment that must be applied only when the GR cost surface shows credible ambiguity.
# The useful part is not “jumping” to another mode. The useful part is a small guarded posterior move when the data supports two plausible datums.

# %% [markdown]
# ## Experiment 11: Simple Bimodal Hedge from Research Paper
# 
# **Base notebook:** [ROGII PF Contact Gold Calibration Stack](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack)  
# **My experimental notebook:** [ROGII PF Contact Gold Calibration Stack — Simple Bimodal Hedge](https://www.kaggle.com/code/rokaiyasomapti/rogii-pf-contact-gold-calibration-stack?scriptVersionId=332464511)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.189** |
# | Experiment LB | **7.44** |
# | Status | **Not Improvement** |
# 
# ### Motivation
# 
# A research-paper-inspired bimodal hedge was tested to handle cases where the hidden TVT path may have two plausible trajectory modes instead of a single confident path.
# 
# In the ROGII task, some wells can have ambiguous hidden intervals where the visible prefix does not clearly determine one best continuation. A single PF or calibrated trajectory may become over-confident in one path. The goal of this experiment was to test whether a simple bimodal hedge could reduce this risk by softly considering an alternative midpoint-style trajectory.
# 
# ### Core Mechanism
# 
# The experiment added a simple bimodal hedge on top of the existing PF + Contact + Gold calibration stack.
# 
# The main idea was:
# 
# - Keep the original base prediction as the primary trajectory
# - Detect uncertain or ambiguous trajectory behavior
# - Add a secondary hedge candidate inspired by bimodal continuation
# - Combine or adjust the final prediction using a simple hedge rule
# - Keep the method lightweight and easy to integrate into the existing stack
# 
# The hedge was not a full learned model. It was a rule-based adjustment designed to reduce risk in ambiguous wells.
# 
# ### Expected Benefit
# 
# The expected benefit was that the hedge could improve wells where the original base prediction selected the wrong mode.
# 
# The experiment was intended to help in cases such as:
# 
# - Multiple plausible hidden TVT continuations
# - Uncertain PF alignment
# - Candidate paths with similar likelihood
# - Wells where midpoint-style correction may reduce large errors
# 
# ### Result
# 
# The experiment did not produce a reliable improvement over the base notebook.
# 
# | Metric | Value |
# |---|---:|
# | Base LB | **7.189** |
# | Experiment LB | **7.44** |
# | Status | **Not Improvement** |
# 
# ### Interpretation
# 
# Although the idea was theoretically useful, the simple implementation was not strong enough to improve the final leaderboard result.
# 
# The likely issue was that the hedge was too broad and not sufficiently gated. In some wells, the alternative bimodal path may help, but applying it without strong confidence checks can damage wells where the base trajectory is already correct.
# 
# This showed that a bimodal hedge should not be applied globally or too simply. It needs better gating, candidate selection, and confidence control.
# 
# ### Decision
# 
# The simple bimodal hedge was not selected as a final improvement.
# 
# The key decision from this experiment was:
# 
# - Do not use the simple hedge directly
# - Keep the base PF + Contact + Gold calibration stack unchanged
# - Use bimodal logic only if it is strongly gated
# - Future versions should apply the hedge only inside carefully selected candidate pools
# 
# ### Final Conclusion
# 
# Experiment 11 tested a research-paper-inspired simple bimodal hedge for ambiguous hidden TVT trajectories.
# 
# The experiment was useful as an idea-validation step, but the simple version was not reliable enough for final use. It showed that bimodal hedging needs stronger gating and should not be applied as a broad correction.

# %% [markdown]
# ## Experiment 12: L1-LGB v3 Conservative Correction Model
# 
# **My experimental notebook:** [ROGII L1-LGB From Scratch Training v2](https://www.kaggle.com/code/foysalemonshanto/rogii-l1-lgb-from-scratch-training-v2?scriptVersionId=333086383)  
# **External blend notebook:** [Fork of ROGII PF Contact Gold Calibration](https://www.kaggle.com/code/rokaiyasomapti/fork-of-rogii-pf-contact-gold-calibra-0b19e9?scriptVersionId=333170328)
# 
# | Item | Value |
# |---|---:|
# | Experiment notebook type | **Test / training notebook** |
# | Direct LB | **Not used as final standalone** |
# | Final LB reference | **[Fork of ROGII PF Contact Gold Calibration](https://www.kaggle.com/code/rokaiyasomapti/fork-of-rogii-pf-contact-gold-calibra-0b19e9?scriptVersionId=333170328)** |
# | Status | **Feature / correction source** |
# 
# ### Objective
# 
# This experiment tested whether a freshly trained L1-LightGBM residual model could provide a conservative correction signal for the strong PF + Contact + Gold stack.
# 
# The goal was not to replace the geosteering pipeline. The goal was to train a separate tabular correction model and check whether it contains complementary residual information that can be blended later with a much stronger base submission.
# 
# ### Model Idea
# 
# The model is trained as an anchor-residual style correction model.
# 
# Instead of predicting TVT from scratch, the model uses engineered well-level, trajectory-level, PF-derived, and structural features to learn a correction around an anchored prediction.
# 
# The L1 objective was chosen because the error distribution is heavy-tailed. A small number of difficult wells contributes a large share of total squared error, so an L1-style model can be more robust than a pure L2 objective.
# 
# ### Why It Was Kept Conservative
# 
# Earlier experiments showed that standalone correction models can easily damage strong anchored submissions. The known `TVT_input` prefix and the PF/contact/gold stack are already strong, so replacing them with a tabular model is risky.
# 
# For that reason, this notebook is treated as a **test notebook** and a **correction-source notebook**, not as the final submission path.
# 
# ### Usage
# 
# The output from this experiment is intended to be used only through a later external blend:
# 
# ```python
# final = (1 - w) * strong_base + w * lgb_v3_correction

# %% [markdown]
# ## Experiment 13: L1-LGB v4 with HMM Posterior Features
# 
# **Base notebook:** [ROGII PF Contact Gold Calibration Stack Base](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack-base)  
# **My experimental notebook:** [ROGII L1-LGB From Scratch Training v2 — Version 6](https://www.kaggle.com/code/foysalemonshanto/rogii-l1-lgb-from-scratch-training-v2?scriptVersionId=333103246)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.185** |
# | Experiment LB | **See Version 1** |
# | LB Reference | [Fork Submission Version 1](https://www.kaggle.com/code/rokaiyasomapti/fork-of-rogii-pf-contact-gold-calibra-574939?scriptVersionId=333178635) |
# | Status | **Candidate Generated / Requires Careful Blending** |
# 
# ### Motivation
# 
# Earlier L1-LGB experiments used PF-based features to train a correction model. However, PF alone may not fully capture uncertainty in the hidden TVT interval. The HMM-based path can provide an additional posterior-style estimate of the likely hidden trajectory.
# 
# This experiment tested whether adding HMM posterior features into the L1-LGB training pipeline could improve the correction model. The main idea was that the LGB model may learn when to trust PF, when to trust HMM, and when to apply a correction between them.
# 
# ### Core Mechanism
# 
# This experiment extends the previous L1-LGB feature set by adding HMM posterior features during training and test-time inference.
# 
# The model uses PF-derived features such as:
# 
# - `pf_pred`
# - `pf_delta`
# - `pf_cumrate`
# - `pf_gradient`
# - `pf_vs_flat`
# - `pf_log_lik`
# - `pf_smooth`
# - `pf_curvature`
# - `pf_gr_resid`
# 
# It also adds HMM-derived posterior features:
# 
# - `hmm_mean`
# - `hmm_delta`
# - `hmm_std`
# - `hmm_std_norm`
# - `hmm_vs_pf`
# - `hmm_uncertain`
# 
# The final L1 model is trained to predict the hidden `tvt` target using both PF and HMM information.
# 
# ### Generated Outputs
# 
# The experiment generated the following main files:
# 
# - `submission_exp13_lgb_v4_hmm.csv`
# - `submission_exp13_pf.csv`
# - `submission_exp13_hmm.csv`
# - `submission_exp13_pf_hmm50.csv`
# - `submission_l1_lgb_v4_hmm.csv`
# - `test_candidates_exp13.csv`
# - `train_features_v4_hmm.parquet`
# 
# The default direct submission from this experiment was:
# 
# 
# submission_exp13_lgb_v4_hmm.csv
# 
# The PF/HMM50 candidate was calculated as:
# 
# pf_hmm50 = 0.5 * pf_pred + 0.5 * hmm_mean
# Format and Consistency Check
# 
# The generated files were checked before blending.
# 
# ### The check confirmed:
# 
# All submission files had shape (14151, 2)
# Columns were exactly id and tvt
# ID order matched sample_submission.csv
# No duplicate IDs
# No missing or non-finite tvt values
# submission.csv was exactly equal to submission_exp13_lgb_v4_hmm.csv
# submission_l1_lgb_v4_hmm.csv was also equal to submission_exp13_lgb_v4_hmm.csv
# test_candidates_exp13.csv matched all corresponding submission files
# pf_hmm50 = 0.5 * pf_pred + 0.5 * hmm_mean
# train_features_v4_hmm.parquet contained the required HMM feature columns
# 
# ### The training feature cache had:
# 
# Shape: (3783989, 53)
# 
# ### Required HMM columns were present and finite:
# 
# hmm_mean
# hmm_delta
# hmm_std
# hmm_std_norm
# hmm_vs_pf
# hmm_uncertain
# Result
# 
# The experiment successfully produced a valid L1-LGB v4 HMM candidate and a separate PF/HMM50 candidate.
# 
# ### The main candidate files for later blending were:
# 
# submission_exp13_lgb_v4_hmm.csv
# submission_exp13_pf_hmm50.csv
# test_candidates_exp13.csv
# Interpretation
# 
# The L1-LGB v4 HMM model was technically valid and correctly generated. The output files were aligned with the competition submission format, and the HMM posterior features were correctly included in the training cache.
# 
# However, later multi-cut validation showed that the direct LGB v4 HMM prediction was less stable than the simpler PF/HMM50 candidate. This means the model may have learned useful patterns, but its standalone prediction was risky under hidden-region simulation.
# 
# The PF/HMM50 candidate was more conservative because it directly averaged two trajectory estimates instead of relying on a learned correction model.
# 
# Decision
# 
# The direct LGB v4 HMM submission should not be used aggressively.
# 
# ### The safer decision is:
# 
# Use submission_exp13_pf_hmm50.csv as the main Exp13 blend candidate
# Use submission_exp13_lgb_v4_hmm.csv only with a very small blend weight
# Avoid large LGB v4 HMM blend weights such as 10% or 15% unless extra submission slots are available
# 
# ### Recommended external blend after this experiment:
# 
# 0.90 * Base 7.185 + 0.10 * Exp13 PF/HMM50
# 
# Optional cautious LGB blend:
# 
# 0.95 * Base 7.185 + 0.05 * Exp13 LGB v4 HMM
# 
# ### Final Conclusion
# 
# Experiment 13 successfully introduced HMM posterior features into the L1-LGB correction model and generated valid submission candidates.
# 
# The most useful output from this experiment was not necessarily the direct LGB v4 HMM submission, but the verified candidate set that enabled safer external blending with the strong Base 7.185 notebook.

# %% [markdown]
# ## Experiment 14: L1-LGB v4 HMM Multi-cut Validation
# 
# **Base notebook:** [ROGII PF Contact Gold Calibration Stack Base](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack-base)  
# **My experimental notebook:** [ROGII L1-LGB From Scratch Training v2](https://www.kaggle.com/code/foysalemonshanto/rogii-l1-lgb-from-scratch-training-v2)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.185** |
# | Experiment LB | **[See Version 2](https://www.kaggle.com/code/rokaiyasomapti/fork-of-rogii-pf-contact-gold-calibra-574939?scriptVersionId=333178635) **  |
# | Status | **Validation / Diagnostic Experiment** |
# 
# ### Motivation
# 
# Earlier experiments showed that the L1-LGB correction model could improve OOF performance, especially when PF-derived features and HMM posterior features were added. However, public leaderboard performance does not always match OOF performance in this competition because the hidden test interval can behave differently from the visible prefix.
# 
# This experiment was created to test whether the L1-LGB v4 HMM model is actually robust under different hidden-region scenarios. Instead of trusting only OOF score, the notebook performs a multi-cut validation where each well is partially hidden at different cut fractions.
# 
# The main goal was to compare several candidate strategies under simulated public/private-test-like conditions.
# 
# ### Core Mechanism
# 
# The validation was performed by cutting each well at multiple visible-prefix fractions and predicting the remaining hidden interval.
# 
# The tested cut fractions were:
# 
# - `0.50`
# - `0.65`
# - `0.80`
# 
# For each validation case, the notebook compared the following prediction strategies:
# 
# - **Flat baseline**
# - **PF prediction**
# - **HMM prediction**
# - **PF/HMM50 prediction**
# - **L1-LGB v4 HMM prediction**
# 
# ### The PF/HMM50 candidate was calculated as:
# 
# 
# pf_hmm50 = 0.5 * pf_pred + 0.5 * hmm_mean
# 
# The L1-LGB v4 HMM model used HMM posterior features during training, including:
# 
# hmm_mean
# hmm_delta
# hmm_std
# hmm_std_norm
# hmm_vs_pf
# hmm_uncertain
# Validation Result
# 
# The multi-cut validation produced 150 valid cases.
# 
# ### Validation Result
# 
# The multi-cut validation produced **150 valid cases**.
# 
# ### Overall mean RMSE comparison:
# 
# | Candidate | Mean RMSE |
# |---|---:|
# | PF/HMM50 | **7.8555** |
# | HMM | **7.9363** |
# | PF | **8.0375** |
# | Flat | **9.1490** |
# | LGB v4 HMM | **9.7062** |
# 
# ### Overall median RMSE comparison:
# 
# | Candidate | Median RMSE |
# |---|---:|
# | PF/HMM50 | **5.7701** |
# | HMM | **5.8333** |
# | PF | **6.0032** |
# | Flat | **7.4134** |
# | LGB v4 HMM | **8.4654** |
# 
# ### Per-cut mean RMSE summary:
# 
# | Cut Fraction | Best Candidate | Best RMSE | LGB v4 HMM RMSE |
# |---:|---|---:|---:|
# | 0.50 | PF/HMM50 | **8.6297** | 10.4973 |
# | 0.65 | PF/HMM50 | **8.3154** | 9.5574 |
# | 0.80 | PF/HMM50 | **6.6214** | 9.0640 |
# 
# ### Success rate summary:
# 
# | Comparison | Success Rate |
# |---|---:|
# | LGB v4 HMM better than Flat | **49.33%** |
# | LGB v4 HMM better than PF | **36.00%** |
# | HMM better than PF | **46.67%** |
# | PF/HMM50 better than PF | **59.33%** |
# 
# ### Interpretation
# 
# The result showed that the L1-LGB v4 HMM model was not robust enough under multi-cut validation.
# 
# Although the LGB model had access to stronger engineered features and HMM posterior information, it performed worse than PF, HMM, PF/HMM50, and even the flat baseline on average. This suggests that the model may have learned patterns that fit the OOF setting but do not generalize well to hidden test intervals.
# 
# The most stable candidate in this validation was PF/HMM50. It achieved the best mean RMSE, best median RMSE, and also performed best across all three cut fractions.
# 
# This means that the direct PF/HMM combination was more reliable than using the LGB v4 HMM prediction as a standalone final prediction.
# 
# Decision
# 
# ### The main decision from this experiment was:
# 
# Do not use L1-LGB v4 HMM as a direct standalone submission.
# Do not use a large blend weight for LGB v4 HMM.
# Prefer PF/HMM50 as the safer candidate for external blending.
# If LGB v4 HMM is used, keep the blend weight very small, such as 5-10%.
# 
# The updated blending priority after this experiment became:
# 
# 1. Base 7.185 + Exp15A PF/HMM50
# 2. Base 7.185 + Exp13 PF/HMM50
# 3. Base 7.185 + Exp12 LGB v3 only as low-priority blend
# 4. Base 7.185 + Exp13 LGB v4 HMM only with very small weight
# Final Conclusion
# 
# Experiment 14 was a validation experiment, not mainly a leaderboard-improvement experiment.
# 
# Its most important finding was that PF/HMM50 is more stable than L1-LGB v4 HMM under multi-cut hidden-region validation.
# 
# Therefore, this experiment helped reject the risky LGB v4 HMM standalone path and redirected the next experiments toward conservative external blends using PF/HMM50.

# %% [markdown]
# ## Experiment 15: External Blend - Base 7.185 + Exp12 LGB v3
# 
# **Base notebook:** [ROGII PF Contact Gold Calibration Stack Base](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack-base/notebook?scriptVersionId=332959039)  
# **My experimental notebook:** [Fork of ROGII PF Contact Gold Calibration](https://www.kaggle.com/code/rokaiyasomapti/fork-of-rogii-pf-contact-gold-calibra-0b19e9?scriptVersionId=333170328)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.185** |
# | Experiment LB | **See Version 2** |
# | LB Reference | [Experiment Version 2](https://www.kaggle.com/code/rokaiyasomapti/fork-of-rogii-pf-contact-gold-calibra-0b19e9?scriptVersionId=333170328) |
# | Status | **External blend candidate** |
# 
# ### Objective
# 
# This experiment tested whether the Exp12 LGB v3 correction model could add a small useful signal on top of the stronger PF + Contact + Gold base.
# 
# The LGB v3 model was not used as a standalone replacement, because its pure prediction did not contain the full guarded geosteering stack. Instead, it was treated as an external residual-style candidate.
# 
# ### Change
# 
# The base submission remains the dominant prediction.
# 
# The experiment blends two final CSV-level predictions:
# 
# 
# final = (1 - w) * base_submission + w * lgb_v3_submission
# 
# where w is kept small so that the PF/contact/gold anchor is preserved.
# This is a submission-level blend only. It does not change:
# PF tracking;
# contact logic;
# gold calibration;
# selector rules;
# bimodal hedge logic.
# 
# ### Motivation
# 
# The previous experiments showed that strong gains rarely come from replacing the base path. Most aggressive corrections hurt because the base anchor is already strong.
# The LGB v3 model may still contain weak complementary signal, especially if it captures row-level residual structure that the PF/contact stack misses. A small blend tests this possibility while limiting damage.
# 
# ### Risk
# 
# The main risk is that the LGB v3 output may be correlated with existing errors or may move already-good wells away from the anchor.
# Because the blend happens after all base post-processing, any bad LGB movement directly affects the final submission. For that reason, the blend weight must stay conservative and should be audited by mean/p95/max movement before submission.
# 
# Checkpoints
# 
# Before submission, confirm:
# id_order_matches_sample = True
# row_count matches sample_submission
# no NaN in tvt
# mean/p95/max absolute movement vs base is small
# submission.csv is the blended file
# 
# ### Result
# 
# Pending final LB reading from Version 2.

# %% [markdown]
# ## Experiment 16: External Blend — Base 7.185 + Exp15A PF/HMM50
# 
# **Base notebook:** [ROGII PF Contact Gold Calibration Stack Base](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack-base/notebook?scriptVersionId=332959039)  
# **My experimental notebook:** [ROGII PF Contact Gold Calibration External Blend — Version 2](https://www.kaggle.com/code/rokaiyasomapti/rogii-pf-contact-gold-calibration-external-blend?scriptVersionId=333174670)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.185** |
# | Experiment LB | **See Version 2** |
# | LB Reference | [External Blend Version 2](https://www.kaggle.com/code/rokaiyasomapti/rogii-pf-contact-gold-calibration-external-blend?scriptVersionId=333174670) |
# | Status | **External Blend Candidate** |
# 
# ### Motivation
# 
# Experiment 15A generated a PF/HMM50 candidate by keeping the Experiment 12 LGB training pipeline unchanged and adding a test-time HMM helper. The goal of this experiment was to test whether that PF/HMM50 signal could improve the strong Base 7.185 submission through a conservative external blend.
# 
# The base notebook already had strong PF, Contact, Gold calibration, and guarded candidate logic. Therefore, instead of changing the internal base pipeline, this experiment only blends the final CSV output with the Exp15A PF/HMM50 candidate.
# 
# ### Core Mechanism
# 
# This experiment performs submission-level external blending.
# 
# The base prediction is taken from the base notebook output:
# 
# 
# base_submission = submission.csv from the base notebook
# 
# 
# ### The Experiment 15A candidate is:
# 
# submission_exp15a_pf_hmm50.csv
# 
# The Exp15A PF/HMM50 candidate was calculated as:
# 
# pf_hmm50 = 0.5 * pf_pred + 0.5 * hmm_mean
# 
# ### The final external blend is calculated as:
# 
# final_tvt = 0.90 * base_tvt + 0.10 * exp15a_pf_hmm50_tvt
# 
# No internal part of the base notebook was modified.
# 
# The following base components remained unchanged:
# 
# PF logic
# Contact logic
# Gold calibration
# Bimodal midpoint hedge
# Internal candidate pool
# Final guarded calibration
# Safety Checks
# 
# ### Before creating the final submission, the notebook verifies:
# 
# Base submission row count matches sample_submission.csv
# Exp15A PF/HMM50 row count matches sample_submission.csv
# ID order matches sample_submission.csv
# No duplicate IDs
# No missing tvt values
# No non-finite tvt values
# test_candidates_exp15a.csv is aligned
# Candidate pf_hmm50 matches submission_exp15a_pf_hmm50.csv
# pf_hmm50 = 0.5 * pf_pred + 0.5 * hmm_mean
# 
# The Exp15A training cache was also checked to confirm that HMM was not used as a training feature. HMM was only used at test time to create the PF/HMM50 candidate.
# 
# ### Generated Outputs
# 
# The experiment saves multiple blend files for comparison:
# 
# base_7185_submission.csv
# blend_base7185_exp15a_pfhmm50_90_10.csv
# blend_base7185_exp15a_pfhmm50_95_05.csv
# blend_base7185_exp15a_pfhmm50_85_15.csv
# submission.csv
# 
# ### The default Kaggle submission file is:
# 
# submission.csv
# 
# ### This file corresponds to:
# 
# 0.90 * Base 7.185 + 0.10 * Exp15A PF/HMM50
# 
# ### Interpretation
# 
# This experiment is conservative because the Exp15A PF/HMM50 candidate only contributes 10% to the final prediction. The base submission remains the main driver of the final output.
# 
# The reason for choosing PF/HMM50 is that the multi-cut validation experiments showed that PF/HMM50 was more stable than the direct LGB v4 HMM prediction. Since Exp15A does not change the LGB training features and only adds HMM at test time, it acts as a safer trajectory-level candidate rather than a fully learned replacement model.
# 
# ### Decision
# 
# The main submission candidate from this experiment is:
# 
# blend_base7185_exp15a_pfhmm50_90_10.csv
# 
# and the final Kaggle-ready file is:
# 
# submission.csv
# 
# ### The preferred blend is:
# 
# 0.90 * Base 7.185 + 0.10 * Exp15A PF/HMM50
# 
# The 95/05 and 85/15 blend files were saved only for comparison. The 90/10 blend is the main candidate because it keeps the base model dominant while still testing the Exp15A PF/HMM50 signal.
# 
# ### Final Conclusion
# 
# Experiment 16 tested a conservative external blend between the strong Base 7.185 notebook and the Exp15A PF/HMM50 candidate.
# 
# The experiment does not modify the base model internally. It only applies a small CSV-level blend after the base submission is created.
# 
# This makes the experiment lower-risk than replacing the base prediction with a standalone LGB or HMM-based model.

# %% [markdown]
# ## Experiment 17: External Blend — Base + Exp13 PF/HMM50
# 
# **Base notebook:** [ROGII PF Contact Gold Calibration Stack Base](https://www.kaggle.com/code/foysalemonshanto/rogii-pf-contact-gold-calibration-stack-base/notebook?scriptVersionId=332959039)  
# **My experimental notebook:** [ROGII PF Contact Gold Calibration External Blend](https://www.kaggle.com/code/rokaiyasomapti/rogii-pf-contact-gold-calibration-external-blend)
# 
# | Item | Value |
# |---|---:|
# | Base LB | **7.185** |
# | Experiment LB | **See Version 2** |
# | LB Reference | [External Blend Version 2](https://www.kaggle.com/code/rokaiyasomapti/rogii-pf-contact-gold-calibration-external-blend) |
# | Status | **External Blend Candidate** |
# 
# ### Motivation
# 
# Experiment 13 generated two useful candidates: the direct `LGB v4 HMM` prediction and the simpler `PF/HMM50` trajectory candidate. Later validation showed that the direct LGB v4 HMM prediction was less stable under hidden-region simulation, while the PF/HMM50 candidate was more robust.
# 
# This experiment tested whether a small external blend between the strong base submission and the Exp13 PF/HMM50 candidate could improve leaderboard performance without changing the internal logic of the base notebook.
# 
# The main goal was to keep the strong PF + Contact + Gold calibrated base model as the anchor, while adding a small amount of Exp13 PF/HMM50 signal.
# 
# ### Core Mechanism
# 
# This experiment performs only CSV-level external blending.
# 
# The base notebook output is used as the frozen anchor:
# 
# base_submission = submission.csv from the base notebook
# 
# The Experiment 13 candidate is:
# 
# submission_exp13_pf_hmm50.csv
# 
# The PF/HMM50 candidate was generated as:
# 
# pf_hmm50 = 0.5 * pf_pred + 0.5 * hmm_mean
# 
# The final external blend is calculated as:
# 
# final_tvt = 0.90 * base_tvt + 0.10 * exp13_pf_hmm50_tvt
# 
# No internal part of the base notebook was modified.
# 
# The following components remained unchanged:
# 
# PF logic
# Contact logic
# Gold calibration
# Bimodal midpoint hedge
# Internal candidate pool
# Final guarded calibration
# Safety Checks
# 
# Before creating the final blend, the notebook verifies:
# 
# Base submission row count matches sample_submission.csv
# Exp13 PF/HMM50 row count matches sample_submission.csv
# ID order matches sample_submission.csv
# No duplicate IDs
# No missing tvt values
# No non-finite tvt values
# test_candidates_exp13.csv is aligned
# Candidate pf_hmm50 matches submission_exp13_pf_hmm50.csv
# pf_hmm50 = 0.5 * pf_pred + 0.5 * hmm_mean
# Generated Outputs
# 
# ### The experiment saves multiple blend files for comparison:
# 
# base_7185_submission.csv
# blend_base7185_exp13_pfhmm50_90_10.csv
# blend_base7185_exp13_pfhmm50_95_05.csv
# blend_base7185_exp13_pfhmm50_85_15.csv
# blend_base7185_exp13_lgbv4hmm_95_05.csv
# blend_base7185_exp13_lgbv4hmm_90_10.csv
# submission.csv
# 
# The default Kaggle submission file is:
# 
# submission.csv
# 
# ### This file corresponds to:
# 
# 0.90 * Base + 0.10 * Exp13 PF/HMM50
# 
# ### Interpretation
# 
# This experiment is conservative because the Exp13 candidate only contributes 10% to the final prediction. The base submission remains the main driver of the final result.
# 
# The reason for choosing PF/HMM50 instead of the direct LGB v4 HMM candidate is that Experiment 14 multi-cut validation showed PF/HMM50 to be more stable. The LGB v4 HMM prediction was valid, but it showed weaker robustness under simulated hidden-region validation.
# 
# Therefore, this experiment tests the safer Exp13 signal rather than aggressively trusting the learned LGB correction model.
# 
# ### Decision
# 
# The main submission candidate from this experiment is:
# 
# blend_base7185_exp13_pfhmm50_90_10.csv
# 
# and the final Kaggle-ready file is:
# 
# submission.csv
# 
# ### The preferred blend is:
# 
# 0.90 * Base + 0.10 * Exp13 PF/HMM50
# 
# The LGB v4 HMM blend files were saved only as backup candidates. They should be treated more cautiously because the multi-cut validation did not support LGB v4 HMM as strongly as PF/HMM50.
# 
# ### Final Conclusion
# 
# Experiment 17 tested a conservative external blend between the strong base notebook and the Exp13 PF/HMM50 candidate.
# 
# The experiment does not change the base model internally. It only applies a small CSV-level blend after the base submission is created.
# 
# This makes the experiment low-risk compared to replacing the base prediction completely with the Exp13 model.
