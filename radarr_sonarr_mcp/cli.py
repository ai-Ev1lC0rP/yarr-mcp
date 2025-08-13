"""Command-line interface for the Radarr/Sonarr MCP server."""

import argparse
import logging
import os

from .config import Config, NasConfig, RadarrConfig, SonarrConfig, ServerConfig, load_config, save_config
from .server import create_server

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def configure():
    """Run the configuration wizard."""
    logging.info("==== Radarr/Sonarr MCP Server Configuration Wizard ====")
    
    # Try to load existing config
    config = None
    try:
        config = load_config()
        logging.info("Loaded existing configuration. Press Enter to keep current values.")
    except Exception:
        # No existing config or error loading
        pass
    
    # NAS configuration
    nas_ip = input(f"NAS/Server IP address [{config.nas_config.ip if config else '10.0.0.23'}]: ")
    nas_ip = nas_ip or (config.nas_config.ip if config else '10.0.0.23')
    
    nas_port = input(f"Default port [{config.nas_config.port if config else '7878'}]: ")
    nas_port = nas_port or (config.nas_config.port if config else '7878')
    
    # Radarr configuration
    radarr_api_key = input(f"Radarr API key [{config.radarr_config.api_key if config else ''}]: ")
    radarr_api_key = radarr_api_key or (config.radarr_config.api_key if config else '')
    if not radarr_api_key:
        logging.warning("Warning: Radarr API key is required for movie functionality!")
    
    radarr_base_url = input(
        f"Radarr base URL [{config.radarr_config.base_url if config else f'http://{nas_ip}:7878/api/v3'}]: "
    )
    radarr_base_url = radarr_base_url or (
        config.radarr_config.base_url if config else f"http://{nas_ip}:7878/api/v3"
    )
    
    # Sonarr configuration
    sonarr_api_key = input(f"Sonarr API key [{config.sonarr_config.api_key if config else ''}]: ")
    sonarr_api_key = sonarr_api_key or (config.sonarr_config.api_key if config else '')
    if not sonarr_api_key:
        logging.warning("Warning: Sonarr API key is required for TV show functionality!")
    
    sonarr_base_url = input(
        f"Sonarr base URL [{config.sonarr_config.base_url if config else f'http://{nas_ip}:8989/api/v3'}]: "
    )
    sonarr_base_url = sonarr_base_url or (
        config.sonarr_config.base_url if config else f"http://{nas_ip}:8989/api/v3"
    )
    
    # Server configuration
    default_port = config.server_config.port if config else int(os.getenv("MCP_SERVER_PORT", "3333"))
    server_port = input(f"MCP server port [{default_port}]: ")
    if server_port:
        try:
            server_port = int(server_port)
        except ValueError:
            logging.warning("Invalid port number, using default.")
            server_port = default_port
    else:
        server_port = default_port
    
    # Create new config
    new_config = Config(
        nas_config=NasConfig(
            ip=nas_ip,
            port=nas_port
        ),
        radarr_config=RadarrConfig(
            api_key=radarr_api_key,
            base_url=radarr_base_url
        ),
        sonarr_config=SonarrConfig(
            api_key=sonarr_api_key,
            base_url=sonarr_base_url
        ),
        server_config=ServerConfig(
            port=server_port
        )
    )
    
    # Save config
    save_config(new_config)
    logging.info("Configuration saved successfully!")
    logging.info(f"To start the server, run: radarr-sonarr-mcp start")
    
    return new_config


def start(config_path=None):
    """Start the MCP server."""
    server = create_server(config_path)
    server.start()


def show_status():
    """Show the current status of the server."""
    try:
        config = load_config()
        logging.info("==== Radarr/Sonarr MCP Server Status ====")
        logging.info(f"NAS IP: {config.nas_config.ip}")
        logging.info(f"Radarr Port: {config.radarr_config.port or config.nas_config.port}")
        logging.info(f"Sonarr Port: {config.sonarr_config.port or config.nas_config.port}")
        logging.info(f"MCP Server Port: {config.server_config.port}")
        logging.info(f"MCP Endpoint URL: http://localhost:{config.server_config.port}")
        logging.info(f"Server is configured. Use 'radarr-sonarr-mcp start' to run the server.")
    except Exception as e:
        logging.error(f"Server is not configured: {e}")
        logging.info("Run 'radarr-sonarr-mcp configure' to set up the server.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Radarr/Sonarr MCP Server")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Configure command
    configure_parser = subparsers.add_parser("configure", help="Configure the MCP server")
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start the MCP server")
    start_parser.add_argument("--config", help="Path to config.json file")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show the server status")
    
    args = parser.parse_args()
    
    if args.command == "configure":
        configure()
    elif args.command == "start":
        start(args.config)
    elif args.command == "status":
        show_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
