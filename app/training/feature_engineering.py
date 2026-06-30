"""
Feature engineering functions for the machine learning models.

This module recreates the preprocessing pipeline used by PROJECT_2/main.ipynb:
- Drop redundant or non-predictive columns
- Build ordinal label encoders for Distrito/Concelho
- Create the classification target utilizRede from Util_Decimal
- Scale numeric features for SVM, KNN, and neural networks
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from typing import Any, Dict, List, Optional, Tuple

REGRESSION_TARGETS = [
    "PFolga_PTD",
    "Ganho_LED_PTD",
    "D_PTD",
    "Rate_Ineficiencia",
    "PVE_PTD",
]
CLASSIFICATION_TARGET = "utilizRede"
UTIL_DECIMAL = "Util_Decimal"

DROP_COLUMNS = [
    "Código de Instalação",
    "CodDistritoConcelho",
    "Coordenadas Geográficas",
    "Nível de Utilização [%]",
    "Cap_PTD_kVA",
    "Pot_Geracao_kW",
    "Geracao_per_Cliente",
    "N_Clientes_Produtores",
    "Clientes_Produtores_Ratio",
    "Pot_Contratada_kVA",
    "PContratada_per_Cliente",
    "N_PTDs_Concelho",
    "IP_per_PTD",
    "IP_Inef_per_PTD",
]


def load_dataset(path: str) -> pd.DataFrame:
    """Load the PTD dataset from an Excel file."""
    return pd.read_excel(path)


def drop_unused_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop columns that are not used for modeling."""
    return df.drop(columns=[col for col in DROP_COLUMNS if col in df.columns])


def create_classification_target(
    df: pd.DataFrame,
    low_threshold: float = 0.33,
    medium_threshold: float = 0.66,
) -> pd.DataFrame:
    """Create the utilizRede class target from Util_Decimal."""
    if UTIL_DECIMAL not in df.columns:
        raise ValueError(f"Expected column '{UTIL_DECIMAL}' in the dataframe")

    df = df.copy()
    df[CLASSIFICATION_TARGET] = pd.cut(
        df[UTIL_DECIMAL],
        bins=[-np.inf, low_threshold, medium_threshold, np.inf],
        labels=["baixo", "medio", "alto"],
    )
    return df


def build_label_encoders(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, LabelEncoder, LabelEncoder]:
    """Build label encoders for Distrito and Concelho and append encoded columns."""
    if "Distrito" not in df.columns or "Concelho" not in df.columns:
        raise ValueError("Expected columns 'Distrito' and 'Concelho' in the dataframe")

    df = df.copy()
    le_distrito = LabelEncoder()
    le_concelho = LabelEncoder()
    df["Distrito_enc"] = le_distrito.fit_transform(df["Distrito"])
    df["Concelho_enc"] = le_concelho.fit_transform(df["Concelho"])
    return df, le_distrito, le_concelho


def select_feature_columns(df: pd.DataFrame) -> List[str]:
    """Select numeric feature columns excluding targets and leakage columns."""
    excluded = set(
        REGRESSION_TARGETS + [CLASSIFICATION_TARGET, UTIL_DECIMAL, "D_PTD_LED"]
    )
    return [c for c in df.select_dtypes(include="number").columns if c not in excluded]


def scale_features(
    X: pd.DataFrame,
    scaler: Optional[StandardScaler] = None,
) -> Tuple[pd.DataFrame, StandardScaler]:
    """Standardize numeric features using StandardScaler."""
    if scaler is None:
        scaler = StandardScaler()

    X_scaled = pd.DataFrame(
        scaler.fit_transform(X),
        columns=X.columns,
        index=X.index,
    )
    return X_scaled, scaler


def prepare_training_data(
    df: pd.DataFrame,
    low_threshold: float = 0.33,
    medium_threshold: float = 0.66,
) -> Dict[str, Any]:
    """Prepare training datasets, encoders, and scaler for regression and classification."""
    df = df.copy()
    df = drop_unused_columns(df)
    df = create_classification_target(
        df,
        low_threshold=low_threshold,
        medium_threshold=medium_threshold,
    )
    df = df.dropna(
        subset=["D_PTD", "D_PTD_LED", UTIL_DECIMAL, "PFolga_PTD", CLASSIFICATION_TARGET]
    )
    df, le_distrito, le_concelho = build_label_encoders(df)

    feature_columns = select_feature_columns(df)
    X = df[feature_columns].copy()
    X_scaled, scaler = scale_features(X)

    categories = ["baixo", "medio", "alto"]
    df[CLASSIFICATION_TARGET] = pd.Categorical(
        df[CLASSIFICATION_TARGET], categories=categories, ordered=True
    )
    y_clf = df[CLASSIFICATION_TARGET].cat.codes.to_numpy()

    return {
        "df": df,
        "feature_columns": feature_columns,
        "X": X,
        "X_scaled": X_scaled,
        "y_reg": df["PFolga_PTD"].copy(),
        "y_clf": y_clf,
        "scaler": scaler,
        "le_distrito": le_distrito,
        "le_concelho": le_concelho,
        "class_names": categories,
        "low_threshold": low_threshold,
        "medium_threshold": medium_threshold,
    }
