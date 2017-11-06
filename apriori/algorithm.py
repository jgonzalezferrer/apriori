from collections import Counter


def create_items(basket):
    items = set()
    for basket in basket:
        for item in basket:
            items.add(item)
    return items


def candidate_tuples(tuples, items):
    candidate_k_tuples = set()
    for t in tuples:
        for item in items:
            candidate_k_tuples.add(t.add(item))

    return candidate_k_tuples


def count_occurrences(baskets, tuples):
    occurrences = Counter()
    for t in tuples:
        for basket in baskets:
            if set(t).issubset(basket):
                occurrences[t] += 1
    return occurrences


def frequent_items(occurrences, s):
    for k, count in occurrences:
        if count >= s:
            yield k
