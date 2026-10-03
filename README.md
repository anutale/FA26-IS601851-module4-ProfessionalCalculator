# Professional Calculator

A modular, command-line calculator written in Python. It supports six arithmetic operations, keeps a calculation history for the current session, and separates arithmetic, calculation objects, and the interactive interface.

## Features

- Addition, subtraction, multiplication, division, exponentiation, and modulo.
- Interactive REPL with built-in help and session history.
- Decimal operands are accepted for all operations. Exponents must be whole-number values; values such as `3.0` are accepted, while `1.5` is rejected.
- Clear handling for invalid commands, unsupported operations, and zero divisors.
- An abstract calculation interface and registry-based factory make operation classes easy to extend.

## Requirements

- Python 3
- `pip` for installing the test and development dependencies

The calculator has no third-party runtime dependencies. The pinned packages in `requirements.txt` provide the project's testing, coverage, and code-quality tools.

## Setup

From the project root, create and activate a virtual environment, then install the dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the Calculator

Start the interactive calculator from the project root:

```sh
python main.py
```

Enter an operation followed by two numbers:

```text
>> add 10 5
Result: AddCalculation: 10.0 Add 5.0 = 15.0

>> power 2 3
Result: PowerCalculation: 2.0 Power 3.0 = 8.0

>> history
Calculation History:
1. AddCalculation: 10.0 Add 5.0 = 15.0
2. PowerCalculation: 2.0 Power 3.0 = 8.0
```

The history is held in memory and is cleared when the calculator exits. Type `help` at the prompt to display usage instructions. Type `exit`, press Ctrl+C, or send EOF to quit.

### Supported Operations

| Command | Behavior | Example |
| --- | --- | --- |
| `add` | Adds the two numbers. | `add 10 5` returns `15.0`. |
| `subtract` | Subtracts the second number from the first. | `subtract 10 5` returns `5.0`. |
| `multiply` | Multiplies the two numbers. | `multiply 7 8` returns `56.0`. |
| `divide` | Divides the first number by the second. | `divide 20 4` returns `5.0`. A zero divisor is rejected. |
| `power` | Raises the first number to the second number's power. | `power 2 3` returns `8.0`. Negative and zero whole-number exponents are supported. |
| `modulo` | Returns the remainder after dividing the first number by the second. | `modulo 10 3` returns `1.0`. A zero divisor is rejected. |

Each command must have exactly two numeric operands, for example `divide 20 4`. Unsupported operation names and malformed input produce a message and return to the prompt. Division by zero is reported as an error; modulo by zero is also rejected. A fractional power exponent raises a `ValueError` and the REPL displays the calculation error.

## Project Structure

```text
app/
	calculation/  Calculation base class, concrete calculation types, and factory
	calculator/   Interactive command-line interface and session history
	operation/    Stateless arithmetic operations
main.py         Application entry point
tests/          Operation and calculation tests
```

The application is divided into three layers:

1. `app.operation.Operation` implements the arithmetic methods.
2. `app.calculation` wraps each operation in a `Calculation` object. `CalculationFactory` maps command names to calculation classes, and each calculation's `execute()` method delegates to `Operation`.
3. `app.calculator` parses user input, creates and executes calculations, prints results, and tracks history.

This structure demonstrates separation of concerns, an abstract base class, a factory/registry pattern, and the LBYL and EAFP approaches to handling user input and errors.

## Run Tests

Run the test suite from the project root:

```sh
python -m pytest
```

Pytest is configured in `pytest.ini` to discover tests under `tests/`, measure statement and branch coverage for `app` and `main.py`, print a coverage summary, and generate an HTML report in `htmlcov/`. The local test command fails unless coverage reaches 100%.

GitHub Actions runs the tests on pushes and pull requests to `main` and enforces the same 100% coverage threshold. The abstract `Calculation.execute()` method contains an intentionally unimplemented `pass`; it is excluded from coverage with `# pragma: no cover` because abstract methods are implemented by their subclasses. All executable calculator paths are tested.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.
