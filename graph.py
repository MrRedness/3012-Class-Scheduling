import matplotlib.pyplot as plt
import networkx as nx
from ordered_set import OrderedSet

class Graph:

    def __init__(self):
        self.adjLst = dict()
        self.nodeSet = OrderedSet([])

    def add_node(self, node):
        if node not in self.nodeSet:
            self.adjLst[node] = {}
            self.nodeSet.add(node)

    def add_edge(self, n1, n2):
        if n1 not in self.adjLst:
            self.add_node(n1)
        if n2 not in self.adjLst:
            self.add_node(n2)

        self.adjLst[n1][n2] = True
        self.adjLst[n2][n1] = True

    def remove_edge(self, n1, n2):
        if n1 not in self.adjLst:
            self.add_node(n1)
        if n2 not in self.adjLst:
            self.add_node(n2)

        self.adjLst[n1][n2] = False
        self.adjLst[n2][n1] = False

    def get_neighbors(self, node):
        return [k for k in self.adjLst[node].keys() if self.adjLst[node][k]]
    
    @staticmethod
    def visualize(graph, coloring):
        G = nx.Graph()
        for node in graph.nodeSet:
            G.add_node(node)
        for node, neighbors in graph.adjLst.items():
            for neighbor, connected in neighbors.items():
                if connected:
                    G.add_edge(node, neighbor)

        node_colors = [coloring.get(node, 'lightgrey') for node in G.nodes()]

        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(G, seed=42)

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000, edgecolors='black')
        nx.draw_networkx_edges(G, pos, edge_color='black', width=1.5)
        nx.draw_networkx_labels(G, pos, font_size=12, font_color='black', font_weight='bold')

        plt.axis('off')
        plt.show()