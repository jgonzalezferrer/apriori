from apriori.rule import Rule


class AssociationRule:
    def __init__(self, confidence_threshold, support_itemset, frequent_itemsets=dict()):
        self.confidence_threshold = confidence_threshold
        self.support_itemset = support_itemset
        self.frequent_itemsets = frequent_itemsets

    def generate_rules_from_single_itemset(self, itemset):
        def _generate_association_rules(candidate_rule):
            if len(candidate_rule.antecedent) == 0:
                return

            if candidate_rule.confidence >= self.confidence_threshold or len(
                    candidate_rule.consequent) == 0:  # second condition for {a,b,c} -> {}
                if len(candidate_rule.consequent) > 0: rules.add(candidate_rule)

                for i in candidate_rule.antecedent:
                    new_antecedent = candidate_rule.antecedent.difference({i})
                    new_consequent = candidate_rule.consequent.union({i})
                    if len(new_antecedent) == 0:  # next iteration -> {} -> {a,b,c}
                        new_confidence = 0
                    else:
                        new_confidence = self.support_itemset[new_antecedent.union(new_consequent)] / self.support_itemset[
                            new_antecedent]

                    _generate_association_rules(Rule(new_antecedent, new_consequent, new_confidence))
            return

        candidate_rule = Rule(itemset)
        rules = set()
        _generate_association_rules(candidate_rule)

        return rules

    def generate_all_rules(self):
        rules = set()
        for _, frequent_itemsets in self.frequent_itemsets.items():
            for itemset in frequent_itemsets:
                rules = rules.union(self.generate_rules_from_single_itemset(itemset))

        return rules

