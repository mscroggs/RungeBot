import re
from Equation import Expression


class ParsingError(BaseException):
    pass


def parse(func):
    func = func.replace("^", "**")

    for i in ["exp", "sin", "cos", "tan", "log"]:
        func = func.replace(i, f"math.{i}")
    func = func.replace("math.math", "math")

    func = re.sub(r"([0-9])x", r"\1*x", func)
    parsed = Expression(func, ["x"])
    return parsed
