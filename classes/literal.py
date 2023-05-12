

# Class to represent a single literal in a clause
class Literal:
    def __init__(self, value, negated):
        self.value = value
        self.negated = negated


    # Printing function for a literal
    def __repr__(self):
        if self.negated:
            return "¬" + self.value
        else:
            return self.value
        

    # Equality operator for Literals
    def __eq__(self, other):
        return self.value == other.value and self.negated == other.negated
    

    # eq makes this type unhashable, so introduce new hash function
    def __hash__(self):
        return id(self)
    