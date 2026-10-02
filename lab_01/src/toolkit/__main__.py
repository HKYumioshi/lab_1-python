"""
Консольный интерфейс пакета toolkit.

Команды:
    python -m toolkit calc "EXPRESSION"
    python -m toolkit convert VALUE --from UNIT --to UNIT
    python -m toolkit --help
"""

import argparse
import sys

from toolkit.calculator import calculate
from toolkit.calculator import rpn_conversion
from toolkit.calculator import tokenize
from toolkit.calculator import validate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Консольный набор утилит: калькулятор выражений и конвертер величин.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser(
        "calc",
        help="Вычислить арифметическое выражение",
    )
    calc_parser.add_argument(
        "expression",
        help='Выражение для вычисления, например "2 + 2 * (3 - 1)"',
    )

    convert_parser = subparsers.add_parser(
        "convert",
        help="Конвертировать значение между единицами измерения",
    )
    convert_parser.add_argument(
        "value",
        type=float,
        help="Числовое значение для конвертации",
    )
    convert_parser.add_argument(
        "--from",
        dest="unit_from",
        required=True,
        metavar="UNIT",
        help="Единица измерения, из которой конвертируем",
    )
    convert_parser.add_argument(
        "--to",
        dest="unit_to",
        required=True,
        metavar="UNIT",
        help="Единица измерения, в которую конвертируем",
    )

    return parser


def run_calc(expression: str) -> float:
    """Прогоняет выражение через tokenization -> validation -> RPN -> calculation."""
    tokens = tokenize(expression)
    tokens = validate(tokens)
    rpn_tokens = rpn_conversion(tokens)
    return calculate(rpn_tokens)


def run_convert(value: float, unit_from: str, unit_to: str) -> float:
    return convert(value, unit_from, unit_to)


def main(argv: list | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "calc":
            result = run_calc(args.expression)
        elif args.command == "convert":
            result = run_convert(args.value, args.unit_from, args.unit_to)
        else:
            parser.print_help(sys.stderr)
            return 2
    except ToolkitError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except ZeroDivisionError:
        print("Error: division by zero", file=sys.stderr)
        return 2

    print(float(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
