from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel, Field, constr


class PredictionRequest(BaseModel):
    profile: str = Field(
        default="leve",
        description="Training profile tag to use for loading artifacts",
        example="leve",
    )
    version: Optional[str] = Field(
        default=None,
        description="Model version to load; omitted means latest",
        example="20260630195806",
    )
    task: constr(pattern=r"^(regression|classification)$") = Field(
        ...,
        description="Prediction task type",
        example="classification",
    )
    model_name: Optional[str] = Field(
        default=None,
        description=(
            "Model identifier within the task family. "
            "For classification: Decision_Tree, NeuralNet, SVM, KNN. "
            "For regression: Linear, Tree, SVM, NeuralNet."
        ),
        example="Decision_Tree",
    )
    features: Dict[str, float] = Field(
        ...,
        description=(
            "Input feature values. Must include **all** features that the model expects. "
            "The exact feature set is stored in the model artifacts and can be retrieved "
            "via the `/feature-importance` endpoint. "
            "For the `leve` profile, typical features include: "
            "`Potência instalada [kVA]`, `P_IP_Total`, `P_IP_Inef`, `LED_Ratio`, "
            "`N_Luminarias`, `N_Lampadas`, `Cap_per_Cliente`, `Distrito_enc`, "
            "`Concelho_enc`, `N_Clientes`."
        ),
        example={
            "Potência instalada [kVA]": 15.5,
            "P_IP_Total": 123.4,
            "P_IP_Inef": 56.7,
            "LED_Ratio": 0.8,
            "N_Luminarias": 50,
            "N_Lampadas": 100,
            "Cap_per_Cliente": 2.5,
            "Distrito_enc": 3,
            "Concelho_enc": 5,
            "N_Clientes": 4,
        },
    )

    class Config:
        json_schema_extra = {
            "example": {
                "profile": "leve",
                "version": "20260630195806",
                "task": "classification",
                "model_name": "Decision_Tree",
                "features": {
                    "Potência instalada [kVA]": 15.5,
                    "P_IP_Total": 123.4,
                    "P_IP_Inef": 56.7,
                    "LED_Ratio": 0.8,
                    "N_Luminarias": 50,
                    "N_Lampadas": 100,
                    "Cap_per_Cliente": 2.5,
                    "Distrito_enc": 3,
                    "Concelho_enc": 5,
                    "N_Clientes": 4,
                },
            }
        }


class PredictionResponse(BaseModel):
    profile: str
    version: str
    model_name: str
    task: str
    prediction: float | str
    raw_scores: Optional[Dict[str, float]] = None