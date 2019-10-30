import argparse


class cli:
    class BadArguments(Exception):
        def __init__(self, message):
            self.message = message

    parser = None

    def args(self):
        arguments = self.parser.parse_args()

        potential_errors = self.check_argument_validity(arguments)
        if potential_errors is None:
            return arguments

        raise self.BadArguments(potential_errors)

    def check_argument_validity(self, args) -> str:
        # Check validity of arguments passed in
        if not len(args.yErrors) == 0 and not len(args.yErrors) == len(args.columns):
            return "If yErrors specified, there must be an equal number of columns and y errors."

        if (
            args.regression is None
            and args.displayType == "dashed"
            and (not args.xError is None or len(args.yErrors) > 0)
        ):
            return "x or y errors implies markers, so the line cannot be dashed"

        return None

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
            "--xMultiplier", help="Multiplier for the x axis", type=float, default=1.0
        )
        self.parser.add_argument(
            "--yMultiplier", help="Multiplier for the y axis", type=float, default=1.0
        )
