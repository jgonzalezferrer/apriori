from nose.tools import assert_equal

from apriori.algorithm import create_items, generate_candidates, generate_candidates_optimizations


def test_create_items():

    baskets = [[1,2,3], [2,5,3], [2,5,4,1,1]]
    singletons = create_items(baskets)

    assert_equal(singletons, {frozenset({1}), frozenset({2}), frozenset({3}), frozenset({4}), frozenset({5})})


def test_generate_candidates():

    baskets = [[1,2,3,4, 5]]
    singletons = create_items(baskets)
    candidates_2 = generate_candidates(singletons, singletons)

    # Let's restrict the size of the elements for interpretability
    candidates_2 = set([frozenset([2,4]), frozenset([3,4]), frozenset([2,5]), frozenset([2,3])])

    # Wrong, we still have to discard items who have subsets that are not frequent
    print(generate_candidates(candidates_2, singletons))

    # The correct answer is {frozenset({2, 3, 4})}
    print(generate_candidates_optimizations(candidates_2, 3))

    # TODO: still I would like to try it with other cases...



if __name__ == '__main__':
    test_create_items()
    test_generate_candidates()