import scipy.odr as odr
from scipy import stats
import numpy as np
import plots
from helpers import rSquared, Value
from typing import List


def perform_linear_regression(plot: plots.Plottable) -> plots.Plottable:
    slope, intercept, _, _, _ = stats.linregress(plot.x, plot.y)
    RealData = odr.RealData(plot.x, y=plot.y, sx=plot.xErr, sy=plot.yErr)
    o = odr.ODR(
        RealData, odr.Model(lambda B, x: B[0] * x + B[1]), beta0=[slope, intercept]
    )
    output = o.run()
    beta = output.beta
    f_x = beta[0] * plot.x + beta[1]

    return (
        f_x,
        {
            "gradient": Value(beta[0], output.sd_beta[0]),
            "intercept": Value(beta[1], output.sd_beta[1]),
        },
    )


def perform_arbitrary_regression(
    plot: plots.Plottable, function: str
) -> plots.Plottable:
    pyFunc = mathsFunction(function)
    ODRModel = odr.Model(pyFunc.function)
    RealData = odr.RealData(plot.x, y=plot.y, sy=plot.yErr, sx=plot.xErr)
    o = odr.ODR(RealData, ODRModel, beta0=[1] * pyFunc.numberOfConstants)
    output = o.run()

    f_x = pyFunc.function(output.beta, plot.x)

    coefficients = {}
    for number, letter in enumerate(pyFunc.letterToNumber):
        coefficients[letter] = Value(output.beta[number], output.sd_beta[number])

    return f_x, coefficients


def perform_regressions(
    regressionType: str, plot_arr: List[plots.Plottable]
) -> List[plots.Plottable]:

    fits = []
    if regressionType == "linear":
        for plot in plot_arr:
            fit, params = perform_linear_regression(plot)
            print(params)
            fits.append(plots.Plottable(x=plot.x, y=fit))
    elif regressionType:
        for plot in plot_arr:
            fit, params = perform_arbitrary_regression(plot, regressionType)
            print(params)
            fits.append(plots.Plottable(x=plot.x, y=fit))

    return fits


class mathsFunction:
    __globals__ = {
        "sin": np.sin,
        "sinh": np.sinh,
        "cos": np.cos,
        "cosh": np.cosh,
        "tan": np.tan,
        "tanh": np.tanh,
        "asin": np.arcsin,
        "acos": np.arccos,
        "atan": np.arctan,
        "asinh": np.arcsinh,
        "acosh": np.arccosh,
        "atanh": np.arctanh,
        "pi": np.pi,
        "e": np.e,
        "exp": np.exp,
        "log": np.log,
        "__builtins__": None,
    }

    letterToNumber = None
    numberOfConstants = 0

    class variables:

        letterToNumber = {}
        beta = []
        x = 0
        dry_run = True

        def __getitem__(self, key):
            if key == "x":
                return self.x

            if len(key) == 1 and key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if not key in self.letterToNumber:
                    self.letterToNumber[key] = len(self.letterToNumber)
                if self.dry_run and len(self.beta) <= self.letterToNumber[key]:
                    return 0
                return self.beta[self.letterToNumber[key]]
            raise KeyError

        def set_values(self, b, x):
            self.beta = b
            self.x = x

    def __init__(self, functionString):
        self.__vars__ = self.variables()
        eval(functionString, self.__globals__, self.__vars__)
        self.numberOfConstants = len(self.__vars__.letterToNumber)
        self.letterToNumber = self.__vars__.letterToNumber

        self.__vars__.dry_run = False

        def f(B, x):
            self.__vars__.set_values(B, x)
            return eval(functionString, self.__globals__, self.__vars__)

        self.function = f
