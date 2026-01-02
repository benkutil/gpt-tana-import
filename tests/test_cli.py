"""Tests for CLI module."""

import json

from click.testing import CliRunner

from tana_import.cli import main


def test_cli_help() -> None:
    """Test CLI help message."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Import ChatGPT export files to Tana" in result.output


def test_cli_with_file(tmp_path, mock_tana_config) -> None:  # type: ignore
    """Test CLI with a file path."""
    # Create a valid ChatGPT export file
    test_file = tmp_path / "test.json"
    test_data = [
        {
            "title": "Test Conversation",
            "create_time": 1704153000.0,
            "mapping": {
                "root": {"id": "root", "message": None, "children": ["msg1"]},
                "msg1": {
                    "id": "msg1",
                    "message": {
                        "author": {"role": "user"},
                        "content": {"parts": ["Hello"]},
                        "create_time": 1704153000.0,
                    },
                    "children": [],
                },
            },
        }
    ]
    test_file.write_text(json.dumps(test_data))

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file), "--dry-run"])
    assert result.exit_code == 0
    assert "Found 1 JSON file(s) to process" in result.output
    assert "Parsed 1 conversation(s)" in result.output


def test_cli_with_dry_run(tmp_path, mock_tana_config) -> None:  # type: ignore
    """Test CLI with dry-run flag."""
    # Create a valid ChatGPT export file
    test_file = tmp_path / "test.json"
    test_data = [
        {
            "title": "Test Conversation",
            "create_time": 1704153000.0,
            "mapping": {
                "root": {"id": "root", "message": None, "children": []},
            },
        }
    ]
    test_file.write_text(json.dumps(test_data))

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file), "--dry-run"])
    assert result.exit_code == 0
    assert "DRY RUN MODE" in result.output


def test_cli_missing_config(tmp_path) -> None:  # type: ignore
    """Test CLI with missing configuration."""
    test_file = tmp_path / "test.json"
    test_file.write_text("{}")

    runner = CliRunner()
    result = runner.invoke(main, [str(test_file)])
    assert result.exit_code == 1
    assert "Configuration error:" in result.output
