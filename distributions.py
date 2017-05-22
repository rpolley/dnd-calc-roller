import random
from functools import reduce

def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):

            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

@memoize
def dice(sides_i):
	return distr({n: 1/sides_i for n in range(1,sides_i+1)})


"""convert a value into a dice that always rolls that value"""
@memoize
def unit(scalar):
	return distr({scalar: 1})

class distr(dict):
	uid = 1
	def __init__(self, d):
		self.uid = distr.uid<<16+random.randint(0,1<<15)
		distr.uid+=1
		dict.__init__(self, d)

	def __hash__(self):
		return hash(self.uid)

	def __missing__(self, key):
		self[key]=0
		return 0

def to_distr(item):
	if type(item)==list or type(item)==tuple:
		return sum_distr(item)
	elif item==None:
		return unit(0)
	elif type(item)!=distr:
		return unit(item)
	else:
		return item

@memoize
def enforce_boolean(bool_dist):
	if not True in bool_dist.keys() or not False in bool_dist.keys():
		if(True in bool_dist.keys()):
			return distr({True: bool_dist[True], False: 1-bool_dist[True]})
		elif(False in bool_dist.keys()):
			return distr({False: bool_dist[False], True: 1-bool_dist[False]})
	elif True in bool_dist.keys() and False in bool_dist.keys():
		return bool_dist
	return enforce_boolean(unit(True))

def conditional_distr(cond, ontrue, onfalse):
	cond = enforce_boolean(to_distr(cond))
	ontrue = to_distr(ontrue)
	onfalse = to_distr(onfalse)
	result = distr({})
	for val, prob in ontrue.items():
		result[val]+=prob*cond[True]
	for val, prob in onfalse.items():
		result[val]+=prob*cond[False]
	return result

def do_cond_oper(dist, cond, oper):
	result = []
	for value, prob in dist.items():
		if cond(value):
			result+=oper(dist({value: prob}))
		else:
			result+=dist({value: prob})
	return fold(result)

def fold(distrl):
	result = {}
	for dist in distrl:
		for value,prob in dist.items():
			dist[value]+=prob

def roll(dice):
	r = random.random()
	dice = to_distr(dice)
	dice = normalize(dice)
	for value, prob in dice.items():
		r-=prob
		if r<=0:
			return value

def average(dice):
	dice = normalize(dice)
	weighted_sum = 0
	for value, prob in dice.items():
		weighted_sum+=value*prob
	return weighted_sum

"""make sure that the sum of probabilities is 1"""
@memoize
def normalize(dice):
	prob_sum = sum([prob for value, prob in dice.items()])
	return distr({value: prob/prob_sum for value, prob in dice.items()})


@memoize
def matrix(arg1_d, arg2_d):
	return {(value1,value2): prob1*prob2 for value1, prob1 in arg1_d.items() for value2, prob2 in arg2_d.items()}

def do_oper(funct, *args_d):
	args_d = list(to_distr(arg) for arg in args_d)

	if len(args_d)==1:
		return do_oper1(funct, args_d[0])
	if len(args_d)==2:
		return do_oper2(funct,args_d[0],args_d[1])
	reduced = reduce(matrix, args_d)
	dist = {funct(*vals): 0 for vals in reduced.keys()}
	for vals, prob in reduced.items():
		dist[funct(*vals)] += prob
	return distr(dist)

def do_oper1(funct, arg_d):
	return distr({funct(n): prob for n, prob in arg_d.items()})

def do_oper2(funct, arg1_d, arg2_d):
	dist = distr({})
	for val1, prob1 in arg1_d.items():
		for val2, prob2 in arg2_d.items():
			dist[funct(val1,val2)]+=prob1*prob2
	return dist

def iter_oper(funct, args_d):
	return reduce((lambda arg1_d, arg2_d: do_oper2(funct, arg1_d,arg2_d)), args_d)

def add_distr(dist1, dist2):
	return do_oper2(lambda x, y: x+y, dist1, dist2)



def sum_distr(dlist):
	if len(dlist)==1:
		return dlist[0]
	return iter_oper(lambda x,y: x+y, dlist)
