"""Service wrappers for the various *arr* applications."""

from .base import BaseArrService
from .radarr import RadarrService, Movie
from .sonarr import SonarrService, Series, Episode, Statistics
from .whisparr import WhisparrService
from .lidarr import LidarrService, Artist
from .readarr import ReadarrService, Book

__all__ = [
    "BaseArrService",
    "RadarrService",
    "SonarrService",
    "WhisparrService",
    "LidarrService",
    "ReadarrService",
    "Movie",
    "Series",
    "Episode",
    "Statistics",
    "Artist",
    "Book",
]
