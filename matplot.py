import matplotlib.pyplot as plt
import plots
from typing import List
from arguments import arguments

styles = plots.Plotstyle()


def plot_single(axis: plt.Axes, plot: plots.Plottable):
    if plot.displayType == "marker":
        p = axis.errorbar(
            plot.x,
            plot.y,
            yerr=plot.yErr,
            xerr=plot.xErr,
            capsize=3,
            linestyle="None",
            markersize=10,
            marker=styles.style("marker"),
        )
    else:
        p = axis.plot(plot.x, plot.y, linestyle=styles.style(plot.displayType))
    if plot.label:
        p[0].set_label(plot.label)


def plot(plots: List[plots.Plottable]):
    _, axis = plt.subplots()
    for plot in plots:
        plot_single(axis, plot)


def set_style(args: arguments):
    if not args.hideLegend:
        plt.legend()

    # Start standard style, if you don't like how this is done you can change it
    plt.tick_params(axis="both", direction="in", top=True, right=True)

    # Apply custom style. These modifications are commonly used so are included
    # as command line arguments.
    if args.hideXLabels:
        plt.tick_params(axis="x", labelbottom=False)

    if args.hideYLabels:
        plt.tick_params(axis="y", labelleft=False)

    if args.hideXTicks:
        plt.tick_params(axis="x", bottom=False, top=False)

    if args.hideYTicks:
        plt.tick_params(axis="y", left=False, right=False)

    plt.xlabel(args.x)
    plt.ylabel(args.y)
