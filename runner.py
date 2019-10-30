import ast

class Runner:
	def __init__(self):
		lookup = {  # Initialize the lookup table with primitive functions
			'variable': {

			},

			'function': {
				'print': print
			}
		}
		self.lines = []

	def load_program(self, lines):
		self.lines = lines

	def run(self):
		for line in self.lines:
			self.run_line(line)

	def run_line(self, line):
		if isinstance(line, ast.ASTAssignment):
			self.lookup.variable.update(line.lhs, line.rhs.value())
		
