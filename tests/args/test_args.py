import pytest

from args.args import Args


@pytest.mark.parametrize(
    "schema, args, expected",
    [
        ("l", ["-l"], 1),
        ("l", [], 0),
        ("l,m,n", ["-l", "-m", "-n"], 3),
        ("l,m,n", ["-n"], 1),
    ],
)
def test_cardinality(schema: str, args: list[str], expected: int) -> None:
    arg = Args(schema, args)
    assert arg.cardinality() == expected


@pytest.mark.parametrize(
    "schema, expected",
    [
        ("l", "-[l]"),
        ("l,m,n", "-[l,m,n]"),
        ("", ""),
    ],
)
def test_usage(schema: str, expected: int) -> None:
    arg = Args(schema, [])
    assert arg.usage() == expected


@pytest.mark.parametrize(
    "schema, args, expected",
    [
        ("l", ["-l"], ""),
        ("l", ["-l", "-m"], "Argument(s) -m unexpected."),
        ("l", ["-l", "-m", "-n"], "Argument(s) -mn unexpected."),
    ],
)
def test_error_message(schema: str, args: list[str], expected: int) -> None:
    arg = Args(schema, args)
    assert arg.error_message() == expected


@pytest.mark.parametrize(
    "schema, args, arg, expected",
    [
        ("l", ["-l"], "l", True),
        ("l", [], "l", False),
        ("l,m", ["-l"], "l", True),
        ("l,m", ["-l"], "m", False),
    ],
)
def test_get_boolean(schema: str, args: list[str], arg: str, expected: bool) -> None:
    a = Args(schema, args)
    assert a.get_boolean(arg) == expected
