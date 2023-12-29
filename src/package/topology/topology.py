import math
import src.package.h.config as h
import networkx as nx
import numpy as np


class Topology(object):
    """
    Topology class
    """
    def __init__(self):
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
        # 创建有向图
        G = nx.DiGraph()
        # 添加所有节点
        G.add_nodes_from(nodes)
        # 添加带权重的边
        G.add_weighted_edges_from(weighted_edges)
        # 获取带权重的邻接矩阵
        adjacency_matrix = nx.to_numpy_array(G, weight='weight')
        # 计算带权重的拉普拉斯矩阵
        # TODO: 这里计算入度还是出度
        degrees = np.sum(adjacency_matrix, axis=0)
        laplacian_matrix = np.diag(degrees) - adjacency_matrix
        return adjacency_matrix, laplacian_matrix


if __name__ == '__main__':
    topo = Topology()
    adjacency, laplacian = topo.generate_sample_topology()
    print(adjacency)
