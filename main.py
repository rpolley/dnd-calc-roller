from distributions import *
import parser
import fileinput
import code
import atexit
import os
import readline
import sys

__log__ = False


def evaluate(cmd):
	if(__log__): 
		print(cmd)
	if type(cmd)==str and str.isnumeric(cmd):
		return int(cmd)
	elif type(cmd)==str and cmd in variables.keys():
		return variables[cmd]
	elif type(cmd)==str:
		return cmd
	elif type(cmd)==int:
		return cmd
	elif len(cmd)==1:
		return evaluate(cmd[0])
	elif len(cmd)==2:
		cmd[1] = evaluate(cmd[1])
		if cmd[0]=="roll":				
			return roll(cmd[1])
		elif cmd[0]=="d":
			return typed_call(lambda n, m: n*[dice(m)], 1, cmd[1])
	elif len(cmd)==3:
		if cmd[1] == "=":
			variables[cmd[0]]=evaluate(cmd[2])
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
		
	else:
		return cmd
		

def typed_call(funct, arg1, arg2):
	#first sum any lists
	if type(arg1)==list:
		arg1 = sum_distr(arg1)
	if type(arg2)==list:
		arg2 = sum_distr(arg2)

	#then guess the type and apply the correct function
	if type(arg1)==int and type(arg2)==int:
		return funct(arg1,arg2)
	elif type(arg1)==distr and type(arg2)==int:
		return do_oper1(lambda num: funct(num, arg2), arg1)
	elif type(arg1)==int and type(arg2)==distr:
		return do_oper1(lambda num: funct(num, arg2), arg1)
	elif type(arg1)==distr and type(arg2)==distr:
		return do_oper2(funct, arg1, arg2)



variables = {}

class DicePrompt(code.InteractiveConsole):
	def __init__(self, locals=None, filename="<console>",
		histfile=os.path.expanduser("~/.console-history")):
		code.InteractiveConsole.__init__(self, locals, filename)
		self.init_history(histfile)

	def init_history(self, histfile):
		readline.parse_and_bind("tab: complete")
		if hasattr(readline, "read_history_file"):
			try:
				readline.read_history_file(histfile)
			except FileNotFoundError:
				pass
			atexit.register(self.save_history, histfile)

	def save_history(self, histfile):
		readline.set_history_length(1000)
		readline.write_history_file(histfile)
	def runcode(self, code):
		print(evaluate(code))
	def runsource(self, source, filename='<input>', symbol='single'):
		code = parser.expr.parseString(source)
		self.runcode(code)

def runfile(name):
	for line in fileinput.input(name):
		code = parser.expr.parseString(line)
		evaluate(code)

runfile(".defaults")

if len(sys.argv)>1:
	runfile(sys.argv[1])
	sys.exit(0)


prompt = DicePrompt()

while True:
	prompt.interact("dice>")