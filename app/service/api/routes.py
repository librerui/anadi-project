from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..core.logging import configure_logging
from ..core.config import settings
from ..repositories.model_repository import ModelRepository
from ..repositories.ptd_repository import PTDRepository
from ..schemas.health import HealthResponse
from ..schemas.model import FeatureImportanceResponse
from ..schemas.prediction import PredictionRequest, PredictionResponse
from ..schemas.simulation import SimulationRequest, SimulationResponse
from ..schemas.ptd import PTDResponse, PTDListResponse
from ..services.prediction_service import PredictionService

router = APIRouter(prefix="/api/v1", tags=["Prediction API"])


_model_repository: ModelRepository | None = None
_ptd_repository: PTDRepository | None = None


def get_repository() -> ModelRepository:
    global _model_repository
    if _model_repository is None:
        _model_repository = ModelRepository(settings.model_root)
    return _model_repository


def get_ptd_repository() -> PTDRepository:
    global _ptd_repository
    if _ptd_repository is None:
        _ptd_repository = PTDRepository(settings.raw_ptd_data_path)
    return _ptd_repository


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


def _parse_coordinates(raw: dict) -> tuple[float | None, float | None]:
    raw_value = raw.get("Coordenadas Geográficas")
    if isinstance(raw_value, str):
        parts = [part.strip() for part in raw_value.split(",")]
        if len(parts) == 2:
            try:
                latitude = float(parts[0])
                longitude = float(parts[1])
                return latitude, longitude
            except ValueError:
                pass

    try:
        latitude = raw.get("Latitude")
        longitude = raw.get("Longitude")
        return (float(latitude), float(longitude)) if latitude is not None and longitude is not None else (None, None)
    except (TypeError, ValueError):
        return None, None


def _normalize_ptd_record(raw: dict) -> dict:
    latitude, longitude = _parse_coordinates(raw)
    return {
        "distrito": raw.get("Distrito"),
        "concelho": raw.get("Concelho"),
        "codigo_instalacao": raw.get("Código de Instalação"),
        "potencia_instalada": raw.get("Potência instalada [kVA]"),
        "n_clientes": int(raw.get("N_Clientes", 0)),
        "p_ip_total": float(raw.get("P_IP_Total", 0.0)),
        "p_ip_inef": float(raw.get("P_IP_Inef", 0.0)),
        "led_ratio": float(raw.get("LED_Ratio", 0.0)),
        "n_luminarias": int(raw.get("N_Luminarias", 0)),
        "n_lampadas": int(raw.get("N_Lampadas", 0)),
        "cap_per_cliente": float(raw.get("Cap_per_Cliente", 0.0)),
        "distrito_enc": raw.get("Distrito_enc"),
        "concelho_enc": raw.get("Concelho_enc"),
        "pfolga_ptd": raw.get("PFolga_PTD"),
        "util_decimal": raw.get("Util_Decimal"),
        "latitude": latitude,
        "longitude": longitude,
    }


@router.get(
    "/ptds",
    response_model=PTDListResponse,
    summary="List available PTDs",
    description="List PTDs filtered by distrito and concelho, returning a small selection of metadata for the UI.",
)
def list_ptds(
    distrito: str | None = None,
    concelho: str | None = None,
    profile: str = "leve",
    version: str | None = None,
    limit: int | None = None,
    repository: PTDRepository = Depends(get_ptd_repository),
    model_repository: ModelRepository = Depends(get_repository),
) -> PTDListResponse:
    try:
        ptds = repository.list_ptds(distrito, concelho, limit)
        geo_mapping = model_repository.get_geo_mapping(profile, version)
        ptds = ptds.merge(
            geo_mapping,
            on=["Distrito", "Concelho"],
            how="left",
            suffixes=(None, None),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    normalized = [_normalize_ptd_record(record) for record in ptds.to_dict(orient="records")]
    return PTDListResponse(items=normalized)


@router.get(
    "/ptds/{ptd_id}",
    response_model=PTDResponse,
    summary="Get PTD details",
    description="Fetch a single PTD row by its installation code.",
)
def get_ptd(
    ptd_id: str,
    profile: str = "leve",
    version: str | None = None,
    repository: PTDRepository = Depends(get_ptd_repository),
    model_repository: ModelRepository = Depends(get_repository),
) -> PTDResponse:
    try:
        ptd = repository.get_ptd(ptd_id)
        geo_mapping = model_repository.get_geo_mapping(profile, version)
        encoded = geo_mapping[
            (geo_mapping["Distrito"] == ptd["Distrito"]) 
            & (geo_mapping["Concelho"] == ptd["Concelho"])
        ]
        if not encoded.empty:
            ptd["Distrito_enc"] = int(encoded.iloc[0]["Distrito_enc"])
            ptd["Concelho_enc"] = int(encoded.iloc[0]["Concelho_enc"])
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return PTDResponse(item=_normalize_ptd_record(ptd.to_dict()))


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