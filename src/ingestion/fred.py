from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import requests

@dataclass
class FredSeriesObs:
    series_id: str
    date: str
    value: float

class FredClient:
    def __init__(self, api_key: str, base_url: str = "https://api.stlouisfed.org/fred", timeout_s: int = 30):
        if not api_key:
            raise ValueError("Missing FRED API key. Set env var FRED_API_KEY.")
        self.api_key = api_key
        self.base_url = base_url
        self.timeout_s = timeout_s
    

    def get_series_observations(self, series_id: str) -> List[FredSeriesObs]:
        url = f"{self.base_url}/series/observations"
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json"
        }
        r = requests.get(url, params=params, timeout=self.timeout_s)
        r.raise_for_status()
        data: Dict = r.json()
        out: List[FredSeriesObs] = []
        for obs in data.get("observations", []):
            val= obs.get("value",".")
            if val==".":
                continue
            out.append(FredSeriesObs(series_id=series_id, date=obs["date"], value=float(val)))
        return out 