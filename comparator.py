
from classes.clause import Clause
from classes.expression import Expression
from classes.clause_difference import ClauseDifference
import random_clause_generator as rcnf
import preprocess
import greedy2
import full_search
from classes.expression import Expression
import sys

import rtfunicode



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
    rcnf.generate_random_clauses()
    expression1 = Expression().read_from_file("first_expression")
    expression2 = Expression().read_from_file("second_expression")
else:
    print("Invalid commands given")
    exit(1)


print(expression1)
print(expression2)


# Helper function that returns the sum of matching scores, based on a given set
# of matchings and a dict containing the matchings as keys with their 
# information as values
def get_diff_expr_score(possible_clause_differences, difference_expression):
    return sum([possible_clause_differences[clause_difference].score 
                for clause_difference in difference_expression])

            
# Step 1 & 2 - remove full & non-overlap (strip)
remainder1, remainder2, overlap = preprocess.remove_overlap(expression1, expression2)

print('Overlap = ', overlap)

print("\nStep 3, create clause differences between partially overlapping" +
      " clauses...")
possible_clause_differences = preprocess.partial_overlap_compare(remainder1, remainder2)
print(list(possible_clause_differences.keys()))


result = []


# Greedy
if algorithm_choice == "greedy":
    print("\nStep4, Greedy")
    result = greedy2.greedy_difference_expression(possible_clause_differences)
    print("Result: ")
    print(result)
    print("Score = ", get_diff_expr_score(possible_clause_differences, result))
# Full search
elif algorithm_choice == "full":
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
# import docx
# from docx.enum.text import WD_COLOR_INDEX

# colors = [WD_COLOR_INDEX.BLUE, WD_COLOR_INDEX.BRIGHT_GREEN, WD_COLOR_INDEX.DARK_RED, WD_COLOR_INDEX.VIOLET, WD_COLOR_INDEX.TURQUOISE]

# def getcolors(colors):
#     return (color for color in colors)

# # Create an instance of a word document
# doc = docx.Document()
  
# # Add a Title to the document 
# doc.add_heading('Expression difference', 2)
# doc.add_paragraph().add_run(str(expression1))
# doc.add_paragraph().add_run(str(expression2))
# # original_clauses_desc.add_run(str(expression1))
# # original_clauses_desc.add_run(str(expression2))

# doc.add_paragraph()
# doc.add_paragraph().add_run("Overlap between rulesets: ")
# doc.add_paragraph().add_run(str(overlap))
# doc.add_paragraph().add_run(str(overlap))

# highlight_colors = getcolors(colors)


# doc.add_paragraph()
# doc.add_paragraph().add_run("Changed rules: ")
# for matching in result:
#     print(possible_clause_differences[matching])
#     clause_difference = possible_clause_differences[matching]
#     negations = possible_clause_differences[matching].negations

#     # first_rule = str(possible_clause_differences[matching].clause)
#     # second_rule = str(possible_clause_differences[matching].target)
#     first_clause = doc.add_paragraph()
#     first_clause.add_run("(")

    
#     for overlapping_literal in clause_difference.overlap:
#         first_clause.add_run(str(overlapping_literal))
#         first_clause.add_run(" ∨ ")

#     for negation in clause_difference.negations:
#         first_clause.add_run(str(negation[0]))
#         first_clause.add_run(" ∨ ")

# # Creating paragraph with some content and Highlighting it.
# # highlight_para = doc.add_paragraph(
# #        ).add_run(
# #            str(expression1)
# #                  ).font.highlight_color = next(highlight_colors)
  
# # Now save the document to a location 
# doc.save('gfg.docx')