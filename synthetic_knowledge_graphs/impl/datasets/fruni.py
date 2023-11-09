import random


import networkx as nx


from synthetic_knowledge_graphs.core.contracts.synthetic_dataset import SyntheticDataset
from synthetic_knowledge_graphs.core.entities.name_generator import NameGeneratorFRUNI
from synthetic_knowledge_graphs.core.values.constants import EntityType, Relation


import numpy as np

from synthetic_knowledge_graphs.impl.graph_utils import GraphUtilsNX


class FRUNIDataset(SyntheticDataset):
    """
    Generates a synthetic dataset representing a simplified friendship,
    university interaction model.

    Parameters:
    -----------
    n_u : int
        Number of universities in the dataset.
    lambda_f : float
        Average number of friends per student
    alpha_u : float, optional
        Probability of collaborative relationships between universities (default is 0.0).
    n_f : int
        Number of universities that foster friendship.
    """

    def __init__(
        self,
        n_u: int,
        lambda_f: float,
        alpha_u: float = 0.0,
        n_f: float | None = None,
        **kwargs,
    ):
        if n_f is None:
            n_f = n_u // 2
        assert n_u > 0
        assert lambda_f > 0.0
        assert alpha_u >= 0.0 and alpha_u <= 1.0
        assert n_f >= 0 and n_f <= n_u

        self.n_u = n_u
        self.lambda_f = lambda_f
        self.alpha_u = alpha_u
        self.n_f = n_f
        self.num_students = 2

        super().__init__(**kwargs)

    def _id_str(self):
        return {
            "n_u": self.n_u,
            "lambda_f": self.lambda_f,
            "alpha_u": self.alpha_u,
            "n_f": self.n_f,
            "num_students": self.num_students,
        }

    def create_graph(self):
        NameGeneratorFRUNI.reset_counter()
        graph = nx.DiGraph()
        graph_list = []

        for uni_id in range(self.n_u):
            # Create graph for a university
            graph_uni = nx.DiGraph()

            # Add university node
            uni_name = NameGeneratorFRUNI.generate(EntityType.UNIVERSITY, uni_id=uni_id)
            graph_uni.add_node(uni_name, category=EntityType.UNIVERSITY)

            friends_of_student = {}

            # Create students nodes and add edges to the university
            for student_id in range(self.num_students):
                student_name = NameGeneratorFRUNI.generate(
                    EntityType.STUDENT, uni_id=uni_id, student_id=student_id
                )
                graph_uni.add_node(student_name, category=EntityType.STUDENT)
                graph_uni.add_edge(uni_name, student_name, relation=Relation.ENROLLS)
                friend_list = []

                # Create friends of students and add edges to the student
                num_friends = max(1, int(np.random.poisson(self.lambda_f)))
                for fr_id in range(num_friends):
                    friend_name = NameGeneratorFRUNI.generate(
                        EntityType.FRIEND,
                        uni_id=uni_id,
                        student_id=student_id,
                        friend_id=fr_id,
                    )
                    friend_list.append(friend_name)
                    graph_uni.add_node(friend_name, category=EntityType.FRIEND)
                    graph_uni.add_edge(
                        student_name,
                        friend_name,
                        relation=Relation.FRIEND_OF,
                    )

                friends_of_student[student_id] = friend_list
            if uni_id < self.n_f:
                # Add edges between friends of different students in the same uni
                for student_id, friends in friends_of_student.items():
                    for friend_i in friends:
                        for student_id_j, friends_j in friends_of_student.items():
                            if student_id_j == student_id:
                                continue
                            for friend_j in friends_j:
                                graph_uni.add_edge(
                                    friend_i, friend_j, relation=Relation.FRIEND_OF
                                )
            graph_list.append(graph_uni)

        for graph_i in graph_list:
            graph.add_nodes_from(graph_i.nodes(data=True))
            graph.add_edges_from(graph_i.edges(data=True))

        uni_nodes = GraphUtilsNX.filter_nodes_contain(graph, str(EntityType.UNIVERSITY))

        # Add edges between universities
        if self.alpha_u > 0:
            for uni_i in range(self.n_u):
                for uni_j in range(self.n_u):
                    if uni_i == uni_j:
                        continue
                    if random.random() < self.alpha_u:
                        uni_name_i = uni_nodes[uni_i]
                        uni_name_j = uni_nodes[uni_j]
                        graph.add_edge(
                            uni_name_i, uni_name_j, relation=Relation.COLLABORATES_WITH
                        )

        return graph

    def get_explanation(self, head: str, relation: str, tail: str):
        head_type = head.split("-")[0]
        tail_type = tail.split("-")[0]

        uni_type = EntityType.UNIVERSITY
        student_type = EntityType.STUDENT
        friend_type = EntityType.FRIEND
        explanation = []
        if head_type == uni_type and tail_type == uni_type:
            explanation.append((head, relation, tail))
        elif head_type == uni_type and tail_type == student_type:
            explanation.append((head, relation, tail))
        elif head_type == student_type and tail_type == friend_type:
            explanation.append((head, relation, tail))
        elif head_type == friend_type and tail_type == student_type:
            explanation.append((head, relation, tail))
        elif head_type == friend_type and tail_type == friend_type:
            uni_h, st_h, idx_h = head.split("-")[1:]
            uni_t, st_t, idx_t = tail.split("-")[1:]
            if uni_t != uni_h:
                raise ValueError(f"Wrong triple ({head}, {relation}, {tail})")
            explanation.append((head, relation, tail))
            st_h_name = f"{student_type}-{uni_t}-{st_h}"
            explanation.append((head, Relation.FRIEND_OF, st_h_name))
            st_t_name = f"{student_type}-{uni_t}-{st_t}"
            explanation.append((tail, Relation.FRIEND_OF, st_t_name))
            uni_name = f"{uni_type}-{uni_h}"
            if st_h != st_t:  # Inter edge
                explanation.append((st_h_name, Relation.ENROLLS, uni_name))
                explanation.append((st_t_name, Relation.ENROLLS, uni_name))
        else:
            raise ValueError(f"Wrong triple ({head}, {relation}, {tail})")

        explanation = tuple(item for sublist in explanation for item in sublist)

        return explanation
