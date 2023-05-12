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

print(expression1)
print(expression2)


# first identify overlap & obtain the parts of the expressions that do *not* overlap
# overlap = size of biggest expression / amount of literals in common clauses
def remove_overlap(expression1, expression2):
    print("********************")
    print("Step 1, remove full overlapping clauses...")

    remainder1, remainder2 = expression1 ^ expression2
    print(remainder1)
    print(remainder2)
    print()

    # TODO
    # overlap = (size_of_biggest_expression - remainder1.amount_of_literals) / size_of_biggest_expression
    overlap = 0

    print("Step 2, remove non-overlapping clauses...")
    remainder1 = remainder1.partial_overlap(remainder2)
    remainder2 = remainder2.partial_overlap(remainder1)
    print(remainder1)
    print(remainder2)

    return remainder1, remainder2, overlap


# Function that compares partially overlapping clauses and creates
# clause_difference objects containing information about the difference
# between pairs of partially overlapping clauses.
def partial_overlap_compare(expression1, expression2):
    possible_differences = []

    for clause in expression1.clauses:
        for i, other_clause in enumerate(expression2.clauses):
            if clause.has_partial_overlap(other_clause):
                diff = ClauseDifference(clause, other_clause)
                possible_differences.append(diff)
    
    print("\nClause expressions: ")
    {print(expr) for expr in possible_differences}

    
remainder1, remainder2, score = remove_overlap(expression1, expression2)
print("\nStep 3, create clause differences between partially overlapping clauses...")
partial_overlap_compare(remainder1, remainder2)

