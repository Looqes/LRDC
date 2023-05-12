

class ClauseDifference():
    # Class to represent difference between two clauses.
    # Contains the two clauses and the weight of the operations required to
    # change clause into target.
    # Weight is determined by params of weight of the individual transformation
    # operations.

    def __init__(self, clause, target):
        self.clause = clause
        self.target = target
        print("\nCreating difference for clauses: ")
        print(clause, target, "...\n")
        (self.overlap,
        self.negations,
        self.mutations,
        self.deletions,
        self.additions) = clause.difference(target)

        self.score = \
            len(self.overlap) \
            - 0.5 * len(self.negations) \
            - 3 * len(self.mutations) \
            - 5 * (len(self.deletions) + len(self.additions))
        # self.edit_operations, self.weight = difference(clause, target)

    
    def __repr__(self):
        return "Results for diff expression between " + str(self.clause) +    \
            " & " + str(self.target) + ":\n" \
            + "    Overlap:   " + str(self.overlap)   + "\n" \
            + "    Negations: " + str(self.negations) + "\n" \
            + "    Mutations: " + str(self.mutations) + "\n" \
            + "    Deletions: " + str(self.deletions) + "\n" \
            + "    Additions: " + str(self.additions) + "\n" \
            + "------------------- WEIGHT : " + str(self.score) + "\n"
                


        

    
