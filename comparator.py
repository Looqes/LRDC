import cnfgen

from classes.clause import Clause
from classes.expression import Expression
from classes.clause_difference import ClauseDifference
import preprocess
import greedy
import full_search

import sys

k1 = input("Amount of literals per clause in first expression: ")
k1 = int(k1) if k1.isdigit() else {print("Not a number!"), exit(0)}
n1 = input("Amount of variables to choose from in first expression: ")
n1 = int(n1) if n1.isdigit() else {print("Not a number!"), exit(0)}
m1 = input("Amount of clauses to generate for first expression: ")
m1 = int(m1) if m1.isdigit() else {print("Not a number!"), exit(0)}

k2 = input("Amount of literals per clause in first expression: ")
k2 = int(k2) if k2.isdigit() else {print("Not a number!"), exit(0)}
n2 = input("Amount of variables to choose from in first expression: ")
n2 = int(n2) if n2.isdigit() else {print("Not a number!"), exit(0)}
m2 = input("Amount of clauses to generate for first expression: ")
m2 = int(m2) if m2.isdigit() else {print("Not a number!"), exit(0)}


# Handle command line input
usage = "python3 comparator.py [greedy/full]"
if len(sys.argv) < 2 or \
   sys.argv[1].lower() not in {"greedy", "full"}:
    print("Usage: ", usage)
    exit(1)



# k = amount of literals per clause, 
# n = amount of variables, 
# m = amount of clauses to generate
first_expr = cnfgen.RandomKCNF(k1, n1, m1).to_dimacs()
with open("cnffiles/test", "w") as text_file:
    text_file.write(first_expr)

second_expr = cnfgen.RandomKCNF(k2, n2, m2).to_dimacs()
with open("cnffiles/test2", "w") as text_file:
    text_file.write(second_expr)




# name = sys.argv[1]
# name1 = "6clauses7variables"
# name1 = "6clauses7variablesv2"
# name1 = "largecnf"
# name2 = "largecnf"
# name2 = "6clauses7variables_slightchange"
# name2 = "6clauses7variables_slightchangev2"

# name1 = "clausematchtest1"
# name2 = "clausematchtest2"


name1 = "test"
name2 = "test2"


expression1 = Expression().read_from_file(name1)
expression2 = Expression().read_from_file(name2)

print(expression1)
print(expression2)


# Helper function that returns the sum of matching scores, based on a given set
# of matchings and a dict containing the matchings as keys with their 
# information as values
def get_diff_expr_score(possible_clause_differences, difference_expression):
    return sum([possible_clause_differences[clause_difference].score 
                for clause_difference in difference_expression])

            
# Step 1 & 2 - remove full & non-overlap (strip)
remainder1, remainder2, score = preprocess.remove_overlap(expression1, expression2)

print("\nStep 3, create clause differences between partially overlapping" +
      " clauses...")
possible_clause_differences = preprocess.partial_overlap_compare(remainder1, remainder2)
print(list(possible_clause_differences.keys()))


selection = sys.argv[1]
print(selection)


result = []

# Greedy
if selection == "greedy":
    print("\nStep4, Greedy")
    result = greedy.greedy_difference_expression(possible_clause_differences)
    print("Result: ")
    print(result)
    print("Score = ", get_diff_expr_score(possible_clause_differences, result))
# Full search
elif selection == "full":
    print("\nStep 4, Full search, Find all possible difference expressions...")
    difference_expressions = full_search.find_all_difference_expressions(
                            list(possible_clause_differences.keys()))
    [print(x, " Score = ", get_diff_expr_score(possible_clause_differences, x)) for x in difference_expressions]


    print("\nStep 4.5, weigh difference expressions based on the weight of their" +
        " contained clause differences")
    weighed_difference_expressions = []
    for difference_expression in difference_expressions:
        weighed_difference_expressions.append(
            (difference_expression,
            get_diff_expr_score(possible_clause_differences, difference_expression))
        )

    # Sorting to get best scoring expressions (most minimal = highest score)
    weighed_difference_expressions = sorted(weighed_difference_expressions, key=lambda pair: pair[1], reverse = True)
    # [print(x) for x in weighed_difference_expressions]
    result = weighed_difference_expressions[0][0]
    print("Result: ")
    print(result)
    print("Score = ", weighed_difference_expressions[0][1])




# TODO: Result feedback (show what changed and how similar the rulesets are)
# TODO: Handle clauses that did not get matched (these should be treated as additions/deletions)
if result:
    pass