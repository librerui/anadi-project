"""Service package entrypoint for training CLI."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

PROFILE_FILES = {
    "leve": "profiles/leve.json",
    "regular": "profiles/regular.json",
    "pesado": "profiles/pesado.json",
}

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = REPO_ROOT / "PROJECT_2" / "data" / "PTD_level_dataset.xlsx"
DEFAULT_RESULTS_DIR = REPO_ROOT / "models"


def parse_args(args=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train models and save versioned artifacts under service/models.",
    )
    parser.add_argument(
        "--data-path",
        default=str(DEFAULT_DATA_PATH),
        help="Path to the input PTD dataset Excel file.",
    )
    parser.add_argument(
        "--results-dir",
        default=str(DEFAULT_RESULTS_DIR),
        help="Base directory where versioned training artifacts are stored.",
    )
    parser.add_argument(
        "--profile",
        choices=list(PROFILE_FILES.keys()),
        default="leve",
        help="Training profile to use for configuration.",
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Optional version tag to use for artifact versioning. Defaults to timestamp.",
    )
    parser.add_argument(
        "--low-threshold",
        type=float,
        default=0.33,
        help="Low threshold for classification target creation.",
    )
    parser.add_argument(
        "--medium-threshold",
        type=float,
        default=0.66,
        help="Medium threshold for classification target creation.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging verbosity level.",
    )
    return parser.parse_args(args)


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=getattr(logging, level),
    )


def main(args=None) -> int:
    parsed = parse_args(args)
    configure_logging(parsed.log_level)
    from .train import build_cfg, set_cfg, train_all

    cfg = build_cfg(parsed.profile)
    set_cfg(cfg)
    summary = train_all(
        data_path=str(Path(parsed.data_path).resolve()),
        result_dir=str(Path(parsed.results_dir).resolve()),
        profile_tag=parsed.profile,
        version=parsed.version,
        low_threshold=parsed.low_threshold,
        medium_threshold=parsed.medium_threshold,
    )
    logging.info("Training completed for profile %s", parsed.profile)
    logging.info("Version: %s", summary["version"])
    logging.info("Artifacts saved in %s", summary["result_dir"])
    return 0
