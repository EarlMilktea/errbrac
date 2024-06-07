"""Test the parse method."""

import pytest

from errbrac import ErrorBracket


def test_invalidtype() -> None:
    """Test with invalid type."""
    with pytest.raises(TypeError, match=r"1 is not a string."):
        _ = ErrorBracket.parse(1)  # type: ignore[arg-type]


def test_ng_nobrac() -> None:
    """Provide a string without brackets."""
    with pytest.raises(ValueError, match=r".* does not have proper bracket."):
        _ = ErrorBracket.parse("100")


def test_ng_halfbrac() -> None:
    """Provide a string with broken bracket."""
    with pytest.raises(ValueError, match=r".* does not have proper bracket."):
        _ = ErrorBracket.parse("100(3")


def test_ng_emptybrac() -> None:
    """Provide a string with empty brackets."""
    with pytest.raises(ValueError, match=r".* does not have proper bracket."):
        _ = ErrorBracket.parse("100()")


def test_ng_invbrac() -> None:
    """Provide a string with inverted brackets."""
    with pytest.raises(ValueError, match=r".* does not have proper bracket."):
        _ = ErrorBracket.parse("100)3(")


def test_ng_manybrac() -> None:
    """Provide a string with multiple brackets."""
    with pytest.raises(ValueError, match=r".* does not have proper bracket."):
        _ = ErrorBracket.parse("100(2)(3)")


def test_ng_nestbrac() -> None:
    """Provide a string with nested brackets."""
    with pytest.raises(ValueError, match=r".* does not have proper bracket."):
        _ = ErrorBracket.parse("100(2(3))")


def test_ng_invalidval() -> None:
    """Provide a string with invalid characters for val."""
    with pytest.raises(ValueError, match="Cannot construct Decimal from '10a'."):
        _ = ErrorBracket.parse("10a(2)")


def test_ng_invaliderr() -> None:
    """Provide a string with invalid characters for err."""
    with pytest.raises(ValueError, match="Cannot construct Decimal from '2a'."):
        _ = ErrorBracket.parse("10(2a)")


def test_ng_longerr() -> None:
    """Provide a string with too long err."""
    with pytest.raises(ValueError, match=r".* has too many digits inside the bracket."):
        _ = ErrorBracket.parse("100(2000000000)")


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
