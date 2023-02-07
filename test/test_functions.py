import function_parser as fp
import interpolator as ip
import pytest


@pytest.mark.parametrize("function_string", [
    "x**0.5", "x**2", "x", "abs(x)", "cos(pi*x)",
    "5**x", "1/(1+25*x**2)", "arctan(x)", "arcsin(x)", "arccos(x)",
    # Functions from Twitter/Mathstodon that have previously failed
    "x^x", "1/x", "(25/24)abs(x+(1/7))-(7/24)(x+(1/7))", "2*x + -x^(x-2)",
    "log(x)", "ln(x)", "cos x", "x!", "factorial(x)", "factorial(x*lnx)"
])
def test_parsing(function_string):
    f = fp.parse(function_string)
    ip.interpolate_and_rate(f)
