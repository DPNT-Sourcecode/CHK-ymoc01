# noinspection PyShadowingBuiltins,PyUnusedLocal
def compute(x: int, y: int) -> int:
    if any([input_param >= 100 for input_param in [x, y]]):
        raise ValueError("Inputs must be less than 100")
    if any([input_param <= 0 for input_param in [x, y]]):
        raise ValueError("Inputs must be greater than 0")

    return x + y


