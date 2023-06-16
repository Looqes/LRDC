

# Class to represent an expression of difference between two CNF
# logical rulesets
class DifferenceExpression():
    def __init__(self,
                 expression1,
                 expression2,
                 overlap,
                 partial_overlap,
                 unmatched) -> None:
        self.expression1 = expression1
        self.expression2 = expression2

        self.overlap = overlap
        self.partial_overlap = partial_overlap
        self.unmatched_clauses = unmatched

        self.similarity_score = self.get_expression_similarity_score()

    # Function to calculate final similarity score of difference expresssion
    # For full explanation see thesis section 3.2.2
    # In short, (sum of overlapping clauses + sum of similarities of partial
    # overlapping clauses) / size of biggest ruleset
    def get_expression_similarity_score(self):
        return ((len(self.overlap.clauses) + 
                sum([match.score for match in self.partial_overlap]))
                    #  [self.partial_overlap[key] for key in self.partial_overlap.keys()]]))
                / max(len(self.expression1.clauses), len(self.expression2.clauses)))

