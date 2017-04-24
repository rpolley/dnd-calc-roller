from lib.pyparsing import *
integer = Word(nums)
variable = Word(srange("[A-Z]"))#variable names must be all caps
dice_func = infixNotation(integer | variable, 
	[
		("d", 2, opAssoc.LEFT),
		(oneOf("* /"), 2, opAssoc.LEFT),
		(oneOf("+ -"), 2, opAssoc.LEFT),
	])