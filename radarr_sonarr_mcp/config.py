from __future__ import annotations
"""Configuration models and helpers for arr services."""

from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional
import json

try:
    import keyring  # type: ignore
except Exception:  # pragma: no cover - keyring optional for tests
    keyring = None  # type: ignore

CONFIG_FILE = Path("config.json")


@dataclass
class ServiceConfig:
    """Base configuration for an Arr service."""

    base_url: str = ""
    api_key: str = ""


@dataclass
class RadarrConfig(ServiceConfig):
    pass


@dataclass
class SonarrConfig(ServiceConfig):
    pass


@dataclass
class WhisparrConfig(ServiceConfig):
    pass


@dataclass
class LidarrConfig(ServiceConfig):
    pass


@dataclass
class ReadarrConfig(ServiceConfig):
    pass


@dataclass
class NasConfig:
    ip: str = "10.0.0.23"
    port: str = "7878"


@dataclass
class ServerConfig:
    port: int = 3000


@dataclass
class Config:
    """Top level configuration container."""

    nas_config: NasConfig = field(default_factory=NasConfig)
    radarr_config: RadarrConfig = field(default_factory=RadarrConfig)
    sonarr_config: SonarrConfig = field(default_factory=SonarrConfig)
    whisparr_config: WhisparrConfig = field(default_factory=WhisparrConfig)
    lidarr_config: LidarrConfig = field(default_factory=LidarrConfig)
    readarr_config: ReadarrConfig = field(default_factory=ReadarrConfig)
    server_config: ServerConfig = field(default_factory=ServerConfig)


def _apply_keyring(config: ServiceConfig, service_name: str) -> None:
    """Populate API key from keyring if available and not set."""
    if config.api_key or keyring is None:
        return
    try:
        stored = keyring.get_password("yarr-mcp", service_name)
        if stored:
            config.api_key = stored
    except Exception:
        pass


def load_config(path: Optional[str] = None) -> Config:
    """Load configuration from a JSON file."""
    path_obj = Path(path) if path else CONFIG_FILE
    if not path_obj.exists():
        return Config()

    with path_obj.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    nas_data = data.get("nasConfig", {})
    nas_config = NasConfig(**nas_data)

    def _svc(cfg_class, raw, default_port):
        if "base_url" in raw or "baseUrl" in raw:
            base_url = raw.get("base_url") or raw.get("baseUrl")
        else:
            port = raw.get("port", default_port)
            base_path = raw.get("basePath", "/api/v3")
            base_url = f"http://{nas_data.get('ip', 'localhost')}:{port}{base_path}"
        api_key = raw.get("api_key") or raw.get("apiKey", "")
        return cfg_class(base_url=base_url, api_key=api_key)

    cfg = Config(
        nas_config=nas_config,
        radarr_config=_svc(RadarrConfig, data.get("radarrConfig", {}), "7878"),
        sonarr_config=_svc(SonarrConfig, data.get("sonarrConfig", {}), "8989"),
        whisparr_config=_svc(WhisparrConfig, data.get("whisparrConfig", {}), "6969"),
        lidarr_config=_svc(LidarrConfig, data.get("lidarrConfig", {}), "8686"),
        readarr_config=_svc(ReadarrConfig, data.get("readarrConfig", {}), "8787"),
        server_config=ServerConfig(**data.get("server", {})),
    )

    _apply_keyring(cfg.radarr_config, "radarr")
    _apply_keyring(cfg.sonarr_config, "sonarr")
    _apply_keyring(cfg.whisparr_config, "whisparr")
    _apply_keyring(cfg.lidarr_config, "lidarr")
    _apply_keyring(cfg.readarr_config, "readarr")

    return cfg


def save_config(config: Config, path: Optional[str] = None) -> None:
    """Persist configuration to JSON file."""
    path_obj = Path(path) if path else CONFIG_FILE
    data = {
        "nasConfig": asdict(config.nas_config),
        "radarrConfig": asdict(config.radarr_config),
        "sonarrConfig": asdict(config.sonarr_config),
        "whisparrConfig": asdict(config.whisparr_config),
        "lidarrConfig": asdict(config.lidarr_config),
        "readarrConfig": asdict(config.readarr_config),
        "server": asdict(config.server_config),
    }
    with path_obj.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)

    # Store API keys securely if keyring is available
    if keyring is not None:
        try:
            if config.radarr_config.api_key:
                keyring.set_password("yarr-mcp", "radarr", config.radarr_config.api_key)
            if config.sonarr_config.api_key:
                keyring.set_password("yarr-mcp", "sonarr", config.sonarr_config.api_key)
            if config.whisparr_config.api_key:
                keyring.set_password("yarr-mcp", "whisparr", config.whisparr_config.api_key)
            if config.lidarr_config.api_key:
                keyring.set_password("yarr-mcp", "lidarr", config.lidarr_config.api_key)
            if config.readarr_config.api_key:
                keyring.set_password("yarr-mcp", "readarr", config.readarr_config.api_key)
        except Exception:
            pass
