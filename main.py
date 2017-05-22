from distributions import *
import parser
import fileinput
import code
import atexit
import os
import readline
import sys

__log__ = False
__show_tree__ = False

eval_cache = {}

def cache(cmd, result):
	tcmd = tuple(list(cmd))
	if not tcmd in eval_cache.keys():
		eval_cache[tcmd] = result
	return result


def evaluate(cmd):
	if(__log__): 
		print(cmd)
	if type(cmd)==tuple:
		cmd = list(cmd)
	
	if type(cmd)==str and str.isnumeric(cmd):
		return int(cmd)
	elif type(cmd)==str and cmd in variables.keys():
		return variables[cmd]
	elif type(cmd)==str:
		return cmd
	elif type(cmd)==int:
		return cmd
	elif type(cmd)==distr:
		return cmd
	elif tuple(list(cmd)) in eval_cache.keys():
		if(__log__):
			print("cache hit")
		return eval_cache[tuple(list(cmd))]
	elif len(cmd)==1:
		return evaluate(cmd[0])
	elif len(cmd)==2:
		cmd[1] = evaluate(cmd[1])
		if cmd[0]=="roll":				
			return roll(cmd[1])
		elif cmd[0]=="d":
			return typed_call(lambda n, m: n*(dice(m),), 1, cmd[1])
	elif len(cmd)==3:
		if cmd[1] == "=":
			variables[cmd[0]]=evaluate(cmd[2])
		cmd[0] = evaluate(cmd[0])
		cmd[2] = evaluate(cmd[2])
		if cmd[1] == 'd':
			return cmd[0]*(dice(cmd[2]),)
		elif cmd[1] == "*":
			return cache(cmd,typed_call(lambda n, m: n*m, cmd[0], cmd[2]))
		elif cmd[1] == "/":
			return cache(cmd,typed_call(lambda n, m: n/m, cmd[0], cmd[2]))
		elif cmd[1] == "+":
			return cache(cmd,typed_call(lambda n, m: n+m, cmd[0], cmd[2]))
		elif cmd[1] == "-":
			return cache(cmd,typed_call(lambda n, m: n-m, cmd[0], cmd[2]))
		elif cmd[1] == ">":
			return cache(cmd,typed_call(lambda n, m: n>m, cmd[0], cmd[2]))
		elif cmd[1] == ">=":
			return cache(cmd,typed_call(lambda n, m: n>=m, cmd[0], cmd[2]))
		elif cmd[1] == "==":
			return cache(cmd,typed_call(lambda n, m: n==m, cmd[0], cmd[2]))
		elif cmd[1] == "<=":
			return cache(cmd,typed_call(lambda n, m: n<=m, cmd[0], cmd[2]))
		elif cmd[1] == "<":
			return cache(cmd,typed_call(lambda n, m: n>m, cmd[0], cmd[2]))
	elif len(cmd)>=4 and cmd[0]=="if":
		cmd[1] = cache(cmd,evaluate(cmd[1]))
		cmd[3] = cache(cmd,evaluate(cmd[3]))
		if cmd[2]=="then" and len(cmd)==4:
			return conditional_distr(cmd[1], cmd[3], 0)
		elif len(cmd)==6 and cmd[4]=="else":
			cmd[5] = evaluate(cmd[5])
			return conditional_distr(cmd[1], cmd[3], cmd[5])
	else:
		return cmd
		

def typed_call(funct, *args):
	args = [to_distr(arg) for arg in args]

	return do_oper(funct, *args)



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
		if(__show_tree__): print(code.dump())
		print(evaluate(code))
	def runsource(self, source, filename='<input>', symbol='single'):
		code = parser.expr.parseString(source)
		self.runcode(code)

def runfile(name):
	for line in fileinput.input(name):
		code = parser.expr.parseString(line)
		evaluate(code)

if __name__ == "__main__":
	runfile(".defaults")

	if len(sys.argv)>1:
		runfile(sys.argv[1])
		sys.exit(0)


	prompt = DicePrompt()

	while True:
		prompt.interact("D&D dice prompt")