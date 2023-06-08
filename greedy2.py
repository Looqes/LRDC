# Algorithm that picks overlap pairs between clauses with a greedy method
# It iteratively checks each clause in the first expression and picks
# a highest scoring clause it matches to from the second expression
def greedy_difference_expression(possible_differences):
    weight_sorted_list = sorted([(dictkey, possible_differences[dictkey]) 
                                 for dictkey in possible_differences.keys()], 
                                 key = lambda x : x[1].score, reverse = True)
    # print(weight_sorted_list[0:5])
    # print("############")
  

    # Set to keep track of which clauses from the second expression have been
    # picked, for clauses in an expression cannot be picked more than once
    used_in_first = set()
    used_in_second = set()

    difference_expression = set()
    for matching in weight_sorted_list:
        indexes = matching[0]

        if indexes[0] not in used_in_first and indexes[1] not in used_in_second:
            difference_expression.add(indexes)
            used_in_first.add(indexes[0])
            used_in_second.add(indexes[1])

    return difference_expression