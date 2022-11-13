import re
from Equation import Expression


class ParsingError(BaseException):
    pass


def parse(func):
    func = func.replace("^", "**")
    func = func.replace("exp", "e**")
    func = func.replace(")(", ")*(")

    func = re.sub(r"([0-9])(A-Za-z)", r"\1*\2", func)
    func = re.sub(r"\)(A-Za-z)", r")*\1", func)
    func = re.sub(r"-x\*\*([0-9]+)", r"-(x**\1)", func)

    print(func)

    parsed = Expression(func, ["x"])
    return parsed
