"""Test __str__ method."""

import pytest

from errbrac import ErrorBracket


@pytest.mark.parametrize(
    ("val", "err", "prec", "ref"),
    [
        ("100", "2", 1, "100(2)"),
        ("100", "2", 2, "100.0(20)"),
        ("100", "20", 1, "1.0(2)E+2"),
        ("100", "20", 2, "100(20)"),
        ("1000", "2", 1, "1000(2)"),
        ("1000", "2", 2, "1000.0(20)"),
        ("1E+102", "2E+100", 1, "1.00(2)E+102"),
        ("1E+102", "2E+100", 2, "1.000(20)E+102"),
    ],
)
def test_intint(val: str, err: str, prec: int, ref: str) -> None:
    """Provide integer arguments."""
    x = ErrorBracket(val, err, prec)
    assert str(x) == ref
    xneg = ErrorBracket("-" + val, err, prec)
    assert str(xneg) == "-" + ref


@pytest.mark.parametrize(
    ("val", "err", "prec", "ref"),
    [
        ("1", "0.02", 1, "1.00(2)"),
        ("1", "0.02", 2, "1.000(20)"),
        ("1", "0.2", 1, "1.0(2)"),
        ("1", "0.2", 2, "1.00(20)"),
        ("10", "0.02", 1, "10.00(2)"),
        ("10", "0.02", 2, "10.000(20)"),
        ("1E+3", "2E-3", 1, "1000.000(2)"),
        ("1E+3", "2E-3", 2, "1000.0000(20)"),
    ],
)
def test_intfloat(val: str, err: str, prec: int, ref: str) -> None:
    """Provide int and float arguments."""
    x = ErrorBracket(val, err, prec)
    assert str(x) == ref
    xneg = ErrorBracket("-" + val, err, prec)
    assert str(xneg) == "-" + ref


@pytest.mark.parametrize(
    ("val", "err", "prec", "ref"),
    [
        ("100.1", "2", 1, "100(2)"),
        ("100.1", "2", 2, "100.1(20)"),
        ("100.1", "20", 1, "1.0(2)E+2"),
        ("100.1", "20", 2, "100(20)"),
        ("1000.1", "2", 1, "1000(2)"),
        ("1000.1", "2", 2, "1000.1(20)"),
    ],
)
def test_floatint(val: str, err: str, prec: int, ref: str) -> None:
    """Provide float and int arguments."""
    x = ErrorBracket(val, err, prec)
    assert str(x) == ref
    xneg = ErrorBracket("-" + val, err, prec)
    assert str(xneg) == "-" + ref


@pytest.mark.parametrize(
    ("val", "err", "prec", "ref"),
    [
        ("10.1", "0.02", 1, "10.10(2)"),
        ("10.1", "0.02", 2, "10.100(20)"),
        ("10.1", "0.2", 1, "10.1(2)"),
        ("10.1", "0.2", 2, "10.10(20)"),
        ("100.1", "0.02", 1, "100.10(2)"),
        ("100.1", "0.02", 2, "100.100(20)"),
    ],
)
def test_floatfloat(val: str, err: str, prec: int, ref: str) -> None:
    """Provide float arguments."""
    x = ErrorBracket(val, err, prec)
    assert str(x) == ref
    xneg = ErrorBracket("-" + val, err, prec)
    assert str(xneg) == "-" + ref


@pytest.mark.parametrize(
    ("val", "err", "prec", "ref"),
    [
        # No . before E
        ("2E+100", "1E+100", 1, "2(1)E+100"),
        ("2E+100", "1E+100", 2, "2.0(10)E+100"),
    ],
)
def test_bigclose(val: str, err: str, prec: int, ref: str) -> None:
    """Test big numbers with close error."""
    x = ErrorBracket(val, err, prec)
    assert str(x) == ref
    xneg = ErrorBracket("-" + val, err, prec)
    assert str(xneg) == "-" + ref
