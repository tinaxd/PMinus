class Token:
	FUNCTION = 0
	LPAREN = 1
	RPAREN = 2
	IDENTIFIER = 3
	BLOCKEND = 4
	INTEGER = 5
	STRING = 6
	EOF = 7

	IDENTIFIER_LOOKUP = {
		'end': BLOCKEND,
		'function': FUNCTION,
	}

	def __init__(self, token_type, literal):
		self.token_type = token_type
		self.literal = literal

	def __str__(self):
		return "token type: {} literal: {}".format(self.token_type, self.literal)