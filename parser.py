from lib.pyparsing import *
integer = Word(nums)
variable = Word(alphas,alphanums+"_")
value_expr = Forward()
dice_expr = Forward()
arithmatic_expr = infixNotation(Or([integer,variable,dice_expr]), 
	[
		(oneOf("* /"), 2, opAssoc.LEFT),
		(oneOf("+ -"), 2, opAssoc.LEFT),
		(Keyword("roll"), 1, opAssoc.RIGHT),
	])
dice_expr << infixNotation(integer,
	[
		("d", 1, opAssoc.RIGHT),
		("d", 2, opAssoc.LEFT),
	])
value_expr << Or([arithmatic_expr,dice_expr,variable])
variable_definition = variable + "=" + value_expr
expr = value_expr ^ variable_definition
