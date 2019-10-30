class Plottable:
    def __init__(self, **kwargs):
        self.x = kwargs.get("x", None)
        self.y = kwargs.get("y", None)

        self.label = kwargs.get("label", None)
        self.xErr = kwargs.get("xErr", None)
        self.yErr = kwargs.get("yErr", None)
        self.displayType = kwargs.get("displayType", None)


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
