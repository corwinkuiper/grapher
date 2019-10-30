from typing import List
import plots
from arguments import arguments


def apply_all(plot_list: List[plots.Plottable], args: arguments):
    for index, plot in enumerate(plot_list):
        labels(plot, index, args.labels)
        x_multiplier(plot, args.xMultiplier)
        y_multiplier(plot, args.yMultiplier)


def labels(plot: plots.Plottable, index: int, labels: List[str]):
    if not labels is None and len(labels) > index:
        plot.label = labels[index]


def x_multiplier(plot: plots.Plottable, multiplier: float):
    plot.x = plot.x * multiplier


def y_multiplier(plot: plots.Plottable, multiplier: float):
    plot.y = plot.y * multiplier
