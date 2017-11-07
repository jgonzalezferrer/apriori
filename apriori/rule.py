class Rule:
    def __init__(self, confidence, antecedent, consequent=frozenset()):
        self.confidence = confidence
        self.antecedent = antecedent
        self.consequent = consequent

    def __str__(self):
        antecedent = [x for x in self.antecedent]
        consequent = [x for x in self.consequent]
        return "{} -> {}".format(antecedent, consequent)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.antecedent == other.antecedent and self.consequent == other.consequent
        return False

    def __hash__(self):
        return hash((self.antecedent, self.consequent))
