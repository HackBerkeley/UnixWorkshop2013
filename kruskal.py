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

