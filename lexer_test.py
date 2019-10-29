from lexer import Lexer
from token import Token

lexer = Lexer()
lexer.load_program('function bar() yeah end')
while True:
	tok = lexer.next_token()
	print(tok)
	if tok.token_type == Token.EOF:
		break