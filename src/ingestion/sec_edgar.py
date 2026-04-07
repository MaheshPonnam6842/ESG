from __future__ import annotations
import json
import time
from dataclasses import dataclass
from typing import Dict, List, Optional
import requests

@dataclass
class SecFilingRef:
    cik: str
    form: str
    filing_date: str
    report_date: Optional[str]


class SecEdgarClient:
    """
    Minimal SEC EDGAR client using data.sec.gov endpoints.
    IMPORTANT: SEC expects a descriptive User-Agent identifying the requester.
    """    
    def __init__(self, user_agent: str, timeout_s: int = 30):
        self.user_agent = user_agent
        self.timeout_s = timeout_s
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent,
                      "Accept-Encoding": "gzip, deflate"
                      })
    
    def get_submissions(self, cik: str) -> Dict:
        cik_padded= str(cik).lstrip("0").zfill(10) #10 digit format
        url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"  
        r= self.session.get(url, timeout=self.timeout_s)   # sends http request to SEC
        r.raise_for_status() # checking for HTTP errors
        time.sleep(0.2) # SEC recommends no more than 10 requests per second
        return r.json() # parse JSON response into Python dict
    
    def list_recent_filings(self, cik: str, forms: List[str]) -> List[SecFilingRef]:
        data= self.get_submissions(cik)
        recent= data.get("filings", {}).get("recent", {})
        accessions= recent.get("accessionNumber", [])
        form_types= recent.get("form", [])      
        filing_dates= recent.get("filingDate", [])
        report_dates= recent.get("reportDate", [])

        out: List[SecFilingRef] = []

        for i in range(len(accessions)):
            if form_types[i] in forms:
                out.append(SecFilingRef(
                    accession_number=accessions[i],
                    form=form_types[i],
                    filing_date=filing_dates[i],
                    report_date=report_dates[i] if report_dates[i] else None
                ))


        return out

        