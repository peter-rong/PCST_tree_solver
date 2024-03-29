import tree

from collections import deque

class Algorithm:

	def __init__(self, current_tree: tree.Tree):
		self.tree = current_tree

	def execute(self):

			for node in self.tree.nodes:
				node.score = node.reward
				node.visitOnce = False
				node.visitTwice = False
				node.solutionChecked = False

			stack = deque() #the order of tracing back
			leaves = self.tree.get_leaves()

			#first level of leaves
			for leaf in leaves:
				stack.append(leaf)
				leaf.visitOnce = True

			leaves = self.tree.get_leaves()
			temp_leaf_count = 0

			#forward
			while len(leaves) != 0:

				temp_leaf_count = len(leaves)
				for leaf in leaves:
					stack.append(leaf)
					leaf.set_score()

				for leaf in leaves:
					leaf.visitOnce = True

				leaves = self.tree.get_leaves()
			'''
			for node in self.tree.nodes:
				print(str(node.point) + ' ' + str(node.score))
			'''
			# trace back

			if temp_leaf_count > 2:
				print('Error in algorithm, more than 2 ending point')

			if temp_leaf_count == 1:
				temp = stack.pop()
				temp.visitTwice = True

			if temp_leaf_count == 2:
				temp1 = stack.pop()
				temp2 = stack.pop()
				boost_to_temp1 = max(0,temp2.score+temp1.get_edge_cost(temp2))
				boost_to_temp2 = max(0,temp1.score+temp2.get_edge_cost(temp1))

				temp1.score += boost_to_temp1
				temp2.score += boost_to_temp2

				temp1.visitTwice = True
				temp2.visitTwice = True

			while len(stack) > 0:
				temp = stack.pop()
				temp.visitTwice = True
				temp.update_score()

			root = self.get_solution_node()

			self.get_solution_tree(root)

			return self.tree


	def get_solution_node(self):

		max_node = self.tree.nodes[0]

		for node in self.tree.nodes:
			#print(str(node.point) + ' ' + str(node.score))
			if node.score > max_node.score:
				max_node = node

		return max_node

	def get_solution_tree(self,root):

		queue = deque()
		queue.append(root)
		root.solutionChecked = True

		total_score = 0
		sol_list = []

		while len(queue) > 0:
			curr = queue.popleft()
			total_score += curr.reward

			sol_list.append(curr.point)
			curr.inSol = True

			for e in curr.edges:
				neighbor = curr.get_other_node(e)
				if not neighbor.solutionChecked:
					if neighbor.score == root.score:
						total_score += e.cost
						queue.append(neighbor)
					neighbor.solutionChecked = True

		print(sol_list)
		print("Total score is "+ str(total_score))

		for e in self.tree.edges:
			print("Edge score between "+ str(e.one.point)+ " and "
				  + str(e.other.point)+" is "+ str(e.one_to_other_score))
			print("Edge score between "+ str(e.other.point)+ " and "
				  + str(e.one.point)+" is "+ str(e.other_to_one_score))

		'''

		queue = deque()
		solution_tree = tree.Tree(list(),list(),list(),list())
		queue.append(root)
		solution_tree.add_node(root)
		root.solutionChecked = True

		while len(queue) > 0:

			curr = queue.popleft()

			for e in curr.edges:
				neighbor = curr.get_other_node(e)
				if not neighbor.solutionChecked:
					if neighbor.score == root.score:
						queue.append(neighbor)
						solution_tree.add_node(neighbor)
						solution_tree.add_edge(e)

					neighbor.solutionChecked = True
		print('here')

		return solution_tree
		
		'''