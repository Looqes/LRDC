
from classes.clause import Clause
from classes.expression import Expression
from classes.clause_difference import ClauseDifference
import preprocess
import greedy2
import full_search
import docx_output

import random_clause_generator as rcnf
import sys


def get_line_input():
    # Setting to enable writing used expressions to file
    use_dimacs = False

    # Handle command line input
    usage = "python3 comparator.py [random/{filenames}] [greedy/full]"

    if (len(sys.argv) < 3 or
        # Enforce algorithm choice
        sys.argv[-1].lower() not in {"greedy", "full"} or \
        # Either random generation must be specified or two filenames must be given
        (sys.argv[1] != "random" and len(sys.argv) != 4)):
        print(len(sys.argv))
        print("Usage: ", usage)
        exit(1)


    algorithm_choice = sys.argv[-1]


    # File input
    if len(sys.argv) == 4:
        first_file, second_file = sys.argv[1:3]
        print(first_file, second_file)
        try:
            expression1 = Expression().read_from_file(first_file)
            expression2 = Expression().read_from_file(second_file)
        except OSError:
            print("Files could not be opened correctly...")
            print("Are you sure you gave the correct filenames?")
            exit(1)
    # Random cnf clause generation
    elif sys.argv[1] == "random":
        if use_dimacs == True:
            # expressions are writtten to first_expression and second_expression in cnffiles
            rcnf.generate_random_clauses(True)
            expression1 = Expression().read_from_file("first_expression")
            expression2 = Expression().read_from_file("second_expression")
        else:
            kcnf1, kcnf2 = rcnf.generate_random_clauses(False)
            expression1 = Expression().read_from_kcnf(kcnf1)
            expression2 = Expression().read_from_kcnf(kcnf2)
    else:
        print("Invalid commands given")
        exit(1)

    return expression1, expression2, algorithm_choice


# print(expression1)
# print(expression2)


# Helper function that returns the sum of matching scores, based on a given set
# of matchings and a dict containing the matchings as keys with their 
# information as values
def get_diff_expr_score(possible_clause_differences, difference_expression):
    return sum([possible_clause_differences[clause_difference].score 
                for clause_difference in difference_expression])


# Main function that creates the desired difference expression
def create_difference_expression(expression1, expression2, algorithm_choice):
    # Step 1 & 2 - remove full & non-overlap (strip)
    remainder1, remainder2, overlap, non_overlap = preprocess.remove_overlap(expression1, expression2)

    # print('Overlap = ', overlap)
    # print('Non-overlap = ', non_overlap)

    # print("\nStep 3, create clause differences between partially overlapping" +
    #     " clauses...")
    possible_clause_differences = preprocess.partial_overlap_compare(remainder1, remainder2)
    # print(list(possible_clause_differences.keys()))

    result = []


    # Greedy
    if algorithm_choice == "greedy":
        # print("\nStep4, Greedy")
        result = greedy2.greedy_difference_expression(possible_clause_differences)
        # print("Result: ")
        # print(result)
        # print("Score = ", get_diff_expr_score(possible_clause_differences, result))

        # print(result)
        # print("\n&&&")
        # print(sorted(list(result), key = lambda q: q[0]))

        # print(get_diff_expr_score(possible_clause_differences, result))

    # Full search
    elif algorithm_choice == "full":
        # print("\nStep 4, Full search, Find all possible difference expressions...")
        difference_expressions = full_search.find_all_difference_expressions(
                                list(possible_clause_differences.keys()))
        # [print(x, " Score = ", get_diff_expr_score(possible_clause_differences, x)) for x in difference_expressions]
        # [print(sorted(list(x), key = lambda q : q[0]), get_diff_expr_score(possible_clause_differences, x)) for x in difference_expressions]


        # print("\nStep 4.5, weigh difference expressions based on the weight of their" +
        #     " contained clause differences")
        weighed_difference_expressions = []
        for difference_expression in difference_expressions:
            weighed_difference_expressions.append(
                (difference_expression,
                get_diff_expr_score(possible_clause_differences, difference_expression))
            )

        # Sorting to get best scoring expressions (most minimal = highest score)
        weighed_difference_expressions = sorted(weighed_difference_expressions, key=lambda pair: pair[1], reverse = True)
        # [print(x) for x in weighed_difference_expressions[0:3]]
        # print("#####")

        if weighed_difference_expressions:
            result = weighed_difference_expressions[0][0]
        else:
            return None, None, None, None
        # print("Result: ")
        # print(result)
        # print("Score = ", weighed_difference_expressions[0][1])

    return result, overlap, non_overlap, possible_clause_differences





    # # TODO: Result feedback (show what changed and how similar the rulesets are)
    # # TODO: Handle clauses that did not get matched (these should be treated as additions/deletions)
    # docx_output.write_output_docx(expression1, expression2, overlap, non_overlap, result, possible_clause_differences)


# Comment below code in case of not running from commandline
# expression1, expression2, algorithm_choice = get_line_input()
