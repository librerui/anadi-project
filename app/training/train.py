"""
Training script for the machine learning models.

This module ports the regression and classification training workflow from PROJECT_2/main.ipynb into
reusable functions for the new service training architecture.
"""

from __future__ import annotations

import pickle
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, LinearSVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from .feature_engineering import prepare_training_data, load_dataset
from .tuning import build_cfg

CFG = build_cfg()


def set_cfg(cfg: Dict[str, Any]) -> None:
    global CFG
    CFG = cfg


def get_version(version: Optional[str] = None) -> str:
    return version if version else datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def save_pickle(obj: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.sqrt(mean_squared_error(y_true, y_pred))


def subsample(
    X: pd.DataFrame, y: Any, n: Optional[int], random_state: int
) -> Tuple[pd.DataFrame, Any]:
    """Subsample X/y to at most `n` rows using CFG's sample size knobs.

    `n=None` (or 0) means "use the full dataset". X and y must be in the
    same row order (positionally aligned) — this is true coming out of
    prepare_training_data, but X's pandas index may have gaps (e.g. after
    dropna), so we sample by *position* via `.iloc` / integer indexing
    rather than by X's index labels. Using labels to index into a plain
    ndarray y would silently break (or raise IndexError) whenever the
    label values exceed len(y).
    """
    if not n or len(X) <= n:
        return X, y
    rng = np.random.RandomState(random_state)
    positions = rng.choice(len(X), size=n, replace=False)
    X_sub = X.iloc[positions]
    y_sub = y.iloc[positions] if isinstance(y, pd.Series) else np.asarray(y)[positions]
    return X_sub, y_sub


def run_cv_regression(
    model: Any, X: pd.DataFrame, y: pd.Series, kf: KFold
) -> Dict[str, float]:
    mae, rmse_scores = [], []
    for train_idx, test_idx in kf.split(X):
        model.fit(X.iloc[train_idx], y.iloc[train_idx])
        y_pred = model.predict(X.iloc[test_idx])
        mae.append(mean_absolute_error(y.iloc[test_idx], y_pred))
        rmse_scores.append(rmse(y.iloc[test_idx], y_pred))

    return {
        "mae_mean": np.mean(mae),
        "mae_std": np.std(mae),
        "rmse_mean": np.mean(rmse_scores),
        "rmse_std": np.std(rmse_scores),
    }


def run_cv_classification(
    model: Any, X: pd.DataFrame, y: np.ndarray, kf: KFold
) -> Dict[str, float]:
    acc, prec, rec, f1 = [], [], [], []
    for train_idx, test_idx in kf.split(X):
        model.fit(X.iloc[train_idx], y[train_idx])
        y_pred = model.predict(X.iloc[test_idx])
        acc.append(np.mean(y_pred == y[test_idx]))
        from sklearn.metrics import precision_score, recall_score, f1_score

        prec.append(
            precision_score(y[test_idx], y_pred, average="weighted", zero_division=0)
        )
        rec.append(
            recall_score(y[test_idx], y_pred, average="weighted", zero_division=0)
        )
        f1.append(f1_score(y[test_idx], y_pred, average="weighted", zero_division=0))

    return {
        "Accuracy_mean": np.mean(acc),
        "Accuracy_std": np.std(acc),
        "Precision_mean": np.mean(prec),
        "Precision_std": np.std(prec),
        "Recall_mean": np.mean(rec),
        "Recall_std": np.std(rec),
        "F1_mean": np.mean(f1),
        "F1_std": np.std(f1),
    }


def train_regression_candidates(
    X: pd.DataFrame, y: pd.Series
) -> Tuple[
    Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[Dict[str, Any]]
]:
    kf = KFold(
        n_splits=CFG["kfold_splits"], shuffle=True, random_state=CFG["random_state"]
    )

    # All CV scoring happens on the CFG-bounded sample so every model family
    # (including the previously-unsampled Linear/Tree/SVM) is compared on the
    # same budget. Final models are always refit on the FULL dataset below.
    X_cv, y_cv = subsample(X, y, CFG["sample_cv"], CFG["random_state"])
    X_loss, y_loss = subsample(X, y, CFG["sample_loss"], CFG["random_state"])

    results = {}
    models = {}

    models["Linear"] = LinearRegression()
    results["Linear"] = run_cv_regression(models["Linear"], X_cv, y_cv, kf)
    models["Linear"].fit(X, y)

    models["Tree"] = DecisionTreeRegressor(
        max_depth=CFG["tree_max_depth"], random_state=CFG["random_state"]
    )
    results["Tree"] = run_cv_regression(models["Tree"], X_cv, y_cv, kf)
    models["Tree"].fit(X, y)

    svm_candidates = []
    for config in CFG["svm_configs"]:
        model = LinearSVR(
            C=config["C"],
            max_iter=CFG["svm_max_iter"],
            random_state=CFG["random_state"],
            dual=True,
        )
        metrics = run_cv_regression(model, X_cv, y_cv, kf)
        svm_candidates.append({**config, **metrics})
    best_svm = min(svm_candidates, key=lambda r: r["mae_mean"])
    results["SVM"] = best_svm
    models["SVM"] = LinearSVR(
        C=best_svm["C"],
        max_iter=CFG["svm_max_iter"],
        random_state=CFG["random_state"],
        dual=True,
    )
    models["SVM"].fit(X, y)

    nn_candidates = []
    loss_curves = []
    for config in CFG["nn_configs"]:
        model = MLPRegressor(
            hidden_layer_sizes=config["hidden_layer_sizes"],
            alpha=config["alpha"],
            learning_rate_init=config["learning_rate_init"],
            max_iter=CFG["nn_max_iter"],
            early_stopping=CFG["nn_early_stopping"],
            validation_fraction=CFG["nn_validation_fraction"],
            n_iter_no_change=CFG["nn_n_iter_no_change"],
            random_state=CFG["random_state"],
        )
        metrics = run_cv_regression(model, X_cv, y_cv, kf)
        nn_candidates.append({**config, **metrics})

        # Loss curves are plotted separately on CFG['sample_loss'] rows
        # (usually smaller than sample_cv) purely to keep curve-fitting fast.
        model_full = MLPRegressor(
            hidden_layer_sizes=config["hidden_layer_sizes"],
            alpha=config["alpha"],
            learning_rate_init=config["learning_rate_init"],
            max_iter=CFG["nn_max_iter"],
            early_stopping=CFG["nn_early_stopping"],
            validation_fraction=CFG["nn_validation_fraction"],
            n_iter_no_change=CFG["nn_n_iter_no_change"],
            random_state=CFG["random_state"],
        )
        model_full.fit(X_loss, y_loss)
        loss_curves.append(
            {
                "name": config["name"],
                "train_loss": model_full.loss_curve_,
                "val_loss": model_full.validation_scores_,
            }
        )

    best_nn = min(nn_candidates, key=lambda r: r["mae_mean"])
    results["NeuralNet"] = best_nn
    models["NeuralNet"] = MLPRegressor(
        hidden_layer_sizes=best_nn["hidden_layer_sizes"],
        alpha=best_nn["alpha"],
        learning_rate_init=best_nn["learning_rate_init"],
        max_iter=CFG["nn_max_iter"],
        early_stopping=CFG["nn_early_stopping"],
        validation_fraction=CFG["nn_validation_fraction"],
        n_iter_no_change=CFG["nn_n_iter_no_change"],
        random_state=CFG["random_state"],
    )
    models["NeuralNet"].fit(X, y)

    return results, models, best_svm, best_nn, loss_curves


def train_classification_candidates(X: pd.DataFrame, y: np.ndarray) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[Dict[str, Any]],
]:
    kf = KFold(
        n_splits=CFG["kfold_splits"], shuffle=True, random_state=CFG["random_state"]
    )

    X_cv, y_cv = subsample(X, y, CFG["sample_cv"], CFG["random_state"])
    X_loss, y_loss = subsample(X, y, CFG["sample_loss"], CFG["random_state"])

    results = {}
    models = {}

    models["Decision_Tree"] = DecisionTreeClassifier(
        max_depth=CFG["tree_max_depth"], random_state=CFG["random_state"]
    )
    results["Decision_Tree"] = run_cv_classification(
        models["Decision_Tree"], X_cv, y_cv, kf
    )
    models["Decision_Tree"].fit(X, y)

    nn_candidates = []
    loss_curves = []
    for config in CFG["nn_configs"]:
        model = MLPClassifier(
            hidden_layer_sizes=config["hidden_layer_sizes"],
            alpha=config["alpha"],
            learning_rate_init=config["learning_rate_init"],
            max_iter=CFG["nn_max_iter"],
            early_stopping=CFG["nn_early_stopping"],
            validation_fraction=CFG["nn_validation_fraction"],
            n_iter_no_change=CFG["nn_n_iter_no_change"],
            random_state=CFG["random_state"],
        )
        metrics = run_cv_classification(model, X_cv, y_cv, kf)
        nn_candidates.append({**config, **metrics})

        # Loss curves plotted on the smaller CFG['sample_loss'] budget.
        model_full = MLPClassifier(
            hidden_layer_sizes=config["hidden_layer_sizes"],
            alpha=config["alpha"],
            learning_rate_init=config["learning_rate_init"],
            max_iter=CFG["nn_max_iter"],
            early_stopping=True,
            validation_fraction=CFG["nn_validation_fraction"],
            n_iter_no_change=CFG["nn_n_iter_no_change"],
            random_state=CFG["random_state"],
        )
        model_full.fit(X_loss, y_loss)
        loss_curves.append(
            {
                "name": config["name"],
                "train_loss": model_full.loss_curve_,
                "val_loss": model_full.validation_scores_,
            }
        )

    best_nn = max(nn_candidates, key=lambda r: r["F1_mean"])
    models["NeuralNet"] = MLPClassifier(
        hidden_layer_sizes=best_nn["hidden_layer_sizes"],
        alpha=best_nn["alpha"],
        learning_rate_init=best_nn["learning_rate_init"],
        max_iter=CFG["nn_max_iter"],
        early_stopping=CFG["nn_early_stopping"],
        validation_fraction=CFG["nn_validation_fraction"],
        n_iter_no_change=CFG["nn_n_iter_no_change"],
        random_state=CFG["random_state"],
    )
    models["NeuralNet"].fit(X, y)
    results["NeuralNet"] = best_nn

    svm_candidates = []
    for config in CFG["svm_configs"]:
        model = LinearSVC(
            C=config["C"],
            max_iter=CFG["svm_max_iter"],
            random_state=CFG["random_state"],
        )
        metrics = run_cv_classification(model, X_cv, y_cv, kf)
        svm_candidates.append({**config, **metrics})
    best_svm = max(svm_candidates, key=lambda r: r["F1_mean"])
    results["SVM"] = best_svm
    models["SVM"] = LinearSVC(
        C=best_svm["C"], max_iter=CFG["svm_max_iter"], random_state=CFG["random_state"]
    )
    models["SVM"].fit(X, y)

    knn_candidates = []
    for k in [3, 5, 7, 11, 15]:
        model = KNeighborsClassifier(n_neighbors=k, n_jobs=-1)
        metrics = run_cv_classification(model, X_cv, y_cv, kf)
        knn_candidates.append({"k": k, **metrics})
    best_knn = max(knn_candidates, key=lambda r: r["F1_mean"])
    results["KNN"] = best_knn
    models["KNN"] = KNeighborsClassifier(n_neighbors=best_knn["k"], n_jobs=-1)
    models["KNN"].fit(X, y)

    return results, models, best_svm, best_nn, best_knn, loss_curves


def get_artifact_paths(
    result_dir: str, profile_tag: str, version: str
) -> Dict[str, Path]:
    base_dir = Path(result_dir) / profile_tag / version
    return {
        "base_dir": base_dir,
        "models": base_dir / "models",
        "metadata": base_dir / "metadata",
        "scaler": base_dir / "models" / f"{profile_tag}_scaler.pkl",
        "geo_mapping": base_dir / "models" / f"{profile_tag}_geo_mapping.pkl",
        "regression": {
            "Linear": base_dir / "models" / f"{profile_tag}_model_lr.pkl",
            "Tree": base_dir / "models" / f"{profile_tag}_model_tree.pkl",
            "SVM": base_dir / "models" / f"{profile_tag}_model_svm.pkl",
            "NeuralNet": base_dir / "models" / f"{profile_tag}_model_nn.pkl",
        },
        "classification": {
            "Decision_Tree": base_dir / "models" / f"{profile_tag}_model_tree_clf.pkl",
            "NeuralNet": base_dir / "models" / f"{profile_tag}_model_nn_clf.pkl",
            "SVM": base_dir / "models" / f"{profile_tag}_model_svm_clf.pkl",
            "KNN": base_dir / "models" / f"{profile_tag}_model_knn_clf.pkl",
        },
        "summary": base_dir / "metadata" / "summary.json",
        "results": base_dir / "metadata" / "results.json",
        "results_clf": base_dir / "metadata" / "results_clf.json",
        "curves": base_dir / "metadata" / "curves.json",
        "config": base_dir / "metadata" / "config.json",
    }


def save_training_artifacts(
    result_dir: str,
    profile_tag: str,
    version: str,
    scaler: Any,
    regression_models: Dict[str, Any],
    classification_models: Dict[str, Any],
    regression_results: Dict[str, Any],
    classification_results: Dict[str, Any],
    best_svm_reg: Dict[str, Any],
    best_nn_reg: Dict[str, Any],
    best_svm_clf: Dict[str, Any],
    best_nn_clf: Dict[str, Any],
    best_knn_clf: Dict[str, Any],
    curves: Dict[str, Any],
    geo_mapping: pd.DataFrame,
    cfg: Dict[str, Any],
) -> Dict[str, Any]:
    paths = get_artifact_paths(result_dir, profile_tag, version)
    paths["models"].mkdir(parents=True, exist_ok=True)
    paths["metadata"].mkdir(parents=True, exist_ok=True)

    save_pickle(regression_models["Linear"], paths["regression"]["Linear"])
    save_pickle(regression_models["Tree"], paths["regression"]["Tree"])
    save_pickle(regression_models["SVM"], paths["regression"]["SVM"])
    save_pickle(regression_models["NeuralNet"], paths["regression"]["NeuralNet"])
    save_pickle(
        classification_models["Decision_Tree"], paths["classification"]["Decision_Tree"]
    )
    save_pickle(
        classification_models["NeuralNet"], paths["classification"]["NeuralNet"]
    )
    save_pickle(classification_models["SVM"], paths["classification"]["SVM"])
    save_pickle(classification_models["KNN"], paths["classification"]["KNN"])
    save_pickle(scaler, paths["scaler"])
    save_pickle(geo_mapping, paths["geo_mapping"])

    save_pickle(regression_results, paths["results"])
    save_pickle(classification_results, paths["results_clf"])
    save_pickle(curves, paths["curves"])
    save_pickle(
        {
            "best_svm_reg": best_svm_reg,
            "best_nn_reg": best_nn_reg,
            "best_svm_clf": best_svm_clf,
            "best_nn_clf": best_nn_clf,
            "best_knn_clf": best_knn_clf,
        },
        paths["summary"],
    )
    save_pickle(cfg, paths["config"])

    return {
        "version": version,
        "base_dir": str(paths["base_dir"]),
        "models_dir": str(paths["models"]),
        "metadata_dir": str(paths["metadata"]),
        "paths": paths,
    }


def train_all(
    data_path: str,
    result_dir: str,
    profile_tag: str,
    version: Optional[str] = None,
    low_threshold: float = 0.33,
    medium_threshold: float = 0.66,
) -> Dict[str, Any]:
    version = get_version(version)
    data = load_dataset(data_path)
    prepared = prepare_training_data(data, low_threshold, medium_threshold)

    X_scaled = prepared["X_scaled"]
    y_reg = prepared["y_reg"]
    y_clf = prepared["y_clf"]
    scaler = prepared["scaler"]
    le_distrito = prepared["le_distrito"]
    le_concelho = prepared["le_concelho"]

    (
        regression_results,
        regression_models,
        best_svm_reg,
        best_nn_reg,
        reg_loss_curves,
    ) = train_regression_candidates(X_scaled, y_reg)
    (
        classification_results,
        classification_models,
        best_svm_clf,
        best_nn_clf,
        best_knn_clf,
        clf_loss_curves,
    ) = train_classification_candidates(X_scaled, y_clf)

    curves = {
        "regression_loss_curves": reg_loss_curves,
        "classification_loss_curves": clf_loss_curves,
    }

    geo_mapping = pd.DataFrame(
        {
            "Distrito": le_distrito.inverse_transform(prepared["df"]["Distrito_enc"]),
            "Concelho": le_concelho.inverse_transform(prepared["df"]["Concelho_enc"]),
            "Distrito_enc": prepared["df"]["Distrito_enc"],
            "Concelho_enc": prepared["df"]["Concelho_enc"],
        }
    ).drop_duplicates()

    saved = save_training_artifacts(
        result_dir,
        profile_tag,
        version,
        scaler,
        regression_models,
        classification_models,
        regression_results,
        classification_results,
        best_svm_reg,
        best_nn_reg,
        best_svm_clf,
        best_nn_clf,
        best_knn_clf,
        curves,
        geo_mapping,
        CFG,
    )

    return {
        "profile_tag": profile_tag,
        "version": version,
        "result_dir": saved["base_dir"],
        "models_dir": saved["models_dir"],
        "metadata_dir": saved["metadata_dir"],
        "regression_results": regression_results,
        "classification_results": classification_results,
        "best_svm_reg": best_svm_reg,
        "best_nn_reg": best_nn_reg,
        "best_svm_clf": best_svm_clf,
        "best_nn_clf": best_nn_clf,
        "best_knn_clf": best_knn_clf,
        "geo_mapping": geo_mapping,
        "curves": curves,
    }
