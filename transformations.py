from typing import List
import plots


def apply_all(plot_list: List[plots.Plottable], arguments):
    for index, plot in enumerate(plot_list):
        labels(plot, index, arguments.labels)
        x_multiplier(plot, arguments.xMultiplier)
        y_multiplier(plot, arguments.yMultiplier)


def labels(plot: plots.Plottable, index: int, labels: List[str]):
    if not labels is None and len(labels) > index:
        plot.label = labels[index]


def x_multiplier(plot: plots.Plottable, multiplier: float):
    plot.x = plot.x * multiplier


def y_multiplier(plot: plots.Plottable, multiplier: float):
    plot.y = plot.y * multiplier
