#!/usr/bin/env bash
# Simple setup script for configuring arr service endpoints and API keys on Linux.
set -e

read -p "Please enter your Sonarr Host URL: " SONARR_URL
read -p "Please enter your Sonarr Api Key: " SONARR_KEY
read -p "Please enter your Radarr Host URL: " RADARR_URL
read -p "Please enter your Radarr Api Key: " RADARR_KEY
read -p "Please enter your Whisparr Host URL: " WHISPARR_URL
read -p "Please enter your Whisparr Api Key: " WHISPARR_KEY
read -p "Please enter your Lidarr Host URL: " LIDARR_URL
read -p "Please enter your Lidarr Api Key: " LIDARR_KEY
read -p "Please enter your Readarr Host URL: " READARR_URL
read -p "Please enter your Readarr Api Key: " READARR_KEY

python3 - <<PY
import json, os, keyring
config_path = os.path.expanduser("~/.yarr_config.json")
try:
    with open(config_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
except FileNotFoundError:
    data = {}

data["sonarr"] = {"host": "${SONARR_URL}"}
data["radarr"] = {"host": "${RADARR_URL}"}
data["whisparr"] = {"host": "${WHISPARR_URL}"}
data["lidarr"] = {"host": "${LIDARR_URL}"}
data["readarr"] = {"host": "${READARR_URL}"}

with open(config_path, "w", encoding="utf-8") as fh:
    json.dump(data, fh, indent=2)

keyring.set_password("yarr-mcp", "sonarr", "${SONARR_KEY}")
keyring.set_password("yarr-mcp", "radarr", "${RADARR_KEY}")
keyring.set_password("yarr-mcp", "whisparr", "${WHISPARR_KEY}")
keyring.set_password("yarr-mcp", "lidarr", "${LIDARR_KEY}")
keyring.set_password("yarr-mcp", "readarr", "${READARR_KEY}")
print(f"Configuration written to {config_path}")
PY
