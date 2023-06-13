import time
import timeit
import comparator
import random_clause_generator as rcg

from classes.expression import Expression

# Function to run experiments with the algorithms
# Takes characteristics of logical rulesets (expressions), n_runs
# defining how many times the algorithms should solve, and a filename for output
# as parameters
def experiment(k1, n1, m1, k2, n2, m2, n_runs, filename):
    # Experimentation
    with open(filename + ".txt", "w") as f:
        f.write("Result execution times:\n")

        amount_of_runs = n_runs

        full_results = []
        greedy_results = []
        for _ in range(amount_of_runs):
            kcnf1, kcnf2 = rcg.generate_random_clauses(k1, n1, m1, k2, n2, m2, False)
            expression1 = Expression().read_from_kcnf(kcnf1)
            expression2 = Expression().read_from_kcnf(kcnf2)

            # Full
            t0 = time.perf_counter()
            result, overlap, non_overlap, possible_clause_differences = comparator.create_difference_expression(expression1, expression2, "full")
            t1 = time.perf_counter()
            execution_time = t1 - t0

            if result == None:
                execution_time = None
                score = None
            else:
                score = comparator.get_diff_expr_score(possible_clause_differences, result)
            full_results.append((execution_time, result, score))
        
            # Greedy
            t0 = time.perf_counter()
            result, overlap, non_overlap, possible_clause_differences = comparator.create_difference_expression(expression1, expression2, "greedy")
            t1 = time.perf_counter()
            execution_time = t1 - t0

            if result == None:
                execution_time = None
                score = None
            else:
                score = comparator.get_diff_expr_score(possible_clause_differences, result)
            greedy_results.append((execution_time, result, score))
        
        # [f.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + "\n") for line in full_results]
        [f.write(str(line[0]) + " " + str(line[2]) + "\n") for line in full_results]
        f.write("\n")
        # [f.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + "\n") for line in greedy_results]
        [f.write(str(line[0]) + " " + str(line[2]) + "\n") for line in greedy_results]


# k = amount of literals per clause, 
# n = amount of variables, 
# m = amount of clauses to generate

n_runs = 100
k1, n1, m1 = 2, 20, 5
k2, n2, m2 = 2, 20, 5

for k in [2, 3, 4, 5, 8, 12, 20]:
    experiment(k, n1, m1, k, n2, m2, n_runs, "output_files/execution_timesk" + str(k))