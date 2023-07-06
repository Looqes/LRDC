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
    print("\n", str(m1), " clauses....")

    i = 1

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
            diff_exp = comparator.create_difference_expression(expression1, expression2, "full")
            t1 = time.perf_counter()
            execution_time = t1 - t0

            if diff_exp == None:
                execution_time = None
                score = None
            else:
                score = diff_exp.similarity_score
            full_results.append((execution_time, score))
            # f.write(str(execution_time) + " " + str(score) + "\n")
        
            # Greedy
            t0 = time.perf_counter()
            diff_exp = comparator.create_difference_expression(expression1, expression2, "greedy")
            t1 = time.perf_counter()
            execution_time = t1 - t0

            if diff_exp == None:
                execution_time = None
                score = None
            else:
                score = diff_exp.similarity_score
            greedy_results.append((execution_time, score))
        
            print(i)
            # f.write(str(execution_time) + " " + str(score) + "\n")
            i += 1

        [f.write(str(line[0]) + " " + str(line[1]) + "\n") for line in full_results]
        f.write("\n")
        [f.write(str(line[0]) + " " + str(line[1]) + "\n") for line in greedy_results]



# Function to experiment with the greedy algorithm only
# performance of full algorithm is bad enough where it bottlenecks the tests
# for the greedy algorithm
def experiment_greedy(k1, n1, m1, k2, n2, m2, n_runs, filename):
    # Experimentation
    with open(filename + ".txt", "w") as f:
        f.write("Result execution times:\n")

        amount_of_runs = n_runs
        print(m1, " clauses...")

        for _ in range(amount_of_runs):
            kcnf1, kcnf2 = rcg.generate_random_clauses(k1, n1, m1, k2, n2, m2, False)
            expression1 = Expression().read_from_kcnf(kcnf1)
            expression2 = Expression().read_from_kcnf(kcnf2)

        
            # Greedy
            t0 = time.perf_counter()
            diff_exp = comparator.create_difference_expression(expression1, expression2, "greedy")
            t1 = time.perf_counter()
            execution_time = t1 - t0

            if diff_exp == None:
                execution_time = None
                score = None
            else:
                score = diff_exp.similarity_score
            f.write(str(execution_time) + " " + str(score) + "\n")
        

        # f.write("\n")
        # [f.write(str(line[0]) + " " + str(line[1]) + " " + str(line[2]) + "\n") for line in greedy_results]
        # [f.write(str(line[0]) + " " + str(line[2]) + "\n") for line in greedy_results]




# k = amount of literals per clause, 
# n = amount of variables, 
# m = amount of clauses to generate


# # single basic configuration 100 runs
#######################
# n_runs = 100
# k1, n1, m1 = 3, 20, 5
# k2, n2, m2 = 3, 20, 5

# experiment(k1, n1, m1, k2, n2, m2, 100, "output_files/basic")


# single basic configuration 100 runs for quick fullvsgreedy overview
#######################
# n_runs = 100
# k1, n1, m1 = 3, 20, 8
# k2, n2, m2 = 3, 20, 8

# experiment(k1, n1, m1, k2, n2, m2, n_runs, "output_files/fullvsgreedy")  


# Runs for full vs greedy comparison (will take a long time) & amount of clauses generated m
#######################
# n_runs = 100
# amount_of_clauses = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# amount_of_clauses = [11, 12]
# k = 3

# for m in amount_of_clauses:
#     n = k * m
    # experiment(k, n, m, k, n, m, n_runs, "output_files/fullvsgreedy" + str(m) + "clauses")


# Varying the amount of literals k per rule
#######################
# n_runs = 100
# k_values =  [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# m = 6

# for k in k_values:
#     n = k * m
#     experiment(k, n, m, k, n, m, n_runs, "output_files/experimentk" + str(k))


# Varying the amount variables to pick from as literals n
#######################
# n_runs = 100
# k =  5
# m = 6
# n_values = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

# for n in n_values:
#     experiment(k, n, m, k, n, m, n_runs, "output_files/experimentn" + str(n))



n_runs = 100
k = 5
m_values = list(range(25, 1001, 25))


print(m_values)

for m in m_values:
    n = k * m
    experiment_greedy(k, n, m, k, n, m, n_runs, "output_files/greedytests/greedy" + str(m) + "clauses")



