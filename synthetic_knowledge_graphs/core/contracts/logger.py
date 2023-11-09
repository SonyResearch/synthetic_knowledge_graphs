from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any


class Logger(ABC, logging.Logger):
    def __init__(self, enable: bool = True):
        self.is_enabled = enable

    def enable(self):
        self.is_enabled = True

    def disable(self):
        self.is_enabled = False

    @abstractmethod
    def log(self, key: str, value: Any) -> None:
        pass


#
