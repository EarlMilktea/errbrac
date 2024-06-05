"""Parse & format scientific error notations."""

from __future__ import annotations

import itertools
import re
from decimal import Decimal

_BRACKET_RE = re.compile(r"^(.*)\((\d+)\)(.*)$")
_DIGITS = frozenset("0123456789")


class ErrorBracket:
    """Represent a value with error."""

    __val: Decimal
    __err: Decimal
    __prec: int

    def __init__(
        self,
        val: Decimal | str,
        err: Decimal | str,
        prec: int = 1,
    ) -> None:
        """Initialize with value, error, and precision.

        Parameters
        ----------
        val : :class:`Decimal` or :class:`str`
            Value to represent.
        err : :class:`Decimal` or :class:`str`
            Associated error.
        prec : :class:`int`, optional
            Number of digits inside the bracket. Default is `1`.

        Raises
        ------
        :class:`ValueError`
            If inputs are in invalid domain, or `err` is too large.

        """
        try:
            val = Decimal(val)
        except Exception as e:
            msg = f"Cannot construct Decimal from {val}."
            raise ValueError(msg) from e
        try:
            err = Decimal(err)
        except Exception as e:
            msg = f"Cannot construct Decimal from {err}."
            raise ValueError(msg) from e
        if err <= 0:
            msg = "err must be positive."
            raise ValueError(msg)
        if prec <= 0:
            msg = "prec must be positive."
            raise ValueError(msg)
        if abs(val) < err:
            msg = "Cannot format properly as err is larger than val."
            raise ValueError(msg)
        exp = Decimal(f"1E{err.adjusted()-prec+1:+}")
        self.__val = val.quantize(exp)
        self.__err = err.quantize(exp)
        self.__prec = prec

    @property
    def val(self) -> Decimal:
        """Get the value.

        Returns
        -------
        :class:`Decimal`
            The value after rounding.

        """
        # NOTE: Decimal is immutable
        return self.__val

    @property
    def err(self) -> Decimal:
        """Get the error.

        Returns
        -------
        :class:`Decimal`
            The error associated with the value, rounded.

        """
        return self.__err

    @property
    def prec(self) -> int:
        """Return the precision.

        Returns
        -------
        :class:`int`
            Number of digits inside bracket.

        """
        return self.__prec

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ErrorBracket):
            return NotImplemented
        return self.__val == other.__val and self.__err == other.__err and self.__prec == other.__prec

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__val}, {self.__err}, {self.__prec})"

    def __str__(self) -> str:
        """Format as bracket notation."""
        work = itertools.chain(
            filter(lambda c: c != ".", f"{self.__err:f}"),
            itertools.repeat("0"),
        )
        err = "".join(
            itertools.islice(
                itertools.dropwhile(lambda c: c == "0", work),
                self.__prec,
            ),
        )
        val = f"{self.__val}"  # Let Python decide how to format
        assert "e" not in val
        i = val.find("E")
        if i == -1:
            return f"{val}({err})"
        return f"{val[:i]}({err}){val[i:]}"

    @staticmethod
    def parse(ex: str) -> ErrorBracket:
        """Parse bracket notation.

        Parameters
        ----------
        ex : :class:`str`
            String to parse.

        Returns
        -------
        :class:`ErrorBracket`
            Resulting object.

        """
        if not isinstance(ex, str):
            msg = f"{ex} is not a string."
            raise TypeError(msg)
        if not (m := _BRACKET_RE.match(ex)):
            msg = f"{ex!r} does not have proper bracket."
            raise ValueError(msg)
        head = str(m.group(1))
        err_d = str(m.group(2))
        tail = str(m.group(3))
        arg = head + tail
        try:
            val = Decimal(arg)
        except Exception as e:
            msg = f"Cannot construct Decimal from {arg!r}."
            raise ValueError(msg) from e
        rest = list(err_d)
        # Drop negative sign here
        work = ["0" if c in _DIGITS else c for c in head if c != "-"]
        for i in reversed(range(len(work))):
            if work[i] in _DIGITS and rest:
                work[i] = rest.pop()
        if rest:
            msg = f"{ex!r} has too many digits inside the bracket."
            raise ValueError(msg)
        arg = "".join(work) + tail
        try:
            err = Decimal(arg)
        except Exception as e:
            msg = f"Cannot construct Decimal from {arg!r}."
            raise ValueError(msg) from e
        return ErrorBracket(val, err, len(err_d))
