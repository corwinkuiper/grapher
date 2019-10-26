# grapher

Many people use matplotlib to plot graphs by using some script that they modify each time.
I am too lazy to consider modifying a script to load the data that I want, so here is my lazy solution.

A CLI python script for making graphs that I sometimes use.
Made when I had a bunch of files with data that I wanted to plot.
In general I think it works best when you have a bunch of data sets in different files that you want to plot.

[And yes, making a CLI is more work than the lazy option.](https://xkcd.com/1205/)

## Usage

`python grapher.py --help` displays the help information.
The only required parameter is `--files`.
So `python grapher.py --files data.dat` will plot the data found in `data.dat`.
It attempts this by loading the file using `numpy.loadtxt` and taking the first column as the x data and the second column as y data.
If you want to specify to use another, or multiple y columns, use `--cols` to pass in one or multiple y columns.

I will not cover all the other options as I think some if not most are somewhat self explanatory.
If you want to know what a parameter does, open an issue.
If you want to know if it can do something open an issue.
If you want it to do something open an issue.


## File format

Since by default the data is loaded by `numpy.loadtxt` using default settings, columns are separated with white space and `#` can be used to comment out lines.
Here is an example file and a command that can be used to plot it with some *fancy* features.

```
#x     x_err    y      y_err
 1     0.1      13     4
 2     0.1      18     3
 3     0.1      27     3
 4     0.1      44     5
```

`python grapher.py --files data.dat --cols 2 --xError 1 --yErrors 3 --regression linear`

## Requirements

* Python of some sort. I use one of the 3s.
* Numpy.
* Matplotlib
* Scipy (optional, for the regression)