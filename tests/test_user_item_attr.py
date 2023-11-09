import os

import pytest

from synthetic_knowledge_graphs import UserItemAttrDataset
from synthetic_knowledge_graphs.core.values.constants import EntityType
from synthetic_knowledge_graphs.impl.graph_utils import GraphUtilsNX


def create_default_dataset():
    return UserItemAttrDataset(
        num_attrs=4,
        num_items=20,
        num_users=10,
        lambda_a=0.01,
        lambda_i=3.0,
        percentages=[0.8, 0.2],
        seed=0,
    )


@pytest.mark.parametrize("num_attrs", [5, 10])
@pytest.mark.parametrize("num_items", [50, 100])
@pytest.mark.parametrize("num_users", [50, 100])
@pytest.mark.parametrize("lambda_a", [0.001, 1.0])
@pytest.mark.parametrize("lambda_i", [1.0, 5.0])
@pytest.mark.parametrize("percentages", [[0.5, 0.3, 0.2]])
@pytest.mark.parametrize("seed", list(range(2)))
def test_constructor(
    num_attrs: int,
    num_items: int,
    num_users: int,
    lambda_a: float,
    lambda_i: float,
    percentages: list[float],
    seed: int,
):
    dataset = UserItemAttrDataset(
        num_attrs=num_attrs,
        num_items=num_items,
        num_users=num_users,
        lambda_a=lambda_a,
        lambda_i=lambda_i,
        percentages=percentages,
        seed=seed,
    )

    user_nodes = GraphUtilsNX.filter_nodes_contain(dataset.graph, EntityType.USER)
    assert (
        len(user_nodes) == num_users
    ), f"Number of user entities mismatch {len(user_nodes)} != {num_users}"

    it_nodes = GraphUtilsNX.filter_nodes_contain(dataset.graph, EntityType.ITEM)
    assert (
        len(it_nodes) == num_items
    ), f"Number of item entities mismatch {len(it_nodes)} != {num_items}"

    attr_nodes = GraphUtilsNX.filter_nodes_contain(dataset.graph, EntityType.ATTRIBUTE)
    assert (
        len(attr_nodes) == num_attrs
    ), f"Number of attribute entities mismatch {len(attr_nodes)} != {num_attrs}"


@pytest.mark.parametrize("num_attrs", [5, 10])
@pytest.mark.parametrize("num_items", [50, 100])
@pytest.mark.parametrize("seed", list(range(20)))
def test_items_with_single_attr(
    num_attrs: int,
    num_items: int,
    seed: int,
):
    dataset = UserItemAttrDataset(
        num_attrs=num_attrs,
        num_items=num_items,
        num_users=50,
        lambda_a=0.0,
        lambda_i=3.0,
        percentages=[0.5, 0.25, 0.25],
        seed=seed,
    )
    for item_node in GraphUtilsNX.filter_nodes_contain(dataset.graph, EntityType.ITEM):
        assert len(list(dataset.graph.predecessors(item_node))) == 1


def test_save():
    dataset = create_default_dataset()
    root = os.path.join("tests", "data", "user_item_attr")
    dataset.save(root)
    dataset.save_triples(root)

    hash = dataset.get_hash()

    folder = os.path.join(root, hash)
    assert os.path.exists(folder)

    for split in ["train", "test"]:
        path = os.path.join(folder, f"{split}.txt")
        assert os.path.exists(path)


def test_load():
    my_hash = "128110ffab86357d70e6970a75a369771c821b6021c6d35b6736837de0fa5103"
    root = os.path.join("tests", "data", "user_item_attr")
    folder_hash = os.path.join(root, my_hash)
    dataset = UserItemAttrDataset.load(folder_hash=folder_hash)

    assert isinstance(dataset, UserItemAttrDataset)
