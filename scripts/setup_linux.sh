#!/usr/bin/env bash
# All-in-one setup script for configuring arr service endpoints, API keys, and Python environment on Linux.
set -e

# Ensure Python 3 is installed
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found, attempting to install..."
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv
  else
    echo "Please install Python 3 manually and re-run this script."
    exit 1
  fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Collect configuration details
read -p "Please enter your Sonarr Host URL: " SONARR_URL
read -p "Please enter your Sonarr API Key: " SONARR_KEY
read -p "Please enter your Radarr Host URL: " RADARR_URL
read -p "Please enter your Radarr API Key: " RADARR_KEY
read -p "Please enter your Whisparr Host URL: " WHISPARR_URL
read -p "Please enter your Whisparr API Key: " WHISPARR_KEY
read -p "Please enter your Lidarr Host URL: " LIDARR_URL
read -p "Please enter your Lidarr API Key: " LIDARR_KEY
read -p "Please enter your Readarr Host URL: " READARR_URL
read -p "Please enter your Readarr API Key: " READARR_KEY

# Write .env file
cat > .env <<ENV
SONARR_URL=$SONARR_URL
SONARR_API_KEY=$SONARR_KEY
RADARR_URL=$RADARR_URL
RADARR_API_KEY=$RADARR_KEY
WHISPARR_URL=$WHISPARR_URL
WHISPARR_API_KEY=$WHISPARR_KEY
LIDARR_URL=$LIDARR_URL
LIDARR_API_KEY=$LIDARR_KEY
READARR_URL=$READARR_URL
READARR_API_KEY=$READARR_KEY
ENV

echo ".env configuration written."

# Persist configuration and API keys using keyring
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
