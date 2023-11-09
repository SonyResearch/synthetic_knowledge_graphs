from __future__ import annotations
from typing import Any
import yaml
import pickle

import os

import numpy as np

import logging


class IOUtils:
    @staticmethod
    def dict_to_yaml(my_dict: dict[str, Any], file_path: str) -> None:
        with open(file_path, "w") as file:
            yaml.dump(my_dict, file)

    @staticmethod
    def object_to_pickle(obj: Any, file_path: str) -> None:
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)

    @staticmethod
    def list_to_txt(
        my_list: list[Any],
        file_path: str,
        fmt: str = "%s",
        delimiter: str = "\t",
        as_string: bool = False,
    ) -> None:
        # Assuming `path` is the file path
        if os.path.exists(file_path):
            logging.info(f"{file_path} already exists. Overwriting...")
        else:
            logging.info(f"Creating {file_path}...")

        if as_string:
            with open(file_path, "w") as file:
                for my_tuple in my_list:
                    # Flatten and convert to a comma-separated string
                    flattened_tuple = ",".join(my_tuple)
                    file.write(flattened_tuple + "\n")
        else:
            np.savetxt(file_path, my_list, fmt=fmt, delimiter=delimiter)

    @staticmethod
    def makedirs(folder: str) -> None:
        if not os.path.exists(folder):
            os.makedirs(folder)
