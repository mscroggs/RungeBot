from Equation import Expression


class ParsingError(BaseException):
    pass


def parse(func):
    parsed = Expression(func, ["x"])
    return parsed
