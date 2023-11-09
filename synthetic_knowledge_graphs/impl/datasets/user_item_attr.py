import random


import networkx as nx


from synthetic_knowledge_graphs.core.contracts.synthetic_dataset import SyntheticDataset
from synthetic_knowledge_graphs.core.entities.name_generator import NameGeneratorUIA
from synthetic_knowledge_graphs.core.values.constants import EntityType, Relation


import numpy as np


class UserItemAttrDataset(SyntheticDataset):
    """
    The UserItemAttrDataset represents a dataset for a user-item-attribute knowledge graph.

    Args:
    - num_attr (int): The number of attributes in the dataset.
    - num_it (int): The number of items in the dataset.
    - num_u (int): The number of users in the dataset.
    - lambda_a (float): The average number of attributes that an item possesses.
    - lambda_i (float):The average number of items that a user has bought.
    """

    def __init__(
        self,
        num_attrs: int,
        num_items: int,
        num_users: int,
        lambda_a: float,
        lambda_i: float,
        **kwargs,
    ):
        assert num_attrs >= 2
        assert num_items >= 2
        assert num_users >= 2
        assert lambda_a >= 0.0
        assert lambda_i >= 0.0

        self.num_attr = num_attrs
        self.num_it = num_items
        self.num_u = num_users

        self.lambda_a = lambda_a
        self.lambda_i = lambda_i

        super().__init__(**kwargs)

    def _id_str(self):
        return {
            "num_attr": self.num_attr,
            "num_it": self.num_it,
            "num_u": self.num_u,
            "lambda_a": self.lambda_a,
            "lambda_i": self.lambda_i,
        }

    def create_graph(self):
        NameGeneratorUIA.reset_counter()
        graph = nx.DiGraph()

        r = np.eye(2, 2)
        self.rel_emb = {}
        self.rel_emb[Relation.HELD_BY] = r[0]
        self.rel_emb[Relation.BOUGHT_BY] = r[1]

        attr_name_list = []

        # Generate attribute nodes
        for i in range(self.num_attr):
            x = np.zeros(self.num_attr)
            x[i] = 1.0
            attr_name = NameGeneratorUIA.generate(EntityType.ATTRIBUTE)
            graph.add_node(attr_name, x=x, category=EntityType.ATTRIBUTE)
            attr_name_list.append(attr_name)

        # Generate item nodes
        for i in range(self.num_it):
            x = np.zeros(self.num_attr)
            if self.lambda_a > 0.0:
                n = max(1, np.random.poisson(self.lambda_a))
            else:
                n = 1
            n = min(n, self.num_attr)
            # Sample n elements from a list of elements without replacement
            attr_names_of_item = np.random.choice(attr_name_list, n, replace=False)
            item_name = NameGeneratorUIA.generate(EntityType.ITEM)
            graph.add_node(item_name, x=x, category=EntityType.ITEM)
            for attr_name_j in attr_names_of_item:
                graph.add_edge(
                    attr_name_j,
                    item_name,
                    x=self.rel_emb[Relation.HELD_BY],
                    relation=Relation.HELD_BY,
                )

        # Generate user nodes
        for i in range(self.num_u):
            x = -1.0 * np.ones(self.num_attr)
            # Sample attribute of user
            user_name = NameGeneratorUIA.generate(EntityType.USER)
            attr_name_i = np.random.choice(attr_name_list, 1, replace=False)[0]

            graph.add_node(
                user_name, x=x, attribute=attr_name_i, category=EntityType.USER
            )

            # Find item nodes that are connected to attr-attr_idx
            it_nodes = [n for n in graph.successors(attr_name_i)]

            n = max(1, np.random.poisson(self.lambda_i))
            # n = int(lambda_i)
            n = min(n, len(it_nodes))
            for it_j in np.random.choice(it_nodes, n, replace=False):
                graph.add_edge(
                    it_j,
                    user_name,
                    x=self.rel_emb[Relation.BOUGHT_BY],
                    relation=Relation.BOUGHT_BY,
                )

        return graph

    def get_explanation(self, head: str, relation: str, tail: str):
        explanation = []
        if Relation.HELD_BY in relation:
            explanation.append((head, relation, tail))
        elif Relation.BOUGHT_BY in relation:
            assert EntityType.USER in tail
            explanation.append((head, relation, tail))

            item_names = self.graph.predecessors(tail)
            attr_name = self.graph.nodes[tail]["attribute"]

            for item_name in item_names:
                explanation.append((attr_name, Relation.HELD_BY, item_name))
                explanation.append((item_name, Relation.BOUGHT_BY, tail))

                # Assert the edges exist in the graph
                assert self.graph.has_edge(attr_name, item_name)
                assert self.graph.has_edge(item_name, tail)
        explanation = tuple(item for sublist in explanation for item in sublist)

        return explanation
