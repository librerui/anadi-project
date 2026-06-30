from __future__ import annotations

from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field


class SimulationRequest(BaseModel):
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
    task: Literal["classification"] = Field(
        ...,
        description="Task type (only classification is supported for simulation)",
        example="classification",
    )
    model_name: Optional[str] = Field(
        default=None,
        description=(
            "Model identifier within the classification family. "
            "Available: Decision_Tree, NeuralNet, SVM, KNN."
        ),
        example="Decision_Tree",
    )
    features: Dict[str, float] = Field(
        ...,
        description=(
            "Input feature values. Must include **all** features that the model expects. "
            "See the `/predict` endpoint documentation for details."
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
    iterations: int = Field(
        default=1000,
        ge=1,
        description="Number of Monte Carlo samples",
        example=1000,
    )
    noise_scale: float = Field(
        default=0.1,
        gt=0,
        description="Standard deviation of Gaussian noise applied to scaled features",
        example=0.1,
    )
    overload_class: str = Field(
        default="alto",
        description="Class label considered as overload (must be one of: baixo, medio, alto)",
        example="alto",
    )
    seed: Optional[int] = Field(
        default=None,
        description="Random seed for reproducibility",
        example=42,
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
                "iterations": 1000,
                "noise_scale": 0.1,
                "overload_class": "alto",
                "seed": 42,
            }
        }


class SimulationResponse(BaseModel):
    profile: str
    version: str
    model_name: str
    task: str
    iterations: int
    overload_class: str
    overload_probability: float
    distribution: Dict[str, float]