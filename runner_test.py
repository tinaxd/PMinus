from lexer import Lexer
from token import Token
from parser import Parser
from runner import Runner

lexer = Lexer()
lexer.load_program('''
i = 5
fn1 = function fn1(x)
	x - 1
end

fn2 = function fn2(x)
	y = x + 3
	y - 4
end

mul2 = function mul2(x)
	fn1(x) * 2 + 10 / 3
end

print(mul2(i))
print(888888888888888888)
print(1 + 2 + 3 + 4)
print(fn1(1 + 2 + 3 + 4))
print(fn2(1 + 2 + 3 + 4))

''')

parser = Parser(lexer)
parser.prepare()
lines = parser.parse_program()
for line in lines:
	print(line)

print()
print('------- RUNNING PROGRAM -------')
print()

runner = Runner()
runner.load_asts(lines)
runner.run()

print()