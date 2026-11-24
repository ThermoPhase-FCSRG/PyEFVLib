import numpy as np
import pytest

from PyEFVLib.BoundaryConditions import getFunction


@pytest.mark.parametrize("expression, expected", [
	("2*x + y - z", 2 * 1.0 + 2.0 - 3.0),
	("exp(x)", np.exp(1.0)),
	("sqrt(y)", np.sqrt(2.0)),
	("tan(x) + cosh(y)", np.tan(1.0) + np.cosh(2.0)),
	("max(x, y)", 2.0),
	("sin(pi*x) * exp(-t)", np.sin(np.pi) * np.exp(-4.0)),
	("np.hypot(x, y)", np.hypot(1.0, 2.0)),
])
def test_named_functions_are_evaluated(expression, expected):
	assert getFunction(expression)(1.0, 2.0, 3.0, 4.0) == pytest.approx(expected)


def test_time_is_optional():
	assert getFunction("x + t")(1.0, 0.0, 0.0) == pytest.approx(1.0)


def test_python_builtins_are_not_available():
	with pytest.raises(NameError):
		getFunction("open('file')")(0.0, 0.0, 0.0)
