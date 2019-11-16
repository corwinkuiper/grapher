import numpy as np
import numpy.fft as fft
import plots
from typing import List

# Must be over a linear space
def perform_transform(plot: plots.Plottable) -> plots.Plottable:
    f_y = fft.fftshift(np.real(fft.fft(plot.y)))
    f_x = fft.fftshift(fft.fftfreq(len(plot.x), plot.x[1] - plot.x[0]))

    return plots.Plottable(
        x=f_x, y=f_y, derived=True, description=f"Fourier Transform of {plot.label}"
    )


def perform_transforms(plot: List[plots.Plottable]) -> List[plots.Plottable]:
    p = []
    for plt in plot:
        p.append(perform_transform(plt))
    return p
