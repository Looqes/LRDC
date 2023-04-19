

# Class to represent a single literal in a clause
class Literal:
    def __init__(self, value, negated):
        self.value = value
        self.negated = negated


    def __repr__(self):
        if self.negated:
            return "¬" + self.value
        else:
            return self.value
        
    # eq compares only the value of the two literals compared
    # For the purpose of the LRDC two literals share some relation
    # if their values are the same, regardless of being negated or not.
    def __eq__(self, other):
        return self.value == other.value and self.negated == other.negated
    
    # eq makes this type unhashable, so introduce new hash function
    def __hash__(self):
        return id(self)
    