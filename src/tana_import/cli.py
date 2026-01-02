"""CLI entry point for tana-import tool."""

from typing import Optional

import click


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True, help="Generate events without sending to Tana")
@click.option("--timezone", type=str, help="Override system timezone")
def main(path: str, dry_run: bool = False, timezone: Optional[str] = None) -> None:
    """Import ChatGPT export files to Tana.

    PATH can be a single JSON file or a directory containing JSON files.
    """
    click.echo(f"Importing from: {path}")
    click.echo(f"Dry run: {dry_run}")
    if timezone:
        click.echo(f"Timezone: {timezone}")
    click.echo("Not yet implemented")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
