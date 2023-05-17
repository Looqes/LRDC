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
    

    # "&"- override Function that returns literals that appear in both clauses
    def __and__(self, other_clause):
        result = set()
        for literal in self.literals:
            if literal in other_clause:
                result.add(literal)
                
        return result


    # Function that returns true if two given clauses have at least a single
    # literal that share the same value
    def has_partial_overlap(self, other_clause):
        for literal in self.literals:
            for other_literal in other_clause.literals:
                if literal.value == other_literal.value:
                    return True
        return False
    
    
    # Function to extract a "clause difference" from a pair of two clauses.
    # Stepwise algorithm that returns the overlap between the two clauses, the
    # negations of literals between clauses (a set of pairs of literals between
    # clauses that share value but differ in negation), mutations of literals
    # between clauses and finally deletions or additions depending on the
    # difference in size of the clauses (empty if the size is equal).
    def difference(clause1, clause2):
        # Step 1: Outer join (unchanged literals) to extract full overlapping
        # literals
        remainder1 = clause1.literals
        remainder2 = clause2.literals

        overlap = clause1 & clause2
        if overlap:
            remainder1 = clause1.literals - overlap
            # This doesnt work since the overlap set contains only objects obtained from clause 1:
            # remainder2 = clause2 - overlap
            # Therefore...
            remainder2 = {literal for literal in clause2.literals 
                          if all([literal == overlap_literal for overlap_literal in overlap])}
        
        # Step 2: Match literals to their negated/unnegated counterpart if it
        # exists in the other clause
        negations = []
        for literal in remainder1:
            a, b = contains_negated(literal, remainder2)

            if a and b:
                negations.append((a, b))
        
        # update remainders
        remainder1 = remainder1 - {pair[0] for pair in negations}
        remainder2 = remainder2 - {pair[1] for pair in negations}

        deletions = remainder1
        additions = remainder2

        # # Step 3: remaining literals are regarded as having mutated
        # # If one clause contains more literals than the other, the
        # # difference is either additions or deletions
        # # if length remainder of clause1 > clause2
        # #   difference is deletions
        # # if length remainder of clause2 > clause1
        # #   difference is additions
        # mutation_pairs = set()
        # for _ in range(len(remainder2)):
        #     mutation_pairs.add((remainder1.pop(), remainder2.pop()))

        # deletions = remainder1 if remainder1 else set()
        # additions = remainder2 if remainder1 else set()

        return overlap, negations, deletions, additions
    

# Function that matches a literal to another literal in clause that shares it's value
# but differs in negation.
# To avoid making many clause instances this function works on a simple set of literals
# instead of a clause object. Clauses remain unmutable and only represent the original
# rules of the input ruleset.
def contains_negated(literal, set_of_literals):
    for other_literal in set_of_literals:
        if (literal.value == other_literal.value
            and ((literal.negated == True and other_literal.negated == False) 
                    or 
                    (literal.negated == False and other_literal.negated == True))):
            return literal, other_literal
    
    # No match found
    return None, None