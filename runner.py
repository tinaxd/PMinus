import ast
import context as ctx


class Runner:
	def __init__(self):
		self.lookup = {  # Initialize the lookup table with primitive functions
			'print': print
		}
		self.lines = []
		self.last_value = None

	def load_asts(self, lines):
		self.lines = lines

	def run(self):
		for line in self.lines:
			self.run_line(line)
		return self.last_value

	def run_line(self, line):
		if isinstance(line, ast.ASTAssignmentST):
			line.rhs.lookup = self.lookup
			self.lookup.update({line.lhs: line.rhs.value()})
			#print('Lookup updated')
			#print(self.lookup)
		elif isinstance(line, ast.ASTExpression):
			line.lookup = self.lookup
			self.last_value = line.value()


