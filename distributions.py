import random
from functools import reduce
def dice(sides_i):
	return {n: 1/sides_i for n in range(1,sides_i+1)}


def roll(dice):
	r = random.random()
	for value, prob in dice.items():
		r-=prob
		if r<=0:
			return value

def do_oper1(funct, arg_d):
	return {funct(n): prob for n, prob in arg_d.items()}

def do_oper2(funct, arg1_d, arg2_d):
	distr = {funct(val1, val2): 0 for val1 in arg1_d.keys() for val2 in arg2_d.keys()}
	for val1, prob1 in arg1_d.items():
		for val2, prob2 in arg2_d.items():
			distr[funct(val1,val2)]+=prob1*prob2
	return distr

def iter_oper(funct, args_d):
	return reduce((lambda arg1_d, arg2_d: do_oper2(funct, arg1_d,arg2_d)), args_d)

def scalar_add(distr, scal):
	return do_oper1(lambda x: x+scal, distr)

def scalar_mult(distr, scal):
	return do_oper1(lambda x: x*scal, distr)

def add(distr1, distr2):
	return do_oper2(lambda x, y: x+y, distr1, distr2)

def iter_add(distr, scal):
	return iter_oper(lambda x,y: x+y, [distr]*scal)