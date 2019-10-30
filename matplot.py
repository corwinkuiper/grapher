import matplotlib.pyplot as plt
import plots
from typing import List

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


def set_style(arguments):
    if not arguments.hideLegend:
        plt.legend()

    # Start standard style, if you don't like how this is done you can change it
    plt.tick_params(axis="both", direction="in", top=True, right=True)

    # Apply custom style. These modifications are commonly used so are included
    # as command line arguments.
    if arguments.hideXLabels:
        plt.tick_params(axis="x", labelbottom=False)

    if arguments.hideYLabels:
        plt.tick_params(axis="y", labelleft=False)

    if arguments.hideXTicks:
        plt.tick_params(axis="x", bottom=False, top=False)

    if arguments.hideYTicks:
        plt.tick_params(axis="y", left=False, right=False)

    plt.xlabel(arguments.x)
    plt.ylabel(arguments.y)
