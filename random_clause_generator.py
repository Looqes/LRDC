import cnfgen

def generate_random_clauses(k1, n1, m1, k2, n2, m2, use_dimacs):
    # k1, n1, m1 = 5, 20, 5
    # k2, n2, m2 = 5, 20, 5

    # k = amount of literals per clause, 
    # n = amount of variables, 
    # m = amount of clauses to generate
    first_expr = cnfgen.RandomKCNF(k1, n1, m1)
    second_expr = cnfgen.RandomKCNF(k2, n2, m2)


    if use_dimacs:
        with open("cnffiles/first_expression", "w") as text_file:
            text_file.write(first_expr.to_dimacs())

        with open("cnffiles/second_expression", "w") as text_file:
            text_file.write(second_expr.to_dimacs())

    else:
        return first_expr, second_expr
