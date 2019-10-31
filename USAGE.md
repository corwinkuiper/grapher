# Usage

The README contains limited detail on usage, covering only the very and most extreme of basics.
This document will do precisely the opposite, containing what could almost be described as detailed information detailing what each option does in excruciating detail.

## --options

*All* of the options are accessed by using some sort of `--optionName` with any parameters after it.
All options are in the camelCase style, at least I'm pretty sure it's called that.

The options are as follows:


### --files

The most important option,

```
grapher --files list of files
```

The files `list`, `of`, and `files` will be read and attempted to be plotted.
By default, the first column will be treated as the x axis and the second column the y axis.

### --columns

Specifies the column(s) to be interpreted as the y axis.

```
grapher --columns 1
```

This is the default behaviour

### --x and --y

Sets the axis titles.

```
grapher --x "The x-axis" --y "The y-axis $\left(\times 10^{-14}\right)$"
```

### --xError and --yErrors

xError accepts a single number representing the column to be treated as the x error.
yErrors takes a list that if specified must be equal in length to columns.
It specifies the columns to be interpreted as errors in y.


### --xMultiplier and --yMultiplier

A number to multiply all x values by, and similarly for yMultiplier.
This is useful if you want to convert between SI unit prefixes.


### --regression

My personal favourite feature.

A linear regression can be performed by passing `linear`.
It uses scipy to estimate the initial values and performs a regression using `scipy.odr`, this takes into account weightings provided by errors.
This is the best way to perform a linear regression using this grapher.

However, if you want to fit to some arbitrary function of x, you can!
Pass in the function with fitting coefficients represented by single capital letters.

```
grapher --files data.txt --regression "A*exp(-B*x) + C"
```

That will attempt to fit the data to some exponential decay.
Initial parameters can be specified by calling the coefficient as a function, this may sound strange but the following example may be easier to understand.

```
grapher --files data.txt --regression "A(40)*exp(-B*x) + C"
```

This uses `A=40` as an initial value for A and performs the fit using that information.
Additionally `A(10, 100)` will scan between 10 and 100 to try to find the best possible fit.
In general, `A(a, b, c)` searches over `numpy.linspace(a, b, c)` where by default `c=10` (as opposed to numpy's default of 50).

As shown I used an `exp` function in there. The available functions are: `sin`, `sinh`, `cos`, `cosh`, `tan`, `tanh`, `asin`, `acos`, `atan`, `asinh`, `acosh`, `atanh`, `exp`, and `log`.
These are defined by the numpy equivalents of these functions.
Additionally the constants `pi` and `e` are allowed.

### --displayType

Display type tells grapher how to tell matplotlib how to draw the points.
By default it draws as a `"line"`.
If you pass `dashed` it tries to draw a dashed line.
If you pass `marker` it tries to draw individual dots.

However, if you specify `dashed` and x/y errors, it errors (unless you perform a regression).
A regression will never be marker, but it may be a dashed line.


### --hideXLabels and --hideYLabels

Hides the tick labels for the x and y axis.
Will do so when present, will not do so when not present.

### --hideXTicks and --hideYTicks

Hides the ticks for the x and y axis.
Will do so when present, will not do so when not present.


### --latex

Render text using a latex installation.
This is not needed to use latex notation in labels.
Matplotlib has it's own renderer.
Will do so when present, will not do so when not present.
