from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel


class ModelInfo(BaseModel):
    name: str
    profile: str
    version: str
    task: str
    model_name: str
    available_models: List[str]


class FeatureImportanceResponse(BaseModel):
    profile: str
    version: str
    task: str
    feature_importances: Dict[str, Dict[str, float]]
