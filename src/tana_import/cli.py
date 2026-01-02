"""CLI entry point for tana-import tool."""

import sys
from pathlib import Path
from typing import List, Optional

import click
from dotenv import load_dotenv

from tana_import.api_client import TanaAPIClient
from tana_import.config import TanaConfig
from tana_import.converter import create_tana_events
from tana_import.parser import parse_export_file


def find_json_files(path: Path) -> List[Path]:
    """Find all JSON files in path (file or directory).

    Args:
        path: Path to a file or directory.

    Returns:
        List of JSON file paths.
    """
    if path.is_file():
        if path.suffix.lower() == ".json":
            return [path]
        return []

    # If it's a directory, find all JSON files
    if path.is_dir():
        return list(path.glob("*.json"))

    return []


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True, help="Generate events without sending to Tana")
@click.option("--timezone", type=str, help="Override system timezone")
def main(path: str, dry_run: bool = False, timezone: Optional[str] = None) -> None:
    """Import ChatGPT export files to Tana.

    PATH can be a single JSON file or a directory containing JSON files.
    """
    # Load environment variables from .env file if it exists
    load_dotenv()

    # Validate configuration
    try:
        config = TanaConfig.from_env()
    except ValueError as e:
        click.echo(f"Configuration error: {e}", err=True)
        sys.exit(1)

    # Find JSON files to process
    path_obj = Path(path)
    json_files = find_json_files(path_obj)

    if not json_files:
        click.echo(f"No JSON files found in: {path}")
        return

    click.echo(f"Found {len(json_files)} JSON file(s) to process")

    # Parse all conversations from all files
    all_conversations = []
    for json_file in json_files:
        try:
            conversations = parse_export_file(json_file)
            all_conversations.extend(conversations)
            click.echo(f"✓ Parsed {len(conversations)} conversation(s) from {json_file.name}")
        except Exception as e:  # pylint: disable=broad-except
            click.echo(f"✗ Error parsing {json_file.name}: {e}", err=True)
            continue

    if not all_conversations:
        click.echo("No conversations found to import")
        return

    # Generate Tana events
    events = create_tana_events(all_conversations, config.inbox_node_id)
    click.echo(f"Generated {len(events)} event(s) for {len(all_conversations)} conversation(s)")

    # Send events to Tana or save in dry-run mode
    if dry_run:
        click.echo("\n=== DRY RUN MODE ===")
        click.echo("Events would be sent to Tana API:")
        import json

        click.echo(json.dumps({"targetNodeId": config.inbox_node_id, "nodes": events}, indent=2))
    else:
        try:
            client = TanaAPIClient(config)
            response = client.send_events(events)
            click.echo(f"✓ Successfully sent events to Tana (status: {response.status_code})")
        except Exception as e:  # pylint: disable=broad-except
            click.echo(f"✗ Error sending to Tana API: {e}", err=True)
            sys.exit(1)

    click.echo("\n=== Summary ===")
    click.echo(f"Files scanned: {len(json_files)}")
    click.echo(f"Conversations found: {len(all_conversations)}")
    click.echo(f"Events generated: {len(events)}")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
