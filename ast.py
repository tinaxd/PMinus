import context as ctx
import copy


class ASTExpression:
	def __init__(self):
		self.lookup = None

	def value(self):
		raise Error("Subclass responsibility")

class ASTStatement:
	pass

class ASTInteger(ASTExpression):
	def __init__(self, value):
		super().__init__()
		self.val = value

	def value(self):
		return self.val

	def __str__(self):
		return "Integer {}".format(self.val)

class ASTPlus(ASTExpression):
	def __init__(self, left, right):
		super().__init__()
		self.left = left
		self.right = right

	def value(self):
		self.left.lookup = self.lookup
		self.right.lookup = self.lookup
		return self.left.value() + self.right.value()

class ASTMinus(ASTExpression):
	def __init__(self, left, right):
		super().__init__()
		self.left = left
		self.right = right

	def value(self):
		self.left.lookup = self.lookup
		self.right.lookup = self.lookup
		return self.left.value() - self.right.value()

class ASTMultiply(ASTExpression):
	def __init__(self, left, right):
		super().__init__()
		self.left = left
		self.right = right

	def value(self):
		self.left.lookup = self.lookup
		self.right.lookup = self.lookup
		return self.left.value() * self.right.value()

class ASTDivide(ASTExpression):
	def __init__(self, left, right):
		super().__init__()
		self.left = left
		self.right = right

	def value(self):
		self.left.lookup = self.lookup
		self.right.lookup = self.lookup
		return self.left.value() / self.right.value()

class ASTLookupValue(ASTExpression):
	def __init__(self, type, name):
		self.type = type
		self.name = name
		self.lookup = None
		self.args = None

	def value(self):
		if self.type == 'variable':
			return self.lookup[self.name]
		elif self.type == 'function':
			def deep_value(exp):
				exp.lookup = self.lookup
				return exp.value()

			evaluated = [deep_value(arg) for arg in self.args]
			return self.lookup[self.name](*evaluated)

	def __str__(self):
		if self.type == 'function':
			return "Lookup {} name: {} with args {}".format(self.type, self.name, self.args)	
		return "Lookup {} name: {}".format(self.type, self.name)

class ASTFunction(ASTExpression):
	def __init__(self, args, sentences):
		super().__init__()
		self.args = args
		self.sentences = sentences

	def __str__(self):
		return "Function with {} arguments: {}".format(len(self.args), self.sentences)

	def value(self):
		fc = ctx.FunctionContext(self.sentences)
		fc.context = copy.copy(self.lookup)
		for i, arg in enumerate(self.args):
			fc.add_argument(i, arg)
		return fc 

class ASTAssignmentST(ASTStatement):
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs

	def __str__(self):
		return "Assignment {} = {}".format(self.lhs, self.rhs)

