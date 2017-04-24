import random
from functools import reduce
def dice(sides_i):
	return distr({n: 1/sides_i for n in range(1,sides_i+1)})
class distr(dict):
	def __init__(self, d):
		dict.__init__(self, d)


def conditional_distr(cond, ontrue, onfalse):
	result = {k:0 for k in list(ontrue)+list(onfalse)}
	for val, prob in ontrue.items():
		result[val]+=prob*cond[1]
	for val, prob in onfalse.items():
		result[val]+=prob*cond[0]
	return distr(result)


def bool_scalar(funct, dist, scal):
	result = {0: 0, 1: 0}
	for value, prob in dist.items():
		if(funct(value,scal)):
			result[1]+=prob
		else:
			result[0]+=prob
	return distr(result)

def bool_distr(funct, dist1, dist2):
	result = {0: 0, 1: 0}
	for value1, prob1 in dist1.items():
		for value2, prob2 in dist2.items():
			if(funct(value1, value2)):
				result[1]+=prob1*prob2
			else:
				result[0]+=prob1*prob2
	return distr(result)

def roll(dice):
	r = random.random()
	dice = normalize(dice)
	for value, prob in dice.items():
		r-=prob
		if r<=0:
			return value

"""make sure that the sum of probabilities is 1"""
def normalize(dice):
	prob_sum = sum([prob for value, prob in dice.items()])
	return distr({value: prob/prob_sum for value, prob in dice.items()})


def do_oper1(funct, arg_d):
	return distr({funct(n): prob for n, prob in arg_d.items()})

def do_oper2(funct, arg1_d, arg2_d):
	dist = {funct(val1, val2): 0 for val1 in arg1_d.keys() for val2 in arg2_d.keys()}
	for val1, prob1 in arg1_d.items():
		for val2, prob2 in arg2_d.items():
			dist[funct(val1,val2)]+=prob1*prob2
	return distr(dist)

def iter_oper(funct, args_d):
	return reduce((lambda arg1_d, arg2_d: do_oper2(funct, arg1_d,arg2_d)), args_d)

def scalar_add(dist, scal):
	return do_oper1(lambda x: x+scal, dist)

def scalar_mult(dist, scal):
	return do_oper1(lambda x: x*scal, dist)

def add_distr(dist1, dist2):
	return do_oper2(lambda x, y: x+y, dist1, dist2)

def iter_add_distr(dist, scal):
	return iter_oper(lambda x,y: x+y, [dist]*scal)

def sum_distr(dlist):
	return iter_oper(lambda x,y: x+y, dlist)

