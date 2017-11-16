import collections, itertools


def create_items_catalog(baskets, type=''):
    """
    Creates a dictionary where:
        + key: item
        + value: list of baskets where the item is contained in.

    :param baskets:
    :return:
    """
    items_catalog = collections.defaultdict(list)
    for i, basket in enumerate(baskets):
        for item in basket:
            if type == 'str':
                items_catalog[item].append(i)
            else:
                items_catalog[frozenset({item})].append(i)

    return items_catalog


def create_items_catalog_with_itemsets(baskets):
    """
    Creates a dictionary where:
        + key: item
        + value: list of baskets where the item is contained in.

    :param baskets:
    :return:
    """
    items_catalog = collections.defaultdict(list)
    for i, basket in enumerate(baskets):
        for item in basket:
            items_catalog[frozenset({item})].append(i)

        for pair_i, pair_j in itertools.combinations(basket, 2):
            items_catalog[frozenset({frozenset({pair_i}), frozenset({pair_j})})].append(i)

    return items_catalog


def printify(itemset, n=1):
    msg = "{"
    iterable_itemset = iter(itemset)
    for i in range(n):
        try:
            element = next(iterable_itemset)
            msg += "("
            for j, item in enumerate(element):
                s = next(iter(item))
                msg += str(s)
                if j < len(element) - 1:
                    msg += ", "
            msg += ")"
            if i < n - 1:
                msg += ", "
        except:
            msg = msg[0:-2]
            break
    msg += "}"
    return msg
