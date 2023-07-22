# noinspection PyShadowingBuiltins,PyUnusedLocal
def compute(x: int, y: int) -> int:
    if any([input_param >= 100 for input_param in [x, y]]):
        raise ValueError("Inputs must be less 100")

    return x + y


