"""Test the parse method."""

import pytest

from errbrac import ErrorBracket


@pytest.mark.parametrize(
    ("ex", "ref"),
    [
        ("100(2)", ErrorBracket("100", "2", 1)),
        ("100(20)", ErrorBracket("100", "20", 2)),
        ("-100(2)", ErrorBracket("-100", "2", 1)),
        ("-100(20)", ErrorBracket("-100", "20", 2)),
    ],
)
def test_int_decimal(ex: str, ref: ErrorBracket) -> None:
    """Test with int decimal values."""
    assert ErrorBracket.parse(ex) == ref


@pytest.mark.parametrize(
    ("ex", "ref"),
    [
        ("2(1)E+2", ErrorBracket("200", "100", 1)),
        ("-2(1)E+2", ErrorBracket("-200", "100", 1)),
    ],
)
def test_int_science(ex: str, ref: ErrorBracket) -> None:
    """Test with int scientific notation."""
    assert ErrorBracket.parse(ex) == ref


@pytest.mark.parametrize(
    ("ex", "ref"),
    [
        ("100.1(2)", ErrorBracket("100.1", "0.2", 1)),
        ("100.1(20)", ErrorBracket("100.1", "2", 2)),
        ("-100.1(2)", ErrorBracket("-100.1", "0.2", 1)),
        ("-100.1(20)", ErrorBracket("-100.1", "2", 2)),
    ],
)
def test_float_decimal(ex: str, ref: ErrorBracket) -> None:
    """Test with float decimal values."""
    assert ErrorBracket.parse(ex) == ref


@pytest.mark.parametrize(
    ("ex", "ref"),
    [
        ("2.0(1)E+2", ErrorBracket("200", "10", 1)),
        ("2.0(10)E+2", ErrorBracket("200", "100", 2)),
        ("-2.0(1)E+2", ErrorBracket("-200", "10", 1)),
        ("-2.0(10)E+2", ErrorBracket("-200", "100", 2)),
    ],
)
def test_float_science(ex: str, ref: ErrorBracket) -> None:
    """Test with float scientific notation."""
    assert ErrorBracket.parse(ex) == ref
