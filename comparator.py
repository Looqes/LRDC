from classes.clause import Clause
from classes.expression import Expression
from classes.clause_difference import ClauseDifference
import sys


# if len(sys.argv) < 2:
#     print("Usage: python3 comparator.py [filename]")
#     exit(1)

# name = sys.argv[1]
name1 = "6clauses7variables"
# name1 = "largecnf"
# name2 = "largecnf"
name2 = "6clauses7variables_slightchange"

# name1 = "clausematchtest1"
# name2 = "clausematchtest2"



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
    print("********************")
    print("Step 1, remove full overlapping clauses...")

    remainder1, remainder2 = expression1 ^ expression2
    print(remainder1)
    print(remainder2)
    print()


    # size_of_biggest_expression = max(expression1.amount_of_literals, 
    #                                  expression2.amount_of_literals)

    # overlap = (size_of_biggest_expression - remainder1.amount_of_literals) / size_of_biggest_expression
    overlap = 0

    print("Step 2, remove non-overlapping clauses...")
    remainder1 = remainder1.partial_overlap(remainder2)
    remainder2 = remainder2.partial_overlap(remainder1)
    print(remainder1)
    print(remainder2)


    return remainder1, remainder2, overlap


def partial_overlap_compare(expression1, expression2):
    possible_differences = []

    for clause in expression1.clauses:
        for i, other_clause in enumerate(expression2.clauses):
            if clause.has_partial_overlap(other_clause):
                # TODO: Create clause difference summary
                diff = ClauseDifference(clause, other_clause)
                possible_differences.append(diff)
    
    print("different expressions found: ")
    {print(expr) for expr in possible_differences}

    



remainder1, remainder2, score = remove_overlap(expression1, expression2)

print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
partial_overlap_compare(remainder1, remainder2)




# print("Remainders")
# print(remainder1)
# print(remainder2)

# print(score)