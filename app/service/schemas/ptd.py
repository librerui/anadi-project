from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class PTDBase(BaseModel):
    distrito: str
    concelho: str
    codigo_instalacao: str
    potencia_instalada: float
    n_clientes: int
    p_ip_total: float
    p_ip_inef: float
    led_ratio: float
    n_luminarias: int
    n_lampadas: int
    cap_per_cliente: float
    distrito_enc: Optional[int] = None
    concelho_enc: Optional[int] = None
    pfolga_ptd: Optional[float] = None
    util_decimal: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PTDListResponse(BaseModel):
    items: List[PTDBase]


class PTDResponse(BaseModel):
    item: PTDBase
