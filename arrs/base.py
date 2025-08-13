"""Shared functionality for Arr service wrappers."""

from typing import Any, Dict, Optional
import requests


class BaseArrService:
    """Base class providing HTTP helpers for Arr-style APIs."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        params = params.copy() if params else {}
        if self.api_key:
            params["apikey"] = self.api_key
        response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()
