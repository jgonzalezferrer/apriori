from apriori.utility import printify


class Rule:
    def __init__(self, antecedent, consequent=frozenset(), confidence=-1):
        self.antecedent = antecedent
        self.consequent = consequent
        self.confidence = confidence

    def __str__(self):
        return "{} -> {}".format(printify({self.antecedent}), printify({self.consequent}))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.antecedent == other.antecedent and self.consequent == other.consequent
        return False

    def __hash__(self):
        return hash((self.antecedent, self.consequent))
