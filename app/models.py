from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, Dict, Any


class CurrencyRates(BaseModel):
    usd: float
    eur: float
    gbp: float
    jpy: float
    chf: float
    timestamp: datetime

    @field_validator('usd', 'eur', 'gbp', 'jpy', 'chf', mode='before')
    @classmethod
    def round_to_2_decimals(cls, v: float) -> float:
        return round(v, 2)


class StatsResponse(BaseModel):
    total_requests: int
    average_rates: Dict[str, float]
    last_requests: List[CurrencyRates]
