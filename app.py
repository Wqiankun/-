import networkx as nx
import numpy as np

G = nx.DiGraph()  # 创建图
gaosiT = np.random.normal(loc=500, scale=1, size=4)
gaosiS = np.random.normal(loc=500, scale=1, size=4)


def topology():
    # 图形对象能够添加节点(t=处理量,s=传输量)
    G.add_node(0, t=0, s=0)
    G.add_node(1, t=abs(gaosiT[0]), s=abs(gaosiS[0]))
    G.add_node(2, t=abs(gaosiT[1]), s=abs(gaosiS[1]))
    G.add_node(3, t=abs(gaosiT[2]), s=abs(gaosiS[2]))
    G.add_node(4, t=abs(gaosiT[3]), s=abs(gaosiS[3]))
    G.add_node(5, t=0, s=0)
    # 添加一个边数组
    G.add_edges_from(
        [(1, 0), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3), (5, 4)])
    # 添加边的权值
    G.add_weighted_edges_from(
        [(1, 0, 0), (2, 1, 0), (3, 1, 0), (3, 2, 0), (4, 2, 0), (4, 3, 0), (5, 4, 0)])
    return G
