# Yarr MCP Server

[![PyPI version](https://img.shields.io/pypi/v/yarr-mcp.svg)](https://pypi.org/project/yarr-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/yarr-mcp.svg)](https://pypi.org/project/yarr-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="./docs/images/radarr.svg" alt="Radarr logo" width="130"/>
  <img src="./docs/images/sonarr.svg" alt="Sonarr logo" width="130"/>
</p>

Yarr is a Python-based [Model Context Protocol](https://github.com/modelcontextprotocol) server that gives AI assistants like Claude natural-language access to your Radarr (movies) and Sonarr (TV series) libraries.
Lightweight clients for the rest of the `arr` ecosystem – Lidarr, Whisparr and Readarr – are included so you can extend the same tooling to music, adult content and ebooks.

For additional details on installing and configuring these services, consult the [Servarr Wiki Reference](docs/servarr_wiki_reference.md).

## Architecture

```mermaid
flowchart TD
    Yarr[yarr-mcp]
    Yarr --> Server[radarr_sonarr_mcp/]
    Yarr --> ARR[arrs/]
    ARR --> Radarr[radarr.py]
    ARR --> Sonarr[sonarr.py]
    ARR --> Lidarr[lidarr.py]
    ARR --> Whisparr[whisparr.py]
    ARR --> Readarr[readarr.py]
=======
# Radarr & Sonarr MCP Server

[![PyPI version](https://img.shields.io/pypi/v/radarr-sonarr-mcp.svg)](https://pypi.org/project/radarr-sonarr-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/radarr-sonarr-mcp.svg)](https://pypi.org/project/radarr-sonarr-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



  <img src="docs/images/radarr.svg" alt="Radarr logo" width="130"/>
  <img src="docs/images/sonarr.svg" alt="Sonarr logo" width="130"/>

  <img src="https://raw.githubusercontent.com/Radarr/Radarr/develop/Logo/Radarr.png" alt="Radarr logo" width="130"/>
  <img src="https://raw.githubusercontent.com/Sonarr/Sonarr/develop/Logo/Sonarr.svg" alt="Sonarr logo" width="130"/>

</p>

A Python-based [Model Context Protocol](https://github.com/modelcontextprotocol) server that gives AI assistants like Claude natural-language access to your Radarr (movies) and Sonarr (TV series) libraries.
Lightweight clients for the rest of the `arr` ecosystem – Lidarr, Whisparr and Readarr – are included so you can extend the same tooling to music, adult content and ebooks.

## How does it work?

```mermaid
flowchart LR
    Client[Claude Desktop\n or any MCP Client] -->|MCP| Server[Radarr & Sonarr MCP Server]
    Server -->|REST API| Radarr
    Server -->|REST API| Sonarr
    Server -->|Optional| Whisparr
    Server -->|Optional| Lidarr
    Server -->|Optional| Readarr
```

## Features

- **Native MCP implementation** powered by FastMCP for seamless AI integration
- **Radarr integration** for querying your movie collection
- **Sonarr integration** for series and episode data
- **Whisparr/Lidarr/Readarr support** via reusable service clients
- **Rich filtering** by year, watched status, actors and more
- **Claude Desktop compatible** – works with any MCP client
- **Interactive configuration wizard** with secure keyring storage
- **Comprehensive test suite** for reliability

## Project Structure

```
arrs/
  base.py     # shared HTTP helpers
  radarr/     # Radarr client and Movie model
  sonarr/     # Sonarr client and Series/Episode models
  lidarr/     # Lidarr client
  whisparr/   # Whisparr client
  readarr/    # Readarr client
```


=======

```bash
git clone https://github.com/yourusername/radarr-sonarr-mcp.git
cd radarr-sonarr-mcp
pip install -e .
```

### Using pip (coming soon)

```bash
git clone https://github.com/yourusername/yarr-mcp.git
cd yarr-mcp
pip install -e .
```


```

Example `config.json`:

```json
{
  "nasConfig": {
    "ip": "10.0.0.23",
    "port": "7878"
  },
  "radarrConfig": {
    "apiKey": "YOUR_RADARR_API_KEY",
    "basePath": "/api/v3",
    "port": "7878"
  },
  "sonarrConfig": {
    "apiKey": "YOUR_SONARR_API_KEY",
    "basePath": "/api/v3",
    "port": "8989"
  },
  "server": {
    "port": 3000
  }
}
```

### Setup scripts

Collect keys automatically with the provided scripts:
=======
Bootstrap the project and collect service credentials with the provided scripts:

```bash
# Linux
scripts/setup_linux.sh

# Windows PowerShell
scripts/setup_windows.ps1
```

You will be prompted for each service:

```
Please enter your Sonarr Host URL: https://sonarr.example.com
Please enter your Sonarr Api Key: <your key>
```

## Quick Start

1. Configure the server:
   ```bash
   yarr-mcp configure
   ```
2. Start it:
   ```bash
   yarr-mcp start
=======

These scripts will:

- Ensure Python 3 is available and create a virtual environment in `.venv`
- Install dependencies from `requirements.txt`
- Prompt for service host URLs and API keys
- Write the values to a `.env` file and to `~/.yarr_config.json` with keys stored in your OS keyring

You will be prompted for each service:

```
Please enter your Sonarr Host URL: https://sonarr.example.com
Please enter your Sonarr Api Key: <your key>
```

## Quick Start

1. Configure the server:
   ```bash
   radarr-sonarr-mcp configure
   ```
2. Start it:
   ```bash
   radarr-sonarr-mcp start
   ```
3. Connect Claude Desktop:
   - Open **Settings → MCP Servers**
   - Add `http://localhost:3000` (or your configured port)

## MCP Tools

### Movies
- `get_available_movies` – List movies with optional filters
- `lookup_movie` – Search by title
- `get_movie_details` – Detailed info for a movie

### Series
- `get_available_series` – List TV series with filters
- `lookup_series` – Search by title
- `get_series_details` – Detailed info for a series
- `get_series_episodes` – Episode list for a series

### Resources

- `/movies` – Browse all available movies
- `/series` – Browse all available TV series

### Filtering Options

Most tools support parameters such as:

- `year` – Release year
- `watched` – Watched status (`true`/`false`)
- `downloaded` – Downloaded status (`true`/`false`)
- `watchlist` – Watchlist status (`true`/`false`)
- `actors` – Actor or cast names
- `actresses` – Actress names (movies only)

## Example Queries

Once connected to Claude Desktop you can ask:

- "What sci-fi movies from 2023 do I have?"
- "Show me TV shows starring Pedro Pascal"
- "Do I have any unwatched episodes of *The Mandalorian*?"
- "Find movies with Tom Hanks that I haven't watched yet"
- "How many episodes of *Stranger Things* are downloaded?"



The API key for Lidarr, Whisparr, Readarr, and other Arr apps is found under **Settings → General** as well.
=======
=======
2. Go to Settings → General
3. Copy the **API Key**

## Development

```bash
# Install dev dependencies
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=yarr_mcp
```

For quick local iteration:

```bash
python run.py
```

## Requirements

- Python 3.10+
- FastMCP
- Requests
- Pydantic

## Contributors

- Initial work – [@berry](https://github.com/yourusername)

## License

MIT

