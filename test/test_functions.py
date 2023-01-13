import function_parser as fp
import interpolator as ip
import pytest


@pytest.mark.parametrize("function_string", [
    "x**0.5", "x**2", "x", "abs(x)", "cos(pi*x)",
    "5**x", "1/(1+25*x**2)"
])
def test_parsing(function_string):
    f = fp.parse(function_string)
    ip.interpolate_and_rate(f)
