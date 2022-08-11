import sys

class TreeNode:

    def __init__(self, point, r: float, isSol: bool):

        self.point = point
        self.reward = r
        self.visitOnce = False
        self.visitTwice = False
        self.isSolution = isSol #core node
        self.score = 0 #temporary score
        self.edges = list()

    def add_edge(self, edge):
        self.edges.append(edge)

    #get node on the other end of the edge
    def get_other_node(self,edge):
        if self == edge.one: return edge.other
        return edge.one

    def get_unvisited_neigbor_count(self):
        count = 0
        for e in self.edges:
            if not self.get_other_node(e).visitOnce:
                count += 1
        return count

    def get_edge_cost(self,otherNode):
        for e in self.edges:
            if e.get_other_node == otherNode:
                return e.cost

        return None

    def set_score(self):
        score = self.reward

        for e in self.edges:

            temp_node = self.get_other_node(e)
            if not temp_node.visitOnce:
                continue
            score += max(0, temp_node.score+e.cost)

        self.score = score

    def update_score(self):

        for e in self.edges:

            temp_node = self.get_other_node(e)
            if not temp_node.visitTwice:
                continue

            self.score += max(0, temp_node.score+e.cost)


class TreeEdge:

    def __init__(self,c: float, one: TreeNode, other: TreeNode):
        self.one = one
        self.other = other
        self.cost = c

    def get_other_node(self, node: TreeNode):
        if node == self.one: return self.other
        return self.one


class Tree:

    def __init__(self, graph, reward_list:list, cost_list:list):

        self.nodes = list()
        self.root = None

        for i in range(len(graph.points)):
            self.nodes.append(TreeNode(graph.points[i],reward_list[i], reward_list[i]==sys.maxsize))

        for i in range(len(graph.edgeIndex)):
            firstIndex = graph.edgeIndex[i][0]
            secondIndex = graph.edgeIndex[i][1]
            edge = TreeEdge(cost_list[i],self.nodes[firstIndex], self.nodes[secondIndex])
            self.nodes[firstIndex].add_edge(edge)
            self.nodes[secondIndex].add_edge(edge)

    def get_leaves(self):
        leaves_list = list()
        for node in self.nodes:

            if node.visitOnce:
                pass

            if node.get_unvisited_neigbor_count() < 2:
                leaves_list.append(node)

        return leaves_list

