import numpy as np
from typing import List, Union


class Plottable:
    def __init__(
        self,
        x=[],
        y=[],
        label: Union[str, None] = None,
        xErr: Union[int, None] = None,
        yErr: Union[List[int], None] = None,
        displayType: Union[str, None] = None,
    ):
        self.x = np.array(x)
        self.y = np.array(y)

        self.label = label
        self.xErr = xErr
        self.yErr = yErr
        self.displayType = displayType


class Plotstyle:

    types = {"dashed": ["--", "-.", ":"], "marker": [".", "s", "v", "^", "<", ">"]}

    index = {"dashed": 0, "marker": 0}

    def style(self, displayType):
        if displayType == "line":
            return "-"
        if displayType in self.types:
            style = self.types[displayType][
                self.index[displayType] % len(self.types[displayType])
            ]
            self.index[displayType] += 1
            return style
        return "-"
