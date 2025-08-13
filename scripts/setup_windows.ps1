param()

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

$py = @"
import json, os, keyring
config_path = os.path.join(os.path.expanduser('~'), 'yarr_config.json')
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
