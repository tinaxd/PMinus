from lexer import Lexer
from token import Token
from parser import Parser

lexer = Lexer()
lexer.load_program('''
i = 5
fn1 = function fn1(x)
	x - 1
end

mul2 = function mul2(x)
	fn1(x) * 2 + 10 / 3
end

print(mul2(i))

''')

parser = Parser(lexer)
parser.prepare()
lines = parser.parse_program()
for line in lines:
	print(line)