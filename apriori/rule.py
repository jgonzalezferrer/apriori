from apriori.utility import printify


class Rule:
    def __init__(self, antecedent, consequent=frozenset(), confidence=-1):
        self.antecedent = antecedent
        self.consequent = consequent
        self.confidence = confidence

    def __str__(self):
        return "{} -> {}".format(printify({self.antecedent}), printify({self.consequent}))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.antecedent == other.antecedent and self.consequent == other.consequent
        return False

    def __hash__(self):
        return hash((self.antecedent, self.consequent))


def generate_association_rules(c, itemset, support_itemset):
    def _generate_association_rules(candidate_rule):
        if len(candidate_rule.antecedent) == 0:
            return

        if candidate_rule.confidence >= c or len(
                candidate_rule.consequent) == 0:  # second condition for {a,b,c} -> {}
            if len(candidate_rule.consequent) > 0: rules.add(candidate_rule)

            for i in candidate_rule.antecedent:
                new_antecedent = candidate_rule.antecedent.difference({i})
                new_consequent = candidate_rule.consequent.union({i})
                if len(new_antecedent) == 0:  # next iteration -> {} -> {a,b,c}
                    new_confidence = 0
                else:
                    new_confidence = support_itemset[new_antecedent.union(new_consequent)] / support_itemset[
                        new_antecedent]

                _generate_association_rules(Rule(new_antecedent, new_consequent, new_confidence))
        return

    candidate_rule = Rule(itemset)
    rules = set()
    _generate_association_rules(candidate_rule)

    return rules

