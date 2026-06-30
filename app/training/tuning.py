"""
Tuning script for the machine learning models.
"""

import json
from pathlib import Path
from typing import Any, Dict

BASE_CFG: Dict[str, Any] = {
    # Geral
    "name": "Default",
    "random_state": 32,
    "kfold_splits": 5,
    "sample_viz": 2000,
    # Subsampling (None = usar dataset completo)
    # Reduzir para testes rápidos; None para resultados finais
    "sample_cv": 15_000,  # amostras usadas no CV dos modelos lentos
    "sample_loss": 5_000,  # amostras para curvas de loss das NNs
    "sample_lc": 15_000,  # amostras para learning curves
    # Árvore de Regressão
    "tree_max_depth": 10,  # profundidade do modelo treinado
    "tree_viz_depth": 3,  # profundidade da árvore visualizada
    # SVM
    "svm_configs": [
        {"name": "LinearSVR C=0.1", "C": 0.1},
        {"name": "LinearSVR C=1.0", "C": 1.0},
        {"name": "LinearSVR C=10", "C": 10.0},
    ],
    "svm_max_iter": 3000,
    # Rede Neuronal
    "nn_configs": [
        {
            "name": "Rasa (1 camada, sem reg.)",
            "hidden_layer_sizes": (64,),
            "alpha": 0.0001,
            "learning_rate_init": 0.001,
        },
        {
            "name": "Média (2 camadas, L2 moderado)",
            "hidden_layer_sizes": (128, 64),
            "alpha": 0.001,
            "learning_rate_init": 0.001,
        },
        {
            "name": "Profunda (3 camadas, L2 forte)",
            "hidden_layer_sizes": (256, 128, 64),
            "alpha": 0.01,
            "learning_rate_init": 0.001,
        },
    ],
    "nn_max_iter": 150,
    "nn_early_stopping": True,
    "nn_n_iter_no_change": 10,
    "nn_validation_fraction": 0.1,
}

PROFILE_FILES = {
    "leve": "profiles/leve.json",
    "regular": "profiles/regular.json",
    "pesado": "profiles/pesado.json",
}
PROFILE_DIR = Path(__file__).resolve().parent


def load_profile(profile_name: str = "leve") -> Dict[str, Any]:
    profile_key = profile_name.lower()
    if profile_key not in PROFILE_FILES:
        raise ValueError(
            f"Profile '{profile_name}' is not valid. Choose from {list(PROFILE_FILES)}"
        )
    profile_path = PROFILE_DIR / PROFILE_FILES[profile_key]
    with open(profile_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_cfg(profile_name: str = "leve") -> Dict[str, Any]:
    cfg = BASE_CFG.copy()
    cfg.update(load_profile(profile_name))
    return cfg


CFG = build_cfg()

if __name__ == "__main__":
    profile_name = "leve"
    cfg = build_cfg(profile_name)
    print(f"Configurações do perfil '{profile_name}':")
    for k, v in cfg.items():
        print(f"  {k}: {v}")
