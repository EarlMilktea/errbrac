from __future__ import annotations

import nox
from nox import Session


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"])
def tests(session: Session) -> None:
    session.install("-e", ".[dev]")
    session.run("pytest")
