import plots
import numpy as np
import helpers
from typing import List


class Parser:

    displayType = "line"
    xError = None
    yErrors: List[int] = []
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
        x = [row[0] for row in data]
        all_y: List[List[float]] = []
        yErrors: List[List[float]] = []
        xError: List[float] = []
        for col in self.columns:
            all_y.append([row[col] for row in data])
        for col in self.yErrors:
            yErrors.append([row[col] for row in data])
        if self.xError:
            xError.append([row[self.xError] for row in data])
        for i, y in enumerate(all_y):
            plots_from_file.append(
                plots.Plottable(
                    x=np.array(x),
                    y=np.array(y),
                    label=file_name,
                    yErr=helpers.npArrayOrNone(None if i >= len(yErrors) else yErrors[i]),
                    xErr=helpers.npArrayOrNone(xError),
                    displayType=self.displayType,
                )
            )
        return plots_from_file

