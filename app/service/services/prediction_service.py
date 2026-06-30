from __future__ import annotations

import logging
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable

import numpy as np
import pandas as pd
from fastapi import HTTPException

from ..repositories.model_repository import ModelArtifacts, ModelRepository
from ..schemas.model import FeatureImportanceResponse
from ..schemas.prediction import PredictionRequest, PredictionResponse
from ..schemas.simulation import SimulationRequest, SimulationResponse


class PredictionService:
    DEFAULT_REGRESSION_MODEL = "NeuralNet"
    DEFAULT_CLASSIFICATION_MODEL = "NeuralNet"

    def __init__(self, repository: ModelRepository) -> None:
        self.repository = repository

    def _build_feature_frame(
        self, artifacts: ModelArtifacts, raw_features: Dict[str, float]
    ) -> pd.DataFrame:
        missing = [name for name in artifacts.feature_names if name not in raw_features]
        extra = [name for name in raw_features if name not in artifacts.feature_names]
        if missing or extra:
            messages = []
            if missing:
                messages.append(f"Missing features: {missing}")
            if extra:
                messages.append(f"Unexpected features: {extra}")
            raise HTTPException(status_code=422, detail="; ".join(messages))

        return pd.DataFrame([raw_features], columns=artifacts.feature_names)

    def _select_model(
        self, artifacts: ModelArtifacts, task: str, model_name: str | None
    ) -> Any:
        if task == "regression":
            models = artifacts.regression_models
            default = self.DEFAULT_REGRESSION_MODEL
        else:
            models = artifacts.classification_models
            default = self.DEFAULT_CLASSIFICATION_MODEL

        selected = model_name or default
        if selected not in models:
            raise HTTPException(
                status_code=422,
                detail=f"Unknown model_name for {task}: {selected}. Available: {list(models)}",
            )
        return models[selected]

    def _scale(self, artifacts: ModelArtifacts, X: pd.DataFrame) -> pd.DataFrame:
        try:
            scaled = artifacts.scaler.transform(X)
        except Exception as exc:
            raise HTTPException(
                status_code=400, detail=f"Failed to scale input features: {exc}"
            )
        return pd.DataFrame(scaled, columns=artifacts.feature_names)

    def _probabilities(self, model: Any, X: pd.DataFrame) -> Dict[str, float] | None:
        if hasattr(model, "predict_proba"):
            try:
                probs = model.predict_proba(X)
                if len(probs.shape) == 1:
                    return {str(i): float(probs[0])}
                return {
                    str(label): float(value)
                    for label, value in zip(model.classes_, probs[0])
                }
            except Exception as exc:
                logging.debug("Probability calculation failed: %s", exc)
        return None

    def _extract_coefficients(
        self, model: Any, feature_names: Iterable[str]
    ) -> Dict[str, float]:
        if hasattr(model, "feature_importances_"):
            importance = np.asarray(model.feature_importances_)
        elif hasattr(model, "coef_"):
            coefficients = np.asarray(model.coef_)
            if coefficients.ndim == 1:
                importance = np.abs(coefficients)
            else:
                importance = np.abs(coefficients).mean(axis=0)
        elif (
            hasattr(model, "coefs_") and isinstance(model.coefs_, list) and model.coefs_
        ):
            importance = np.abs(np.asarray(model.coefs_[0])).mean(axis=1)
        else:
            return {name: 0.0 for name in feature_names}

        return {
            name: float(value)
            for name, value in zip(feature_names, importance.tolist())
        }

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        artifacts = self.repository.load_artifacts(request.profile, request.version)
        model = self._select_model(artifacts, request.task, request.model_name)
        X = self._build_feature_frame(artifacts, request.features)
        X_scaled = self._scale(artifacts, X)

        try:
            y_pred = model.predict(X_scaled)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")

        if request.task == "regression":
            prediction = float(y_pred[0])
            raw_scores = None
        else:
            class_index = int(y_pred[0])
            class_label = artifacts.class_names[class_index]
            probabilities = self._probabilities(model, X_scaled)
            prediction = class_label
            raw_scores = probabilities

        return PredictionResponse(
            profile=artifacts.profile,
            version=artifacts.version,
            model_name=request.model_name
            or (
                self.DEFAULT_REGRESSION_MODEL
                if request.task == "regression"
                else self.DEFAULT_CLASSIFICATION_MODEL
            ),
            task=request.task,
            prediction=prediction,
            raw_scores=raw_scores,
        )

    def simulate_overload(self, request: SimulationRequest) -> SimulationResponse:
        if request.task != "classification":
            raise HTTPException(
                status_code=422,
                detail="Monte Carlo overload simulation is only available for classification tasks",
            )

        artifacts = self.repository.load_artifacts(request.profile, request.version)
        model = self._select_model(artifacts, request.task, request.model_name)
        X = self._build_feature_frame(artifacts, request.features)
        X_scaled = self._scale(artifacts, X)
        base = X_scaled.to_numpy()[0]

        rng = np.random.default_rng(request.seed)
        sample_predictions: list[int] = []
        for _ in range(request.iterations):
            noise = rng.normal(loc=0.0, scale=request.noise_scale, size=base.shape)
            sample = np.expand_dims(base + noise, axis=0)
            try:
                sample_pred = model.predict(sample)
            except Exception as exc:
                raise HTTPException(
                    status_code=500,
                    detail=f"Simulation failed during model prediction: {exc}",
                )
            sample_predictions.append(int(sample_pred[0]))

        counts = Counter(sample_predictions)
        target_index = artifacts.class_names.index(request.overload_class)
        overload_count = counts.get(target_index, 0)
        distribution = {
            artifacts.class_names[index]: counts.get(index, 0) / request.iterations
            for index in sorted(set(sample_predictions))
        }

        return SimulationResponse(
            profile=artifacts.profile,
            version=artifacts.version,
            model_name=request.model_name or self.DEFAULT_CLASSIFICATION_MODEL,
            task=request.task,
            iterations=request.iterations,
            overload_class=request.overload_class,
            overload_probability=float(overload_count) / request.iterations,
            distribution=distribution,
        )

    def feature_importance(
        self, profile: str, version: str | None, task: str
    ) -> FeatureImportanceResponse:
        artifacts = self.repository.load_artifacts(profile, version)
        if task == "regression":
            models = artifacts.regression_models
        else:
            models = artifacts.classification_models

        importance: Dict[str, Dict[str, float]] = {}
        for model_name, model in models.items():
            importance[model_name] = self._extract_coefficients(
                model, artifacts.feature_names
            )

        return FeatureImportanceResponse(
            profile=artifacts.profile,
            version=artifacts.version,
            task=task,
            feature_importances=importance,
        )
