from classes.clause_difference import ClauseDifference

# first identify & put aside the fully and non-overlapping the parts of the 
# input expression
# overlap = size of biggest expression / amount of literals in common clauses
def remove_overlap(expression1, expression2):
    remainder1, remainder2, overlap = expression1 ^ expression2

    result1 = remainder1.partial_overlap(remainder2)
    result2 = remainder2.partial_overlap(remainder1)

    non_overlap = (remainder1 - result1,
                   remainder2 - result2)

    return result1, result2, overlap, non_overlap


# Function that compares partially overlapping clauses and creates
# clause_difference objects containing information about the difference
# between pairs of partially overlapping clauses.
# Returns a dict containing a pair of indexes representing the index of each
# Clause in the list of remaining clauses of each expression, with a
# clause_difference object as a value
def partial_overlap_compare(expression1, expression2):
    possible_differences = dict()

    for i, clause in enumerate(expression1.clauses):
        for j, other_clause in enumerate(expression2.clauses):
            if clause.has_partial_overlap(other_clause):
                diff = ClauseDifference(clause, other_clause)
                # ((index of first clause, index of second clause), clause_difference)
                possible_differences[(i, j)] = diff

    return possible_differences