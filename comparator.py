from classes.clause import Clause
from classes.expression import Expression
import sys


# if len(sys.argv) < 2:
#     print("Usage: python3 comparator.py [filename]")
#     exit(1)

# name = sys.argv[1]
name1 = "6clauses7variables"
name2 = "6clauses7variables_slightchange"


expression1 = Expression(name1)
expression2 = Expression(name2)

result = expression1 ^ expression2

print(result)

# print(expression)