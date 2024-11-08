class Graph:

    def __init__(self):
        self.adjLst = dict()
        self.nodeSet = set()

    def add_node(self, node):
        self.adjLst[node] = {}
        self.nodeSet.add(node)

    def add_edge(self, n1, n2):
        if n1 not in self.adjLst:
            self.add_node(n1)
        if n2 not in self.adjLst:
            self.add_node(n2)

        self.adjLst[n1][n2] = True
        self.adjLst[n2][n1] = True

    def get_neighbors(self, node):
        return [k for k in self.adjLst[node].keys() if self.adjLst[node][k]]