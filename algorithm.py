import tree

from collections import deque

class Algorithm:

	def __init__(self, graph, reward_list:list, cost_list:list):
		self.tree = tree.Tree(graph, reward_list, cost_list)

	def execute(self):

		stack = deque() #the order of tracing back
		leaves = self.tree.get_leaves()

		#first level of leaves
		for leaf in leaves:
			stack.append(leaf)
			leaf.visitOnce = True
			leaf.score = leaf.reward

		leaves = self.tree.get_leaves()
		temp_leaf_count = 0

		#forward
		while len(leaves) != 0:
			temp_leaf_count = len(leaves)
			for leaf in leaves:
				stack.append(leaf)
				leaf.visitOnce = True
				leaf.set_score()

			leaves = self.tree.get_leaves()

		# trace back

		if temp_leaf_count > 2:
			print('Error in algorithm, more than 2 ending point')

		if temp_leaf_count == 1:
			temp = stack.pop()
			temp.visitedTwice = True

		if temp_leaf_count == 2:
			temp1 = stack.pop()
			temp2 = stack.pop()

			boost_to_temp1 = max(0,temp2.score+temp1.get_edge_cost(temp2))
			boost_to_temp2 = max(0,temp1.score+temp2.get_edge_cost(temp1))

			temp1.score += boost_to_temp1
			temp2.score += boost_to_temp2
			temp1.visitedTwice = True
			temp2.visitedTwice = True

		while len(stack) > 0:
			temp = stack.pop()
			temp.visitedTwice = True
			temp.update_score()

		root = self.get_solution_node

		self.get_solution_tree(root)

	def get_solution_node(self):

		max_node = self.tree.nodes[0]

		for node in self.tree.nodes:
			if node.score > max_node.score:
				max_node = node

		return max_node

	def get_solution_tree(self,root):

		return