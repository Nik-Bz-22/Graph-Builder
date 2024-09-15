import math
from typing import TypeAlias
import networkx as nx


INNER_GRAPH_TYPE: TypeAlias = nx.Graph
GRAPH_TYPE: TypeAlias = list[tuple[float, tuple[int, int], tuple[int, int]]]


class Algorithms:
    @staticmethod
    def _to_graph(data: GRAPH_TYPE) -> INNER_GRAPH_TYPE:
        g = nx.Graph()
        for weight, node1, node2 in data:
            g.add_edge(node1, node2, weight=weight)
        return g

    def radic_index(self, graph: GRAPH_TYPE) -> dict:
        valid_graph = self._to_graph(graph)
        radic_sum = 0.0

        for u, v in valid_graph.edges():
            degree_u = valid_graph.degree(u)
            degree_v = valid_graph.degree(v)
            segm = 1 / math.sqrt(degree_u * degree_v)
            radic_sum += segm
            valid_graph[u][v]["weight"] = segm

        result_graph = [
            (f"{data['weight']:.3}", node1, node2)
            for node1, node2, data in valid_graph.edges(data=True)
        ]
        return {"graph": result_graph, "data": round(radic_sum, 3)}

    def max_tree(self, graph: GRAPH_TYPE) -> dict:
        valid_graph = self._to_graph(graph)
        mst = nx.maximum_spanning_tree(valid_graph, algorithm="kruskal")
        mst_edges = [
            (data["weight"], node1, node2)
            for node1, node2, data in mst.edges(data=True)
        ]
        # return  mst_edges
        return {"graph": mst_edges, "data": None}

    def min_tree(self, graph: GRAPH_TYPE) -> dict:
        valid_graph = self._to_graph(graph)
        mst = nx.minimum_spanning_tree(valid_graph, algorithm="kruskal")
        mst_edges = [
            (data["weight"], node1, node2)
            for node1, node2, data in mst.edges(data=True)
        ]
        # return  mst_edges
        return {"graph": mst_edges, "data": None}

    @staticmethod
    def calc_weight(graph: GRAPH_TYPE) -> dict:
        total_weight = sum(float(edge[0]) for edge in graph)
        return {"graph": None, "data": total_weight}

    def get_invariant(self, graph: GRAPH_TYPE) -> dict:
        max_tree = self.max_tree(graph)
        min_tree = self.min_tree(graph)
        max_tree_weight = self.calc_weight(max_tree["graph"])
        min_tree_weight = self.calc_weight(min_tree["graph"])
        randic_index_min = self.radic_index(min_tree["graph"])
        randic_index_max = self.radic_index(max_tree["graph"])

        result = f"Minimum tree weight: {min_tree_weight["data"]:.4f}   Maximum tree weight: {max_tree_weight["data"]:.4f}   Min tree randic index: {randic_index_min["data"]:.4f}   Max tree randic index: {randic_index_max["data"]:.4f}"
        return {"graph": None, "data": result}


if __name__ == "__main__":
    a = Algorithms()
    r = a.radic_index(
        [
            (1.0, (536, 226), (755, 350)),
            (0.2, (41, 325), (375, 617)),
            (0.3, (163, 121), (324, 99)),
            (0.4, (163, 121), (41, 325)),
            (3.0, (536, 226), (375, 617)),
        ]
    )
    print(r)
