import matplotlib.pyplot as plt
from typing import Dict, List
from dataclasses import dataclass

SCREEN_DPI = 300


@dataclass
class Subplot:
    name: str
    data: List[float]


def make_plot(
    name: str,
    versions: List[str],
    data: List[Subplot],
    plot_file: str | None = None,
    xlabel="Version",
    ylabel="Time",
    verbose=False,
):
    figure = plt.figure(figsize=(16, 8))

    axes = figure.add_axes((0.1, 0.15, 0.8, 0.7))
    axes.spines[["top", "bottom", "left", "right"]].set_visible(True)
    axes.grid(which="minor", alpha=0.35)
    axes.grid(which="major", alpha=0.7)
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)

    axes.set_title(name)

    for subplot in data:
        axes.plot(
            versions,
            subplot.data,
            label=subplot.name,
        )
    axes.legend()
    if plot_file is not None:
        figure.savefig(
            plot_file,
            dpi=SCREEN_DPI,
        )
    if verbose:
        figure.show()
        plt.show()
