"""Tests for CLI module."""

from click.testing import CliRunner

from tana_import.cli import main


def test_cli_help() -> None:
    """Test CLI help message."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Import ChatGPT export files to Tana" in result.output


def test_cli_with_file(tmp_path) -> None:
    """Test CLI with a file path."""
    test_file = tmp_path / "test.json"
    test_file.write_text("{}")

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file)])
    assert "Importing from:" in result.output
    assert "Not yet implemented" in result.output


def test_cli_with_dry_run(tmp_path) -> None:
    """Test CLI with dry-run flag."""
    test_file = tmp_path / "test.json"
    test_file.write_text("{}")

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file), "--dry-run"])
    assert "Dry run: True" in result.output
