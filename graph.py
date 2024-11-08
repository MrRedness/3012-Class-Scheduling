class Graph:

    def __init__(self):
        self.adjLst = dict()
        self.nodeSet = set()

    def add_node(self, node):
        self.adjLst[node] = {}
        self.nodeSet.add(node)

    def add_edge(self, n1, n2):
        if n1 not in self.adjLst:
            raise Exception("Please add node, " + n1 + ", first before adding edges to it!")
        if n2 not in self.adjLst:
            raise Exception("Please add node, " + n2 + ", first before adding edges to it!")

        self.adjLst[n1][n2] = True
        self.adjLst[n2][n1] = True