import plots
import numpy as np
import helpers
from typing import List


class Parser:

    displayType = "line"
    xError = None
    yErrors = []
    columns = [1]

    def __init__(self, columns, xError, yErrors, suggestedDisplayType):
        self.columns = columns
        self.xError = xError
        self.yErrors = yErrors
        self.displayType = suggestedDisplayType
        if not xError is None or not len(yErrors) == 0:
            self.displayType = "marker"

    def parse_files(self, file_names) -> List[plots.Plottable]:
        fplots = []
        for file_name in file_names:
            fplots.extend(self.parse_file(file_name))

        return fplots

    def parse_file(self, file_name) -> List[plots.Plottable]:

        plots_from_file = []
        data = np.loadtxt(file_name)
        x = []
        y = [[] for i in range(0, len(self.columns))]
        yErrors = [[] for i in range(0, len(self.columns))]
        xError = []
        for item in data:
            x.append(item[0])
            for i, v in enumerate(self.columns):
                val = item[v]
                y[i].append(val)
            for i, v in enumerate(self.yErrors):
                yErrors[i].append(item[v])
            if self.xError:
                xError.append(item[self.xError])
        for i, y in enumerate(y):
            plots_from_file.append(
                plots.Plottable(
                    x=np.array(x),
                    y=np.array(y),
                    label=file_name,
                    yErr=helpers.npArrayOrNone(yErrors[i]),
                    xErr=helpers.npArrayOrNone(xError),
                    displayType=self.displayType,
                )
            )
        return plots_from_file

