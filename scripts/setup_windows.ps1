param()

# Ensure Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Output "Python not found. Attempting to install with winget..."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install -e --id Python.Python.3
    } else {
        Write-Error "winget not found. Please install Python 3 manually and re-run this script."
        exit 1
    }
}

# Create virtual environment if missing
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
.\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt

# Collect configuration details
$sonarrUrl = Read-Host "Please enter your Sonarr Host URL"
$sonarrKey = Read-Host "Please enter your Sonarr Api Key"
$radarrUrl = Read-Host "Please enter your Radarr Host URL"
$radarrKey = Read-Host "Please enter your Radarr Api Key"
$whisparrUrl = Read-Host "Please enter your Whisparr Host URL"
$whisparrKey = Read-Host "Please enter your Whisparr Api Key"
$lidarrUrl = Read-Host "Please enter your Lidarr Host URL"
$lidarrKey = Read-Host "Please enter your Lidarr Api Key"
$readarrUrl = Read-Host "Please enter your Readarr Host URL"
$readarrKey = Read-Host "Please enter your Readarr Api Key"

# Write .env file
$envContent = @"
SONARR_URL=$sonarrUrl
SONARR_API_KEY=$sonarrKey
RADARR_URL=$radarrUrl
RADARR_API_KEY=$radarrKey
WHISPARR_URL=$whisparrUrl
WHISPARR_API_KEY=$whisparrKey
LIDARR_URL=$lidarrUrl
LIDARR_API_KEY=$lidarrKey
READARR_URL=$readarrUrl
READARR_API_KEY=$readarrKey
"@
Set-Content -Path ".env" -Value $envContent -Encoding UTF8
Write-Output ".env configuration written."

$py = @"
import json, os, keyring
config_path = os.path.join(os.path.expanduser('~'), '.yarr_config.json')
try:
    with open(config_path, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
except FileNotFoundError:
    data = {}

data['sonarr'] = {'host': '$sonarrUrl'}
data['radarr'] = {'host': '$radarrUrl'}
data['whisparr'] = {'host': '$whisparrUrl'}
data['lidarr'] = {'host': '$lidarrUrl'}
data['readarr'] = {'host': '$readarrUrl'}

with open(config_path, 'w', encoding='utf-8') as fh:
    json.dump(data, fh, indent=2)

keyring.set_password('yarr-mcp', 'sonarr', '$sonarrKey')
keyring.set_password('yarr-mcp', 'radarr', '$radarrKey')
keyring.set_password('yarr-mcp', 'whisparr', '$whisparrKey')
keyring.set_password('yarr-mcp', 'lidarr', '$lidarrKey')
keyring.set_password('yarr-mcp', 'readarr', '$readarrKey')
print(f'Configuration written to {config_path}')
"@

python - <<PYTHON
$py
PYTHON
