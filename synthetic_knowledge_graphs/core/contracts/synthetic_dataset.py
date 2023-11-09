import hashlib
import os
import pickle
import random


import logging

from abc import ABC, abstractmethod

from synthetic_knowledge_graphs.core.entities.io_utils import IOUtils


class SyntheticDataset(ABC):

    """
    SyntheticDataset represents synthetic knowledge graph.

    Args:
        percentages (list of float, optional): List of percentages to create dataset splits.
            Defaults to [1.0], meaning only train split.

        seed (int, optional): Seed for randomization. Defaults to 42.
    """

    def __init__(self, percentages: list[float] = [1.0], seed: int = 42):
        self.percentages = percentages
        assert sum(percentages) == 1.0
        self.seed = seed

        self.graph = self.create_graph()

    @abstractmethod
    def create_graph(self):
        pass

    @abstractmethod
    def get_explanation(self, head: str, relation: str, tail: str):
        pass

    @classmethod
    def load_explanation(cls, file_path: str, as_dict: bool = False):
        if as_dict:
            explanations = {}
        else:
            explanations = []
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                explanation_flat = tuple(line.split(","))
                explanation = []
                for i in range(0, len(explanation_flat), 3):
                    explanation.append(
                        (
                            explanation_flat[i],
                            explanation_flat[i + 1],
                            explanation_flat[i + 2],
                        )
                    )
                if as_dict:
                    explanations[explanation[0]] = explanation[1:]
                else:
                    explanations.append(explanation)
        return explanations

    @classmethod
    def load(cls, folder_hash: str):
        filename_obj = os.path.join(folder_hash, "dataset.pkl")
        with open(filename_obj, "rb") as file:
            my_obj = pickle.load(file)

        assert isinstance(my_obj, cls)
        return my_obj

    @abstractmethod
    def _id_str(self):
        pass

    def __id_str(self, as_dict=False):
        id_attributes = {
            "percentages": self.percentages,
            "seed": self.seed,
        }

        id_attributes.update(self._id_str())

        if as_dict:
            return id_attributes

        else:
            id_str_list = []
            for key, value in id_attributes.items():
                if isinstance(value, list):
                    value = "_".join([str(v) for v in value])
                id_str_list.append(f"{key}={value}")

            id_str = "-".join(id_str_list)
            return id_str

    def get_hash(self):
        id_str = self.__id_str()

        hash_object = hashlib.new("sha256")
        hash_object.update(id_str.encode("utf-8"))
        my_hash = hash_object.hexdigest()
        return my_hash

    def save(self, root: str):
        """
        Save the dataset to a folder

        Parameters
        ----------
        root : str
            The root folder where the dataset will be saved

        Returns
        -------
        None
        """

        my_hash = self.get_hash()

        folder = os.path.join(root, my_hash)

        # Create the folder if it does not exist
        IOUtils.makedirs(folder)

        filename_id = os.path.join(folder, "parameters.yaml")
        filename_object = os.path.join(folder, "dataset.pkl")
        logging.info(f"Saving dataset to {folder}")
        # Save the dataset parameters
        IOUtils.dict_to_yaml(self.__id_str(as_dict=True), filename_id)
        # Save the dataset object
        IOUtils.object_to_pickle(self, filename_object)

    def save_triples(
        self,
        root,
        only_train=False,
        use_hash=True,
        save_random_test_triples=0,
    ):
        id_str = self.__id_str()

        hash_object = hashlib.new("sha256")
        hash_object.update(id_str.encode("utf-8"))
        my_hash = hash_object.hexdigest()

        if use_hash:
            folder = os.path.join(root, my_hash)
        else:
            folder = root

        IOUtils.makedirs(folder)
        # Convert DiGraph to a list of triples
        triples = []
        explanations = []
        for u, v, attrs in self.graph.edges(data=True):
            relation = attrs["relation"]
            assert isinstance(relation, str)
            triples.append((u, relation, v))
            explanation = self.get_explanation(u, relation, v)
            explanations.append(explanation)

        idx_list = list(range(len(triples)))
        random.shuffle(idx_list)
        triples = [triples[i] for i in idx_list]
        explanations = [explanations[i] for i in idx_list]
        total_elements = len(triples)
        splits = [int(p * total_elements) for p in self.percentages]

        if len(self.percentages) == 2:
            names = ["train", "test"]
        else:
            names = ["train", "valid", "test"]

        start = 0
        for i, split in enumerate(splits):
            end = start + split
            if only_train:
                triples_i = triples
                explanations_i = explanations
            else:
                triples_i = triples[start:end]
                explanations_i = explanations[start:end]
            start = end

            # Save triples to a TSV file
            path = os.path.join(folder, f"{names[i]}.txt")
            path_explanations = os.path.join(folder, f"{names[i]}_explanations.txt")

            IOUtils.list_to_txt(triples_i, path)
            IOUtils.list_to_txt(explanations_i, path_explanations, as_string=True)

        if save_random_test_triples > 0:
            n = len(triples_i)
            assert (
                save_random_test_triples <= n
            ), f"save_random_test_triples={save_random_test_triples} > n={n}"
            random_indices = random.sample(range(n), save_random_test_triples)

            triples_rnd = [triples_i[i] for i in random_indices]
            path = os.path.join(folder, f"test_random_{save_random_test_triples}.txt")

            IOUtils.list_to_txt(triples_rnd, path)

        # Save category of nodes as a dictionary

        path = os.path.join(folder, "node_category.yaml")
        category_dict = {
            n: attrs.get("category") for n, attrs in self.graph.nodes(data=True)
        }

        IOUtils.dict_to_yaml(category_dict, path)
