class ASTExpression:
	def value(self):
		raise Error("Subclass responsibility")

class ASTStatement:
	pass

class ASTInteger(ASTExpression):
	def __init__(self, value):
		self.val = value

	def value(self):
		return self.val

	def __str__(self):
		return "Integer {}".format(self.val)

class ASTPlus(ASTExpression):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def value(self):
		return self.left.value() + self.right.value()

class ASTMinus(ASTExpression):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def value(self):
		return self.left.value() - self.right.value()

class ASTMultiply(ASTExpression):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def value(self):
		return self.left.value() * self.right.value()

class ASTDivide(ASTExpression):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def value(self):
		return self.left.value() / self.right.value()

class ASTLookupValue(ASTExpression):
	def __init__(self, type, name):
		self.type = type
		self.name = name
		self.lookup = None
		self.args = None

	def value(self):
		return self.lookup[self.type][self.name]

	def __str__(self):
		if self.type == 'function':
			return "Lookup {} name: {} with args {}".format(self.type, self.name, self.args)	
		return "Lookup {} name: {}".format(self.type, self.name)

class ASTFunction(ASTStatement):
	def __init__(self, args, sentences):
		self.args = args
		self.sentences = sentences

	def __str__(self):
		return "Function with {} arguments: {}".format(len(self.args), self.sentences)

class ASTAssignmentST(ASTStatement):
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs

	def __str__(self):
		return "Assignment {} = {}".format(self.lhs, self.rhs)

