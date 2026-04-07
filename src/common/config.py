from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Any, Dict
import yaml


@dataclass(frozen=True)
class Config:
    raw: Dict[str, Any]

    @staticmethod
    def load(path: str) -> "Config":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Expand env var references
        data["sources"]["fred"]["api_key"] = os.getenv(
            data["sources"]["fred"]["api_key_env"], ""
        )

        return Config(raw=data)

    def get(self, *keys: str, default=None):
        cur: Any = self.raw
        for k in keys:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                return default
        return cur
    
cfg = Config.load("config/base.yaml")
print(cfg.raw)