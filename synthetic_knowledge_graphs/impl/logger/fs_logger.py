from __future__ import annotations

import os
import shutil
from typing import Any

from synthetic_knowledge_graphs.core.contracts.logger import Logger


class FSLogger(Logger):
    def __init__(self, folder: str = "logs", clean: bool = False):
        self.folder = folder
        if os.path.exists(self.folder) and clean:
            shutil.rmtree(self.folder)

        os.makedirs(self.folder, exist_ok=True)
        super().__init__()

    def log(self, key: str, value: Any) -> None:
        if not self.is_enabled:
            return
        path = os.path.join(self.folder, key)
        with open(path, "a") as f:
            f.write(f"{value}\n")
