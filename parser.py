from lib.pyparsing import *
integer = Word(nums)
variable = Word(alphanums+"_")
value_expr = Forward()
dice_expr = infixNotation(integer | variable, 
	[
		("d", 1, opAssoc.RIGHT),
		("d", 2, opAssoc.LEFT),
		(oneOf("* /"), 2, opAssoc.LEFT),
		(oneOf("+ -"), 2, opAssoc.LEFT),
		(Keyword("roll"), 1, opAssoc.RIGHT)
	])
value_expr = (dice_expr^variable)^("("+value_expr+")")
variable_definition = variable + "=" + value_expr
expr = value_expr ^ variable_definition