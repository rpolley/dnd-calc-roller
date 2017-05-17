from distributions import *
add = lambda x, y: x+y
gt = lambda x, y: x>y
def tuple_subtract(t1,t2):
	return tuple((t1[i]-t2[i] for i in range(0,len(t1))))
class Combatant():
	def __init__(self,max_hp,to_hit,ac,damage,initiative,attacks=1):
		self.max_hp = max_hp
		self.current_hp = max_hp
		self.to_hit = to_hit
		self.ac = ac
		self.damage = damage
		self.attacks = attacks
		self.initiative = initiative

	def initialize_fight(self, other):
		class Fight():
			"""docstring for Fight"""
			def __init__(self, first, second):
				first.damage_calc = sum_distr([conditional_distr(do_oper(gt,do_oper(add,dice(20),first.to_hit),second.ac),first.damage,0)]*first.attacks)
				second.damage_calc = sum_distr([conditional_distr(do_oper(gt,do_oper(add,dice(20),second.to_hit),first.ac),second.damage,0)]*second.attacks)
				self.results = {"win":0,"lose":0}
				self.hp_pairs = unit((first.current_hp,second.current_hp))
				self.first = first
				self.second = second
			def update_results(self):
				lose_prob = 0
				win_prob = 0
				for val, prob in self.hp_pairs.items():
					if val[0]<=0:
						lose_prob+=prob
						self.hp_pairs[val]=0
					if val[1]<=0:
						win_prob+=prob
						self.hp_pairs[val]=0
				self.hp_pairs = distr({value: prob for value, prob in self.hp_pairs.items() if prob>0})
				self.results["win"]+=win_prob
				self.results["lose"]+=lose_prob

			
			def do_round(self):
				if(self.first.initiative>self.second.initiative):
					self.hp_pairs = do_oper(tuple_subtract, self.hp_pairs, distr({(0,val):prob for val, prob in self.first.damage_calc.items()}))
					self.update_results()
					self.hp_pairs = do_oper(tuple_subtract, self.hp_pairs, distr({(val,0):prob for val, prob in self.second.damage_calc.items()}))
					self.update_results()
				else:
					self.hp_pairs = do_oper(tuple_subtract, self.hp_pairs, distr({(val,0):prob for val, prob in self.second.damage_calc.items()}))
					self.update_results()
					self.hp_pairs = do_oper(tuple_subtract, self.hp_pairs, distr({(0,val):prob for val, prob in self.first.damage_calc.items()}))
					self.update_results()
		return Fight(self,other)

me = Combatant(17,5,19,do_oper(lambda x,y: x+y,dice(8),3),10)
lvl1 = Combatant(12,5,18,do_oper(lambda x,y: x+y,dice(8),3),12)
f = me.initialize_fight(lvl1)