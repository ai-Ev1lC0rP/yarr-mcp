"""Service for interacting with Whisparr API."""

from typing import List
import requests

from radarr_sonarr_mcp.config import WhisparrConfig
from .base import BaseArrService
from .radarr import Movie


class WhisparrService(BaseArrService):
    """Service for interacting with Whisparr API."""

    def __init__(self, config: WhisparrConfig):
        super().__init__(config.base_url, config.api_key)
        self.config = config

    def get_all_movies(self) -> List[Movie]:
        try:
            data = self._request("movie")
            return [Movie.from_dict(m) for m in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error fetching movies from Whisparr: {e}")
            raise Exception(f"Failed to fetch movies from Whisparr: {e}")

    def lookup_movie(self, term: str) -> List[Movie]:
        try:
            data = self._request("movie/lookup", params={"term": term})
            return [Movie.from_dict(m) for m in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error looking up movie in Whisparr: {e}")
            raise Exception(f"Failed to lookup movie in Whisparr: {e}")
