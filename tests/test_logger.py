import os

import pytest

from synthetic_knowledge_graphs.impl.logger import DummyLogger, FSLogger


def create_value(mode):
    if mode == "int":
        value = 1
    elif mode == "float":
        value = 1.0
    elif mode == "str":
        value = "my_str"
    elif mode == "bool":
        value = True
    elif mode == "list":
        value = [1, 2, 3]
    elif mode == "dict":
        value = {"a": 1, "b": 2}
    else:
        raise ValueError(f"Unknown mode: {mode}")

    return value


@pytest.mark.parametrize("device", ["cpu"])
@pytest.mark.parametrize("mode", ["int", "float", "str", "bool", "list", "dict"])
def test_fs_logger(device, mode):
    folder = os.path.join("tests", "logs")
    logger = FSLogger(folder=folder, clean=True)

    value = create_value(mode)

    logger.log(f"logging_{mode}.txt", value)


@pytest.mark.parametrize("device", ["cpu"])
@pytest.mark.parametrize("mode", ["int", "float", "str", "bool", "list", "dict"])
def test_dummy_logger(device, mode):
    logger = DummyLogger()

    value = create_value(mode)

    logger.log(f"logging_{mode}.txt", value)
