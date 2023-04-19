# CNF clause object
from classes.literal import Literal
# from LRDC.classes.literal import Literal

# Class to represent a single clause in a CNF expression
# AFAIK the order of the terms in a clause is not important, so for efficient
# comparison clauses contain their variable terms in the form of a set of terms
class Clause():
    def __init__(self, variables):
        self.literals = set()
        for variable in variables:
            if "-" in variable:
                self.literals.add(Literal(variable.replace("-", ""), True))
            else:
                self.literals.add(Literal(variable, False))

        self.length = len(self.literals)

    # String representation of a clause for testing purposes
    def __repr__(self) -> str:
        result = "("

        for literal in self.literals:
            result = result + str(literal) + " ∨ "

        return result[:-3] + ")"
    
    # Equality operator to compare two clauses
    def __eq__(self, other_clause) -> bool:
        for literal in self.literals:
            if literal not in other_clause:
                return False
        return True

    

    # "in" operator override to check if some literal appears in clause
    def __contains__(self, other_literal):
        for literal in self.literals:
            if literal == other_literal:
                return True
        return False
            

    def has_partial_overlap(self, other_clause):
        for literal in self.literals:
            for other_literal in other_clause.literals:
                if literal.value == other_literal.value:
                    return True
        return False