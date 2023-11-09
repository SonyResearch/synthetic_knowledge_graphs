from __future__ import annotations

from typing import Any

from synthetic_knowledge_graphs.core.contracts.logger import Logger


class DummyLogger(Logger):
    def log(self, key: str, value: Any) -> None:
        return
