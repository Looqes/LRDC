from classes.clause import Clause
from classes.expression import Expression
import sys


# if len(sys.argv) < 2:
#     print("Usage: python3 comparator.py [filename]")
#     exit(1)

# name = sys.argv[1]
# name1 = "6clauses7variables"
# name1 = "largecnf"
# name2 = "largecnf"
# name2 = "6clauses7variables_slightchange"

name1 = "clausematchtest1"
name2 = "clausematchtest2"



expression1 = Expression().read_from_file(name1)
expression2 = Expression().read_from_file(name2)

# old_unique, new_unique = expression1 ^ expression2

print(expression1)
print(expression2)
# print("\nClauses that are no longer in the second set: \n", old_unique)
# print("\nNew clauses in the second set: \n", new_unique)

# print(expression)


# first identify overlap & obtain the parts of the expressions that do *not* overlap
# overlap = size of biggest expression / amount of literals in common clauses
def remove_overlap(expression1, expression2):
    remainder1, remainder2 = expression1 ^ expression2

    size_of_biggest_expression = max(expression1.amount_of_literals, 
                                     expression2.amount_of_literals)

    # print(size_of_biggest_expression, remainder1.amount_of_literals)
    overlap = (size_of_biggest_expression - remainder1.amount_of_literals) / size_of_biggest_expression

    remainder1.partial_overlap(remainder2)

    return remainder1, remainder2, overlap

remainder1, remainder2, score = remove_overlap(expression1, expression2)

print("Remainders")
print(remainder1)
print(remainder2)

print(score)