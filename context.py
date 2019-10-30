import copy

class InvalidObject:
	pass

class FunctionWrapper:
	def call(self, ctx):
		pass

class NativeFunction(FunctionWrapper):
	def call(self, ctx):
		return self.call_with_args(self, args)

class FunctionContext(FunctionWrapper):
	def __init__(self, asts):
		self.asts = asts
		self.context = {}
		self.argindex = {}

	def add_argument(self, index, name): # name is str
		self.context.update({name: InvalidObject()})
		self.argindex.update({index: name})

	def __call__(self, *args):
		from runner import Runner
		r = Runner()
		r.load_asts(self.asts)
		r.lookup = self.context
		for i, arg in enumerate(args):
			r.lookup[self.argindex[i]] = arg
		#print(r.lines)
		return r.run()