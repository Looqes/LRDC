# CNF clause object

# Class to represent a single clause in a CNF expression
# AFAIK the order of the terms in a clause is not important, so for efficient
# comparison clauses contain their variable terms in the form of a set of terms
class Clause():
    def __init__(self, variables):
        self.literals = set(variables)
        self.length = len(variables)

    # String representation of a clause for testing purposes
    def __repr__(self) -> str:
        result = "("

        for literal in self.literals:
            result = result + literal + " ∨ "

        return result[:-3] + ")"
    
    # Equality operator to compare two clauses
    def __eq__(self, other_clause) -> bool:
        return self.literals == other_clause.literals
    

    def __and__(self, other_clause):
        remainderself = self.literals & other_clause.literals
        remainderother = other_clause.literals & self.literals

        print("step 1:")
        print(remainderself)
        print(remainderother)

        for literal in self.literals - remainderself:
            for other_literal in other_clause.literals - remainderother:
                if literal.replace("-", "") in other_literal:
                    remainderself.add(literal)
                    remainderother.add(other_literal)

        print("step 2: ")
        print(remainderself)
        print(remainderother)


    # # Symmetric difference between literals in a clause. Returns literals from
    # # clause "self" that do not appear in "other_clause" and vice versa
    # def __xor__(self, other_clause):
    #     unnegatedself = {literal.replace("-", "") for literal in self.literals}
    #     unnegatedother = {literal.replace("-", "") for literal in other_clause.literals}

    #     return unnegatedself - unnegatedother, unnegatedother - unnegatedself



        
