import matplotlib.pyplot as plt
from typing import Dict, List
import random

SCREEN_DPI = 96
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400


def random_color():
    return (random.random(), random.random(), random.random())


def make_plot(name: str, versions: List[str], data: Dict[str, List[float]]):
    figure = plt.figure(figsize=(WINDOW_WIDTH / SCREEN_DPI, WINDOW_HEIGHT / SCREEN_DPI))

    axes = figure.add_axes((0.1, 0.15, 0.8, 0.7))
    axes.spines[["top", "bottom", "left", "right"]].set_visible(True)
    axes.grid(which="minor", alpha=0.35)
    axes.grid(which="major", alpha=0.7)

    axes.set_xlabel("Version")
    axes.set_ylabel("Time")

    axes.set_title(name)

    for subplot_name, subplot_data in data.items():
        axes.plot(
            versions,
            subplot_data,
            label=subplot_name,
            color=random_color(),
        )
    axes.legend()

    figure.show()
    plt.show()
