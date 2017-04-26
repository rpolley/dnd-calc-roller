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
value_expr = dice_expr^variable
variable_definition = variable + "=" + value_expr
expr = dice_expr ^ variable_definition