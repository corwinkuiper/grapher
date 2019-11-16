import scipy.odr as odr
from scipy import stats
import numpy as np
import plots
from helpers import rSquared, Value, DictionaryFormatter
from typing import List, Tuple, Dict, Union


def perform_linear_regression(
    plot: plots.Plottable
) -> Tuple[plots.Plottable, Dict[str, Value], np.ndarray]:
    slope, intercept, _, _, _ = stats.linregress(plot.x, plot.y)
    RealData = odr.RealData(plot.x, y=plot.y, sx=plot.xErr, sy=plot.yErr)
    o = odr.ODR(
        RealData, odr.Model(lambda B, x: B[0] * x + B[1]), beta0=[slope, intercept]
    )
    output = o.run()
    beta = output.beta
    f_x: np.ndarray = beta[0] * plot.x + beta[1]

    return (
        plots.Plottable(x=plot.x, y=f_x),
        {
            "gradient": Value(beta[0], output.sd_beta[0]),
            "intercept": Value(beta[1], output.sd_beta[1]),
        },
        f_x,
    )


def perform_arbitrary_regression(
    plot: plots.Plottable, function: str
) -> Tuple[plots.Plottable, Dict[str, Value], np.ndarray]:
    pyFunc = mathsFunction(function)
    ODRModel = odr.Model(pyFunc.function)
    RealData = odr.RealData(plot.x, y=plot.y, sy=plot.yErr, sx=plot.xErr)
    coeffs = pyFunc.coefficients

    def next_val(l: List, b: List, best: odr.Output) -> odr.Output:
        if len(l) == 0:
            o = odr.ODR(RealData, ODRModel, beta0=b)
            output = o.run()
            if best is None:
                return output
            if best.sum_square > output.sum_square:
                return output
            return best
        for n in np.linspace(l[0].initial, l[0].final, l[0].number):
            new_b = b.copy()
            new_b.append(n)
            best = next_val(l[1:], new_b, best)
        return best

    coList: List[Union[None, mathsFunction.variables.coefficient]] = [
        None
    ] * pyFunc.numberOfCoefficients
    for letter, coef in coeffs.items():
        coList[pyFunc.letterToNumber[letter]] = coef
    output = next_val(coList, [], None)

    space = np.linspace(plot.x[0], plot.x[-1], 1000)
    f_x = pyFunc.function(output.beta, space)

    coefficients = {}
    for letter, number in pyFunc.letterToNumber.items():
        coefficients[letter] = Value(output.beta[number], output.sd_beta[number])

    return (
        plots.Plottable(x=space, y=f_x),
        coefficients,
        pyFunc.function(output.beta, plot.x),
    )


def perform_regressions(
    regressionType: str, plot_arr: List[plots.Plottable]
) -> List[plots.Plottable]:

    if not regressionType:
        return []
    if not regressionType == "linear":
        compiled_regression = compile(regressionType, "regression_function", "eval")

    fits = []
    for index, plot in enumerate(plot_arr):
        if regressionType == "linear":
            fit, params, plot_x_fit = perform_linear_regression(plot)
        else:
            fit, params, plot_x_fit = perform_arbitrary_regression(
                plot, compiled_regression
            )

        description = f"Regression for {plot.label}, which is plot #{index+1}"
        description += f"\n\tFunction was: {regressionType}"
        description += f"\n\tCoefficients:"
        description += "\n\t\t" + "\n\t\t".join(
            DictionaryFormatter(params).splitlines()
        )
        description += f"\n\tRSquared: {rSquared(plot.y, plot_x_fit)}"

        fit.derived = True
        fit.description = description

        print(description)
        fits.append(fit)

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

    class variables:
        class coefficient(float):

            initial: float = 1.0
            final: float = 1.0
            number: int = 1
            dry_run: bool = False

            def __init__(self, value):
                self.value = float(value)

            def __call__(self, *argv) -> float:
                if not self.dry_run:
                    return self.value
                if len(argv) == 0:
                    raise Exception("Wrong call of coefficient")
                if len(argv) == 1:
                    self.initial = argv[0]
                    self.final = self.initial
                if len(argv) == 2:
                    self.initial = argv[0]
                    self.final = argv[1]
                    self.number = 10
                if len(argv) == 3:
                    self.initial = argv[0]
                    self.final = argv[1]
                    self.number = argv[2]

                return self.value

        coeffs: Dict[str, coefficient] = {}
        letterToNumber: Dict[str, int] = {}
        beta: List[float] = []
        x: float = 1.0
        dry_run: bool = True

        def __getitem__(self, key: str):
            if key == "x":
                return self.x

            if len(key) == 1 and key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if not key in self.letterToNumber:
                    self.letterToNumber[key] = len(self.letterToNumber)
                if self.dry_run and len(self.beta) <= self.letterToNumber[key]:
                    self.coeffs[key] = self.coefficient(1.0)
                    self.coeffs[key].dry_run = True
                    return self.coeffs[key]
                return self.coefficient(self.beta[self.letterToNumber[key]])
            raise KeyError

        def set_values(self, b: List[float], x: np.ndarray):
            self.beta = b
            self.x = x

    letterToNumber: Dict[str, int] = {}
    numberOfCoefficients: int = 0
    coefficients: Dict[str, variables.coefficient] = {}

    def __init__(self, functionString):
        self.__vars__ = self.variables()
        eval(functionString, self.__globals__, self.__vars__)
        self.numberOfCoefficients = len(self.__vars__.letterToNumber)
        self.letterToNumber = self.__vars__.letterToNumber
        self.coefficients = self.__vars__.coeffs

        self.__vars__.dry_run = False

        def f(B, x):
            self.__vars__.set_values(B, x)
            return eval(functionString, self.__globals__, self.__vars__)

        self.function = f
