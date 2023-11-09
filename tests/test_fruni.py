import os

import pytest

from synthetic_knowledge_graphs import FRUNIDataset
from synthetic_knowledge_graphs.core.values.constants import EntityType
from synthetic_knowledge_graphs.impl.graph_utils import GraphUtilsNX


def create_default_dataset():
    return FRUNIDataset(
        n_u=20,
        lambda_f=1.0,
        alpha_u=0.0,
        n_f=None,
        percentages=[0.8, 0.2],
        seed=0,
    )


@pytest.mark.parametrize("n_u", [50, 100])
@pytest.mark.parametrize("lambda_f", [0.001, 1.0])
@pytest.mark.parametrize("alpha_u", [0.0, 0.05])
@pytest.mark.parametrize("n_f", [None, 10])
@pytest.mark.parametrize("percentages", [[0.5, 0.3, 0.2]])
@pytest.mark.parametrize("seed", list(range(2)))
def test_constructor(
    n_u: int,
    lambda_f: float,
    alpha_u: float,
    n_f: int | None,
    percentages: list[float],
    seed: int,
):
    dataset = FRUNIDataset(
        n_u=n_u,
        lambda_f=lambda_f,
        alpha_u=alpha_u,
        n_f=n_f,
        percentages=[0.8, 0.2],
        seed=0,
    )

    uni_nodes = GraphUtilsNX.filter_nodes_contain(dataset.graph, EntityType.UNIVERSITY)
    assert (
        len(uni_nodes) == n_u
    ), f"Number of university entities mismatch {len(uni_nodes)} != {n_u}"

    student_nodes = GraphUtilsNX.filter_nodes_contain(dataset.graph, EntityType.STUDENT)
    assert (
        len(student_nodes) == n_u * 2
    ), f"Number of student entities mismatch {len(uni_nodes)} != {n_u}"


def test_save():
    dataset = create_default_dataset()
    root = os.path.join("tests", "data", "fruni")
    dataset.save(root)
    dataset.save_triples(root)


def test_load():
    my_hash = "c905f95e34af69c45f7974e57cf285f5f82a30384719baafa4042ea86c04aa71"
    root = os.path.join("tests", "data", "fruni")
    folder_hash = os.path.join(root, my_hash)
    dataset = FRUNIDataset.load(folder_hash=folder_hash)

    assert isinstance(dataset, FRUNIDataset)
