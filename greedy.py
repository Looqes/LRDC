# Algorithm that picks overlap pairs between clauses with a greedy method
# It iteratively checks each clause in the first expression and picks
# a highest scoring clause it matches to from the second expression
def greedy_difference_expression(possible_differences):
    # Remainder clauses from the first expression with some partial overlap
    left_clauses = {pair[0] for pair in possible_differences}

    # Set to keep track of which clauses from the second expression have been
    # picked, for clauses in an expression cannot be picked more than once
    picked_clauses = set()

    difference_expression = set()
    for clause_nr in left_clauses:
        matchings = [pair for pair in possible_differences if pair[0] == clause_nr]

        # If only a single matching with the clause from the first expression
        # exists, check if it fits and add it if it does.
        if len(matchings) == 1:
            if matchings[0][1] not in picked_clauses:
                difference_expression.add(matchings[0])
                picked_clauses.add(matchings[0][1])
        # If there are multiple options for matchings, check if they can be
        # added based on their score (highest score first)
        else:
            rated = [(matching, possible_differences[matching])
                     for matching in matchings]
            rated = sorted(rated, key = lambda x: x[1].score, reverse = True)

            for matching in rated:
                if matching[0][1] not in picked_clauses:
                    difference_expression.add(matching[0])
                    picked_clauses.add(matching[0][1])
                    # If a matching has been picked, move on to the next
                    # clause from the first expression
                    break

    return difference_expression