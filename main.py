from distributions import *
import parser
import fileinput

for line in fileinput.input()
	parsed_cmd = parser.expr.parseString(line)
	print(evaluate(parsed_cmd))

def evaluate(cmd):
	if len(cmd)==1:
		return cmd[0]
	elif type(cmd)==str:
		return int(cmd)
	elif type(cmd)==int:
		return cmd
	elif len(cmd)==3
		cmd[0] = evaluate(cmd[0])
		cmd[2] = evaluate(cmd[2])
		if cmd[1] == 'd':
			return typed_call(lambda n, m: n*[dice(m)], cmd[0], cmd[2])
		elif cmd[1] == "*":
			return typed_call(lambda n, m: n*m, cmd[0], cmd[2])
		elif cmd[1] == "/":
			return typed_call(lambda n, m: n/m, cmd[0], cmd[2])
		elif cmd[1] == "+":
			return typed_call(lambda n, m: n+m, cmd[0], cmd[2])
		elif cmd[1] == "-":
			return typed_call(lambda n, m: n-m, cmd[0], cmd[2])
		

def typed_call(funct, arg1, arg2):
	#first sum any lists
	if type(arg1)==list:
		arg1 = sum_distr(arg1)
	if type(arg2)==list:
		arg2 = sum_distr(arg2)

	#then guess the type and apply the correct function
	if type(arg1)==int&&type(arg2)==int:
		return funct(arg1,arg2)
	elif type(arg1)==distr&&type(arg2)==int:
		return do_oper1(lambda num: funct(num, arg2), arg1)
	elif type(arg1)==int&&type(arg2)==distr:
		return do_oper1(lambda num: funct(num, arg2), arg1)
	elif type(arg1)==distr&&type(arg2)==distr:
		return do_oper2(funct, arg1, arg2)