"""Test ErrorBracket class."""

from __future__ import annotations

import re
from decimal import Decimal

import pytest

from errbrac import ErrorBracket


def test_init_ok() -> None:
    """Provide valid arguments."""
    _ = ErrorBracket("-1", "0.1", 2)
    _ = ErrorBracket(Decimal("-1"), "0.1", 2)
    _ = ErrorBracket("-1", Decimal("0.1"), 2)
    _ = ErrorBracket(Decimal("-1"), Decimal("0.1"), 2)
    assert ErrorBracket("1", "0.1").prec == 1


def test_init_ng_val() -> None:
    """Provide invalid value."""
    with pytest.raises(ValueError, match=r"Cannot construct Decimal from .*"):
        _ = ErrorBracket("hoge", "1")


def test_init_ng_err() -> None:
    """Provide invalid value."""
    with pytest.raises(ValueError, match=r"Cannot construct Decimal from .*"):
        _ = ErrorBracket("1", "fuga")


def test_init_ng_negerr() -> None:
    """Provide negative error."""
    with pytest.raises(ValueError, match="err must be positive."):
        _ = ErrorBracket("1", "-0.1", 2)


def test_init_ng_negprec() -> None:
    """Provide invalid precision."""
    with pytest.raises(ValueError, match="prec must be positive."):
        _ = ErrorBracket("1", "0.1", -2)


def test_init_ng_zeroprec() -> None:
    """Provide invalid precision."""
    with pytest.raises(ValueError, match="prec must be positive."):
        _ = ErrorBracket("1", "0.1", 0)


def test_init_ng_bigerr() -> None:
    """Provide error larger than value."""
    with pytest.raises(
        ValueError,
        match="Cannot format properly as err is larger than val.",
    ):
        _ = ErrorBracket("1", "2")


def test_getter() -> None:
    """Test the getter methods."""
    x = ErrorBracket("1", "0.1")
    assert x.val == Decimal("1")
    assert x.err == Decimal("0.1")
    assert x.prec == 1


def test_getter_safety() -> None:
    """Check if getter methods are safe."""
    x = ErrorBracket("1", "0.1", 1)
    val = x.val
    val *= 2
    assert val == Decimal("2")
    assert x.val == Decimal("1")


def test_eq() -> None:
    """Test the __eq__ method."""
    x = ErrorBracket("1", "0.1", 2)
    y = ErrorBracket("1", "0.1", 2)
    assert id(x) != id(y)
    assert x == y


def test_eq_notimpl() -> None:
    """Test the __eq__ method with different type."""
    x = ErrorBracket("1", "0.1", 2)
    assert x != "hoge"


def test_repr() -> None:
    """Test the __repr__ method."""
    x = ErrorBracket("1", "0.1", 2)
    cmp = repr(x)
    m = re.match(r"ErrorBracket\((.*)\)", cmp)
    assert m is not None
    val, err, prec = str(m.group(1)).split(", ")
    assert x == ErrorBracket(val, err, int(prec))
