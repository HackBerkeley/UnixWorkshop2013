#!/usr/bin/python

class Tree:
    def __init__(self, root, children):
        self.root = root
        self.children = children

    def addChild(self, child):
        self.children.append(child)

    def vertices(self):
        yield self.root
        for sub in self.children:
            yield from sub.vertices()

    def display(self, lvl = 0):
        print('-' * lvl + '>', self.root)
        for sub in self.children:
            sub.display(lvl + 1)

class VertexSet:
    def __init__(self, vtxs):
        self.forest = {
            vtx : set() for vtx in vtxs
        }
        self.metric = lambda vtx: len(self.forest[vtx])
    
    def addEdge(self, edge):
        u, v = edge
        self.forest[u].add(v)
        self.forest[v].add(u)

    def buildTree(self):
        root = max(self.forest.keys(), key = self.metric)
        return self.expandVertices(root, set(root))

    def expandVertices(self, root, visited):
        toExpand = sorted(self.forest[root].difference(visited), key = self.metric)
        visited.update(toExpand)
        return Tree(root, [self.expandVertices(vtx, visited) for vtx in toExpand])

    def display(self):
        for vtx, connections in self.forest.items():
            print("{0} => {1}".format(vtx, connections))

class ConnectedGraph:
    def __init__(self, weights):
        self.weights = weights
        self.vertices = set()
        for edge in weights.keys():
            self.vertices.update(edge)

    def minimumSpanningTree(self):
        cost = 0
        mergeSet = VertexSet(self.vertices)
        for edge in sorted(self.weights.keys(), key=lambda uv: self.weights[uv]):
            cost += self.weights[edge]
            mergeSet.addEdge(edge)
            soln = mergeSet.buildTree()
            if self.spannedBy(soln):
                return soln, cost

    def spannedBy(self, tree):
        vtxs = set(tree.vertices())
        return vtxs.issubset(self.vertices) and vtxs.issuperset(self.vertices)

    def displaySpan(self):
        mst, cost = self.minimumSpanningTree()
        print("Minimum Spanning Tree (Cost = {0})".format(cost))
        mst.display()

if __name__ == '__main__':
    g = ConnectedGraph({
        ('a', 'b'): 1,
        ('b', 'c'): 3,
        ('a', 'c'): 0,
    })
    g.displaySpan()

    g = ConnectedGraph({
        ('a', 'b'): -1,
        ('a', 'c'): 8,
        ('a', 'd'): 4,
        ('b', 'c'): 7,
        ('b', 'd'): 3,
        ('c', 'd'): 0
    })
    g.displaySpan()

    import random
    import string
    for j in range(50):
        d = {}
        for i in range(100):
            c1 = random.choice(string.ascii_letters)
            c2 = random.choice(string.ascii_letters)
            if c1 != c2:
                d[(c1, c2)] = random.randint(0, 100)
        g = ConnectedGraph(d)
        try:
            g.displaySpan()
        except:
            print("There's a bug!")
