from abc import ABC


class GraphUtils(ABC):
    @staticmethod
    def filter_nodes_contain(
        node_id_list: list[str | int], value: str | int
    ) -> list[str | int]:
        output_nodes = []
        for node_id in node_id_list:
            if value in node_id:
                output_nodes.append(node_id)

        return output_nodes

    @staticmethod
    def filter_nodes_equal_to(
        node_id_list: list[str | int], value: str | int
    ) -> list[str | int]:
        output_nodes = []
        for node_id in node_id_list:
            if value == node_id:
                output_nodes.append(node_id)

        return output_nodes
