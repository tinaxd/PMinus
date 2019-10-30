import ast
from token import Token

class ParseError(Exception):
	pass

class EndOfProgramError(Exception):
	pass

class Parser:
	def __init__(self, lexer):
		self.lexer = lexer
		self.tokens = []
		self.tok_ptr = 0

	def prepare(self):
		while True:
			tok = self.lexer.next_token()
			self.tokens.append(tok)
			if tok.token_type == Token.EOF:
				break
		print('Prepared tokens')
		#for token in self.tokens:
		#	print(token)

	def parse_program(self):
		parsed = []
		while True:
			t = self.parse_statement()
			if not t:
				t = self.parse_expression()
				if not t:
					return parsed
			parsed.append(t)

	def parse_statement(self):
		assignee = self.parse_identifier()
		if not assignee:
			return None
		if not self.check_equal():
			self.tok_ptr -= 1
			return None
		exp = self.parse_expression()
		if not exp:
			print('not exp')
			return None
		return ast.ASTAssignmentST(assignee, exp)

	def parse_identifier(self):
		if self.tokens[self.tok_ptr].token_type == Token.IDENTIFIER:
			name = self.tokens[self.tok_ptr].literal
			self.tok_ptr += 1
			return name
		return None

	def check_equal(self):
		if self.tokens[self.tok_ptr].token_type == Token.ASSIGNMENT:
			self.tok_ptr += 1
			return True
		return False

	def parse_expression(self):
		#print(self.tokens[self.tok_ptr].token_type)
		if self.tokens[self.tok_ptr].token_type == Token.INTEGER:
			integer = ast.ASTInteger(int(self.tokens[self.tok_ptr].literal))
			peek = self.tokens[self.tok_ptr + 1]
			self.tok_ptr += 1
			if peek.token_type == Token.PLUS:
				self.tok_ptr += 1
				return ast.ASTPlus(integer, self.parse_expression())
			elif peek.token_type == Token.MINUS:
				self.tok_ptr += 1
				return ast.ASTMinus(integer, self.parse_expression())
			elif peek.token_type == Token.ASTERISK:
				self.tok_ptr += 1
				return ast.ASTMultiply(integer, self.parse_expression())
			elif peek.token_type == Token.SLASH:
				self.tok_ptr += 1
				return ast.ASTDivide(integer, self.parse_expression())
			else:
				return integer
		elif self.tokens[self.tok_ptr].token_type == Token.FUNCTION:
			return self.parse_function()
		elif self.tokens[self.tok_ptr].token_type == Token.IDENTIFIER:
			raw_val = self.tokens[self.tok_ptr]
			valued = ast.ASTLookupValue('variable', raw_val.literal)
			peek = self.tokens[self.tok_ptr + 1]
			self.tok_ptr += 1
			if peek.token_type == Token.LPAREN:
				args = self.parse_call_arguments()
				lookast = ast.ASTLookupValue('function', raw_val.literal)
				lookast.args = args
				peek = self.tokens[self.tok_ptr]
				if peek.token_type == Token.PLUS:
					self.tok_ptr += 1
					return ast.ASTPlus(lookast, self.parse_expression())
				elif peek.token_type == Token.MINUS:
					self.tok_ptr += 1
					return ast.ASTMinus(lookast, self.parse_expression())
				elif peek.token_type == Token.ASTERISK:
					self.tok_ptr += 1
					return ast.ASTMultiply(lookast, self.parse_expression())
				elif peek.token_type == Token.SLASH:
					self.tok_ptr += 1
					return ast.ASTDivide(lookast, self.parse_expression())
				else:
					return lookast
			elif peek.token_type == Token.PLUS:
				self.tok_ptr += 1
				return ast.ASTPlus(valued, self.parse_expression())
			elif peek.token_type == Token.MINUS:
				self.tok_ptr += 1
				return ast.ASTMinus(valued, self.parse_expression())
			elif peek.token_type == Token.ASTERISK:
				self.tok_ptr += 1
				return ast.ASTMultiply(valued, self.parse_expression())
			elif peek.token_type == Token.SLASH:
				self.tok_ptr += 1
				return ast.ASTDivide(valued, self.parse_expression())
			else:
				return valued

	def parse_function(self):
		assert(self.check_function_keyword())
		(fname, args) = self.parse_function_signature()
		elements = []
		while True:
			el = self.parse_statement()
			if not el:
				el = self.parse_expression()
			if el:
				elements.append(el)
			if self.check_blockend():
				break
		return ast.ASTFunction(args, elements)

	def check_lparen(self):
		if self.tokens[self.tok_ptr].token_type == Token.LPAREN:
			self.tok_ptr += 1
			return True
		return False

	def check_rparen(self):
		if self.tokens[self.tok_ptr].token_type == Token.RPAREN:
			self.tok_ptr += 1
			return True
		return False

	def check_comma(self):
		if self.tokens[self.tok_ptr].token_type == Token.COMMA:
			self.tok_ptr += 1
			return True
		return False

	def check_blockend(self):
		if self.tokens[self.tok_ptr].token_type == Token.BLOCKEND:
			self.tok_ptr += 1
			return True
		return False

	def parse_function_signature(self):
		fname = self.parse_identifier()
		if not fname:
			raise ParseError("expected <function name> got {}".format(self.tokens[self.tok_ptr].literal))
		arguments = self.parse_function_arguments()
		return (fname, arguments)

	def parse_function_arguments(self):
		if not self.check_lparen():
			raise ParseError("expected ( got {}".format(self.tokens[self.tok_ptr].literal))
		arguments = []
		while True:
			ident = self.parse_identifier()
			if ident:
				arguments.append(ident)
			if self.check_rparen():
				break
			if not self.check_comma():
				raise ParseError('expected , got {}'.format(self.tokens[self.tok_ptr].literal))
		return arguments

	def parse_call_arguments(self):
		if not self.check_lparen():
			raise ParseError("expected ( got {}".format(self.tokens[self.tok_ptr].literal))
		arguments = []
		while True:
			el = self.parse_expression()
			if el:
				arguments.append(el)
			if self.check_rparen():
				break
			if not self.check_comma():
				raise ParseError('expected , got {}'.format(self.tokens[self.tok_ptr].literal))
		return arguments	

	def check_function_keyword(self):
		if self.tokens[self.tok_ptr].token_type == Token.FUNCTION:
			self.tok_ptr += 1
			return True
		return False
