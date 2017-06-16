from collections import namedtuple
class Effect(): 
	"""
	check_trigger:
	this should be overrided to check if the effect can be triggered
	do_effect:
	this should be overrided produce a new state with the effect activated
	"""

	def __init__(self, check_trigger,do_effect):
		self.check_trigger = check_trigger
		self.do_effect = do_effect

State = namedtuple("State", [
		"initiative",	#current initiative count
		"phase",		#what phase of the turn it is
 		"chars"			#the current characters involved
	])
Faction = namedtuple("Faction",[
		"name",
		"enemies"
	])
Character = namedtuple("Character",[
		"faction",
		"position",
		"health",
		"effects"
	])
Position = namedtuple("Position",[
		"x",
		"y"
	])