from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt

from synthetic_knowledge_graphs.core.contracts.plotter import Plotter


class MatplotlibFigure:
    def __init__(self, fig: plt.Figure, axis: plt.Axes):
        self.fig = fig
        self.axis = axis


class MatplotlibPlotter(Plotter):
    def create_figure(self, *args, **kwargs) -> MatplotlibFigure:
        fig, ax = plt.subplots(*args, **kwargs)
        figure = MatplotlibFigure(fig, ax)
        return figure

    def get_axis(self, figure: MatplotlibFigure) -> plt.Axes:
        return figure.axis

    def close(self, figure: MatplotlibFigure) -> Any:
        plt.close(figure.fig)

    def save(self, figure: MatplotlibFigure, file_path: str) -> Any:
        figure.fig.savefig(file_path)

    def show(self, figure: MatplotlibFigure) -> None:
        figure.fig.show()
