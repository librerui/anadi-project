from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_MODEL_ROOT = ROOT / "models"
DEFAULT_PROFILE = os.environ.get("SERVICE_PROFILE", "leve")
DEFAULT_VERSION = os.environ.get("SERVICE_MODEL_VERSION")
DEFAULT_RELOAD_ON_START = os.environ.get("SERVICE_RELOAD_ON_START", "true").lower() in (
    "1",
    "true",
    "yes",
)


class Settings:
    def __init__(self) -> None:
        self.model_root: Path = Path(
            os.environ.get("SERVICE_MODEL_ROOT", DEFAULT_MODEL_ROOT)
        ).resolve()
        self.default_profile: str = os.environ.get("SERVICE_PROFILE", DEFAULT_PROFILE)
        self.default_version: Optional[str] = os.environ.get("SERVICE_MODEL_VERSION")
        self.reload_on_start: bool = DEFAULT_RELOAD_ON_START


settings = Settings()
