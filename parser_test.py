from lexer import Lexer
from token import Token
from parser import Parser

lexer = Lexer()
lexer.load_program('a = 3 5 b = function bar(x) x+2 end print(b(5))')

parser = Parser(lexer)
parser.prepare()
lines = parser.parse_program()
for line in lines:
	print(line)