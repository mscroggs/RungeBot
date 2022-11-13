from Equation import Expression


class ParsingError(BaseException):
    pass


def parse(func):
    func = func.replace("^", "**")
    parsed = Expression(func, ["x"])
    return parsed
