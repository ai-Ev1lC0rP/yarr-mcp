"""Minimal MCP server tying the Arr services together."""

from __future__ import annotations

import json
from typing import Optional

from fastmcp import FastMCP

from .config import Config, load_config
from arrs import RadarrService, SonarrService


class RadarrSonarrMCPServer:
    """Server exposing Radarr and Sonarr data via MCP."""

    def __init__(self, config: Config):
        self.config = config
        self.server = FastMCP(
            name="radarr-sonarr-mcp-server",
            description="MCP Server for Radarr and Sonarr media management",
        )
        self.radarr_service = RadarrService(config.radarr_config)
        self.sonarr_service = SonarrService(config.sonarr_config)
        self._register_tools()

    def _register_tools(self) -> None:
        @self.server.tool()
        def get_available_movies(year: Optional[int] = None,
                                 watched: Optional[bool] = None,
                                 actors: Optional[str] = None) -> str:
            """Return movies from Radarr with optional filters."""
            movies = self.radarr_service.get_all_movies()
            if year is not None:
                movies = [m for m in movies if m.year == year]
            if watched is not None:
                movies = [m for m in movies if self.radarr_service.is_movie_watched(m) == watched]
            if actors:
                movies = [
                    m for m in movies
                    if actors.lower() in [
                        c.get("name", "").lower()
                        for c in m.data.get("credits", {}).get("cast", [])
                    ]
                ]
            return json.dumps({"count": len(movies), "movies": [m.data for m in movies]})

        @self.server.tool()
        def get_available_series(year: Optional[int] = None,
                                 downloaded: Optional[bool] = None,
                                 watched: Optional[bool] = None,
                                 actors: Optional[str] = None) -> str:
            """Return series from Sonarr with optional filters."""
            series = self.sonarr_service.get_all_series()
            if year is not None:
                series = [s for s in series if s.year == year]
            if downloaded is not None:
                series = [
                    s for s in series
                    if (s.statistics and s.statistics.episode_file_count > 0) == downloaded
                ]
            if watched is not None:
                series = [s for s in series if self.sonarr_service.is_series_watched(s) == watched]
            if actors:
                series = [
                    s for s in series
                    if actors.lower() in [
                        c.get("name", "").lower()
                        for c in s.data.get("credits", {}).get("cast", [])
                    ]
                ]
            return json.dumps({"count": len(series), "series": [s.data for s in series]})

    def start(self) -> None:  # pragma: no cover - runtime helper
        self.server.run(port=self.config.server_config.port)


def create_server(config_path: Optional[str] = None) -> RadarrSonarrMCPServer:
    """Create a configured server instance."""
    cfg = load_config(config_path)
    return RadarrSonarrMCPServer(cfg)
