from cli import cli
from parse import Parser
import transformations
import regression
from matplotlib import rc
import matplot
import matplotlib.pyplot as plt


def make_graph_of_arguments():
    arguments = cli().args()

    plots = Parser(
        arguments.columns, arguments.xError, arguments.yErrors, arguments.displayType
    ).parse_files(arguments.files)

    transformations.apply_all(plots, arguments)

    if arguments.latex:
        rc("text", usetex=True)

    plots.extend(regression.perform_regressions(arguments.regression, plots))

    matplot.plot(plots)
    matplot.set_style(arguments)

    plt.show()


make_graph_of_arguments()
