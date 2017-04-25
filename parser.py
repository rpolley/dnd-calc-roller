from lib.pyparsing import *
integer = Word(nums)
variable = Word(srange("[A-Z]")+nums)
dice_expr = infixNotation(integer | variable, 
	[
		("d", 1, opAssoc.RIGHT),
		("d", 2, opAssoc.LEFT),
		(oneOf("* /"), 2, opAssoc.LEFT),
		(oneOf("+ -"), 2, opAssoc.LEFT),
		(Keyword("roll"), 1, opAssoc.RIGHT)
	])
variable_definition = variable + "=" + (dice_expr|variable)
expr = dice_expr ^ variable_definition