from lexer import Lexer
from token import Token

lexer = Lexer()
lexer.load_program('a = 3 b = function bar() 3 + 2 * 10 end print(a())')
while True:
	tok = lexer.next_token()
	print(tok)
	if tok.token_type == Token.EOF:
		break