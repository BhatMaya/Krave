#dunder/magic methods - have two underscores on either side (__init__)

class Tree: 

	def __init__(self, name, branches, leaf_color): 
		self.name = name
		self.branches = branches
		self.leaf_color = leaf_color

	#how it would print out the instance of the Class
	def __repr__(self):

		return f'Name: {self.name}, Branches: {self.branches}, Leaf Color: {self.leaf_color}'

	def __add__(self, x): 

		return self.leaf_color + x.leaf_color





t = Tree('Oak', 10, 'Green')
tr = Tree('Birch', 20, 'Orange')

print(t)

print(t + tr)
