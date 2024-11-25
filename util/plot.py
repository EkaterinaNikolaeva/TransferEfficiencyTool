import matplotlib.pyplot as plt
from typing import Dict, List
from dataclasses import dataclass

SCREEN_DPI = 128
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400


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
):
    figure = plt.figure(figsize=(WINDOW_WIDTH / SCREEN_DPI, WINDOW_HEIGHT / SCREEN_DPI))

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
    figure.show()
    plt.show()
