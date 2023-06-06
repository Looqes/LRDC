

class ClauseDifference():
    # Class to represent difference between two clauses.
    # Contains the two clauses and the weight of the operations required to
    # change clause into target.
    # Weight is determined by params of weight of the individual transformation
    # operations.
    def __init__(self, clause, target):
        self.clause = clause
        self.target = target
        # print("Creating clause difference for following clauses: ")
        # print(clause, target, "...")
        (self.overlap,
        self.negations,
        self.deletions,
        self.additions) = clause.difference(target)

        # Weight, currently hardcoded values
        # More similar clauses get a higher score
        self.score = \
              2 * len(self.overlap) \
            + len(self.negations) \
            + 0.25 * (len(self.deletions) + len(self.additions))

    
    def __repr__(self):
        return "Results for clause difference between " + str(self.clause) +    \
            " & " + str(self.target) + ":\n" \
            + "    Overlap:   " + str(self.overlap)   + "\n" \
            + "    Negations: " + str(self.negations) + "\n" \
            + "    Deletions: " + str(self.deletions) + "\n" \
            + "    Additions: " + str(self.additions) + "\n" \
            + "------------------- WEIGHT : " + str(self.score) + "\n"
                


        

    
