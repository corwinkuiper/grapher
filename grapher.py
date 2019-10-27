import argparse
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(
    description='Plot data from files into a single graph.')
parser.add_argument('--files', type=str, nargs='+',
                    help='Files to load, white space seperated colums')
parser.add_argument('--labels', type=str, nargs='*',
                    help='Name the labels for the legend, in the same order as given in files')

parser.add_argument('--x', type=str, help='Title of the x axis')
parser.add_argument('--y', type=str, help='Title of the y axis')

parser.add_argument('--hideLegend', help='Hide the legend',
                    action='store_const', const=True, default=False)

parser.add_argument('--cols', nargs='*', type=int, default=[1],
                    help='Specify the columns to use for y data, numpy parser only')
parser.add_argument('--yErrors', nargs='*', type=int, default=[],
                    help='Specify the columns to read error data from. Multiple can be specified if multiple columns are specified. Numpy parser only.')
parser.add_argument('--xError', type=int, default=None,
                    help='Specify column to read x errors from.')
parser.add_argument('--regression', type=str, default=None,
                    help='Specify the type of regression to perform')
parser.add_argument('--marker', action='store_const', const=True, default=False,
                    help="Render as a set of points rather than a line. This is not that useful as using errors implies markers.")

parser.add_argument('--hideXLabels', help='Hide the x tick labels',
                    action='store_const', const=True, default=False)
parser.add_argument('--hideYLabels', help='Hide the y tick labels',
                    action='store_const', const=True, default=False)
parser.add_argument('--hideXTicks', help='Hide the x ticks',
                    action='store_const', const=True, default=False)
parser.add_argument('--hideYTicks', help='Hide the y ticks',
                    action='store_const', const=True, default=False)

parser.add_argument('--latex', help='Use latex to render text',
                    action='store_const', const=True, default=False)

parser.add_argument('--xMultiplier', help='Multiplier for the x axis',
                    type=float, default=1.0)

parser.add_argument('--dashed', help='Use various dashes instead of solid lines',
                    action='store_const', const=True, default=False)

parser.add_argument('--parser', default='numpy',
                    help='Specify the name of the parser to be used (default=numpy).')


args = parser.parse_args()

# Check validity of arguments passed in
if not len(args.yErrors) == 0 and not len(args.yErrors) == len(args.cols):
    raise ValueError(
        'If yErrors specified, there must be an equal number of columns and y errors.')

if args.dashed == True and args.marker == True:
    raise ValueError(
        'Both dashed and marker cannot be enabled at the same time.')

if args.regression is None and args.dashed == True and (not args.xError is None or len(args.yErrors) > 0):
    raise ValueError(
        'x or y errors implies markers, so the line cannot be dashed')

if args.latex:
    from matplotlib import rc
    rc('text', usetex=True)


# Specify some functions that may be used later on in the script


def npArrayOrNone(a):
    if a is None:
        return None
    if len(a) == 0:
        return None
    return np.array(a)


def rSquareCalculation(y, f):
    mean = y.mean()
    total = ((y-mean)**2).sum()
    residual = ((y-f)**2).sum()
    return 1 - residual/total


# Graphable is some general internal state that can be plotted by
# the system later on.
# It is specified by: [Plottable, Plottable,...]
# As long as that format is kept, doesn't matter how the data
# Is generated. Two parsers are here, one I wrote myself and the other
# is numpy loadtxt. At the moment numpy is more advanced as columns can
# be specified and I'd imagine it's better at parsing files.
graphable = []


class Plottable:
    def __init__(self, **kwargs):
        self.x = kwargs.get('x', None)
        self.y = kwargs.get('y', None)

        self.label = kwargs.get('label', None)
        self.xErr = kwargs.get('xErr', None)
        self.yErr = kwargs.get('yErr', None)
        self.displayType = kwargs.get('displayType', None)


# These are here because of the columns in the numpy parser.
read_cols = args.cols

displayType = 'line'
if args.marker:
    displayType = 'marker'
elif args.dashed:
    displayType = 'dashed'

if not args.xError is None or len(args.yErrors) > 0:
    displayType = 'marker'

if args.parser == 'numpy':
    for file_name in args.files:
        data = np.loadtxt(file_name)
        x = []
        y = [[] for i in range(0, len(read_cols))]
        yErrors = [[] for i in range(0, len(read_cols))]
        xError = []
        for item in data:
            x.append(item[0])
            for i, v in enumerate(read_cols):
                val = item[v]
                y[i].append(val)
            for i, v in enumerate(args.yErrors):
                yErrors[i].append(item[v])
            if args.xError:
                xError.append(item[args.xError])
        for i, y in enumerate(y):
            graphable.append(
                Plottable(x=np.array(x), y=np.array(y), label=file_name,
                          yErr=npArrayOrNone(yErrors[i]), xErr=npArrayOrNone(xError),
                          displayType=displayType))

# This is the old parser I wrote before I realised numpy.loadtxt existed.
# I've kept it in in case I made any assumptions about the data
# I created this for that wouldn't work in numpy due to different assumptions
# made there.
elif args.parser == 'old':
    for file_name in args.files:
        with open(file_name) as f:
            x = []
            y = []
            for line in f:
                n = line.rstrip().split(' ')
                row = []

                # I apologise for this all
                for elem in filter(None, n):
                    try:
                        float(elem)
                    except ValueError:
                        continue
                    number = float(elem)
                    row.append(number)
                if len(row) == 0:
                    continue

                x.append(row[0])
                y.append(row[1])
            graphable.append(
                Plottable(x=np.array(x), y=np.array(y), label=file_name,
                          displayType=displayType))


else:
    raise ValueError('The parser specified is not a valid or known parser')

# Modify the graphable with transformations

# Apply labels
for index, plot in enumerate(graphable):
    if args.labels and len(args.labels) > index:
        plot.label = args.labels[index]

# Apply xMultiplier
for plot in graphable:
    plot.x = plot.x * args.xMultiplier

# Do any regressions
if args.regression == 'linear':
    import scipy.odr
    from scipy import stats

    fits = []
    regressionDisplay = 'line'
    if args.dashed:
        regressionDisplay = 'dashed'

    for i, data in enumerate(graphable):
        # Since scipy has linregress, can get initial values for slope and intercept using that
        # which can then be improved and uncertainties taken into account with odr.
        slope, intercept, _, _, _ = stats.linregress(data.x, data.y)

        RealData = scipy.odr.RealData(
            data.x, y=data.y, sy=data.yErr, sx=data.xErr)

        def __linearModel__(B, x):
            return B[0]*x + B[1]
        linear = scipy.odr.Model(__linearModel__)
        odr = scipy.odr.ODR(RealData, linear, beta0=[slope, intercept])
        output = odr.run()
        gradient = output.beta[0]
        intercept = output.beta[1]

        err_gradient = output.sd_beta[0]
        err_intercept = output.sd_beta[1]

        f_x = gradient * data.x + intercept

        print(
            f'Regression Output for Fit Number {i+1} with data labelled {data.label}')
        print(f'\tGradient: {gradient} ± {err_gradient}')
        print(f'\tIntercept: {intercept} ± {err_intercept}')
        print(f'\tRSquare: {rSquareCalculation(data.y, f_x)}')

        fits.append(
            Plottable(x=data.x, y=f_x, displayType=regressionDisplay))

    for f in fits:
        graphable.append(f)


class Plotstyle:

    types = {
        'dashed': ['--', '-.', ':'],
        'marker': ['.', 's', 'v', '^', '<', '>'],
    }

    index = {
        'dashed': 0,
        'marker': 0,
    }

    def style(self, displayType):
        if displayType == 'line':
            return "-"
        if displayType in self.types:
            style = self.types[displayType][self.index[displayType] % len(
                self.types[displayType])]
            self.index[displayType] += 1
            return style
        return "-"


styles = Plotstyle()
fig, ax = plt.subplots()
for index, a in enumerate(graphable):

    if a.displayType == 'marker':
        p = ax.errorbar(a.x, a.y, yerr=a.yErr, xerr=a.xErr, capsize=3,
                        linestyle='None', markersize=10, marker=styles.style('marker'))
    else:
        p = ax.plot(a.x, a.y, linestyle=styles.style(a.displayType))
    if a.label:
        p[0].set_label(a.label)

if not args.hideLegend:
    ax.legend()


# Start standard style, if you don't like how this is done you can change it
plt.tick_params(axis='both', direction='in', top=True, right=True)


# Apply custom style. These modifications are commonly used so are included
# as command line arguments.
if args.hideXLabels:
    plt.tick_params(axis='x', labelbottom=False)

if args.hideYLabels:
    plt.tick_params(axis='y', labelleft=False)

if args.hideXTicks:
    plt.tick_params(axis='x', bottom=False, top=False)

if args.hideYTicks:
    plt.tick_params(axis='y', left=False, right=False)

plt.xlabel(args.x)
plt.ylabel(args.y)

# I tend to just want to show it, but if you want to use this
# as part of something automated then do something different here.
plt.show()
