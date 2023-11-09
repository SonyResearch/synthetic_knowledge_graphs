import random


import networkx as nx


from synthetic_knowledge_graphs.core.contracts.synthetic_dataset import SyntheticDataset
from synthetic_knowledge_graphs.core.entities.name_generator import NameGeneratorFTREE
from synthetic_knowledge_graphs.core.values.constants import EntityType, Relation


import numpy as np


class FTREEDataset(SyntheticDataset):
    """
    FTREEDataset represents a dataset for family trees.

    Args:
        n_t (int): The number of family trees in the dataset.

        lambda_b (float): The average number of branches per family tree

        n_d (int): The number of different lengths of descendants
    """

    def __init__(
        self,
        n_t: int,
        lambda_b: float,
        n_d: int,
        **kwargs,
    ):
        assert n_d >= 2
        self.n_t = n_t
        self.lambda_b = lambda_b
        self.n_d = n_d

        super().__init__(**kwargs)

    def _id_str(self):
        return {
            "n_t": self.n_t,
            "lambda_b": self.lambda_b,
            "n_d": self.n_d,
        }

    def create_graph(self):
        NameGeneratorFTREE.reset_counter()
        graph = nx.DiGraph()

        graph_list = []

        b_len_list = list(range(1, self.n_d + 1))

        for tree_id in range(self.n_t):
            # Create graph for a family tree
            graph_c = nx.DiGraph()

            # Add progenitor node
            progneitor_name = NameGeneratorFTREE.generate(
                EntityType.PROGENITOR, tree_id
            )

            graph_c.add_node(progneitor_name, category=EntityType.PROGENITOR)

            # Add branches
            num_branches = max(2, np.random.poisson(self.lambda_b))

            for branch_id in range(num_branches):
                # Sample b_len from b_len_list
                b_len = random.choice(b_len_list)
                for kid_id in range(b_len):
                    kid_name = NameGeneratorFTREE.generate(
                        EntityType.KID, tree_id, branch_id, kid_id
                    )
                    graph_c.add_node(kid_name, category=EntityType.KID)

                    if kid_id == 0:
                        graph_c.add_edge(
                            progneitor_name, kid_name, relation=Relation.ANCESTOR_OF
                        )
                    else:
                        kid_prev_name = NameGeneratorFTREE.generate(
                            EntityType.KID, tree_id, branch_id, kid_id - 1
                        )
                        graph_c.add_edge(
                            kid_prev_name, kid_name, relation=Relation.ANCESTOR_OF
                        )

                hobbie_name = NameGeneratorFTREE.generate(
                    EntityType.HOBBIE, tree_id, branch_id
                )
                graph_c.add_node(hobbie_name, category=EntityType.HOBBIE)

                tail_relation = Relation.SENTIMENT(b_len)

                graph_c.add_edge(kid_name, hobbie_name, relation=tail_relation)
                last_kid_name = NameGeneratorFTREE.generate(
                    EntityType.LAST_KID, tree_id, branch_id
                )
                graph_c.add_node(last_kid_name, category=EntityType.LAST_KID)
                graph_c.add_edge(kid_name, last_kid_name, relation=Relation.ANCESTOR_OF)

            graph_list.append(graph_c)

        for graph_i in graph_list:
            graph.add_nodes_from(graph_i.nodes(data=True))
            graph.add_edges_from(graph_i.edges(data=True))

        self.edge_keys = [Relation.ANCESTOR_OF]
        self.edge_keys.extend([Relation.SENTIMENT(b_len) for b_len in b_len_list])

        return graph

    def get_explanation(self, head: str, relation: str, tail: str):
        explanation = []
        if Relation.ANCESTOR_OF in relation:
            explanation.append((head, relation, tail))
        elif Relation.SENTIMENT() in relation:
            explanation.append((head, relation, tail))
            head_list = head.split("-")
            assert len(head_list) == 4
            h_tree_id, h_branch_id, h_kid_id = head_list[1:]

            tail_list = tail.split("-")
            assert len(tail_list) == 3
            t_name, t_tree_id, t_branch_id = tail_list
            assert h_tree_id == t_tree_id
            assert h_branch_id == t_branch_id

            b_len = int(relation.split("_")[-1])
            progenitor_name = NameGeneratorFTREE.generate(
                EntityType.PROGENITOR, t_tree_id
            )
            branch = Relation.ANCESTOR_OF
            for kid_id in range(b_len):
                kid_name = NameGeneratorFTREE.generate(
                    EntityType.KID, t_tree_id, t_branch_id, kid_id
                )
                if kid_id == 0:
                    explanation.append((progenitor_name, branch, kid_name))
                else:
                    kid_prev_name = NameGeneratorFTREE.generate(
                        EntityType.KID, t_branch_id, t_branch_id, kid_id - 1
                    )
                    explanation.append((kid_prev_name, branch, kid_name))

        else:
            raise ValueError(f"Wrong triple ({head}, {relation}, {tail})")
        explanation = tuple(item for sublist in explanation for item in sublist)

        return explanation
