# CNF clause object

# Class to represent a single clause in a CNF expression
# AFAIK the order of the terms in a clause is not important, so for efficient
# comparison clauses contain their variable terms in the form of a set of terms
class Clause():
    def __init__(self, variables):
        self.variables = set(variables)

    # String representation of a clause for testing purposes
    def __repr__(self) -> str:
        result = "("

        for variable in self.variables:
            result = result + variable + " ∨ "

        return result[:-3] + ")"
    
    # Equality operator to compare two clauses
    def __eq__(self, other_clause) -> bool:
        return self.variables == other_clause.variables
        
