from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime


class CurrencyRates(BaseModel):
    usd: float
    eur: float
    gbp: float
    jpy: float
    chf: float
    timestamp: datetime


class StatsResponse(BaseModel):
    total_requests: int
    average_rates: Dict[str, float]
    last_requests: List[CurrencyRates]
