from token import Token

class Lexer:
	def __init__(self):
		self.program = ""
		self.prog_len = 0
		self.pointer = 0
		self.next_ptr = 0
		self.currchar = ''

	def load_program(self, program):
		self.program = program
		self.prog_len = len(program)
		self.read_char()

	def next_token(self):
		self.skip_whitespaces()
		char = self.currchar
		if char is None:
			return Token(Token.EOF, '(EOF)')
		if char == '=':
			if self.peak_char() == '=':
				token = Token(Token.EQUALITY, '==')
				self.read_char()
			else:
				token = Token(Token.ASSIGNMENT, '=')
		elif char == '(':
			token = Token(Token.LPAREN, '(')
		elif char == ')':
			token = Token(Token.RPAREN, ')')
		elif char == ',':
			token = Token(Token.COMMA, ',')
		elif char == '+':
			token = Token(Token.PLUS, '+')
		elif char == '-':
			token = Token(Token.MINUS, '-')
		elif char == '*':
			token = Token(Token.ASTERISK, '*')
		elif char == '/':
			token = Token(Token.SLASH, '/')
		else:
			ident = self.read_identifier()
			if ident in Token.IDENTIFIER_LOOKUP:
				token = Token(Token.IDENTIFIER_LOOKUP[ident], ident)
			else:
				if ident.isdigit():
					token = Token(Token.INTEGER, int(ident))
				else:
					token = Token(Token.IDENTIFIER, ident)
		self.read_char()
		return token

	def peak_char(self):
		return self.program[self.next_ptr]

	def read_char(self):
		if self.next_ptr >= self.prog_len:
			self.currchar = None
			return
		self.currchar = self.program[self.next_ptr]
		self.pointer = self.next_ptr
		self.next_ptr += 1

	def read_identifier(self):
		start_ptr = self.pointer
		self.pointer += 1
		while self.pointer < self.prog_len and self.program[self.pointer].isalnum():
			self.pointer += 1
		self.next_ptr = self.pointer
		return self.program[start_ptr:self.pointer]

	def skip_whitespaces(self):
		while self.currchar is not None and self.currchar.isspace():
			self.read_char()
