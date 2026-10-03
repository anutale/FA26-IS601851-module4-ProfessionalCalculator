import runpy
from pathlib import Path
from unittest.mock import Mock

import pytest

from app.calculation import AddCalculation
from app.calculator import calculator, display_help, display_history


def run_calculator(monkeypatch, commands):
    command_iterator = iter(commands)
    monkeypatch.setattr("builtins.input", lambda _prompt: next(command_iterator))

    with pytest.raises(SystemExit) as exit_info:
        calculator()

    assert exit_info.value.code == 0


def test_display_help_lists_supported_commands(capsys):
    display_help()

    output = capsys.readouterr().out
    assert "add       : Adds two numbers." in output
    assert "power     : Raises the first number to the power of the second." in output
    assert "history   : Show the history of calculations." in output


def test_display_history_when_empty(capsys):
    display_history([])

    assert capsys.readouterr().out.strip() == "No calculations performed yet."


def test_display_history_lists_calculations(capsys):
    display_history([AddCalculation(10.0, 5.0)])

    output = capsys.readouterr().out
    assert "Calculation History:" in output
    assert "1. AddCalculation: 10.0 Add 5.0 = 15.0" in output


def test_calculator_help_and_exit_commands(monkeypatch, capsys):
    run_calculator(monkeypatch, ["help", "exit"])

    output = capsys.readouterr().out
    assert "Calculator REPL Help" in output
    assert "Exiting calculator. Goodbye!" in output


def test_calculator_skips_blank_input_and_records_history(monkeypatch, capsys):
    run_calculator(monkeypatch, ["  ", "add 10 5", "history", "exit"])

    output = capsys.readouterr().out
    assert "Result: AddCalculation: 10.0 Add 5.0 = 15.0" in output
    assert "1. AddCalculation: 10.0 Add 5.0 = 15.0" in output


@pytest.mark.parametrize("command", ["add 1", "add not-a-number 2", "add 1 2 3"])
def test_calculator_reports_malformed_input(monkeypatch, capsys, command):
    run_calculator(monkeypatch, [command, "exit"])

    output = capsys.readouterr().out
    assert "Invalid input. Please follow the format" in output


def test_calculator_reports_unsupported_operation(monkeypatch, capsys):
    run_calculator(monkeypatch, ["unknown 1 2", "exit"])

    output = capsys.readouterr().out
    assert "Unsupported calculation type: 'unknown'" in output


def test_calculator_reports_division_by_zero(monkeypatch, capsys):
    run_calculator(monkeypatch, ["divide 10 0", "exit"])

    output = capsys.readouterr().out
    assert "Cannot divide by zero." in output


@pytest.mark.parametrize(
    "command, error_message",
    [
        ("power 2 1.5", "Power exponent must be an integer value"),
        ("modulo 10 0", "Modulo by zero is not allowed"),
    ],
)
def test_calculator_reports_operation_errors(monkeypatch, capsys, command, error_message):
    run_calculator(monkeypatch, [command, "exit"])

    output = capsys.readouterr().out
    assert f"An error occurred during calculation: {error_message}" in output


def test_calculator_reports_unexpected_calculation_error(monkeypatch, capsys):
    monkeypatch.setattr(
        AddCalculation,
        "execute",
        Mock(side_effect=RuntimeError("unexpected failure")),
    )
    run_calculator(monkeypatch, ["add 1 2", "exit"])

    output = capsys.readouterr().out
    assert "An error occurred during calculation: unexpected failure" in output


@pytest.mark.parametrize(
    "input_error, expected_message",
    [
        (KeyboardInterrupt(), "Keyboard interrupt detected. Exiting calculator."),
        (EOFError(), "EOF detected. Exiting calculator."),
    ],
)
def test_calculator_exits_on_input_interrupt(monkeypatch, capsys, input_error, expected_message):
    monkeypatch.setattr("builtins.input", Mock(side_effect=input_error))

    with pytest.raises(SystemExit) as exit_info:
        calculator()

    assert exit_info.value.code == 0
    assert expected_message in capsys.readouterr().out


def test_calculator_module_entry_point(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "exit")
    calculator_path = Path(__file__).parents[1] / "app" / "calculator" / "__init__.py"

    with pytest.raises(SystemExit):
        runpy.run_path(str(calculator_path), run_name="__main__")

    assert "Exiting calculator. Goodbye!" in capsys.readouterr().out


def test_main_entry_point(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "exit")
    main_path = Path(__file__).parents[1] / "main.py"

    with pytest.raises(SystemExit):
        runpy.run_path(str(main_path), run_name="__main__")

    assert "Exiting calculator. Goodbye!" in capsys.readouterr().out


def test_main_import_does_not_start_calculator(monkeypatch):
    monkeypatch.setattr("builtins.input", Mock(side_effect=AssertionError("input should not be requested")))

    import main

    assert callable(main.calculator)