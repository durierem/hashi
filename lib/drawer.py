import networkx as nx
import matplotlib.pyplot as plt


class Drawer:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def addNode(self, n):
        self.nodes.append(n)

    def addEdge(self, a, b):
        temp = [a, b]
        self.edges.append(temp)

    def visualize(self):
        G = nx.Graph()
        G.add_nodes_from(self.nodes)
        G.add_edges_from(self.edges)
        nx.draw_networkx(G)
        plt.show()
