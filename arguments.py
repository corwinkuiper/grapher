import argparse
from typing import List, Union, Tuple


class arguments:
    def __init__(
        self,
        files: List[str] = [],
        labels: Union[List[str], None] = None,
        x: str = "",
        y: str = "",
        hideLegend: bool = False,
        columns: List[int] = [1],
        yErrors: List[int] = [],
        xError: Union[int, None] = None,
        regression: Union[str, None] = None,
        displayType: str = "line",
        hideXTicks: bool = False,
        hideYTicks: bool = False,
        hideXLabels: bool = False,
        hideYLabels: bool = False,
        latex: bool = False,
        xMultiplier: float = 1.0,
        yMultiplier: float = 1.0,
        saveDerived: Union[str, None] = None,
        fourier: bool = False,
        hide: bool = False,
        derivedOnly: bool = False,
    ):
        self.files: List[str] = files
        self.labels: Union[List[str], None] = labels
        self.x: str = x
        self.y: str = y
        self.hideLegend: bool = hideLegend
        self.columns: List[int] = columns
        self.yErrors: List[int] = yErrors
        self.xError: Union[int, None] = xError
        self.regression: Union[str, None] = regression
        self.displayType: str = displayType
        self.hideXLabels: bool = hideXLabels
        self.hideYLabels: bool = hideYLabels
        self.hideXTicks: bool = hideXTicks
        self.hideYTicks: bool = hideYTicks
        self.latex: bool = latex
        self.xMultiplier: float = xMultiplier
        self.yMultiplier: float = yMultiplier
        self.saveDerived: Union[str, None] = saveDerived
        self.fourier: bool = fourier
        self.hide: bool = hide
        self.derivedOnly: bool = derivedOnly

    def validate(self) -> Tuple[bool, List]:
        error_list = []
        # Check validity of arguments passed in
        if not len(self.yErrors) == 0 and not len(self.yErrors) == len(self.columns):
            error_list.append(
                "If yErrors specified, there must be an equal number of columns and y errors."
            )
        if (
            self.regression is None
            and self.displayType == "dashed"
            and (not self.xError is None or len(self.yErrors) > 0)
        ):
            error_list.append(
                "x or y errors implies markers, so the line cannot be dashed"
            )

        return len(error_list) == 0, error_list


class BadArguments(Exception):
    def __init__(self, errors: List):
        super().__init__("\n".join(errors))


class cli:
    def args(self) -> arguments:
        argument = arguments()

        self.parser.parse_args(namespace=argument)

        ok, potential_errors = argument.validate()
        if ok:
            return argument

        raise BadArguments(potential_errors)

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Plot data from files into a single graph."
        )
        self.parser.add_argument(
            "--files",
            type=str,
            nargs="+",
            help="Files to load, white space seperated colums",
        )
        self.parser.add_argument(
            "--labels",
            type=str,
            nargs="*",
            help="Name the labels for the legend, in the same order as given in files",
        )

        self.parser.add_argument("--x", type=str, help="Title of the x axis")
        self.parser.add_argument("--y", type=str, help="Title of the y axis")

        self.parser.add_argument(
            "--hideLegend",
            help="Hide the legend",
            action="store_const",
            const=True,
            default=False,
        )

        self.parser.add_argument(
            "--columns",
            nargs="*",
            type=int,
            default=[1],
            help="Specify the columns to use for y data, numpy parser only",
        )
        self.parser.add_argument(
            "--yErrors",
            nargs="*",
            type=int,
            default=[],
            help="Specify the columns to read error data from. Multiple can be specified if multiple columns are specified. Numpy parser only.",
        )
        self.parser.add_argument(
            "--xError",
            type=int,
            default=None,
            help="Specify column to read x errors from.",
        )
        self.parser.add_argument(
            "--regression",
            type=str,
            default=None,
            help="Specify the type of regression to perform",
        )
        self.parser.add_argument(
            "--fourier",
            help="Perform a fourier transform on the input",
            action="store_const",
            const=True,
            default=False,
        )

        self.parser.add_argument(
            "--saveDerived",
            default=None,
            type=str,
            help="Save the derived data, such as regressions and fourier transforms",
        )

        self.parser.add_argument(
            "--displayType",
            help="Set how to display the points, eg. dashed or with markers",
            type=str,
            default="line",
        )

        self.parser.add_argument(
            "--hideXLabels",
            help="Hide the x tick labels",
            action="store_const",
            const=True,
            default=False,
        )
        self.parser.add_argument(
            "--hideYLabels",
            help="Hide the y tick labels",
            action="store_const",
            const=True,
            default=False,
        )
        self.parser.add_argument(
            "--hideXTicks",
            help="Hide the x ticks",
            action="store_const",
            const=True,
            default=False,
        )
        self.parser.add_argument(
            "--hideYTicks",
            help="Hide the y ticks",
            action="store_const",
            const=True,
            default=False,
        )

        self.parser.add_argument(
            "--latex",
            help="Use latex to render text",
            action="store_const",
            const=True,
            default=False,
        )

        self.parser.add_argument(
            "--hide",
            help="Don't show the plot, only perform side effects",
            action="store_const",
            const=True,
            default=False,
        )

        self.parser.add_argument(
            "--derivedOnly",
            help="Only display derived plots",
            action="store_const",
            const=True,
            default=False,
        )

        self.parser.add_argument(
            "--xMultiplier", help="Multiplier for the x axis", type=float, default=1.0
        )
        self.parser.add_argument(
            "--yMultiplier", help="Multiplier for the y axis", type=float, default=1.0
        )
