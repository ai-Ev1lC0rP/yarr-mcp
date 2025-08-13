"""Service for interacting with Sonarr API."""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import requests

from radarr_sonarr_mcp.config import SonarrConfig
from .base import BaseArrService


@dataclass
class Statistics:
    """Statistics for a TV series."""
    episode_file_count: int
    episode_count: int
    total_episode_count: int
    size_on_disk: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Statistics":
        return cls(
            episode_file_count=data.get("episodeFileCount", 0),
            episode_count=data.get("episodeCount", 0),
            total_episode_count=data.get("totalEpisodeCount", 0),
            size_on_disk=data.get("sizeOnDisk", 0),
        )


@dataclass
class Series:
    """TV Series data class."""
    id: int
    title: str
    year: Optional[int]
    overview: str
    status: str
    network: str
    tags: List[int]
    genres: List[str]
    statistics: Optional[Statistics]
    data: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Series":
        statistics = Statistics.from_dict(data["statistics"]) if "statistics" in data else None
        return cls(
            id=data["id"],
            title=data["title"],
            year=data.get("year"),
            overview=data.get("overview", ""),
            status=data.get("status", ""),
            network=data.get("network", ""),
            tags=data.get("tags", []),
            genres=data.get("genres", []),
            statistics=statistics,
            data=data,
        )


@dataclass
class Episode:
    """TV Episode data class."""
    id: int
    series_id: int
    episode_file_id: Optional[int]
    season_number: int
    episode_number: int
    title: str
    air_date: Optional[str]
    has_file: bool
    monitored: bool
    overview: str
    data: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Episode":
        return cls(
            id=data["id"],
            series_id=data["seriesId"],
            episode_file_id=data.get("episodeFileId"),
            season_number=data["seasonNumber"],
            episode_number=data["episodeNumber"],
            title=data.get("title", ""),
            air_date=data.get("airDate"),
            has_file=data.get("hasFile", False),
            monitored=data.get("monitored", True),
            overview=data.get("overview", ""),
            data=data,
        )


class SonarrService(BaseArrService):
    """Service for interacting with Sonarr API."""

    def __init__(self, config: SonarrConfig):
        super().__init__(config.base_url, config.api_key)
        self.config = config

    def get_all_series(self) -> List[Series]:
        try:
            data = self._request("series")
            return [Series.from_dict(s) for s in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error fetching series from Sonarr: {e}")
            raise Exception(f"Failed to fetch series from Sonarr: {e}")

    def lookup_series(self, term: str) -> List[Series]:
        try:
            data = self._request("series/lookup", params={"term": term})
            return [Series.from_dict(s) for s in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error looking up series in Sonarr: {e}")
            raise Exception(f"Failed to lookup series from Sonarr: {e}")

    def get_episodes(self, series_id: int) -> List[Episode]:
        try:
            data = self._request("episode", params={"seriesId": series_id})
            return [Episode.from_dict(ep) for ep in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error fetching episodes for series ID {series_id}: {e}")
            raise Exception(f"Failed to fetch episodes: {e}")

    def is_series_watched(self, series: Series) -> bool:  # pragma: no cover - simple logic
        if not series.statistics:
            return False
        return series.statistics.episode_file_count >= series.statistics.episode_count

    def is_series_in_watchlist(self, series: Series) -> bool:  # pragma: no cover - simple logic
        return 1 in (series.tags or [])
