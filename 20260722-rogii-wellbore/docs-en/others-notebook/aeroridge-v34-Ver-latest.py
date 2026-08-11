# extracted from reproduce-strongest-reference-aeroridge-v34.ipynb

# ROGII Contact and U Restore: Codex Q2522 Consensus Gate

This is our experiment `98`. It starts from the fresh
Q0522 control and computes every optional shape signal again from the current
competition-run features.

## Signal

- Q branch total: **2.522 ft**
- feature mode: **consensus**
- residual weight: **0.120**
- row correction cap: **0.50 ft**

The correction never replays a downloaded submission vector. SP45 and learned
trajectory components are outputs of this notebook's current execution, so the
same code is evaluated on the hidden rerun rather than on visible-row geometry.

## Why This Candidate

Keeps the exact Q2522 leader geometry, then applies only a small hidden-recomputed correction where SP45 and learned trajectories agree. The same agreement gate was the best-ranked shape signal within the Q0522 control pack.

## Integrity

- Reference executable SHA256: `82cdc15487d24a6178afa60bd7cb3376b40ea27ccec3ef3b17e2526782ccfa08`
- Current-run component IDs must align exactly with Q0522
- Schema, finiteness, correction RMS/max, and cap hits are audited
- Final file: `/kaggle/working/submission.csv`
- GPU enabled, internet disabled, notebook remains public

# GS1.30 + Q0522 Full-Source Frontier | VISUALS

## Public-source likelihood calibration plus an interior branch continuation

The 45-cell base is hjyact Version 2 (`scriptVersionId=337064157`), whose
public notebook reports **6.568**.  Q0522 then continues the already accepted
two-foot branch move by **0.522 ft** on its single guarded target well.  The
value was fixed from the earlier public 2-ft and 3-ft controls; it is an
interior response-curve hypothesis, not a claimed score.

The PF likelihood multiplier is **1.30**.  Its merged 48-well local
selector RMSE is **10.597562**.  The full source reruns before
Q0522, the transaction validates the exact base hash or numeric signature,
and the final schema audit follows the transaction.

Four figures execute only after scoring and prove `submission.csv` is
unchanged.  This version remains unscored until its own notebook-origin row is
`COMPLETE` with a nonempty public score.

# ROGII Contact-Gated Stratigraphic Alignment

This notebook builds a target-free TVT trajectory from three signals: a ridge/PF anchor, a learned trajectory branch, and contact-based self-verification on the visible prefix. Each correction layer is allowed to modify `submission.csv` only when its local diagnostic supports the move.

## Prediction Flow

The pipeline is ordered from broad fallbacks to highly local self-verification.

1. Build a ridge/PF artifact trajectory and a physical/PF selector trajectory.
2. Blend them into an SP45-style anchor and apply robust projection in normalized MD space.
3. Build the learned trajectory branch from mounted pretrained boosters.
4. Blend the projected anchor and the learned branch.
5. Apply guarded same-well contact reconstruction only when the visible prefix proves compatibility.
6. Run visible-prefix calibration either as an audit or as a bounded final correction.
7. Audit `submission.csv` against `sample_submission.csv`.

The default `contact_gated_anchor` profile keeps the self-verified contact anchor as the final trajectory. The visible-prefix profiles are separate experiments: they let the best prefix-tested candidate make a bounded final move after the same contact guard is re-applied.

## Main Trajectory Equations

The first anchor mixes the ridge/PF artifact path and the selector path:

$$
T_i^{A}=w_rT_i^{ridge}+(1-w_r)T_i^{selector},
\qquad w_r=0.30.
$$

The projection layer denoises the implied stratigraphic level

$$
U_i=T_i+Z_i.
$$

With normalized measured depth \(s_i\), a robust polynomial estimates

$$
\hat U_i=U_{last}+f_d(s_i),
$$

and the projected path is

$$
T_i^{proj}=(1-\lambda_p)T_i^{A}+\lambda_p(\hat U_i-Z_i),
\qquad \lambda_p=0.75.
$$

The learned branch is then blended with the projected anchor:

$$
T_i^{blend}=w_sT_i^{proj}+(1-w_s)T_i^{learned}.
$$

The default anchor profile uses

$$
w_s=0.60.
$$

The variation notebooks change only \(w_s\) or the final visible-prefix selection rule.

## Heel Calibration and Bimodal Hedge

GR matching is sensitive to gain and offset differences between the horizontal well and the typewell. On the visible heel \(H_w\), the notebook fits

$$
(\alpha_w,\beta_w)=\arg\min_{\alpha,\beta}\sum_{i\in H_w}\left(G_i^{hw}-(\alpha G^{tw}(T_i)+\beta)\right)^2.
$$

The hidden horizontal GR is mapped back to typewell scale before datum scanning:

$$
\tilde G_i^{hw}=\frac{G_i^{hw}-\beta_w}{\alpha_w}.
$$

For a candidate datum shift \(\Delta\), the scan score is

$$
J_w(\Delta)=\frac{1}{|M_w|}\sum_{i\in M_w}\operatorname{clip}\left(\frac{\tilde G_i^{hw}-G^{tw}(T_i^{base}+\Delta)}{s_w},-6,6\right)^2.
$$

When the scan has two plausible minima, the hedge avoids over-committing to one branch. The effective branch probability is shrunk by prefix trust:

$$
p_{eff}=\tau_w p_{scan}+(1-\tau_w)\cdot 0.5.
$$

The hedged trajectory is then the posterior mean of the two candidate branches. Active bimodal wells can be protected from later visible-prefix override.

## Guarded Contact Reconstruction

For a reference formation \(c\), the contact-derived TVT path is

$$
T_i^{contact}(c)=T_c^{typewell}-(Z_i-C_i)+b_c,
$$

where the well-specific bias is estimated on the matching train horizontal well:

$$
b_c=\operatorname{mean}_{j\in train}
\left[T_j-\left(T_c^{typewell}-(Z_j-C_j)\right)\right].
$$

This path is accepted only after a visible-prefix self-check:

$$
\operatorname{RMSE}
\left(
\operatorname{interp}_{MD}(T^{contact}_{train},MD_i^{test}),
T_i^{input}
\right)<\epsilon,
\qquad \epsilon=1.0\ \mathrm{ft}.
$$

If the guard passes, hidden rows inside the train MD range are replaced by the MD-interpolated contact path. If the guard fails, the blended trajectory is left untouched.

## Control Panel

The first code cell is the only visible code cell. It selects the final visible-prefix profile or one diagnostic ablation. Heavy diagnostics are off by default; the submission path keeps full PF precision and uses mounted pretrained artifacts when available.

# Profile choices:
# - vp_balanced_final: current submission default; visible-prefix profile output becomes final after contact guard.
# - vp_conservative_final: weaker visible-prefix profile, kept as a conservative comparison.
# - contact_gated_anchor*: diagnostic ablations; they keep the pre-visible-prefix anchor and have underperformed.
# - bimodal_guarded: contact_gated_anchor plus bimodal hedge protection.
SUBMISSION_PROFILE = 'vp_balanced_modelpkg_005'

PROFILE_PRESETS = {
    'contact_gated_anchor': dict(
        visible_prefix_profile='conservative',
        visible_prefix_final_selection='self_verified_anchor',
        visible_prefix_cut_fracs=(0.50, 0.65, 0.75),
        sp45_blend_weight=0.60,
        run_guarded_overlap_override=True,
        run_visible_prefix_calibration=True,
        run_bimodal_detector=False,
        run_vp_bimodal_guard=False,
        run_model_package_correction=False,
    ),
    'contact_gated_anchor_w058': dict(
        visible_prefix_profile='conservative',
        visible_prefix_final_selection='self_verified_anchor',
        visible_prefix_cut_fracs=(0.50, 0.65, 0.75),
        sp45_blend_weight=0.58,
        run_guarded_overlap_override=True,
        run_visible_prefix_calibration=True,
        run_bimodal_detector=False,
        run_vp_bimodal_guard=False,
        run_model_package_correction=False,
    ),
    'contact_gated_anchor_w055': dict(
        visible_prefix_profile='conservative',
        visible_prefix_final_selection='self_verified_anchor',
        visible_prefix_cut_fracs=(0.50, 0.65, 0.75),
        sp45_blend_weight=0.55,
        run_guarded_overlap_override=True,
        run_visible_prefix_calibration=True,
        run_bimodal_detector=False,
        run_vp_bimodal_guard=False,
        run_model_package_correction=False,
    ),
    'vp_conservative_final': dict(
        visible_prefix_profile='conservative',
        visible_prefix_final_selection='profile',
        visible_prefix_cut_fracs=(0.50, 0.65, 0.75),
        sp45_blend_weight=0.60,
        run_guarded_overlap_override=True,
        run_visible_prefix_calibration=True,
        run_bimodal_detector=False,
        run_vp_bimodal_guard=False,
        run_model_package_correction=False,
    ),
    'vp_balanced_final': dict(
        visible_prefix_profile='balanced',
        visible_prefix_final_selection='profile',
        visible_prefix_cut_fracs=(0.50, 0.65, 0.75),
        sp45_blend_weight=0.60,
        run_guarded_overlap_override=True,
        run_visible_prefix_calibration=True,
        run_bimodal_detector=False,
        run_vp_bimodal_guard=False,
        run_model_package_correction=False,
    ),

    'vp_balanced_cut557084': dict(
        visible_prefix_profile='balanced',
        visible_prefix_final_selection='profile',
        visible_prefix_cut_fracs=(0.55, 0.70, 0.84),
        sp45_blend_weight=0.60,
        run_guarded_overlap_override=True,
        run_visible_prefix_calibration=True,
        run_bimodal_detector=False,
        run_vp_bimodal_guard=False,
        run_model_package_correction=False,
    ),
    'vp_balanced_modelpkg_005': dict(
        visible_prefix_profile='balanced',
        visible_prefix_final_selection='profile',
        visible_prefix_cut_fracs=(0.50, 0.65, 0.75),
        sp45_blend_weight=0.60,
        run_guarded_overlap_override=True,
        run_visible_prefix_calibration=True,
        run_bimodal_detector=False,
        run_vp_bimodal_guard=False,
        run_model_package_correction=True,
        model_package_gated_max_weight=0.00425,
        model_package_gated_scale=6.0,
    ),
    'vp_balanced_modelpkg_010': dict(
        visible_prefix_profile='balanced',
        visible_prefix_final_selection='profile',
        visible_prefix_cut_fracs=(0.50, 0.65, 0.75),
        sp45_blend_weight=0.60,
        run_guarded_overlap_override=True,
        run_visible_prefix_calibration=True,
        run_bimodal_detector=False,
        run_vp_bimodal_guard=False,
        run_model_package_correction=True,
        model_package_gated_max_weight=0.010,
        model_package_gated_scale=6.0,
    ),
    'bimodal_guarded': dict(
        visible_prefix_profile='conservative',
        visible_prefix_final_selection='self_verified_anchor',
        visible_prefix_cut_fracs=(0.50, 0.65, 0.75),
        sp45_blend_weight=0.60,
        run_guarded_overlap_override=True,
        run_visible_prefix_calibration=True,
        run_bimodal_detector=True,
        run_vp_bimodal_guard=True,
        run_model_package_correction=False,
    ),
}

if SUBMISSION_PROFILE not in PROFILE_PRESETS:
    raise ValueError(f'SUBMISSION_PROFILE must be one of {sorted(PROFILE_PRESETS)}')

_profile = PROFILE_PRESETS[SUBMISSION_PROFILE]

# Data and artifact roots.
COMPETITION_DATA_ROOT = '/kaggle/input/competitions/rogii-wellbore-geology-prediction'
RIDGE_ARTIFACT_ROOT = '/kaggle/input/datasets/ravaghi/wellbore-geology-prediction-artifacts'
KOOLBOX_OFFLINE_ROOTS = (
    '/kaggle/input/datasets/phongnguyn23021656/koolbox-offline',
    '/kaggle/input/koolbox-offline',
    '/kaggle/input/pm-125564438-at-07-07-2026-07-28-00',
)
LEARNED_MODEL_ROOTS = (
    '/kaggle/input/datasets/fleongg/rogii-claude-models-pub',
    '/kaggle/input/rogii-claude-models-pub',
)

# SP45/PF anchor path.
SP45_RIDGE_MODEL_WEIGHT = 0.30
SP45_SELECTOR_WEIGHT = 0.70
SP45_SELECTOR_N_PARTICLES = 500
SP45_SELECTOR_N_SEEDS = 128
SELECTOR_PF_SEEDS = SP45_SELECTOR_N_SEEDS
SELECTOR_PF_RETURN_STD = False
SP45_PROJECTION_DEGREE = 3
SP45_PROJECTION_BLEND_WEIGHT = 0.75

# Optional diagnostics. The submission path keeps full PF precision but disables all-train CV sweeps.
RUN_CV_REPORT = False
RUN_FULL_STACK_CV_ABLATION = False
CV_N_WELLS = 250
CV_ABLATION_N_WELLS = 250
CV_N_SPLITS = 5
CV_SEED = 0
CV_SELECTOR_PF_SEEDS = 24
ABLATION_VP_POSTERIOR_TRUST_ONLY = False

# Bimodal datum detector for PF/beam disagreement.
RUN_BIMODAL_DETECTOR = bool(_profile['run_bimodal_detector'])
RUN_BIMODAL_SELECTOR_HEDGE = RUN_BIMODAL_DETECTOR
BIMODAL_DZ_RANGE = 20.0
BIMODAL_DZ_STEP = 0.5
BUNDLE_MIN = 10.0
BUNDLE_MAX = 20.0
BIMODAL_J_RATIO_EPS = 0.15
SCAN_MIN_SEP = 8.0
BIMODAL_TEMP = 0.75
RUN_ADAPTIVE_TEMP = True
T_MIN = 0.25
T_MAX = 4.0
RUN_PREFIX_TRUST_GATE = True
TRUST_MIN_PREFIX_ROWS = 60
TRUST_FALLBACK = 0.0
TRUST_KAPPA = 1.0
USE_STRUCTURAL_P_FALLBACK = False
BIMODAL_FORCE_MIDPOINT = False
BIMODAL_TRIGGER_MIN_MEDIAN_DIFF = 12.0
BIMODAL_TRIGGER_MIN_P90_DIFF = 18.0
BIMODAL_TRIGGER_MIN_BIG_DIFF_FRAC = 0.18
BIMODAL_TRIGGER_BIG_DIFF_THRESHOLD = 15.0
BIMODAL_MIN_VALID_GR_ROWS = 80

# Heel-calibrated GR matching. This is read-only unless the bimodal detector is enabled.
RUN_HEEL_CALIBRATION = True
RUN_HEEL_LOCALIZATION_REPORT = False
RUN_HEEL_ABLATION_GRID = False
HEEL_MIN_ROWS = 40
HEEL_LOCALIZATION_TOLERANCE = 2.0
HEEL_ALPHA_MIN = 0.25
HEEL_ALPHA_MAX = 4.0
HEEL_BETA_ABS_MAX = 500.0

# Stretch matcher levers. Off until validated with the diagnostic harness.
RUN_GR_FFT_DENOISE = False
RUN_SEQ_MATCHER = False

# Retained comparison layers. Keep off unless deliberately probing them.
RUN_EXACT_MATCH_RECOVERY = False
RUN_OVERLAP_DRY_RUN_PROBE = True

# Learned-trajectory blend.
SP45_BLEND_WEIGHT = float(_profile['sp45_blend_weight'])
SP45_BLEND_CANDIDATE_WEIGHTS = tuple(sorted(set((0.50, 0.52, 0.55, 0.58, 0.60, SP45_BLEND_WEIGHT))))

# Guarded same-well correction.
RUN_GUARDED_OVERLAP_OVERRIDE = bool(_profile['run_guarded_overlap_override'])
GUARDED_OVERRIDE_REF_COL = 'EGFDU'
GUARDED_OVERRIDE_REF_COLS = ('EGFDU', 'ASTNU', 'ANCC', 'ASTNL', 'EGFDL', 'BUDA')
GUARDED_OVERRIDE_MIN_VALID_PHYS_ROWS = 100
GUARDED_OVERRIDE_MIN_KNOWN_PREFIX_ROWS = 50
GUARDED_OVERRIDE_PREFIX_RMSE_LIMIT = 1.0

# Visible-prefix calibration overlay.
RUN_VISIBLE_PREFIX_CALIBRATION = bool(_profile['run_visible_prefix_calibration'])
VISIBLE_PREFIX_PROFILE = str(_profile['visible_prefix_profile'])
VISIBLE_PREFIX_FINAL_SELECTION = str(_profile.get('visible_prefix_final_selection', 'self_verified_anchor'))
VISIBLE_PREFIX_INCLUDE_PF = True
VISIBLE_PREFIX_CAL_SEEDS = 24
VISIBLE_PREFIX_FINAL_SEEDS = 48
VISIBLE_PREFIX_PARTICLES = 350
VISIBLE_PREFIX_CUT_FRACS = tuple(float(x) for x in _profile.get('visible_prefix_cut_fracs', (0.50, 0.65, 0.75)))
VISIBLE_PREFIX_MAX_WELLS = 1_000_000
RUN_VP_BIMODAL_GUARD = bool(_profile['run_vp_bimodal_guard'])
VP_SKIP_REQUIRES_LOW_TRUST = False
VP_LOW_TRUST_THRESHOLD = 0.25
VISIBLE_PREFIX_SKIP_BIMODAL_WELLS = RUN_VP_BIMODAL_GUARD

# Saved-model correction. This is off for the contact-gated anchor profiles.
RUN_MODEL_PACKAGE_CORRECTION = bool(_profile.get('run_model_package_correction', False))
MODEL_PACKAGE_ROOTS = (
    '/kaggle/input/datasets/pilkwang/rogii-model-package',
    '/kaggle/input/rogii-model-package',
)
MODEL_PACKAGE_REQUIRE = False
MODEL_PACKAGE_ALLOW_AUTO_SEARCH = False
MODEL_PACKAGE_GATED_MAX_WEIGHT = float(_profile.get('model_package_gated_max_weight', 0.01))
MODEL_PACKAGE_GATED_SCALE = float(_profile.get('model_package_gated_scale', 6.0))
MODEL_PACKAGE_GATED_CANDIDATES = (0.005, 0.010, 0.0125, 0.015, 0.020)
MODEL_PACKAGE_DIFF_P95_DISABLE = 25.0

print('submission profile:', SUBMISSION_PROFILE)
print('sp45_blend_weight:', SP45_BLEND_WEIGHT)
print('visible_prefix_profile:', VISIBLE_PREFIX_PROFILE)
print('visible_prefix_final_selection:', VISIBLE_PREFIX_FINAL_SELECTION)
print('visible_prefix_cut_fracs:', VISIBLE_PREFIX_CUT_FRACS)
print('guarded_overlap_override:', RUN_GUARDED_OVERLAP_OVERRIDE)

# Runtime bridge for the visible-prefix implementation.
import os
os.environ['ROGII_GOLD_PREFIX_CAL'] = '1' if RUN_VISIBLE_PREFIX_CALIBRATION else '0'
os.environ['ROGII_GOLD_PROFILE'] = VISIBLE_PREFIX_PROFILE
os.environ['ROGII_GOLD_INCLUDE_PF'] = '1' if VISIBLE_PREFIX_INCLUDE_PF else '0'
os.environ['ROGII_GOLD_CAL_SEEDS'] = str(int(VISIBLE_PREFIX_CAL_SEEDS))
os.environ['ROGII_GOLD_FINAL_SEEDS'] = str(int(VISIBLE_PREFIX_FINAL_SEEDS))
os.environ['ROGII_GOLD_PARTICLES'] = str(int(VISIBLE_PREFIX_PARTICLES))
os.environ['ROGII_GOLD_CUT_FRACS'] = ','.join(str(float(x)) for x in VISIBLE_PREFIX_CUT_FRACS)
os.environ['ROGII_GOLD_MAX_WELLS'] = str(int(VISIBLE_PREFIX_MAX_WELLS))
os.environ['ROGII_GOLD_FINAL_SELECTION'] = VISIBLE_PREFIX_FINAL_SELECTION
os.environ['ROGII_GOLD_SKIP_BIMODAL'] = '1' if RUN_VP_BIMODAL_GUARD else '0'
os.environ['ROGII_GOLD_VP_SKIP_REQUIRES_LOW_TRUST'] = '1' if VP_SKIP_REQUIRES_LOW_TRUST else '0'
os.environ['ROGII_GOLD_VP_LOW_TRUST_THRESHOLD'] = str(float(VP_LOW_TRUST_THRESHOLD))
os.environ['ROGII_GOLD_CONTACT_OVERRIDE'] = '1' if RUN_GUARDED_OVERLAP_OVERRIDE else '0'

import sys, os, glob, subprocess, types
from pathlib import Path

_koolbox_roots = [Path(p) for p in globals().get('KOOLBOX_OFFLINE_ROOTS', ()) if str(p).strip()]
_koolbox_root = next((p for p in _koolbox_roots if p.exists()), None)
if _koolbox_root is None:
    # Some notebook environments mount koolbox through a package-manager input
    # whose folder name changes. Search only for koolbox-looking wheels/folders.
    _auto_hits = []
    for _pat in ('/kaggle/input/**/koolbox*.whl', '/kaggle/input/**/koolbox*'):
        _auto_hits.extend(Path(x).parent if Path(x).suffix == '.whl' else Path(x) for x in glob.glob(_pat, recursive=True))
    _koolbox_root = next((p for p in sorted(set(_auto_hits)) if p.exists()), None)


def _wheel_matches_runtime(path):
    name = Path(path).name
    if ' (' in name or not name.endswith('.whl'):
        return False
    parts = name[:-4].split('-')
    if len(parts) < 5:
        return False
    py_tag, abi_tag, _platform_tag = parts[-3], parts[-2], parts[-1]
    runtime_tag = f'cp{sys.version_info.major}{sys.version_info.minor}'
    if py_tag.startswith('cp') and py_tag != runtime_tag:
        return False
    if abi_tag.startswith('cp') and abi_tag != runtime_tag:
        return False
    return py_tag in {'py2.py3', 'py3', runtime_tag} or py_tag.startswith(runtime_tag)


def _install_or_path_koolbox(root):
    if root is None:
        return False
    print('using koolbox dir:', root)
    whls = [w for w in sorted(root.glob('**/*.whl')) if _wheel_matches_runtime(w)]
    if whls:
        for w in whls:
            print('install', w)
            subprocess.run(['pip', 'install', '--no-deps', str(w)], check=False)
    else:
        sys.path.insert(0, str(root))
        for sub in root.iterdir():
            if sub.is_dir():
                sys.path.insert(0, str(sub))
    return True


def _make_koolbox_fallback_module():
    import numpy as _np
    import joblib as _joblib
    from pathlib import Path as _Path
    from sklearn.base import clone as _clone
    from sklearn.metrics import root_mean_squared_error as _rmse
    from sklearn.model_selection import GroupKFold as _GroupKFold, KFold as _KFold

    def _take(X, idx):
        return X.iloc[idx] if hasattr(X, 'iloc') else X[idx]

    def _score(metric, y_true, y_pred):
        try:
            return float(metric(y_true, y_pred)) if callable(metric) else float(_rmse(y_true, y_pred))
        except Exception:
            return float(_rmse(y_true, y_pred))

    def _drop_fit_keys(kwargs, keys):
        out = dict(kwargs or {})
        for key in keys:
            out.pop(key, None)
        return out

    class Trainer:
        def __init__(self, estimator, task='regression', metric=None, cv=None, cv_args=None,
                     use_early_stopping=False, verbose=False, save=False, save_path=None):
            self.estimator = estimator
            self.task = task
            self.metric = metric or _rmse
            self.cv = cv
            self.cv_args = cv_args or {}
            self.use_early_stopping = bool(use_early_stopping)
            self.verbose = bool(verbose)
            self.save = bool(save)
            self.save_path = save_path
            self.models = []
            self.oof_preds = None
            self.fold_scores = []
            self.overall_score = None

        def _splits(self, X, y):
            groups = self.cv_args.get('groups')
            cv = self.cv
            if cv is None:
                cv = _GroupKFold(n_splits=5) if groups is not None else _KFold(n_splits=5, shuffle=True, random_state=42)
            try:
                return list(cv.split(X, y, groups=groups))
            except TypeError:
                return list(cv.split(X, y))

        def _fit_one(self, estimator, X_tr, y_tr, X_va=None, y_va=None, fit_args=None):
            fit_kwargs = dict(fit_args or {})
            if self.use_early_stopping and X_va is not None and y_va is not None:
                mod = estimator.__class__.__module__.lower()
                name = estimator.__class__.__name__.lower()
                if 'lightgbm' in mod or 'lgbm' in name:
                    fit_kwargs.setdefault('eval_set', [(X_va, y_va)])
                elif 'catboost' in mod or 'catboost' in name:
                    fit_kwargs.setdefault('eval_set', (X_va, y_va))
            try:
                estimator.fit(X_tr, y_tr, **fit_kwargs)
            except TypeError:
                estimator.fit(X_tr, y_tr, **_drop_fit_keys(fit_kwargs, [
                    'callbacks', 'eval_metric', 'eval_set', 'early_stopping_rounds', 'use_best_model', 'verbose'
                ]))
            return estimator

        def fit(self, X, y, fit_args=None):
            y_arr = _np.asarray(y, dtype=float)
            oof = _np.full(len(y_arr), _np.nan, dtype=float)
            self.models = []
            self.fold_scores = []
            for fold, (tr_idx, va_idx) in enumerate(self._splits(X, y_arr), start=1):
                est = _clone(self.estimator)
                X_tr = _take(X, tr_idx); X_va = _take(X, va_idx)
                y_tr = y_arr[tr_idx]; y_va = y_arr[va_idx]
                est = self._fit_one(est, X_tr, y_tr, X_va, y_va, fit_args=fit_args)
                pred = _np.asarray(est.predict(X_va), dtype=float)
                oof[va_idx] = pred
                score = _score(self.metric, y_va, pred)
                self.fold_scores.append(score)
                self.models.append(est)
                if self.verbose:
                    print(f'fallback Trainer fold {fold}: {score:.5f}')
            if not _np.isfinite(oof).all():
                raise RuntimeError('fallback Trainer produced incomplete OOF predictions')
            self.oof_preds = oof
            self.overall_score = _score(self.metric, y_arr, oof)
            if self.save and self.save_path:
                out_dir = _Path(self.save_path)
                out_dir.mkdir(parents=True, exist_ok=True)
                _joblib.dump(self, out_dir / 'trainer.pkl')
            return self

        def predict(self, X):
            if not self.models:
                raise RuntimeError('Trainer has no fitted fold models')
            preds = [_np.asarray(model.predict(X), dtype=float) for model in self.models]
            return _np.mean(preds, axis=0)

    Trainer.__module__ = 'koolbox'
    Trainer.__qualname__ = 'Trainer'
    module = types.ModuleType('koolbox')
    module.Trainer = Trainer
    module.__file__ = '<fallback koolbox Trainer shim>'
    return module


_koolbox_mode = 'fallback'
try:
    _install_or_path_koolbox(_koolbox_root)
    import koolbox as _koolbox_probe
    _koolbox_mode = 'external'
except Exception as _e:
    print('koolbox external unavailable; using fallback Trainer shim:', _e)
    sys.modules['koolbox'] = _make_koolbox_fallback_module()
    import koolbox as _koolbox_probe

print('koolbox mode:', _koolbox_mode, '| module:', getattr(_koolbox_probe, '__file__', '<unknown>'))

from lightgbm import LGBMRegressor, log_evaluation, early_stopping
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge
from catboost import CatBoostRegressor
from scipy.spatial import cKDTree
from scipy.signal import savgol_filter
from joblib import Parallel, delayed
from koolbox import Trainer
from pathlib import Path
from numba import njit
import matplotlib.pyplot as plt
import multiprocessing
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
import joblib
import time
import glob
import os

warnings.filterwarnings("ignore")

class CFG:
    dataset_path = Path(COMPETITION_DATA_ROOT)
    artifacts_path = Path(RIDGE_ARTIFACT_ROOT)

    seed = 42
    n_splits = 5
    cv = GroupKFold(n_splits=n_splits)

    metric = root_mean_squared_error


def _safe_competition_data_root():
    root = globals().get('COMPETITION_DATA_ROOT', None)
    if root is not None:
        return root
    cfg = globals().get('CFG', None)
    if cfg is not None:
        if hasattr(cfg, 'dataset_path'):
            return getattr(cfg, 'dataset_path')
        if hasattr(cfg, 'DATA'):
            return getattr(cfg, 'DATA')
    return '.'

SELECTOR_N_EVAL_THRESHOLD = 4840.0
SELECTOR_Z_SPAN_THRESHOLDS = (136.73000000000016, 185.5133333333342)

SELECTOR_BIN_VARIANTS = {
    0: 'pf_scale_5_hold_0.2',
    1: 'pf_scale_3_hold_0.15',
    2: 'pf_scale_12_beam_0.2_hold_0.15',
    3: 'pf_scale_5_hold_0.15',
    4: 'pf_scale_5_beam_0.05_hold_0.05',
    5: 'pf_scale_12_beam_0.2_hold_0.05',
}

SELECTOR_GLOBAL_VARIANT = 'pf_scale_8_hold_0.2'
SELECTOR_SCALES = (3.0, 5.0, 8.0, 12.0)

FORMATION_COLS = ['ANCC', 'ASTNU', 'ASTNL', 'EGFDU', 'EGFDL', 'BUDA']

BEAM_CONFIGS = [
    (10, 20.0, 144.0, 2),
    (10,  8.0,  64.0, 2),
    ( 8, 35.0, 220.0, 1),
    (10, 14.0,  90.0, 5),
    (20,  4.0,  36.0, 3),
    (12, 12.0, 100.0, 3),
    (15, 25.0, 180.0, 2),
    (20, 30.0, 200.0, 2),
    (15, 10.0,  80.0, 4),
    (25,  6.0,  50.0, 3),
    (10, 40.0, 300.0, 1),
    (12, 18.0, 120.0, 5),
    (30,  8.0,  70.0, 2),
    (10, 50.0, 400.0, 0),
]


def tvt_from_contacts(hw_tr, tw_tr, ref_col='EGFDU'):
    tw_g = tw_tr.dropna(subset=['Geology'])
    ref_tvt = tw_g[tw_g['Geology'] == ref_col]['TVT'].min()
    if np.isnan(ref_tvt):
        ref_col = tw_g['Geology'].iloc[0]
        ref_tvt = tw_g[tw_g['Geology'] == ref_col]['TVT'].min()
    offset = (hw_tr['TVT'] - (ref_tvt - (hw_tr['Z'] - hw_tr[ref_col]))).mean()
    return ref_tvt - (hw_tr['Z'] - hw_tr[ref_col]) + offset


def load_well(wid, split='train'):
    base = CFG.dataset_path / split
    hw = pd.read_csv(base / f'{wid}__horizontal_well.csv')
    tw = pd.read_csv(base / f'{wid}__typewell.csv')
    return hw, tw


def run_particle_filter(hw, tw, n_particles=500, seed=42):
    tw_s   = tw.sort_values('TVT')
    tw_tvt = tw_s['TVT'].values.astype(float)
    tw_gr  = tw_s['GR'].fillna(tw_s['GR'].mean()).values.astype(float)

    kn = hw[hw['TVT_input'].notna()]
    ev = hw[hw['TVT_input'].isna()]
    if len(ev) == 0:
        return hw['TVT_input'].values.astype(float).copy(), 0.0

    last     = kn.iloc[-1]
    last_tvt = float(last['TVT_input'])
    last_Z   = float(last['Z'])
    last_MD  = float(last['MD'])

    tw_at_k = np.interp(kn['TVT_input'].values, tw_tvt, tw_gr)
    gs = float(np.clip(np.nanstd(kn['GR'].fillna(0).values - tw_at_k), 10., 60.))

    tail = kn.tail(30)
    dt = np.diff(tail['TVT_input'].values)
    dz = np.diff(tail['Z'].values)
    dm = np.diff(tail['MD'].values)
    m  = dm > 0
    ir = float(np.median((dt + dz)[m] / dm[m])) if m.sum() >= 3 else 0.0

    N   = n_particles
    rng = np.random.default_rng(seed)
    ls   = last_tvt + last_Z
    pos  = ls + 4.5 * rng.standard_normal(N)  # sp45 patch (sel15 vb best)
    rate = ir + 0.01 * rng.standard_normal(N)
    w    = np.ones(N) / N

    MOM = 0.998; VN = 0.002; PN = 0.005; RP = 0.1; RR = 0.001; RESAMP = 0.5

    md_v = ev['MD'].values.astype(float)
    z_v  = ev['Z'].values.astype(float)
    # Interpolate GR gaps before tracking
    gr_interp = hw['GR'].interpolate(limit_direction='both').fillna(tw_gr.mean())
    gr_v = gr_interp.values.astype(float)[ev.index]

    out_vals = hw['TVT_input'].values.astype(float).copy()
    res = np.empty(len(ev))
    prev_MD = last_MD
    log_lik = 0.0

    for i in range(len(ev)):
        dm_step = max(md_v[i] - prev_MD, 1.0)
        rate = MOM * rate + VN * rng.standard_normal(N)
        pos  = pos + rate * dm_step + PN * rng.standard_normal(N)
        tvt_p = pos - z_v[i]
        tvt_p = np.clip(tvt_p, tw_tvt[0] - 100, tw_tvt[-1] + 100)
        pos   = tvt_p + z_v[i]

        eg = np.interp(tvt_p, tw_tvt, tw_gr)
        d  = (gr_v[i] - eg) / gs
        lk = np.exp(-0.5 * np.minimum(d**2, 600.))
        lk = np.maximum(lk, 1e-300)
        avg_lk = float((w * lk).sum())
        log_lik += np.log(max(avg_lk, 1e-300))
        w = w * lk
        ws = w.sum()
        w = w / ws if ws > 0 else np.ones(N) / N

        n_eff = 1.0 / (w**2).sum()
        if n_eff < RESAMP * N:
            cum = np.cumsum(w)
            u0  = rng.uniform(0, 1.0 / N)
            idx = np.clip(np.searchsorted(cum, u0 + np.arange(N) / N), 0, N - 1)
            pos  = pos[idx]  + RP * rng.standard_normal(N)
            rate = rate[idx] + RR * rng.standard_normal(N)
            w    = np.ones(N) / N

        res[i] = float(np.dot(w, pos - z_v[i]))
        prev_MD = md_v[i]

    out_vals[list(ev.index)] = res
    return out_vals, log_lik


def run_pf_lik_ensemble(hw, tw, n_particles=500, n_seeds=128, scale=5.0):
    preds = []
    liks  = []
    for s in range(n_seeds):
        p, ll = run_particle_filter(hw, tw, n_particles=n_particles, seed=s)
        preds.append(p)
        liks.append(ll)

    liks   = np.array(liks)
    liks_n = liks - liks.max()
    weights = np.exp(liks_n / scale)
    weights /= weights.sum()

    return (weights[:, None] * np.stack(preds, 0)).sum(0)


def run_pf_lik_ensemble_scales(hw, tw, scales=SELECTOR_SCALES, n_particles=500, n_seeds=128, branch_stats=None):
    preds = []
    liks = []
    for s in range(n_seeds):
        p, ll = run_particle_filter(hw, tw, n_particles=n_particles, seed=s)
        preds.append(p)
        liks.append(ll)
    pred_arr = np.stack(preds, 0)
    liks = np.array(liks)
    liks_n = liks - liks.max()
    out = {}
    for scale in scales:
        weights = np.exp(liks_n / float(scale))
        weights /= weights.sum()
        out[f'pf_scale_{scale:g}'] = (weights[:, None] * pred_arr).sum(0)
    out['pf_mean'] = pred_arr.mean(0)
    if bool(globals().get('SELECTOR_PF_RETURN_STD', False)):
        out['pf_seed_std'] = pred_arr.std(0)
    if branch_stats is not None:
        try:
            eval_mask = pd.to_numeric(hw['TVT_input'], errors='coerce').isna().to_numpy()
            if int(eval_mask.sum()) >= 10:
                seed_weight = np.exp(liks_n / 5.0)
                seed_weight = seed_weight / max(float(seed_weight.sum()), 1e-12)
                level = np.nanmedian(pred_arr[:, eval_mask], axis=1)
                valid = np.isfinite(level) & np.isfinite(seed_weight) & (seed_weight > 0)
                level = level[valid]
                seed_weight = seed_weight[valid]
                seed_weight = seed_weight / max(float(seed_weight.sum()), 1e-12)
                if len(level) >= 4:
                    order = np.argsort(level)
                    x = level[order]
                    w = seed_weight[order]
                    cw = np.cumsum(w)
                    cx = np.cumsum(w * x)
                    cx2 = np.cumsum(w * x * x)
                    total_w, total_x, total_x2 = float(cw[-1]), float(cx[-1]), float(cx2[-1])
                    best = None
                    for cut in range(1, len(x)):
                        wl = float(cw[cut - 1])
                        wr = total_w - wl
                        if wl < 0.05 or wr < 0.05:
                            continue
                        xl = float(cx[cut - 1])
                        xr = total_x - xl
                        ssel = float(cx2[cut - 1] - xl * xl / wl)
                        sser = float(total_x2 - cx2[cut - 1] - xr * xr / wr)
                        score = max(0.0, ssel) + max(0.0, sser)
                        if best is None or score < best[0]:
                            best = (score, wl, wr, xl / wl, xr / wr)
                    if best is not None:
                        _, mass_low, mass_high, center_low, center_high = best
                        branch_stats.update(
                            center_low=float(center_low),
                            center_high=float(center_high),
                            mass_low=float(mass_low),
                            mass_high=float(mass_high),
                            weighted_center=float(np.sum(seed_weight * level)),
                            eval_rows=np.flatnonzero(eval_mask).astype(int).tolist(),
                            seed_count=int(len(level)),
                        )
        except Exception as exc:
            branch_stats['error'] = repr(exc)
    return out


def beam_search(hgr, tw_tvt, tw_gr, last_tvt, bs=10, mc=20.0, es=144.0, r=2):
    n  = len(hgr)
    nt = len(tw_tvt)
    if n == 0:
        return np.array([last_tvt])

    if r > 0 and n > max(3, 2 * r + 1):
        win = min(2 * r + 1, n if n % 2 == 1 else n - 1)
        sgr = savgol_filter(hgr, win, min(2, win - 1))
    else:
        sgr = hgr.copy()

    si = int(np.argmin(np.abs(tw_tvt - last_tvt)))

    MOVES = np.array([-2, -1, 0, 1, 2], dtype=np.int64)
    MC    = mc * np.array([2., 1., 0., 1., 2.])

    bidx  = np.full(bs, si, dtype=np.int64)
    bcost = np.full(bs, np.inf)
    bcost[0] = 0.
    bn = 1

    result = np.zeros(n)

    for step in range(n):
        gv = sgr[step]
        ni = bidx[:bn, None] + MOVES[None, :]
        ci = np.clip(ni, 0, nt - 1)
        valid = (ni >= 0) & (ni < nt)

        gr_e = (gv - tw_gr[ci])**2 / es
        tot  = bcost[:bn, None] + gr_e + MC[None, :]
        tot  = np.where(valid, tot, np.inf)

        ni_f  = ni.flatten()
        tot_f = tot.flatten()
        vf    = valid.flatten()
        ni_f  = ni_f[vf]
        tot_f = tot_f[vf]

        order = np.argsort(tot_f)
        ni_s  = ni_f[order]
        tot_s = tot_f[order]

        _, first = np.unique(ni_s, return_index=True)
        ni_u  = ni_s[first]
        tot_u = tot_s[first]

        kept = min(bs, len(ni_u))
        top  = np.argpartition(tot_u, min(kept - 1, len(tot_u) - 1))[:kept]
        top  = top[np.argsort(tot_u[top])]

        bidx[:kept]  = ni_u[top]
        bcost[:kept] = tot_u[top]
        if kept < bs:
            bidx[kept:]  = bidx[kept - 1]
            bcost[kept:] = np.inf
        bn = kept

        result[step] = tw_tvt[bidx[0]]

    return result


def run_beam_ensemble(hw, tw):
    kn = hw[hw['TVT_input'].notna()]
    ev = hw[hw['TVT_input'].isna()]
    if len(ev) == 0:
        return hw['TVT_input'].values.astype(float).copy()

    last_tvt = float(kn.iloc[-1]['TVT_input'])
    tw_s  = tw.sort_values('TVT')
    tw_tvt = tw_s['TVT'].values.astype(float)
    tw_gr  = tw_s['GR'].fillna(tw_s['GR'].mean()).values.astype(float)

    gr_all = hw['GR'].interpolate(limit_direction='both').fillna(tw_gr.mean()).values.astype(float)
    hgr    = gr_all[ev.index]

    beam_results = [beam_search(hgr, tw_tvt, tw_gr, last_tvt, bs, mc, es, r)
                    for (bs, mc, es, r) in BEAM_CONFIGS]

    beam_mean = np.stack(beam_results, 0).mean(0)

    out = hw['TVT_input'].values.astype(float).copy()
    out[list(ev.index)] = beam_mean
    return out


def selector_well_code(hw):
    eval_mask = hw['TVT_input'].isna().to_numpy()
    n_eval = float(eval_mask.sum())
    z_eval = hw.loc[eval_mask, 'Z'].values.astype(float)
    z_span = float(np.nanmax(z_eval) - np.nanmin(z_eval)) if len(z_eval) else 0.0
    n_bin = int(n_eval > SELECTOR_N_EVAL_THRESHOLD)
    z_bin = int(np.searchsorted(SELECTOR_Z_SPAN_THRESHOLDS, z_span, side='right'))
    code = n_bin + 2 * z_bin
    variant = SELECTOR_BIN_VARIANTS.get(code, SELECTOR_GLOBAL_VARIANT)
    return code, variant, n_eval, z_span


def parse_selector_variant(name):
    parts = name.split('_')
    scale = float(parts[2])
    beam_weight = 0.0
    hold_weight = 0.0
    if 'beam' in parts:
        beam_weight = float(parts[parts.index('beam') + 1])
    if 'hold' in parts:
        hold_weight = float(parts[parts.index('hold') + 1])
    return scale, beam_weight, hold_weight


def _selector_tw_gr_arrays(tw):
    if tw is None or 'TVT' not in tw.columns or 'GR' not in tw.columns:
        return None, None
    tw_s = tw.sort_values('TVT')
    tw_tvt = pd.to_numeric(tw_s['TVT'], errors='coerce').to_numpy(dtype=float)
    tw_gr = pd.to_numeric(tw_s['GR'], errors='coerce').to_numpy(dtype=float)
    valid = np.isfinite(tw_tvt) & np.isfinite(tw_gr)
    if int(valid.sum()) < 10:
        return None, None
    tw_tvt = tw_tvt[valid]
    tw_gr = tw_gr[valid]
    order = np.argsort(tw_tvt)
    return tw_tvt[order], tw_gr[order]


def _selector_eval_mask(hw, n):
    if hw is not None and 'TVT_input' in hw.columns:
        return hw['TVT_input'].isna().to_numpy()[:n]
    return np.ones(n, dtype=bool)


def _selector_gr_scale(hw, tw_tvt, tw_gr, hgr, fallback_resid=None):
    if hw is not None and 'TVT_input' in hw.columns:
        known = hw['TVT_input'].notna().to_numpy()[:len(hgr)] & np.isfinite(hgr)
        if int(known.sum()) >= 25:
            known_tvt = pd.to_numeric(hw.loc[known, 'TVT_input'], errors='coerce').to_numpy(dtype=float)
            known_gr = hgr[known]
            ref_gr = np.interp(known_tvt, tw_tvt, tw_gr)
            scale = np.nanmedian(np.abs(known_gr - ref_gr)) * 1.4826
            if np.isfinite(scale) and scale >= 8.0:
                return float(scale)
    if fallback_resid is not None and len(fallback_resid):
        scale = np.nanmedian(np.abs(fallback_resid - np.nanmedian(fallback_resid))) * 1.4826
        if np.isfinite(scale) and scale >= 8.0:
            return float(scale)
    return 20.0




def _selector_fft_denoise_gr(hgr):
    x = np.asarray(hgr, dtype=float).copy()
    if not bool(globals().get('RUN_GR_FFT_DENOISE', False)):
        return x, False
    m = np.isfinite(x)
    if int(m.sum()) < 64:
        return x, False
    idx = np.arange(len(x), dtype=float)
    filled = x.copy()
    filled[~m] = np.interp(idx[~m], idx[m], x[m])
    centered = filled - np.nanmedian(filled)
    spec = np.fft.rfft(centered)
    if len(spec) < 5:
        return x, False
    amp = np.abs(spec)
    amp[0] = 0.0
    peak = int(np.argmax(amp))
    if peak <= 0 or not np.isfinite(amp[peak]):
        return x, False
    # A light notch: remove only the strongest periodic component and its closest neighbors.
    for j in range(max(1, peak - 1), min(len(spec), peak + 2)):
        spec[j] = 0.0
    denoised = np.fft.irfft(spec, n=len(centered)) + np.nanmedian(filled)
    out = x.copy()
    out[m] = denoised[m]
    return out, True


def _selector_apply_heel_calibration(hw, tw_tvt, tw_gr, hgr):
    info = {
        'heel_calibrated': False,
        'heel_rows': 0,
        'heel_alpha': np.nan,
        'heel_beta': np.nan,
        'heel_rmse_raw': np.nan,
        'heel_rmse_calibrated': np.nan,
        'heel_denoised': False,
    }
    raw = np.asarray(hgr, dtype=float).copy()
    prepared, denoised = _selector_fft_denoise_gr(raw)
    info['heel_denoised'] = bool(denoised)
    if not bool(globals().get('RUN_HEEL_CALIBRATION', False)):
        return prepared, info
    if hw is None or 'TVT_input' not in hw.columns:
        return prepared, info
    n = min(len(hw), len(prepared))
    tvt_input = pd.to_numeric(hw['TVT_input'], errors='coerce').to_numpy(dtype=float)[:n]
    gr_obs = prepared[:n]
    mask = np.isfinite(tvt_input) & np.isfinite(gr_obs)
    min_rows = int(globals().get('HEEL_MIN_ROWS', 40))
    if int(mask.sum()) < min_rows:
        info['heel_rows'] = int(mask.sum())
        return prepared, info
    ref = np.interp(tvt_input[mask], tw_tvt, tw_gr)
    ok = np.isfinite(ref) & np.isfinite(gr_obs[mask])
    if int(ok.sum()) < min_rows:
        info['heel_rows'] = int(ok.sum())
        return prepared, info
    ref = ref[ok]
    obs = gr_obs[mask][ok]
    A = np.column_stack([ref, np.ones_like(ref)])
    try:
        alpha, beta = np.linalg.lstsq(A, obs, rcond=None)[0]
    except Exception:
        return prepared, info
    alpha = float(alpha)
    beta = float(beta)
    amin = float(globals().get('HEEL_ALPHA_MIN', 0.25))
    amax = float(globals().get('HEEL_ALPHA_MAX', 4.0))
    bmax = float(globals().get('HEEL_BETA_ABS_MAX', 500.0))
    if not (np.isfinite(alpha) and np.isfinite(beta)):
        return prepared, info
    if alpha < amin or alpha > amax or abs(beta) > bmax:
        info.update({'heel_rows': int(ok.sum()), 'heel_alpha': alpha, 'heel_beta': beta})
        return prepared, info
    calibrated = (prepared - beta) / max(alpha, 1e-12)
    raw_resid = obs - ref
    cal_resid = ((obs - beta) / max(alpha, 1e-12)) - ref
    info.update({
        'heel_calibrated': True,
        'heel_rows': int(ok.sum()),
        'heel_alpha': alpha,
        'heel_beta': beta,
        'heel_rmse_raw': float(np.sqrt(np.nanmean(raw_resid * raw_resid))),
        'heel_rmse_calibrated': float(np.sqrt(np.nanmean(cal_resid * cal_resid))),
    })
    return calibrated, info


def _selector_heel_report_fields(info):
    info = info or {}
    return {
        'heel_calibrated': bool(info.get('heel_calibrated', False)),
        'heel_rows': int(info.get('heel_rows', 0) or 0),
        'heel_alpha': float(info.get('heel_alpha', np.nan)) if np.isfinite(info.get('heel_alpha', np.nan)) else np.nan,
        'heel_beta': float(info.get('heel_beta', np.nan)) if np.isfinite(info.get('heel_beta', np.nan)) else np.nan,
        'heel_rmse_raw': float(info.get('heel_rmse_raw', np.nan)) if np.isfinite(info.get('heel_rmse_raw', np.nan)) else np.nan,
        'heel_rmse_calibrated': float(info.get('heel_rmse_calibrated', np.nan)) if np.isfinite(info.get('heel_rmse_calibrated', np.nan)) else np.nan,
        'heel_denoised': bool(info.get('heel_denoised', False)),
    }

def _selector_gr_misfit(hw, tw, tvt_path, eval_mask=None):
    tw_tvt, tw_gr = _selector_tw_gr_arrays(tw)
    if tw_tvt is None:
        return np.nan, 0
    if hw is None or 'GR' not in hw.columns or tvt_path is None:
        return np.nan, 0
    hgr = pd.to_numeric(hw['GR'], errors='coerce').interpolate(limit_direction='both').to_numpy(dtype=float)
    hgr, _heel_info = _selector_apply_heel_calibration(hw, tw_tvt, tw_gr, hgr)
    path = np.asarray(tvt_path, dtype=float)
    n = min(len(hgr), len(path))
    mask = _selector_eval_mask(hw, n) if eval_mask is None else np.asarray(eval_mask, dtype=bool)[:n]
    mask &= np.isfinite(hgr[:n]) & np.isfinite(path[:n])
    if int(mask.sum()) < int(globals().get('BIMODAL_MIN_VALID_GR_ROWS', 80)):
        return np.nan, int(mask.sum())
    pred_gr = np.interp(path[:n][mask], tw_tvt, tw_gr)
    resid = hgr[:n][mask] - pred_gr
    scale = _selector_gr_scale(hw, tw_tvt, tw_gr, hgr[:n], fallback_resid=resid)
    z = np.clip(resid / scale, -6.0, 6.0)
    return float(np.nanmean(z * z)), int(mask.sum())


def _selector_lag1_autocorr(resid):
    x = np.asarray(resid, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 3:
        return 0.0
    x0 = x[:-1] - np.nanmean(x[:-1])
    x1 = x[1:] - np.nanmean(x[1:])
    denom = float(np.sqrt(np.sum(x0 * x0) * np.sum(x1 * x1)))
    if denom <= 1e-12 or not np.isfinite(denom):
        return 0.0
    return float(np.clip(np.sum(x0 * x1) / denom, 0.0, 0.999))


def _selector_temp_from_resid(resid, n_valid):
    legacy = max(float(globals().get('BIMODAL_TEMP', 0.75)), 1e-6)
    if not bool(globals().get('RUN_ADAPTIVE_TEMP', False)):
        return legacy, np.nan, np.nan
    rho1 = _selector_lag1_autocorr(resid)
    n_eff = float(max(n_valid, 1)) * (1.0 - rho1) / max(1.0 + rho1, 1e-6)
    temp = 2.0 / max(n_eff, 1.0)
    temp = float(np.clip(temp, float(globals().get('T_MIN', 0.25)), float(globals().get('T_MAX', 4.0))))
    return temp, float(rho1), float(n_eff)


def _selector_prefix_trust(hw, tw, base, delta_b):
    fallback = float(globals().get('TRUST_FALLBACK', 0.0))
    if not bool(globals().get('RUN_PREFIX_TRUST_GATE', False)):
        return 1.0, np.nan, np.nan, np.nan, 0
    if hw is None or 'TVT_input' not in hw.columns:
        return fallback, np.nan, np.nan, np.nan, 0
    n = min(len(hw), len(base))
    prefix_mask = hw['TVT_input'].notna().to_numpy()[:n]
    try:
        j_pre0, prefix_rows = _selector_gr_misfit(hw, tw, base, eval_mask=prefix_mask)
        j_predb, _ = _selector_gr_misfit(hw, tw, np.asarray(base, dtype=float) + float(delta_b), eval_mask=prefix_mask)
    except Exception:
        return fallback, np.nan, np.nan, np.nan, 0
    if int(prefix_rows) < int(globals().get('TRUST_MIN_PREFIX_ROWS', 60)):
        return fallback, j_pre0, j_predb, np.nan, int(prefix_rows)
    if not (np.isfinite(j_pre0) and np.isfinite(j_predb)):
        return fallback, j_pre0, j_predb, np.nan, int(prefix_rows)
    margin = float(j_predb - j_pre0)
    denom = max(float(globals().get('TRUST_KAPPA', 1.0)) * max(float(j_pre0), 1e-12), 1e-12)
    trust = float(np.clip(margin / denom, 0.0, 1.0))
    return trust, float(j_pre0), float(j_predb), margin, int(prefix_rows)


def selector_bimodal_scan(hw, tw, base_path, eval_mask=None):
    tw_tvt, tw_gr = _selector_tw_gr_arrays(tw)
    if tw_tvt is None or hw is None or 'GR' not in hw.columns or base_path is None:
        return None
    hgr = pd.to_numeric(hw['GR'], errors='coerce').interpolate(limit_direction='both').to_numpy(dtype=float)
    hgr, heel_info = _selector_apply_heel_calibration(hw, tw_tvt, tw_gr, hgr)
    heel_fields = _selector_heel_report_fields(heel_info)
    base = np.asarray(base_path, dtype=float)
    n = min(len(hgr), len(base))
    mask = _selector_eval_mask(hw, n) if eval_mask is None else np.asarray(eval_mask, dtype=bool)[:n]
    mask &= np.isfinite(hgr[:n]) & np.isfinite(base[:n])
    if int(mask.sum()) < int(globals().get('BIMODAL_MIN_VALID_GR_ROWS', 80)):
        return None

    h = hgr[:n][mask]
    b = base[:n][mask]
    pred0 = np.interp(b, tw_tvt, tw_gr)
    resid0 = h - pred0
    scale = _selector_gr_scale(hw, tw_tvt, tw_gr, hgr[:n], fallback_resid=resid0)

    dz_range = float(globals().get('BIMODAL_DZ_RANGE', 20.0))
    dz_step = float(globals().get('BIMODAL_DZ_STEP', 0.5))
    if dz_step <= 0:
        dz_step = 0.5
    deltas = np.arange(-dz_range, dz_range + 0.5 * dz_step, dz_step, dtype=float)
    scores = []
    for dz in deltas:
        pred_gr = np.interp(b + dz, tw_tvt, tw_gr)
        z = np.clip((h - pred_gr) / scale, -6.0, 6.0)
        scores.append(float(np.nanmean(z * z)))
    scores = np.asarray(scores, dtype=float)
    finite = np.isfinite(scores)
    if int(finite.sum()) < 3:
        return None

    best_idx = int(np.nanargmin(scores))
    delta_a = float(deltas[best_idx])
    score_a = float(scores[best_idx])
    sep_min = float(globals().get('SCAN_MIN_SEP', 8.0))
    bundle_min = float(globals().get('BUNDLE_MIN', 10.0))
    bundle_max = float(globals().get('BUNDLE_MAX', 20.0))
    sep = np.abs(deltas - delta_a)
    candidate = finite & (sep >= max(sep_min, bundle_min)) & (sep <= bundle_max)
    pred_a = np.interp(b + delta_a, tw_tvt, tw_gr)
    resid_a = h - pred_a
    temp, rho1, n_eff = _selector_temp_from_resid(resid_a, int(mask.sum()))
    if not bool(candidate.any()):
        return {
            'is_bimodal': False,
            'delta_a': delta_a,
            'delta_b': np.nan,
            'delta_star': delta_a,
            'p_base': 1.0,
            'p_eff': 1.0,
            'prefix_trust': 1.0,
            'j_prefix_base': np.nan,
            'j_prefix_decoy': np.nan,
            'prefix_trust_margin': np.nan,
            'prefix_rows': 0,
            'temperature': float(temp),
            'rho1': float(rho1) if np.isfinite(rho1) else np.nan,
            'n_eff': float(n_eff) if np.isfinite(n_eff) else np.nan,
            'score_a': score_a,
            'score_b': np.nan,
            'j_ratio': np.nan,
            'dz_gap': np.nan,
            'valid_gr_rows': int(mask.sum()),
            'forced_midpoint': False,
            **heel_fields,
        }
    idxs = np.flatnonzero(candidate)
    second_idx = int(idxs[np.nanargmin(scores[idxs])])
    delta_b = float(deltas[second_idx])
    score_b = float(scores[second_idx])
    j_ratio = float(score_b / max(score_a, 1e-12))
    dz_gap = float(abs(delta_b - delta_a))
    eps = float(globals().get('BIMODAL_J_RATIO_EPS', 0.15))
    is_bimodal = bool(score_b <= (1.0 + eps) * max(score_a, 1e-12))
    p_base = 1.0 / (1.0 + np.exp(np.clip((score_a - score_b) / max(temp, 1e-6), -50.0, 50.0)))
    trust, j_prefix_base, j_prefix_decoy, trust_margin, prefix_rows = _selector_prefix_trust(hw, tw, base, delta_b)
    if bool(globals().get('BIMODAL_FORCE_MIDPOINT', False)):
        p_eff = 0.5
        forced_midpoint = True
    else:
        p_eff = 0.5 + float(trust) * (float(p_base) - 0.5)
        forced_midpoint = False
    delta_star = float(p_eff * delta_a + (1.0 - p_eff) * delta_b)
    return {
        'is_bimodal': is_bimodal,
        'delta_a': delta_a,
        'delta_b': delta_b,
        'delta_star': delta_star,
        'p_base': float(p_base),
        'p_eff': float(p_eff),
        'prefix_trust': float(trust),
        'j_prefix_base': float(j_prefix_base) if np.isfinite(j_prefix_base) else np.nan,
        'j_prefix_decoy': float(j_prefix_decoy) if np.isfinite(j_prefix_decoy) else np.nan,
        'prefix_trust_margin': float(trust_margin) if np.isfinite(trust_margin) else np.nan,
        'prefix_rows': int(prefix_rows),
        'temperature': float(temp),
        'rho1': float(rho1) if np.isfinite(rho1) else np.nan,
        'n_eff': float(n_eff) if np.isfinite(n_eff) else np.nan,
        'score_a': score_a,
        'score_b': score_b,
        'j_ratio': j_ratio,
        'dz_gap': dz_gap,
        'valid_gr_rows': int(mask.sum()),
        'forced_midpoint': bool(forced_midpoint),
        **heel_fields,
    }

def _bimodal_selector_weight(base, beam, hw=None, tw=None):
    base = np.asarray(base, dtype=float)
    beam = np.asarray(beam, dtype=float)
    n = min(len(base), len(beam))
    if n == 0:
        return None
    eval_mask = _selector_eval_mask(hw, n)
    diff = np.abs(base[:n] - beam[:n])
    valid = eval_mask & np.isfinite(diff)
    if int(valid.sum()) < int(globals().get('BIMODAL_MIN_VALID_GR_ROWS', 80)):
        return None
    med_diff = float(np.nanmedian(diff[valid]))
    p90_diff = float(np.nanquantile(diff[valid], 0.90))
    big_frac = float(np.nanmean(diff[valid] >= float(globals().get('BIMODAL_TRIGGER_BIG_DIFF_THRESHOLD', 15.0))))
    if med_diff < float(globals().get('BIMODAL_TRIGGER_MIN_MEDIAN_DIFF', 12.0)) and p90_diff < float(globals().get('BIMODAL_TRIGGER_MIN_P90_DIFF', 18.0)):
        return None
    if big_frac < float(globals().get('BIMODAL_TRIGGER_MIN_BIG_DIFF_FRAC', 0.18)):
        return None

    scan = selector_bimodal_scan(hw, tw, base, eval_mask=eval_mask)
    if not scan or not scan.get('is_bimodal'):
        return None
    return {
        'delta_star': float(scan['delta_star']),
        'p_base': float(scan['p_base']),
        'p_eff': float(scan.get('p_eff', scan['p_base'])),
        'prefix_trust': float(scan.get('prefix_trust', np.nan)),
        'j_prefix_base': float(scan.get('j_prefix_base', np.nan)),
        'j_prefix_decoy': float(scan.get('j_prefix_decoy', np.nan)),
        'prefix_trust_margin': float(scan.get('prefix_trust_margin', np.nan)),
        'prefix_rows': int(scan.get('prefix_rows', 0)),
        'temperature': float(scan.get('temperature', np.nan)),
        'rho1': float(scan.get('rho1', np.nan)),
        'n_eff': float(scan.get('n_eff', np.nan)),
        'forced_midpoint': bool(scan.get('forced_midpoint', False)),
        'score_base': float(scan['score_a']),
        'score_second': float(scan['score_b']),
        'delta_a': float(scan['delta_a']),
        'delta_b': float(scan['delta_b']),
        'j_ratio': float(scan['j_ratio']),
        'dz_gap': float(scan['dz_gap']),
        'median_abs_diff': med_diff,
        'p90_abs_diff': p90_diff,
        'big_diff_frac': big_frac,
        'valid_gr_rows': int(scan['valid_gr_rows']),
        'heel_calibrated': bool(scan.get('heel_calibrated', False)),
        'heel_rows': int(scan.get('heel_rows', 0)),
        'heel_alpha': float(scan.get('heel_alpha', np.nan)),
        'heel_beta': float(scan.get('heel_beta', np.nan)),
        'heel_rmse_raw': float(scan.get('heel_rmse_raw', np.nan)),
        'heel_rmse_calibrated': float(scan.get('heel_rmse_calibrated', np.nan)),
        'heel_denoised': bool(scan.get('heel_denoised', False)),
    }


def apply_selector_variant(name, pf_by_scale, tvt_beam, last_known_tvt, hw=None, tw=None, return_info=False):
    scale, beam_weight, hold_weight = parse_selector_variant(name)
    base = pf_by_scale.get(f'pf_scale_{scale:g}')
    if base is None:
        base = pf_by_scale[SELECTOR_GLOBAL_VARIANT.split('_beam_')[0].split('_hold_')[0]]
    base = np.asarray(base, dtype=float)
    tvt_beam = np.asarray(tvt_beam, dtype=float)
    info = {
        'bimodal_active': False,
        'base_beam_weight': float(beam_weight),
        'effective_beam_weight': float(beam_weight),
        'delta_star': 0.0,
        'p_base': np.nan,
        'p_eff': np.nan,
        'prefix_trust': np.nan,
        'temperature': np.nan,
        'rho1': np.nan,
        'n_eff': np.nan,
        'heel_calibrated': False,
        'heel_rows': 0,
        'heel_alpha': np.nan,
        'heel_beta': np.nan,
        'heel_rmse_raw': np.nan,
        'heel_rmse_calibrated': np.nan,
        'heel_denoised': False,
    }
    if bool(globals().get('RUN_BIMODAL_DETECTOR', globals().get('RUN_BIMODAL_SELECTOR_HEDGE', False))):
        hedge = _bimodal_selector_weight(base, tvt_beam, hw=hw, tw=tw)
        if hedge is not None:
            info.update(hedge)
            info['bimodal_active'] = True
            info['effective_beam_weight'] = float(beam_weight)
            pred = base + float(hedge['delta_star'])
        else:
            pred = (1.0 - beam_weight) * base + beam_weight * tvt_beam
    else:
        pred = (1.0 - beam_weight) * base + beam_weight * tvt_beam
    pred = (1.0 - hold_weight) * pred + hold_weight * last_known_tvt
    if return_info:
        return pred, info
    return pred

# Optional read-only oracle/tail diagnostics for train wells.
if bool(globals().get('RUN_CV_REPORT', False)):
    import numpy as _cv_np
    import pandas as _cv_pd
    from pathlib import Path as _CvPath

    def _cv_rmse(y, p):
        y = _cv_np.asarray(y, dtype=float)
        p = _cv_np.asarray(p, dtype=float)
        m = _cv_np.isfinite(y) & _cv_np.isfinite(p)
        if not bool(m.any()):
            return _cv_np.nan, 0, 0.0
        err = y[m] - p[m]
        return float(_cv_np.sqrt(_cv_np.mean(err * err))), int(m.sum()), float(_cv_np.sum(err * err))

    def _cv_robust_polyfit(x, y, deg=6):
        x = _cv_np.asarray(x, dtype=float)
        y = _cv_np.asarray(y, dtype=float)
        m = _cv_np.isfinite(x) & _cv_np.isfinite(y)
        if int(m.sum()) < max(4, deg + 2):
            return _cv_np.full_like(y, float(_cv_np.nanmean(y)), dtype=float)
        xx = x[m]
        yy = y[m]
        d = min(int(deg), max(1, int(m.sum()) - 2))
        coef = _cv_np.polyfit(xx, yy, d)
        for _ in range(4):
            resid = yy - _cv_np.polyval(coef, xx)
            scale = _cv_np.nanmedian(_cv_np.abs(resid)) * 1.4826 + 1e-6
            w = 1.0 / (1.0 + (resid / (2.0 * scale)) ** 2)
            coef = _cv_np.polyfit(xx, yy, d, w=w)
        out = _cv_np.full_like(y, _cv_np.nan, dtype=float)
        out[m] = _cv_np.polyval(coef, xx)
        return out

    def _rogii_oracle_ladder_report():
        data_root = _CvPath(_safe_competition_data_root())
        train_dir = data_root / 'train'
        wells = sorted(p.name.replace('__horizontal_well.csv', '') for p in train_dir.glob('*__horizontal_well.csv'))
        rng = _cv_np.random.default_rng(int(globals().get('CV_SEED', 0)))
        n_wells = int(globals().get('CV_N_WELLS', len(wells)))
        if n_wells > 0 and n_wells < len(wells):
            wells = sorted(rng.choice(wells, size=n_wells, replace=False).tolist())
        pooled = {k: {'sse': 0.0, 'n': 0} for k in ['flat', 'constant', 'line', 'smooth']}
        smooth_well_sse = []
        rows = []
        for wid in wells:
            hw_path = train_dir / f'{wid}__horizontal_well.csv'
            if not hw_path.exists():
                continue
            hw = _cv_pd.read_csv(hw_path)
            if 'TVT' not in hw.columns or 'TVT_input' not in hw.columns:
                continue
            eval_mask = hw['TVT_input'].isna().to_numpy()
            if int(eval_mask.sum()) < 10:
                continue
            y = _cv_pd.to_numeric(hw.loc[eval_mask, 'TVT'], errors='coerce').to_numpy(dtype=float)
            md = _cv_pd.to_numeric(hw.loc[eval_mask, 'MD'], errors='coerce').to_numpy(dtype=float)
            known = _cv_pd.to_numeric(hw.loc[hw['TVT_input'].notna(), 'TVT_input'], errors='coerce').dropna()
            if len(known):
                flat_pred = _cv_np.full(len(y), float(known.iloc[-1]))
            else:
                flat_pred = _cv_np.full(len(y), float(_cv_np.nanmean(y)))
            constant_pred = _cv_np.full(len(y), float(_cv_np.nanmean(y)))
            s = md - _cv_np.nanmin(md)
            denom = _cv_np.nanmax(s)
            if _cv_np.isfinite(denom) and denom > 0:
                s = s / denom
            else:
                s = _cv_np.linspace(0.0, 1.0, len(y))
            if _cv_np.isfinite(y).sum() >= 3:
                line_pred = _cv_np.polyval(_cv_np.polyfit(s[_cv_np.isfinite(y)], y[_cv_np.isfinite(y)], 1), s)
            else:
                line_pred = constant_pred
            smooth_pred = _cv_robust_polyfit(s, y, deg=6)
            preds = {'flat': flat_pred, 'constant': constant_pred, 'line': line_pred, 'smooth': smooth_pred}
            row = {'well': wid, 'eval_rows': int(len(y))}
            for name, pred in preds.items():
                rmse, n, sse = _cv_rmse(y, pred)
                pooled[name]['sse'] += sse
                pooled[name]['n'] += n
                row[name + '_rmse'] = rmse
                if name == 'smooth':
                    smooth_well_sse.append((wid, sse, n))
            rows.append(row)
        summary = []
        for name, vals in pooled.items():
            rmse = _cv_np.sqrt(vals['sse'] / max(vals['n'], 1))
            summary.append({'oracle': name, 'pooled_rmse': float(rmse), 'rows': int(vals['n'])})
        smooth_well_sse.sort(key=lambda x: x[1], reverse=True)
        total_sse = float(sum(x[1] for x in smooth_well_sse))
        k = max(1, int(_cv_np.ceil(0.10 * len(smooth_well_sse)))) if smooth_well_sse else 0
        tail_share = float(sum(x[1] for x in smooth_well_sse[:k]) / max(total_sse, 1e-12)) if k else _cv_np.nan
        summary_df = _cv_pd.DataFrame(summary)
        well_df = _cv_pd.DataFrame(rows)
        summary_df.to_csv('oracle_ladder_summary.csv', index=False)
        well_df.to_csv('oracle_ladder_by_well.csv', index=False)
        _cv_pd.Series({'wells': int(len(rows)), 'worst_decile_smooth_sse_share': tail_share}).to_csv('oracle_tail_concentration.csv')
        print(summary_df.to_string(index=False))
        print(f'worst_decile_smooth_sse_share={tail_share:.4f}')
        return summary_df, well_df



    def _rogii_selector_cv_report():
        data_root = _CvPath(_safe_competition_data_root())
        train_dir = data_root / 'train'
        wells = sorted(p.name.replace('__horizontal_well.csv', '') for p in train_dir.glob('*__horizontal_well.csv'))
        rng = _cv_np.random.default_rng(int(globals().get('CV_SEED', 0)))
        n_wells = int(globals().get('CV_N_WELLS', len(wells)))
        if n_wells > 0 and n_wells < len(wells):
            wells = sorted(rng.choice(wells, size=n_wells, replace=False).tolist())
        rows = []
        total_sse = 0.0
        total_n = 0
        selector_seeds = int(globals().get('CV_SELECTOR_PF_SEEDS', globals().get('SELECTOR_PF_SEEDS', SP45_SELECTOR_N_SEEDS)))
        for idx, wid in enumerate(wells):
            try:
                hw, tw = load_well(wid, 'train')
                eval_mask = hw['TVT_input'].isna().to_numpy()
                if 'TVT' not in hw.columns or int(eval_mask.sum()) < 10:
                    continue
                selector_code, selector_variant, selector_n_eval, selector_z_span = selector_well_code(hw)
                pf_by_scale = run_pf_lik_ensemble_scales(
                    hw, tw,
                    n_particles=int(globals().get('SP45_SELECTOR_N_PARTICLES', 500)),
                    n_seeds=selector_seeds,
                )
                tvt_pf = pf_by_scale.get('pf_scale_8', pf_by_scale.get('pf_mean'))
                try:
                    tvt_beam = run_beam_ensemble(hw, tw)
                except Exception:
                    tvt_beam = tvt_pf.copy()
                last_known = hw['TVT_input'].dropna()
                last_known_tvt = float(last_known.iloc[-1]) if len(last_known) else float(_cv_np.nanmean(tvt_pf))
                pred, info = apply_selector_variant(
                    selector_variant, pf_by_scale, tvt_beam, last_known_tvt,
                    hw=hw, tw=tw, return_info=True,
                )
                y = _cv_pd.to_numeric(hw.loc[eval_mask, 'TVT'], errors='coerce').to_numpy(dtype=float)
                p_eval = _cv_np.asarray(pred, dtype=float)[eval_mask]
                rmse, n, sse = _cv_rmse(y, p_eval)
                if n <= 0 or not _cv_np.isfinite(rmse):
                    continue
                total_sse += sse
                total_n += n
                rows.append({
                    'well': wid,
                    'eval_rows': int(n),
                    'selector_variant': selector_variant,
                    'selector_code': int(selector_code),
                    'z_span': float(selector_z_span),
                    'rmse': float(rmse),
                    'sse': float(sse),
                    'bimodal_active': bool(info.get('bimodal_active', False)),
                    'delta_star': float(info.get('delta_star', 0.0)),
                    'p_base': float(info.get('p_base', _cv_np.nan)),
                    'j_ratio': float(info.get('j_ratio', _cv_np.nan)),
                    'dz_gap': float(info.get('dz_gap', _cv_np.nan)),
                    'heel_calibrated': bool(info.get('heel_calibrated', False)),
                    'heel_rows': int(info.get('heel_rows', 0)),
                    'heel_alpha': float(info.get('heel_alpha', _cv_np.nan)),
                    'heel_beta': float(info.get('heel_beta', _cv_np.nan)),
                    'heel_rmse_raw': float(info.get('heel_rmse_raw', _cv_np.nan)),
                    'heel_rmse_calibrated': float(info.get('heel_rmse_calibrated', _cv_np.nan)),
                })
            except Exception as exc:
                rows.append({'well': wid, 'error': repr(exc)})
        report = _cv_pd.DataFrame(rows)
        if not report.empty:
            report.to_csv('selector_cv_by_well.csv', index=False)
        if not report.empty and 'eval_rows' in report.columns:
            eval_rows = _cv_pd.to_numeric(report['eval_rows'], errors='coerce').fillna(0)
            ok = report[eval_rows > 0].copy()
        else:
            ok = report.iloc[0:0].copy()
        pooled_rmse = float(_cv_np.sqrt(total_sse / max(total_n, 1)))
        if not ok.empty:
            rmse_values = _cv_pd.to_numeric(ok['rmse'], errors='coerce').dropna().to_numpy(dtype=float)
            ok = ok.sort_values('sse', ascending=False)
            k = max(1, int(_cv_np.ceil(0.10 * len(ok))))
            tail_share = float(ok.head(k)['sse'].sum() / max(ok['sse'].sum(), 1e-12))
            bimodal_count = int(ok['bimodal_active'].sum()) if 'bimodal_active' in ok.columns else 0
        else:
            rmse_values = _cv_np.asarray([], dtype=float)
            tail_share = _cv_np.nan
            bimodal_count = 0
        summary = _cv_pd.Series({
            'wells': int(len(ok)),
            'rows': int(total_n),
            'selector_pf_seeds': int(selector_seeds),
            'pooled_rmse': pooled_rmse,
            'per_well_rmse_p50': float(_cv_np.nanquantile(rmse_values, 0.50)) if len(rmse_values) else _cv_np.nan,
            'per_well_rmse_p90': float(_cv_np.nanquantile(rmse_values, 0.90)) if len(rmse_values) else _cv_np.nan,
            'per_well_rmse_p99': float(_cv_np.nanquantile(rmse_values, 0.99)) if len(rmse_values) else _cv_np.nan,
            'worst_decile_sse_share': tail_share,
            'bimodal_active_wells': bimodal_count,
        })
        summary.to_csv('selector_cv_summary.csv')
        print(summary.to_string())
        return summary, report


    def _rogii_heel_localization_report():
        if not bool(globals().get('RUN_HEEL_LOCALIZATION_REPORT', True)):
            return _cv_pd.DataFrame(), _cv_pd.DataFrame()
        data_root = _CvPath(_safe_competition_data_root())
        train_dir = data_root / 'train'
        wells = sorted(p.name.replace('__horizontal_well.csv', '') for p in train_dir.glob('*__horizontal_well.csv'))
        rng = _cv_np.random.default_rng(int(globals().get('CV_SEED', 0)))
        n_wells = int(globals().get('CV_N_WELLS', len(wells)))
        if n_wells > 0 and n_wells < len(wells):
            wells = sorted(rng.choice(wells, size=n_wells, replace=False).tolist())
        rows = []
        old_heel = globals().get('RUN_HEEL_CALIBRATION', False)
        tol = float(globals().get('HEEL_LOCALIZATION_TOLERANCE', 2.0))
        try:
            for wid in wells:
                hw_path = train_dir / f'{wid}__horizontal_well.csv'
                tw_path = train_dir / f'{wid}__typewell.csv'
                if not hw_path.exists() or not tw_path.exists():
                    continue
                hw = _cv_pd.read_csv(hw_path)
                tw = _cv_pd.read_csv(tw_path)
                if 'TVT' not in hw.columns or 'TVT_input' not in hw.columns or 'GR' not in hw.columns:
                    continue
                eval_mask = hw['TVT_input'].isna().to_numpy()
                if int(eval_mask.sum()) < 10:
                    continue
                truth_path = _cv_pd.to_numeric(hw['TVT'], errors='coerce').to_numpy(dtype=float)
                for heel_on in [False, True]:
                    globals()['RUN_HEEL_CALIBRATION'] = bool(heel_on)
                    scan = selector_bimodal_scan(hw, tw, truth_path, eval_mask=eval_mask)
                    if not scan:
                        rows.append({'well': wid, 'heel_on': bool(heel_on), 'status': 'scan_skip'})
                        continue
                    delta = float(scan.get('delta_a', _cv_np.nan))
                    rows.append({
                        'well': wid,
                        'heel_on': bool(heel_on),
                        'status': 'ok',
                        'eval_rows': int(eval_mask.sum()),
                        'delta_a': delta,
                        'abs_delta_a': abs(delta) if _cv_np.isfinite(delta) else _cv_np.nan,
                        'localized_within_tol': bool(_cv_np.isfinite(delta) and abs(delta) <= tol),
                        'score_a': float(scan.get('score_a', _cv_np.nan)),
                        'score_b': float(scan.get('score_b', _cv_np.nan)),
                        'j_ratio': float(scan.get('j_ratio', _cv_np.nan)),
                        'valid_gr_rows': int(scan.get('valid_gr_rows', 0)),
                        'heel_calibrated': bool(scan.get('heel_calibrated', False)),
                        'heel_rows': int(scan.get('heel_rows', 0)),
                        'heel_alpha': float(scan.get('heel_alpha', _cv_np.nan)),
                        'heel_beta': float(scan.get('heel_beta', _cv_np.nan)),
                        'heel_rmse_raw': float(scan.get('heel_rmse_raw', _cv_np.nan)),
                        'heel_rmse_calibrated': float(scan.get('heel_rmse_calibrated', _cv_np.nan)),
                    })
        finally:
            globals()['RUN_HEEL_CALIBRATION'] = old_heel
        report = _cv_pd.DataFrame(rows)
        if not report.empty:
            report.to_csv('heel_calibration_localization_report.csv', index=False)
        summary_rows = []
        if not report.empty and 'status' in report.columns:
            ok = report[report['status'].eq('ok')].copy()
            for heel_on, g in ok.groupby('heel_on'):
                abs_delta = _cv_pd.to_numeric(g['abs_delta_a'], errors='coerce')
                summary_rows.append({
                    'heel_on': bool(heel_on),
                    'wells': int(len(g)),
                    'localized_tolerance_ft': tol,
                    'localized_rate': float(g['localized_within_tol'].mean()) if len(g) else _cv_np.nan,
                    'median_abs_delta_a': float(abs_delta.median()) if len(abs_delta.dropna()) else _cv_np.nan,
                    'p90_abs_delta_a': float(abs_delta.quantile(0.90)) if len(abs_delta.dropna()) else _cv_np.nan,
                    'calibrated_rate': float(g['heel_calibrated'].mean()) if 'heel_calibrated' in g else _cv_np.nan,
                    'median_heel_alpha': float(_cv_pd.to_numeric(g['heel_alpha'], errors='coerce').median()),
                    'median_heel_beta': float(_cv_pd.to_numeric(g['heel_beta'], errors='coerce').median()),
                })
        summary = _cv_pd.DataFrame(summary_rows)
        if not summary.empty:
            summary.to_csv('heel_calibration_localization_summary.csv', index=False)
            print('heel calibration localization summary')
            print(summary.to_string(index=False))
        return summary, report

    _heel_localization_summary, _heel_localization_report = _rogii_heel_localization_report()
    _oracle_summary, _oracle_well_report = _rogii_oracle_ladder_report()
    _selector_cv_summary, _selector_cv_report = _rogii_selector_cv_report()

## Ridge/PF and Selector Anchor

This block builds the first trajectory family. It loads the ridge artifact cache when available, trains or loads the residual ensemble, creates the particle-filter path, and combines it with the SP45 selector trajectory. This anchor is the input to projection, learned blending, contact verification, and visible-prefix calibration.

SEED=42
NCPU=min(4,multiprocessing.cpu_count())

FORMATIONS=["ANCC","ASTNU","ASTNL","EGFDU","EGFDL","BUDA"]
PLANE_K=10; DENSE_SPW=60; DENSE_K=20; N_SPLITS=5

BEAMS=[
    (10,20.0,144.0,2,"cons"),
    (10, 8.0, 64.0,2,"loose"),
    ( 8,35.0,220.0,1,"vcons"),
    (10,14.0, 90.0,5,"sm5"),
    (20, 4.0, 36.0,3,"vloose"),
    (12,12.0,100.0,3,"mid"),
    (15,25.0,180.0,2,"stiff"),
]

PF_N=600; ANCC_N=600
PF_MOM=0.993; PF_VN=0.005; PF_PN=0.01
PF_GR_SIG_MIN=10.; PF_GR_SIG_MAX=60.; PF_GR_SIG_DEF=30.
PF_INIT_V_STD=0.02; PF_INIT_SPR=0.5; PF_RESAMP=0.5
PF_ROUGH_P=0.2; PF_ROUGH_V=0.003; PF_GR_WIN=5; PF_GR_WT=0.3
ANCC_ALPHA=0.998; ANCC_RN=0.002; ANCC_PN=0.005
ANCC_IR=0.01; ANCC_IS=0.3; ANCC_RP=0.1; ANCC_RR=0.001

@njit(cache=True)
def _interp1(grid, v, vmin, step):
    i = int((v - vmin) / step)
    if i < 0: return grid[0]
    n = len(grid) - 1
    if i >= n: return grid[n]
    t = (v - vmin) / step - i
    return grid[i]*(1.-t) + grid[i+1]*t

@njit(cache=True)
def _resamp(pos, aux, w, N, rp, rv):
    cum = np.zeros(N+1)
    for j in range(N): cum[j+1]=cum[j]+w[j]
    u0=np.random.uniform(0.,1./N)
    np2=np.empty(N); na=np.empty(N); ci=0
    for j in range(N):
        u=u0+j/N
        while ci<N-1 and cum[ci+1]<u: ci+=1
        np2[j]=pos[ci]+rp*np.random.randn()
        na[j] =aux[ci]+rv*np.random.randn()
    return np2,na

@njit(cache=True)
def _beam_jit(sgr, tw_gr, si, BS, mc, es):
    """Beam search Ã‚Â±2 delta, Numba JIT."""
    n=len(sgr); nt=len(tw_gr); MAX=BS*6
    bidx=np.zeros(BS,np.int64); bidx[0]=si
    bcost=np.full(BS,1e30);     bcost[0]=0.; bn=np.int64(1)
    hI=np.zeros((n,BS),np.int64); hP=np.zeros((n,BS),np.int64)
    cI=np.zeros(MAX,np.int64); cC=np.full(MAX,1e30); cP=np.zeros(MAX,np.int64)
    for step in range(n):
        gv=sgr[step]; nc=np.int64(0)
        for bi in range(bn):
            idx=bidx[bi]; cost=bcost[bi]
            for d in range(-2,3):            # Ã‚Â±2: TVT can go down
                ni=idx+d
                if ni<0 or ni>=nt: continue
                tot=cost+(gv-tw_gr[ni])**2/es+mc*(d if d>=0 else -d)
                fnd=np.int64(-1)
                for ci in range(nc):
                    if cI[ci]==ni: fnd=ci; break
                if fnd>=0:
                    if tot<cC[fnd]: cC[fnd]=tot; cP[fnd]=bi
                else:
                    if nc<MAX: cI[nc]=ni; cC[nc]=tot; cP[nc]=bi; nc+=1
        kept=min(BS,nc)
        for i in range(kept):
            mi=i
            for j in range(i+1,nc):
                if cC[j]<cC[mi]: mi=j
            if mi!=i:
                cI[i],cI[mi]=cI[mi],cI[i]
                cC[i],cC[mi]=cC[mi],cC[i]
                cP[i],cP[mi]=cP[mi],cP[i]
        hI[step,:kept]=cI[:kept]; hP[step,:kept]=cP[:kept]
        bidx[:kept]=cI[:kept]; bcost[:kept]=cC[:kept]; bn=kept
    best=np.int64(0)
    for b in range(1,bn):
        if bcost[b]<bcost[best]: best=b
    path=np.zeros(n,np.int64); b=best
    for s in range(n-1,-1,-1): path[s]=hI[s,b]; b=hP[s,b]
    return path

@njit(cache=True)
def _pf_ancc(md_v,z_v,gr_v,gg,vmin,step,gs,ls,ir,N,
              ALPHA,RN,PN,IS,RP,RR,RESAMP):
    pos=np.empty(N); rate=np.empty(N); w=np.ones(N)/N
    for j in range(N):
        pos[j]=ls+IS*np.random.randn()
        rate[j]=ir+0.01*np.random.randn()
    pts=np.empty(len(md_v)); std_=np.empty(len(md_v)); pm=md_v[0]-1.
    for i in range(len(md_v)):
        dm=md_v[i]-pm; dm=max(dm,1.)
        for j in range(N):
            rate[j]=ALPHA*rate[j]+RN*np.random.randn()
            pos[j]+=rate[j]*dm+PN*np.random.randn()
            tvt_j=pos[j]-z_v[i]
            tvt_j=max(tvt_j,vmin-50.); tvt_j=min(tvt_j,vmin+len(gg)*step+50.)
            pos[j]=tvt_j+z_v[i]
        if not np.isnan(gr_v[i]):
            ws=0.
            for j in range(N):
                eg=_interp1(gg,pos[j]-z_v[i],vmin,step)
                d=(gr_v[i]-eg)/gs
                lk=max(np.exp(-0.5*d*d) if d*d<600. else 0.,1e-300)
                w[j]*=lk; ws+=w[j]
            if ws>0.:
                for j in range(N): w[j]/=ws
            else:
                for j in range(N): w[j]=1./N
        ne=0.
        for j in range(N): ne+=w[j]*w[j]
        if 1./ne<RESAMP*N:
            pos,rate=_resamp(pos,rate,w,N,RP,RR)
            for j in range(N): w[j]=1./N
        tv=0.
        for j in range(N): tv+=w[j]*(pos[j]-z_v[i])
        pts[i]=tv; va=0.
        for j in range(N): va+=w[j]*(pos[j]-z_v[i]-tv)**2
        std_[i]=va**0.5; pm=md_v[i]
    return pts,std_

@njit(cache=True)
def _pf_z(md_v,z_v,gr_v,gr_sm_v,gg_p,gg_s,vmin,step,
          gs,ip,iv,beta,icpt,zsig,N,
          MOM,VN,PN,GR_WT,RP,RV,RESAMP):
    pos=np.empty(N); vel=np.empty(N); w=np.ones(N)/N
    for j in range(N):
        pos[j]=ip+0.5*np.random.randn()
        vel[j]=iv+0.02*np.random.randn()
    pts=np.empty(len(md_v)); std_=np.empty(len(md_v)); pm=md_v[0]-1.; pz=z_v[0]-1.
    for i in range(len(md_v)):
        dm=md_v[i]-pm; dm=max(dm,1.)
        dzd=(z_v[i]-pz)/dm; ve=beta*dzd+icpt
        for j in range(N):
            vel[j]=MOM*vel[j]+VN*np.random.randn()
            pos[j]+=vel[j]*dm+PN*np.random.randn()
            pos[j]=max(pos[j],vmin-50.); pos[j]=min(pos[j],vmin+len(gg_p)*step+50.)
        if not np.isnan(gr_v[i]):
            ws=0.
            for j in range(N):
                ep=_interp1(gg_p,pos[j],vmin,step)
                dp=(gr_v[i]-ep)/gs
                lp=max(np.exp(-0.5*dp*dp) if dp*dp<600. else 0.,1e-300)
                if not np.isnan(gr_sm_v[i]):
                    es=_interp1(gg_s,pos[j],vmin,step)
                    ds=(gr_sm_v[i]-es)/(gs*1.5)
                    ls=max(np.exp(-0.5*ds*ds) if ds*ds<600. else 0.,1e-300)
                    lk=(1.-GR_WT)*lp+GR_WT*ls
                else: lk=lp
                lk=max(lk,1e-300); w[j]*=lk; ws+=w[j]
            if ws>0.:
                for j in range(N): w[j]/=ws
            else:
                for j in range(N): w[j]=1./N
        ws2=0.
        for j in range(N):
            dv=(vel[j]-ve)/max(zsig*2.,0.005)
            lz=max(np.exp(-0.5*dv*dv) if dv*dv<600. else 0.,1e-300)
            w[j]*=lz; ws2+=w[j]
        if ws2>0.:
            for j in range(N): w[j]/=ws2
        else:
            for j in range(N): w[j]=1./N
        ne=0.
        for j in range(N): ne+=w[j]*w[j]
        if 1./ne<RESAMP*N:
            pos,vel=_resamp(pos,vel,w,N,RP,RV)
            for j in range(N): w[j]=1./N
        wm=0.
        for j in range(N): wm+=w[j]*pos[j]
        pts[i]=wm; va=0.
        for j in range(N): va+=w[j]*(pos[j]-wm)**2
        std_[i]=va**0.5; pm=md_v[i]; pz=z_v[i]
    return pts,std_

# Dense grid for O(1) typewell lookup
def _grid(tw_tvt,tw_gr,step=0.2):
    tmin=float(tw_tvt.min()); tmax=float(tw_tvt.max())
    tvt_g=np.arange(tmin,tmax+step,step)
    return np.interp(tvt_g,tw_tvt,tw_gr).astype(np.float64),float(tmin),float(step)

def _gr_sig(hw,tw_tvt,tw_gr):
    kn=hw[hw['TVT_input'].notna()&hw['GR'].notna()]
    if len(kn)<20: return float(PF_GR_SIG_DEF)
    return float(np.clip(np.std(kn['GR'].values-np.interp(kn['TVT_input'].values,tw_tvt,tw_gr)),
                          PF_GR_SIG_MIN,PF_GR_SIG_MAX))

def _nn(arr,v):
    i=int(np.searchsorted(arr,v,'left'))
    if i>=len(arr): return len(arr)-1
    if i>0 and abs(arr[i-1]-v)<=abs(arr[i]-v): return i-1
    return i

def _smooth(vals,fb,r):
    s=pd.Series(vals,dtype='float32').interpolate(limit_direction='both').fillna(fb)
    return (s.rolling(r*2+1,center=True,min_periods=1).mean() if r>0 else s).to_numpy(np.float32)

def beam_search(gr_h,tw_tvt,tw_gr,start_tvt,bs,mc,es,r):
    si=_nn(tw_tvt,start_tvt)
    sgr=_smooth(gr_h,float(np.nanmean(tw_gr)),r).astype(np.float64)
    path=_beam_jit(sgr,tw_gr.astype(np.float64),si,bs,float(mc),float(es))
    return tw_tvt[path].astype(np.float32)

def run_pf_ancc(hw,tw_tvt,tw_gr,N=ANCC_N):
    gs=_gr_sig(hw,tw_tvt,tw_gr)
    kn=hw[hw['TVT_input'].notna()]; ev=hw[hw['TVT_input'].isna()]
    if len(ev)==0: return np.array([]),np.array([])
    ls=float(kn['TVT_input'].iloc[-1]+kn['Z'].iloc[-1])
    tail=kn.tail(30); dt=np.diff(tail['TVT_input'].values)
    dz=np.diff(tail['Z'].values); dm=np.diff(tail['MD'].values); m=dm>0
    ir=float(np.median((dt+dz)[m]/dm[m])) if m.sum()>=3 else 0.
    gg,gmin,gst=_grid(tw_tvt,tw_gr)
    pts,std=_pf_ancc(ev['MD'].values.astype(np.float64),ev['Z'].values.astype(np.float64),
                      ev['GR'].values.astype(np.float64),gg,gmin,gst,
                      gs,ls,ir,N,ANCC_ALPHA,ANCC_RN,ANCC_PN,ANCC_IS,ANCC_RP,ANCC_RR,PF_RESAMP)
    return pts.astype(np.float32),std.astype(np.float32)

def run_pf_z(hw,tw_tvt,tw_gr,N=PF_N):
    gs=_gr_sig(hw,tw_tvt,tw_gr)
    tw_s=pd.Series(tw_gr).rolling(PF_GR_WIN,center=True,min_periods=1).mean().values.astype(np.float32)
    kna=hw[hw['TVT_input'].notna()]; ev=hw[hw['TVT_input'].isna()]
    if len(ev)==0: return np.array([]),np.array([])
    dz_k=np.diff(kna['Z'].values); dvt=np.diff(kna['TVT_input'].values)
    dmd_k=np.diff(kna['MD'].values); m2=dmd_k>0
    if m2.sum()>=10:
        vz=dz_k[m2]/dmd_k[m2]; vt=dvt[m2]/dmd_k[m2]
        A=np.column_stack([vz,np.ones_like(vz)]); c,_,_,_=np.linalg.lstsq(A,vt,rcond=None)
        beta,icpt,zsig=float(c[0]),float(c[1]),max(float(np.std(vt-(c[0]*vz+c[1]))),0.001)
    else: beta,icpt,zsig=-1.,0.,0.1
    t2=kna.tail(20); dvt2=np.diff(t2['TVT_input'].values); dmd2=np.diff(t2['MD'].values); m3=dmd2>0
    iv=float(np.median(dvt2[m3]/dmd2[m3])) if m3.sum()>=3 else 0.
    gg,gmin,gst=_grid(tw_tvt,tw_gr)
    gs2,_,_=_grid(tw_tvt,tw_s)
    gr_sm=hw['GR'].rolling(PF_GR_WIN,center=True,min_periods=1).mean()
    pts,std=_pf_z(ev['MD'].values.astype(np.float64),ev['Z'].values.astype(np.float64),
                   ev['GR'].values.astype(np.float64),
                   gr_sm.loc[ev.index].values.astype(np.float64),
                   gg,gs2,gmin,gst,gs,float(kna['TV