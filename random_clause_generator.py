import cnfgen

def generate_random_clauses(k1, n1, m1, k2, n2, m2, use_dimacs):
    # print("Please specify parameters for random clause generation: ")
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
