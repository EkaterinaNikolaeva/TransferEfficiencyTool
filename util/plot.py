import matplotlib.pyplot as plt
from typing import List
from dataclasses import dataclass
import yaml

SCREEN_DPI = 300


@dataclass
class Subplot:
    name: str
    data: List[float]


def load_plot_data(filename: str):
    with open(filename, "r") as f:
        subplots_data = yaml.load(f, Loader=yaml.BaseLoader)
    subplots = []
    for item in subplots_data:
        subplots.append(
            Subplot(name=item["name"], data=[float(value) for value in item["data"]])
        )
    return subplots


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
    axes.set_xlabel(xlabel, fontsize=16)
    axes.set_ylabel(ylabel, fontsize=16)
    axes.set_title(name, fontsize=16)
    axes.tick_params(axis="both", which="major", labelsize=14)

    for subplot in data:
        print(versions, subplot.data)
        axes.plot(
            versions,
            subplot.data,
            label=subplot.name,
            linewidth=2,
        )
    axes.legend(fontsize=14)

    if plot_file is not None:
        figure.savefig(
            plot_file,
            dpi=SCREEN_DPI,
        )
    if verbose:
        figure.show()
        plt.show()
