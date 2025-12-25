[![Python 3.8](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![nox](https://github.com/EarlMilktea/errbrac/actions/workflows/nox.yml/badge.svg)](https://github.com/EarlMilktea/errbrac/actions/workflows/nox.yml)
[![codecov](https://codecov.io/github/EarlMilktea/errbrac/graph/badge.svg?token=HLUVGWZW2O)](https://codecov.io/github/EarlMilktea/errbrac)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# errbrac: Parse & format scientific error notations

🪽 Minimal dependencies: small and lightweight.

🔢 Using `Decimal` internally: no loss of precision.

## Installation

📦 You can install the package via pip:

```bash
pip install git+https://github.com/EarlMilktea/errbrac
```

## Usage

### Parsing bracket notations

📈 Scientific notation is also supported.

```python
from errbrac import ErrorBracket

# x.val == 1.23, x.err == 0.04, x.prec == 1
x = ErrorBracket.parse("1.23(4)")

# y.val == -2011, y.err == 20, y.prec == 2
y = ErrorBracket.parse("-2.011(20)E+3")
```

### Formatting bracket notations

🤖 Output notation is automatically chosen based on values.

```python
from errbrac import ErrorBracket

x = ErrorBracket.parse("1.23(4)")
print(x) # 1.23(4)

y = ErrorBracket.parse("-2.011(20)E+3")
print(y) # -2011(20)
```

## License

📄 This package is licensed under the MIT license.
