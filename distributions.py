import random
from functools import reduce
def dice(sides_i):
	return distr({n: 1/sides_i for n in range(1,sides_i+1)})

"""convert a value into a dice that always rolls that value"""
def unit(scalar):
	return distr({scalar: 1})

class distr(dict):
	def __init__(self, d):
		dict.__init__(self, d)

def to_distr(item):
	if type(item)==list:
		return sum_distr(item)
	elif item==None:
		return unit(0)
	elif type(item)!=distr:
		return unit(item)
	else:
		return item

def conditional_distr(cond, ontrue, onfalse):
	cond = to_distr(cond)
	ontrue = to_distr(ontrue)
	onfalse = to_distr(onfalse)
	result = {k:0 for k in list(ontrue)+list(onfalse)}
	for val, prob in ontrue.items():
		result[val]+=prob*cond[True]
	for val, prob in onfalse.items():
		result[val]+=prob*cond[False]
	return distr(result)


def roll(dice):
	r = random.random()
	dice = to_distr(dice)
	dice = normalize(dice)
	for value, prob in dice.items():
		r-=prob
		if r<=0:
			return value

"""make sure that the sum of probabilities is 1"""
def normalize(dice):
	prob_sum = sum([prob for value, prob in dice.items()])
	return distr({value: prob/prob_sum for value, prob in dice.items()})


def matrix(arg1_d, arg2_d):
	return {(value1,value2): prob1*prob2 for value1, prob1 in arg1_d.items() for value2, prob2 in arg2_d.items()}

def do_oper(funct, *args_d):
	args_d = list(args_d)
	if len(args_d)==1:
		return do_oper1(funct, args_d[0])
	reduced = reduce(matrix, args_d)
	dist = {funct(*vals): 0 for vals in reduced.keys()}
	for vals, prob in reduced.items():
		dist[funct(*vals)] += prob
	return distr(dist)

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

