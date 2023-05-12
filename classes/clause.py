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
    
    # def __xor__(self, other_literal):

   

    # "&"- override Function that returns literals that appear in both clauses
    def __and__(self, other_clause):
        result = set()
        for literal in self.literals:
            if literal in other_clause:
                result.add(literal)
                
        return result
            

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
        # Step 1: Outer join (unchanged literals)
        remainder1 = clause1.literals
        remainder2 = clause2.literals

        overlap = clause1 & clause2
        if overlap:
            # print("Overlap = ", overlap)
            remainder1 = clause1.literals - overlap
            # This doesnt work since the overlap set contains only objects obtained from clause 1:
            # remainder2 = clause2 - overlap
            # Therefore...
            remainder2 = {literal for literal in clause2.literals if all([literal == overlap_literal for overlap_literal in overlap])}
            num_overlap = len(overlap)
        
        # Step 2: Match literals to their negated/unnegated counterpart
        num_negations = 0
        negations = []
        for literal in remainder1:
            a, b = contains_negated(literal, remainder2)

            if a and b:
                # print("Negation found")
                # print(remainder1, remainder2, " contain the pair:")
                # print(a, b)
                # print()
                num_negations += 1
                negations.append((a, b))
            # If negated literal in clause2 - negation
                # negation second?
                    # Reduce size of clause incrementally
        
        remainder1 = remainder1 - {pair[0] for pair in negations}
        remainder2 = remainder2 - {pair[1] for pair in negations}

        # print("Remainders...")
        # print(remainder1)
        # print(remainder2)            

        # Step 3: remaining literals are regarded as having mutated
            # if len remainder of clause1 > clause2
                # difference is deletions
            # if len remainder of clause2 > clause1
                #difference is additions

        num_of_mutations = min(len(remainder1), len(remainder2))
        mutation_pairs = set()
        for _ in range(len(remainder2)):
                mutation_pairs.add((remainder1.pop(), remainder2.pop()))

        num_of_deletions = 0
        deletions = set()
        num_of_additions = 0
        additions = set()

        if remainder1:
            deletions = remainder1
            num_of_deletions = len(deletions)
        elif remainder2:
            additions = remainder2
            num_of_additions = len(additions)

        # print("Mutations: ")
        # print(mutation_pairs)


        return overlap, negations, mutation_pairs, deletions, additions
    

    # def difference(clause1, clause2):
    #     # If literal in clause2 - overlap
    #         # Handle direct overlap first by &-operator

    #     # Step 1: Outer join (unchanged literals)
    #     overlap = clause1 & clause2
    #     remainder1 = clause1.literals - overlap
    #     remainder2 = clause2.literals - overlap
        

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