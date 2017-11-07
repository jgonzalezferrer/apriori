from nose.tools import assert_equal

from apriori.algorithm import create_items, generate_candidates, filter_candidates


def test_create_items():
    baskets = [[1, 2, 3], [2, 5, 3], [2, 5, 4, 1, 1]]
    c1 = create_items(baskets)

    assert_equal(c1, {frozenset({1}), frozenset({2}), frozenset({3}), frozenset({4}), frozenset({5})})


def test_generate_candidates():
    baskets = [[1,2,3,4,5]]

    # Let us assume L1 and L2 are the set of truly frequent tuples.
    l1 = create_items(baskets)
    l2 = set([frozenset([2,4]), frozenset([3,4]), frozenset([2,5]), frozenset([2,3])])
    c3 = generate_candidates(l2, l1)

    assert_equal(c3, {frozenset({2, 3, 4})})


def test_filter_candidates():
    baskets = [[1, 2, 3, 5], [2, 5, 3], [2, 5, 4, 1, 1]]

    c1 = create_items(baskets)

    l1 = filter_candidates(c1, 0.5, baskets)
    # Discard {4}
    assert_equal(l1, {frozenset({1}), frozenset({2}), frozenset({3}), frozenset({5})})

    c2 = generate_candidates(l1, l1)
    l2 = filter_candidates(c2, 0.5, baskets)
    # Discard {1,3}
    assert_equal(l2, {frozenset({2, 3}), frozenset({2, 5}), frozenset({1, 2}), frozenset({1, 5}), frozenset({3, 5})})


    
    

if __name__ == '__main__':
    test_create_items()
    test_generate_candidates()
    test_filter_candidates()