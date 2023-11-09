import os

import pytest

from synthetic_knowledge_graphs import FTREEDataset
from synthetic_knowledge_graphs.core.values.constants import EntityType
from synthetic_knowledge_graphs.impl.graph_utils import GraphUtilsNX


def create_default_dataset():
    return FTREEDataset(
        n_t=2,
        lambda_b=5,
        n_d=2,
        percentages=[0.8, 0.2],
        seed=0,
    )


@pytest.mark.parametrize("n_t", [1, 2, 5])
@pytest.mark.parametrize("lambda_b", [6.0, 10.0])
@pytest.mark.parametrize("n_d", [2, 3])
@pytest.mark.parametrize("percentages", [[0.5, 0.3, 0.2]])
@pytest.mark.parametrize("seed", list(range(2)))
def test_constructor(
    n_t: int, lambda_b: float, n_d: int, percentages: list[float], seed: int
):
    dataset = FTREEDataset(
        n_t=n_t,
        lambda_b=lambda_b,
        n_d=n_d,
        percentages=percentages,
        seed=seed,
    )

    root_nodes = GraphUtilsNX.filter_nodes_contain(dataset.graph, EntityType.PROGENITOR)
    assert (
        len(root_nodes) == n_t
    ), f"Number of family trees mismatch {len(root_nodes)} != {n_t}"


def test_save():
    dataset = create_default_dataset()
    root = os.path.join("tests", "data", "ftree")
    dataset.save(root)
    dataset.save_triples(root)


def test_load():
    my_hash = "e1573a886a4529f3f37462dfb9ec7744562bfc21996c9d2d4db2164437f2d528"
    root = os.path.join("tests", "data", "ftree")
    folder_hash = os.path.join(root, my_hash)
    dataset = FTREEDataset.load(folder_hash=folder_hash)

    assert isinstance(dataset, FTREEDataset)
