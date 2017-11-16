import logging

from apriori.utility import printify
from apriori.itemset import Itemset
from apriori.association_rule import AssociationRule


def main():
    data_file = "./data/T10I4D100K.dat"

    with open(data_file, 'r') as f:
        content = f.read()
        baskets = []

        for line in content.splitlines():
            baskets.append(line.split())

    support = 0.01
    itemset = Itemset(baskets, support)

    frequent_itemsets, support_itemsets = itemset.run(logging.DEBUG)

    printify(frequent_itemsets[1], 10)
    printify(frequent_itemsets[2], 10)
    printify(frequent_itemsets[3], 10)
    printify(frequent_itemsets[4], 10)

    association_rule = AssociationRule(0.1, support_itemsets, frequent_itemsets)
    rules = association_rule.generate_all_rules()
    for rule in rules:
        print(rule)

if __name__ == "__main__":
    main()
