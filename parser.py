from lib.pyparsing import *
integer = Word(nums)
variable = Word(alphas,alphanums+"_")
value_expr = Forward()
dice_expr = Forward()
if_expr= Forward()
arithmatic_expr = infixNotation(Or([dice_expr,variable,integer,if_expr]), 
	[
		(oneOf("* /"), 2, opAssoc.LEFT),
		(oneOf("+ -"), 2, opAssoc.LEFT),
		(oneOf("> >= == <= <"), 2, opAssoc.LEFT),
		(Keyword("roll"), 1, opAssoc.RIGHT),
	])
dice_expr << infixNotation(integer,
	[
		("d", 1, opAssoc.RIGHT),
		("d", 2, opAssoc.LEFT),
	])
if_expr << Group(Keyword("if")+value_expr+Keyword("then")+value_expr+Optional(Keyword("else")+value_expr))
value_expr << Or([dice_expr,variable,integer,if_expr,arithmatic_expr])
variable_definition = variable + "=" + value_expr
comment = Suppress("#"+SkipTo(LineEnd()))
expr = value_expr ^ variable_definition ^ comment
