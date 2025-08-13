"""Service for interacting with Radarr API."""

from dataclasses import dataclass
from typing import List, Dict, Any
import requests

from radarr_sonarr_mcp.config import RadarrConfig
from ..base import BaseArrService


@dataclass
class Movie:
    """Movie data class."""
    id: int
    title: str
    year: int
    overview: str
    has_file: bool
    status: str
    tags: List[int] | None = None
    genres: List[str] | None = None
    data: Dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Movie":
        """Create a Movie object from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            year=data.get("year", 0),
            overview=data.get("overview", ""),
            has_file=data.get("hasFile", False),
            status=data.get("status", ""),
            tags=data.get("tags", []),
            genres=data.get("genres", []),
            data=data,
        )


class RadarrService(BaseArrService):
    """Service for interacting with Radarr API."""

    def __init__(self, config: RadarrConfig):
        """Initialize the Radarr service with configuration."""
        super().__init__(config.base_url, config.api_key)
        self.config = config

    def get_all_movies(self) -> List[Movie]:
        """Fetch all movies from Radarr."""
        try:
            data = self._request("movie")
            return [Movie.from_dict(m) for m in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error fetching movies from Radarr: {e}")
            raise Exception(f"Failed to fetch movies from Radarr: {e}")

    def lookup_movie(self, term: str) -> List[Movie]:
        """Look up movies by search term."""
        try:
            data = self._request("movie/lookup", params={"term": term})
            return [Movie.from_dict(m) for m in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error looking up movie in Radarr: {e}")
            raise Exception(f"Failed to lookup movie in Radarr: {e}")

    def get_movie_file(self, movie_id: int) -> Dict[str, Any]:
        """Get the file information for a movie."""
        try:
            return self._request("moviefile", params={"movieId": movie_id})
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error fetching movie file for ID {movie_id}: {e}")
            raise Exception(f"Failed to fetch movie file: {e}")

    def is_movie_watched(self, movie: Movie) -> bool:
        """Check if a movie is watched based on tags."""  # pragma: no cover - simple logic
        return movie.data.get("movieFile", {}).get("mediaInfo", {}).get("watched", False)

    def is_movie_in_watchlist(self, movie: Movie) -> bool:
        """Check if a movie is in the watchlist based on tags."""  # pragma: no cover - simple logic
        return 1 in (movie.tags or [])
