from classes.clause import Clause
from classes.expression import Expression
from classes.clause_difference import ClauseDifference
from itertools import permutations

import sys


# if len(sys.argv) < 2:
#     print("Usage: python3 comparator.py [filename]")
#     exit(1)

# name = sys.argv[1]
# name1 = "6clauses7variables"
name1 = "6clauses7variablesv2"
# name1 = "largecnf"
# name2 = "largecnf"
# name2 = "6clauses7variables_slightchange"
name2 = "6clauses7variables_slightchangev2"

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
    # possible_differences = []
    possible_differences = dict()

    for i, clause in enumerate(expression1.clauses):
        for j, other_clause in enumerate(expression2.clauses):
            if clause.has_partial_overlap(other_clause):
                diff = ClauseDifference(clause, other_clause)
                # ((index of first clause, index of second clause), clause_difference)
                # possible_differences.append(((i, j), diff))
                possible_differences[(i, j)] = diff
    
    # print("\nClause expressions: ")
    # {print(expr[0], expr[1]) for expr in possible_differences}

    return possible_differences


# TODO: greedy function
def greedy_difference_expression(possible_differences):
    groups = dict()
    for diff in possible_differences:
        indexes = diff[0]
        clause_difference = diff[1]


# Function to find all unique subsets of a set of pairs of integers that do not
# share overlap of their integers and are not eachothers subsets
def find_all_difference_expressions(possible_differences):
    difference_expressions = []

    # Repeat finding algorithm with each node (clause difference, a pair of 
    # integers representing the indexes of two clauses between expressions)
    # as the head node.
    for i in range(len(possible_differences)):
        result = find_sub_expressions(possible_differences[i:])

        for new_expression in result:
            # If found expressions are subsets of already found expressions, 
            # they can be discarded
            if not any([set(new_expression).issubset(set(expression)) 
                        for expression in difference_expressions]):
                difference_expressions.append(new_expression)

    return difference_expressions

  
# Recursive expression finding function to find all expressions with a given
# head appearing first in the list "possible_differences"
def find_sub_expressions(possible_differences, unavailable=set()):
    head = possible_differences[0]
    # When the final node is reached there can be no further nodes reached, so
    # throw the node immediately
    if len(possible_differences) == 1:
        return [{head}]
    tail = possible_differences[1:]

    # Clauses passed by the previous function calls, or the clauses of the
    # current head cannot be picked again in a difference expression (every 
    # clause exists only once in an expression!)
    new_unavailable = unavailable | {head[0], head[1]}
    result = []
    
    # Check for each of the remaining tuples if they can be added to the
    # current diff expression
    for i, option in enumerate(tail):
        # If match (no overlap)
        if option[0] not in new_unavailable and option[1] not in new_unavailable:
            # Recursively check for tuples further down the line to be added to
            # current difference expression
            subsets = find_sub_expressions(tail[i:], new_unavailable)

            # If any are found, add each of them to result to be passed up
            if subsets:
                for item in subsets:
                    result.append({head} | item)

    # If no matches are found, return head otherwise return all intermediate
    # difference expression results
    if not result:
        return [{head}]
    else:
        return result
            

    
remainder1, remainder2, score = remove_overlap(expression1, expression2)
print("\nStep 3, create clause differences between partially overlapping" +
      " clauses...")
possible_clause_differences = partial_overlap_compare(remainder1, remainder2)
print(list(possible_clause_differences.keys()))
# print(possible_clause_differences)



print("\nStep 4, Find all possible difference expressions...")
difference_expressions = find_all_difference_expressions(
                         list(possible_clause_differences.keys()))
[print(x) for x in difference_expressions]


print("\nStep 5, weigh difference expressions based on the weight of their" +
      " contained clause differences")
weighed_difference_expressions = []
for difference_expression in difference_expressions:
    weighed_difference_expressions.append(
        (difference_expression,
        sum([possible_clause_differences[clause_difference].score for clause_difference in difference_expression]))
    )

# Sorting to get best scoring expressions (most minimal = highest score)
weighed_difference_expressions = sorted(weighed_difference_expressions, key=lambda pair: pair[1], reverse = True)

[print(x) for x in weighed_difference_expressions]

