from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


class PTDRepository:
    def __init__(self, raw_data_path: Path) -> None:
        self.raw_data_path = Path(raw_data_path).resolve()
        self._cache: Optional[pd.DataFrame] = None

    def _load_dataframe(self) -> pd.DataFrame:
        if self._cache is None:
            self._cache = pd.read_excel(self.raw_data_path)
        return self._cache

    def preload(self) -> None:
        self._load_dataframe()

    def list_ptds(
        self,
        distrito: Optional[str] = None,
        concelho: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> pd.DataFrame:
        df = self._load_dataframe()
        if distrito:
            df = df[df["Distrito"] == distrito]
        if concelho:
            df = df[df["Concelho"] == concelho]
        return df.copy() if limit is None else df.head(limit).copy()

    def get_ptd(self, ptd_id: str) -> pd.Series:
        df = self._load_dataframe()
        result = df[df["Código de Instalação"] == ptd_id]
        if result.empty:
            raise KeyError(f"PTD not found: {ptd_id}")
        return result.iloc[0]
