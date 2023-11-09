from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Figure:
    pass


class Axis:
    pass


class Plotter(ABC):
    @abstractmethod
    def create_figure(self, *args, **kwargs) -> Figure:
        pass

    @abstractmethod
    def get_axis(self, figure: Figure) -> Axis:
        pass

    @abstractmethod
    def close(self, figure: Any) -> None:
        pass

    @abstractmethod
    def save(self, figure: Any, file_path: str) -> None:
        pass

    @abstractmethod
    def show(self, figure: Any) -> None:
        pass
