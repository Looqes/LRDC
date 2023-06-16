
# from classes.clause import Clause
from classes.expression import Expression
# from classes.clause_difference import ClauseDifference
from classes.difference_expression import DifferenceExpression
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
    usage = "python3 comparator.py [input/random/{filenames}] [greedy/full]"

    if not (len(sys.argv) >= 3 or
        # Enforce algorithm choice
        (sys.argv[-1].lower() in {"greedy", "full"} and \
        # Either random generation must be specified or two filenames must be given
        ((sys.argv[1] == "random" or sys.argv[1] == "input") and len(sys.argv) != 4))):
        print((sys.argv[1] == "random" or sys.argv[1] == "input") and len(sys.argv) != 4)
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
            print("Please specify parameters for random clause generation: ")
            # k1 = input("Amount of literals per clause in first expression: ")
            # k1 = int(k1) if k1.isdigit() else {print("Not a number!"), exit(0)}
            # n1 = input("Amount of variables to choose from in first expression: ")
            # n1 = int(n1) if n1.isdigit() else {print("Not a number!"), exit(0)}
            # m1 = input("Amount of clauses to generate for first expression: ")
            # m1 = int(m1) if m1.isdigit() else {print("Not a number!"), exit(0)}

            # k2 = input("Amount of literals per clause in first expression: ")
            # k2 = int(k2) if k2.isdigit() else {print("Not a number!"), exit(0)}
            # n2 = input("Amount of variables to choose from in first expression: ")
            # n2 = int(n2) if n2.isdigit() else {print("Not a number!"), exit(0)}
            # m2 = input("Amount of clauses to generate for first expression: ")
            # m2 = int(m2) if m2.isdigit() else {print("Not a number!"), exit(0)}
            k1, n1, m1 = 2, 10, 5
            k2, n2, m2 = 2, 10, 5

            kcnf1, kcnf2 = rcnf.generate_random_clauses(k1, n1, m1, k2, n2, m2, False)
            expression1 = Expression().read_from_kcnf(kcnf1)
            expression2 = Expression().read_from_kcnf(kcnf2)
    else:
        print("Invalid commands given")
        exit(1)

    return expression1, expression2, algorithm_choice



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
        result = greedy2.greedy_difference_expression(possible_clause_differences)
        
        if result == None:
            return None
    # Full search
    elif algorithm_choice == "full":
        difference_expressions = full_search.find_all_difference_expressions(
                                list(possible_clause_differences.keys()))

        weighed_difference_expressions = []
        for difference_expression in difference_expressions:
            weighed_difference_expressions.append(
                (difference_expression,
                get_diff_expr_score(possible_clause_differences, difference_expression))
            )

        # Sorting to get best scoring expressions (most minimal = highest score)
        weighed_difference_expressions = sorted(weighed_difference_expressions, key=lambda pair: pair[1], reverse = True)

        if weighed_difference_expressions:
            result = weighed_difference_expressions[0][0]
        else:
            return None

    # TODO: create difference expression and return it instead of loose vars
    leftout_clauses_exp1 = [index for index in range(0, len(expression1.clauses)) if index not in {match[0] for match in result}]
    leftout_clauses_exp2 = [index for index in range(0, len(expression2.clauses)) if index not in {match[1] for match in result}]

    difference_expression = DifferenceExpression(expression1,
                            expression2,
                            overlap,
                            [possible_clause_differences[match] for match in result],
                            {expression1: [expression1.clauses[leftout_clause] for leftout_clause in leftout_clauses_exp1],
                            expression2: [expression2.clauses[leftout_clause] for leftout_clause in leftout_clauses_exp2]})

    return difference_expression


    # docx_output.write_output_docx(expression1, expression2, overlap, non_overlap, result, possible_clause_differences)


if __name__ == '__main__':
    expression1, expression2, algorithm_choice = get_line_input()
    print(expression1)
    print(expression2)
    diff_exp = create_difference_expression(expression1, expression2, algorithm_choice)

    print("Partial overlap: ")
    print(diff_exp.partial_overlap)
    print("Overlap: ", diff_exp.overlap)
    print(diff_exp.similarity_score)
