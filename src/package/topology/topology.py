import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix


class Topology(object):
    """
    Topology class
    """
    def __init__(self):
        # TODO: you could add yourself parameters at here
        pass

    @staticmethod
    def generate_sample_topology() -> (np.ndarray, np.ndarray):
        """
        Generate sample matrix from book
        :return: adjacency matrix, laplacian matrix
        """
        # 提供带权重的边
        weighted_edges = [
            (1, 3, 3),
            (2, 1, 2.5),
            (3, 2, 3), (3, 4, 2.5), (3, 7, 5),
            (4, 5, 3),
            (5, 4, 3), (5, 6, 4),
            (6, 7, 2.5),
            (7, 5, 2)
        ]

        nodes = set(node for edge in weighted_edges for node in edge[:2])
        # create graph
        G = nx.DiGraph()
        # adding all nodes to graph
        G.add_nodes_from(nodes)
        # add weighted edge
        G.add_weighted_edges_from(weighted_edges)
        # get adj
        adjacency_matrix = nx.to_numpy_array(G, weight='weight')
        # cal laplacian
        # TODO: in or out degree?
        degrees = np.sum(adjacency_matrix, axis=0)
        laplacian_matrix = np.diag(degrees) - adjacency_matrix
        return adjacency_matrix, laplacian_matrix

    @staticmethod
    def generate_random_topology(num_nodes: int, avg_out_degree: float) -> (csr_matrix, csr_matrix):
        """
        Generate a random directed topology with weighted edges.
        :param num_nodes: Number of nodes in the graph
        :param avg_out_degree: Average out-degree of nodes
        :return: adjacency matrix, laplacian matrix (both in sparse format)
        """
        G = nx.DiGraph()

        # 添加所有节点
        G.add_nodes_from(range(num_nodes))

        # 添加带权重的边
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j and np.random.rand() < avg_out_degree / num_nodes:
                    weight = np.random.uniform(1.0, 5.0)  # 随机生成权重
                    G.add_edge(i, j, weight=weight)

        # sparse matrix
        adjacency_matrix = nx.to_numpy_array(G)

        # cal laplacian matrix
        degrees = np.array(adjacency_matrix.sum(axis=1)).flatten()
        laplacian_matrix = csr_matrix(np.diag(degrees) - adjacency_matrix)
        laplacian_matrix = laplacian_matrix.toarray()

        return adjacency_matrix, laplacian_matrix


if __name__ == '__main__':
    topo = Topology()
    adjacency, laplacian = topo.generate_random_topology(10, 3)
    print(adjacency)
    print(adjacency.shape)
