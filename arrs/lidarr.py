"""Service for interacting with Lidarr API."""

from dataclasses import dataclass
from typing import List, Dict, Any
import requests

from radarr_sonarr_mcp.config import LidarrConfig
from .base import BaseArrService


@dataclass
class Artist:
    """Music artist representation."""
    id: int
    artist_name: str
    overview: str
    disambiguation: str
    tags: List[int]
    genres: List[str]
    data: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Artist":
        return cls(
            id=data["id"],
            artist_name=data.get("artistName", ""),
            overview=data.get("overview", ""),
            disambiguation=data.get("disambiguation", ""),
            tags=data.get("tags", []),
            genres=data.get("genres", []),
            data=data,
        )


class LidarrService(BaseArrService):
    """Service for interacting with Lidarr API."""

    def __init__(self, config: LidarrConfig):
        super().__init__(config.base_url, config.api_key)
        self.config = config

    def get_all_artists(self) -> List[Artist]:
        try:
            data = self._request("artist")
            return [Artist.from_dict(a) for a in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error fetching artists from Lidarr: {e}")
            raise Exception(f"Failed to fetch artists from Lidarr: {e}")

    def lookup_artist(self, term: str) -> List[Artist]:
        try:
            data = self._request("artist/lookup", params={"term": term})
            return [Artist.from_dict(a) for a in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error looking up artist in Lidarr: {e}")
            raise Exception(f"Failed to lookup artist in Lidarr: {e}")
