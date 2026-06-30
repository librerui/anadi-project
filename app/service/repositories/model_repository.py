from __future__ import annotations

import logging
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

class ModelArtifacts:
    def __init__(
        self,
        profile: str,
        version: str,
        model_root: Path,
        scaler: Any,
        geo_mapping: Optional[pd.DataFrame],
        regression_models: Dict[str, Any],
        classification_models: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.profile = profile
        self.version = version
        self.model_root = model_root
        self.scaler = scaler
        self.geo_mapping = geo_mapping
        self.regression_models = regression_models
        self.classification_models = classification_models
        self.config = config or {}
        self.feature_names = self._extract_feature_names()
        self.class_names = ["baixo", "medio", "alto"]

    def _extract_feature_names(self) -> List[str]:
        feature_names = getattr(self.scaler, "feature_names_in_", None)
        if feature_names is not None:
            return list(feature_names)
        feature_count = getattr(self.scaler, "n_features_in_", None)
        if feature_count is not None:
            return [f"feature_{i}" for i in range(feature_count)]
        raise ValueError("Unable to determine feature names from scaler object")


class ModelRepository:
    def __init__(self, model_root: Path) -> None:
        self.model_root = Path(model_root)
        self._cache: Dict[tuple[str, str], ModelArtifacts] = {}
        self.ready = False

    def _validate_version(self, version: str) -> None:
        if not version.isdigit() or len(version) != 14:
            raise ValueError(
                f"Invalid version format: '{version}'. Expected a 14-digit timestamp (YYYYMMDDHHMMSS)."
            )

    def _pickle_load(self, path: Path) -> Any:
        if not path.exists():
            raise FileNotFoundError(f"Missing artifact file: {path}")
        with path.open("rb") as handle:
            return pickle.load(handle)

    def _artifact_base(self, profile_tag: str, version: str) -> Path:
        return self.model_root / profile_tag / version

    def list_versions(self, profile_tag: str) -> List[str]:
        profile_dir = self.model_root / profile_tag
        if not profile_dir.exists() or not profile_dir.is_dir():
            raise FileNotFoundError(f"Profile directory not found: {profile_dir}")
        versions = [item.name for item in profile_dir.iterdir() if item.is_dir()]
        versions.sort()
        return versions

    def get_latest_version(self, profile_tag: str) -> str:
        versions = self.list_versions(profile_tag)

        if not versions:
            raise FileNotFoundError(f"No versions found for profile {profile_tag}")
        elif versions[-1] is not None:
            self._validate_version(versions[-1]);

        return versions[-1]

    def load_artifacts(
        self, profile_tag: str = "leve", version: Optional[str] = None
    ) -> ModelArtifacts:
        version = version or self.get_latest_version(profile_tag)
        cache_key = (profile_tag, version)
        if cache_key in self._cache:
            return self._cache[cache_key]

        base_dir = self._artifact_base(profile_tag, version)
        models_dir = base_dir / "models"
        metadata_dir = base_dir / "metadata"

        if not models_dir.exists():
            raise FileNotFoundError(f"Model directory not found: {models_dir}")

        scaler = self._pickle_load(models_dir / f"{profile_tag}_scaler.pkl")
        geo_mapping = None
        geo_path = models_dir / f"{profile_tag}_geo_mapping.pkl"
        if geo_path.exists():
            geo_mapping = self._pickle_load(geo_path)

        regression_models = {
            "Linear": self._pickle_load(models_dir / f"{profile_tag}_model_lr.pkl"),
            "Tree": self._pickle_load(models_dir / f"{profile_tag}_model_tree.pkl"),
            "SVM": self._pickle_load(models_dir / f"{profile_tag}_model_svm.pkl"),
            "NeuralNet": self._pickle_load(models_dir / f"{profile_tag}_model_nn.pkl"),
        }
        classification_models = {
            "Decision_Tree": self._pickle_load(
                models_dir / f"{profile_tag}_model_tree_clf.pkl"
            ),
            "NeuralNet": self._pickle_load(
                models_dir / f"{profile_tag}_model_nn_clf.pkl"
            ),
            "SVM": self._pickle_load(models_dir / f"{profile_tag}_model_svm_clf.pkl"),
            "KNN": self._pickle_load(models_dir / f"{profile_tag}_model_knn_clf.pkl"),
        }

        config = None
        config_path = metadata_dir / "config.json"
        if config_path.exists():
            config = self._pickle_load(config_path)

        artifacts = ModelArtifacts(
            profile=profile_tag,
            version=version,
            model_root=self.model_root,
            scaler=scaler,
            geo_mapping=geo_mapping,
            regression_models=regression_models,
            classification_models=classification_models,
            config=config,
        )
        self._cache[cache_key] = artifacts
        self.ready = True
        logging.info(
            "Loaded model artifacts for profile=%s version=%s", profile_tag, version
        )
        return artifacts

    def reload(
        self, profile_tag: str = "leve", version: Optional[str] = None
    ) -> ModelArtifacts:
        version = version or self.get_latest_version(profile_tag)
        cache_key = (profile_tag, version)
        if cache_key in self._cache:
            del self._cache[cache_key]
        artifacts = self.load_artifacts(profile_tag, version)
        return artifacts


__all__ = ["ModelRepository", "ModelArtifacts"]
