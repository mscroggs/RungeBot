import re
from Equation import Expression


class ParsingError(BaseException):
    pass


def parse(func):
    func = func.replace("^", "**")
    func = func.replace("exp", "e**")
    func = func.replace(")(", ")*(")

    func = func.replace("atan", "arctan")
    func = func.replace("asin", "arcsin")
    func = func.replace("acos", "arccos")
    func = func.replace("tan-1", "arctan")
    func = func.replace("sin-1", "arcsin")
    func = func.replace("cos-1", "arccos")

    func = func.replace("ln", "log")
    func = func.replace("csc", "cosec")

    func = func.replace("cos x", "cos(x)")
    func = func.replace("sin x", "sin(x)")
    func = func.replace("tan x", "tan(x)")
    func = func.replace("sec x", "sec(x)")
    func = func.replace("cosec x", "cosec(x)")
    func = func.replace("cot x", "cot(x)")
    func = func.replace("log x", "log(x)")

    func = re.sub(r"([0-9])([A-Za-z])", r"\1*\2", func)
    func = re.sub(r"\)([A-Za-z])", r")*\1", func)
    func = re.sub(r"-x\*\*([0-9]+)", r"-(x**\1)", func)

    print(func)

    parsed = Expression(func, ["x"])
    return parsed
