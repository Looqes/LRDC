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