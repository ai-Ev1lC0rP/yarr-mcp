"""Service for interacting with Readarr API."""

from dataclasses import dataclass
from typing import List, Dict, Any
import requests

from radarr_sonarr_mcp.config import ReadarrConfig
from ..base import BaseArrService


@dataclass
class Book:
    """Book representation."""
    id: int
    title: str
    author: str
    overview: str
    tags: List[int]
    genres: List[str]
    data: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Book":
        author = ""
        if data.get("author"):
            author = data["author"].get("name", "")
        return cls(
            id=data["id"],
            title=data.get("title", ""),
            author=author,
            overview=data.get("overview", ""),
            tags=data.get("tags", []),
            genres=data.get("genres", []),
            data=data,
        )


class ReadarrService(BaseArrService):
    """Service for interacting with Readarr API."""

    def __init__(self, config: ReadarrConfig):
        super().__init__(config.base_url, config.api_key)
        self.config = config

    def get_all_books(self) -> List[Book]:
        try:
            data = self._request("book")
            return [Book.from_dict(b) for b in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error fetching books from Readarr: {e}")
            raise Exception(f"Failed to fetch books from Readarr: {e}")

    def lookup_book(self, term: str) -> List[Book]:
        try:
            data = self._request("book/lookup", params={"term": term})
            return [Book.from_dict(b) for b in data]
        except requests.RequestException as e:  # pragma: no cover - network failure
            import logging
            logging.error(f"Error looking up book in Readarr: {e}")
            raise Exception(f"Failed to lookup book in Readarr: {e}")
