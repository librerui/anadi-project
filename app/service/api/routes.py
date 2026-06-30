from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..core.logging import configure_logging
from ..repositories.model_repository import ModelRepository
from ..schemas.health import HealthResponse
from ..schemas.model import FeatureImportanceResponse
from ..schemas.prediction import PredictionRequest, PredictionResponse
from ..schemas.simulation import SimulationRequest, SimulationResponse
from ..services.prediction_service import PredictionService
from ..core.config import settings

router = APIRouter(prefix="/api/v1", tags=["Prediction API"])


def get_repository() -> ModelRepository:
    return ModelRepository(settings.model_root)


def get_service(
    repository: ModelRepository = Depends(get_repository),
) -> PredictionService:
    return PredictionService(repository)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the service health status. Always returns `pass` if the service is running.",
    tags=["System"],
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {"status": "pass", "detail": "Service is running"}
                }
            },
        }
    },
)
def health() -> HealthResponse:
    return HealthResponse(status="pass", detail="Service is running")


@router.get(
    "/ready",
    response_model=HealthResponse,
    summary="Readiness check",
    description="Verifies that the model artifacts directory is accessible and contains models.",
    tags=["System"],
    responses={
        200: {
            "description": "Model artifacts are available",
            "content": {
                "application/json": {
                    "example": {"status": "pass", "detail": "Model artifacts available"}
                }
            },
        },
        503: {
            "description": "Model root directory does not exist or is inaccessible",
            "content": {
                "application/json": {
                    "example": {"detail": "Model root is unavailable"}
                }
            },
        },
    },
)
def readiness(repository: ModelRepository = Depends(get_repository)) -> HealthResponse:
    if not repository.model_root.exists():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model root is unavailable",
        )
    return HealthResponse(status="pass", detail="Model artifacts available")


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Run a single prediction",
    description=(
        "Perform a regression or classification prediction using the loaded model. "
        "The task type and model name determine which model is used. "
        "If `version` is omitted, the latest version for the given profile is used."
    ),
    tags=["Prediction"],
    responses={
        200: {
            "description": "Prediction successful",
            "content": {
                "application/json": {
                    "example": {
                        "profile": "leve",
                        "version": "20260630195806",
                        "model_name": "Decision_Tree",
                        "task": "classification",
                        "prediction": "medio",
                        "raw_scores": None,
                    }
                }
            },
        },
        422: {
            "description": "Validation error – invalid input data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "task"],
                                "msg": "value is not a valid enumeration member",
                                "type": "type_error.enum",
                            }
                        ]
                    }
                }
            },
        },
        404: {"description": "Model not found for the given profile/version/task/model_name"},
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "classification_decision_tree": {
                            "summary": "Classification with Decision Tree",
                            "description": "Predict utilization category using Decision Tree",
                            "value": {
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
                            },
                        },
                        "classification_neuralnet": {
                            "summary": "Classification with Neural Network",
                            "description": "Predict utilization category using NeuralNet",
                            "value": {
                                "profile": "leve",
                                "task": "classification",
                                "model_name": "NeuralNet",
                                "features": {
                                    "Potência instalada [kVA]": 20.0,
                                    "P_IP_Total": 150.0,
                                    "P_IP_Inef": 70.0,
                                    "LED_Ratio": 0.9,
                                    "N_Luminarias": 60,
                                    "N_Lampadas": 120,
                                    "Cap_per_Cliente": 3.0,
                                    "Distrito_enc": 1,
                                    "Concelho_enc": 2,
                                    "N_Clientes": 6,
                                },
                            },
                        },
                        "regression_linear": {
                            "summary": "Regression with Linear model",
                            "description": "Predict PFolga_PTD value using Linear Regression",
                            "value": {
                                "profile": "leve",
                                "task": "regression",
                                "model_name": "Linear",
                                "features": {
                                    "Potência instalada [kVA]": 10.0,
                                    "P_IP_Total": 100.0,
                                    "P_IP_Inef": 40.0,
                                    "LED_Ratio": 0.5,
                                    "N_Luminarias": 30,
                                    "N_Lampadas": 60,
                                    "Cap_per_Cliente": 1.8,
                                    "Distrito_enc": 2,
                                    "Concelho_enc": 4,
                                    "N_Clientes": 3,
                                },
                            },
                        },
                    }
                }
            }
        }
    },
)
def predict(
    request: PredictionRequest, service: PredictionService = Depends(get_service)
) -> PredictionResponse:
    return service.predict(request)


@router.post(
    "/simulate",
    response_model=SimulationResponse,
    summary="Run Monte Carlo overload simulation",
    description=(
        "Perform a Monte Carlo simulation to estimate the probability of overload "
        "based on the model predictions. The simulation generates random variations "
        "of the input features (by adding Gaussian noise) and counts how many "
        "predictions fall into the specified `overload_class`. "
        "Only classification tasks are supported."
    ),
    tags=["Simulation"],
    responses={
        200: {
            "description": "Simulation completed",
            "content": {
                "application/json": {
                    "example": {
                        "profile": "leve",
                        "version": "20260630195806",
                        "model_name": "Decision_Tree",
                        "task": "classification",
                        "iterations": 1000,
                        "overload_class": "alto",
                        "overload_probability": 0.78,
                        "distribution": {"baixo": 0.12, "medio": 0.10, "alto": 0.78},
                    }
                }
            },
        },
        422: {
            "description": "Validation error – invalid parameters (e.g., wrong task, missing features, invalid overload_class)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Monte Carlo overload simulation is only available for classification tasks"
                    }
                }
            },
        },
        404: {"description": "Model artifacts not found for the given profile/version/model_name"},
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "simulation_decision_tree": {
                            "summary": "Simulation with Decision Tree (default)",
                            "description": "Estimate overload probability using Decision Tree with 1000 samples",
                            "value": {
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
                            },
                        },
                        "simulation_neuralnet": {
                            "summary": "Simulation with Neural Network (higher noise)",
                            "description": "Estimate overload probability using NeuralNet with 2000 samples and higher noise",
                            "value": {
                                "profile": "leve",
                                "task": "classification",
                                "model_name": "NeuralNet",
                                "features": {
                                    "Potência instalada [kVA]": 20.0,
                                    "P_IP_Total": 150.0,
                                    "P_IP_Inef": 70.0,
                                    "LED_Ratio": 0.9,
                                    "N_Luminarias": 60,
                                    "N_Lampadas": 120,
                                    "Cap_per_Cliente": 3.0,
                                    "Distrito_enc": 1,
                                    "Concelho_enc": 2,
                                    "N_Clientes": 6,
                                },
                                "iterations": 2000,
                                "noise_scale": 0.2,
                                "overload_class": "medio",
                                "seed": 123,
                            },
                        },
                    }
                }
            }
        }
    },
)
def simulate(
    request: SimulationRequest, service: PredictionService = Depends(get_service)
) -> SimulationResponse:
    return service.simulate_overload(request)


@router.get(
    "/feature-importance",
    response_model=FeatureImportanceResponse,
    summary="Get feature importance for available models",
    description=(
        "Retrieve the feature importance scores for a specific model. "
        "If the model does not support feature importances (e.g., SVM), an empty list is returned."
    ),
    tags=["Model Metadata"],
    responses={
        200: {
            "description": "Feature importances retrieved",
            "content": {
                "application/json": {
                    "example": {
                        "profile": "leve",
                        "version": "20250215T123456",
                        "model_name": "tree_clf",
                        "task": "classification",
                        "importances": [
                            {"feature": "Potencia", "importance": 0.45},
                            {"feature": "Tensao", "importance": 0.32},
                        ],
                    }
                }
            },
        },
        422: {"description": "Invalid task (must be 'regression' or 'classification')"},
    },
)
def feature_importance(
    profile: str = "leve",
    version: str | None = None,
    task: str = "classification",
    service: PredictionService = Depends(get_service),
) -> FeatureImportanceResponse:
    if task not in {"classification", "regression"}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Task must be regression or classification",
        )
    return service.feature_importance(profile, version, task)


@router.post(
    "/reload",
    summary="Reload model artifacts into memory",
    description=(
        "Force-reload the model artifacts for a given profile and version. "
        "Useful when new models have been trained and you want the service to pick them up without restarting."
    ),
    tags=["System"],
    responses={
        200: {
            "description": "Models reloaded successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "pass",
                        "detail": "Models reloaded for profile=leve version=latest",
                    }
                }
            },
        },
        404: {"description": "The specified profile or version does not exist"},
    },
)
def reload_models(
    profile: str = "leve",
    version: str | None = None,
    repository: ModelRepository = Depends(get_repository),
) -> HealthResponse:
    
    if version is not None:
        try:
            repository._validate_version(version)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    repository.reload(profile, version)
    return HealthResponse(
        status="pass",
        detail=f'Models reloaded for profile={profile} version={version or "latest"}',
    )