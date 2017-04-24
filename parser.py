from lib.pyparsing import *
integer = Word(nums)
dice_expr = infixNotation(integer, 
	[
		("d", 2, opAssoc.LEFT),
		(oneOf("* /"), 2, opAssoc.LEFT),
		(oneOf("+ -"), 2, opAssoc.LEFT),
		(Keyword("roll"), 1, opAssoc.RIGHT)
	])
expr = dice_expr