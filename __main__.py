from arguments import cli
from parse import Parser
import transformations
import regression
import fourier
from matplotlib import rc
import matplot
import matplotlib.pyplot as plt
import numpy as np


def make_graph_of_arguments():
    arguments = cli().args()

    plots = Parser(
        arguments.columns, arguments.xError, arguments.yErrors, arguments.displayType
    ).parse_files(arguments.files)

    transformations.apply_all(plots, arguments)

    if arguments.latex:
        rc("text", usetex=True)

    regressions = regression.perform_regressions(arguments.regression, plots)
    fourier_transforms = []
    if arguments.fourier:
        fourier_transforms = fourier.perform_transforms(plots)

    derived_quantities = []
    derived_quantities.extend(regressions)
    derived_quantities.extend(fourier_transforms)

    if arguments.saveDerived:
        n = 1
        for p in derived_quantities:
            np.savetxt(
                f"{arguments.saveDerived}_derived_{n}.txt",
                np.transpose([p.x, p.y]),
                header=p.description,
            )

    if arguments.derivedOnly:
        plots = derived_quantities
    else:
        plots.extend(derived_quantities)

    if not arguments.hide:
        matplot.plot(plots)
        matplot.set_style(arguments)

        plt.show()


make_graph_of_arguments()
