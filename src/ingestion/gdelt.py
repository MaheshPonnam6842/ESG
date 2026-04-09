from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import requests

@dataclass
class GdeltDocHit:
    url: str
    title: str
    seendate: str
    sourcecountry: str
    language: str
    tone: float


class GdeltClient:
    def __init__(self, doc_api: str="https://api.gdeltproject.org/api/v2/doc/doc", timeout_s: int = 30):
        self.doc_api = doc_api
        self.timeout_s = timeout_s

    def search(self, query: str,mode: str = "ArtList", max_records: int = 250) -> List[GdeltDocHit]:
        params= {
            "query": query,
            "mode": mode,
            "format": "json",
            "maxrecords": max_records,
            "sort": "HybridRel"
        }

        r= requests.get(self.doc_api, params=params, timeout=self.timeout_s)
        r.raise_for_status()
        data= r.json()
        out: List[GdeltDocHit] = []
        for art in data.get("articles", []):
            out.append(GdeltDocHit(
                url= art.get("url", ""),
                title= art.get("title", ""),
                seendate= art.get("seendate", ""),
                sourcecountry= art.get("sourcecountry", ""),
                language= art.get("language", ""),
                tone= float(art.get("tone", 0.0))
            ))
        
        return out