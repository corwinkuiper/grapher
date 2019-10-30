import numpy as np


def npArrayOrNone(a):
    if a is None:
        return None
    if len(a) == 0:
        return None
    return np.array(a)


def rSquared(y, f) -> float:
    mean = y.mean()
    total = ((y - mean) ** 2).sum()
    residual = ((y - f) ** 2).sum()
    return 1 - residual / total


class Value:
    def __init__(self, number, error):
        self.number = number
        self.error = error

    def __repr__(self):
        return f"{self.number} ± {self.error}"


def DictionaryFormatter(dictionary: dict):
    output = ""

    for key, value in dictionary.items():
        output = f"{output}\n{key}:\t{value}"
    return output.strip()
