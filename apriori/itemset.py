import itertools
import collections
import time
import logging
import apriori.utility as utility


class Itemset:
    def __init__(self, baskets=[], support_threshold=0):
        self.baskets = baskets
        self.n = len(self.baskets)
        self.support_threshold = support_threshold
        self.logger = logging.getLogger('itemset')
        self.logger.addHandler(logging.StreamHandler())

    def generate_candidates(self, prev_candidates, singletons):
        """
       Candidates in Ck can be generated by combining itemsets from Lk-1 and singletons from L1.

        One should be careful and selective with candidate generation: for a candidate in Ck to be a frequent itemset,
        all its subsets must be frequent, not only the itemsets from Lk-1 and L1 that the candidate is constructed from,
        i.e., each of its subsets should be in the corresponding Lm, m = 1,…, k-1
       :param prev_candidates:
       :param singletons:
       :return:
       """
        k = len(next(iter(prev_candidates)))+1  # Extract size of an element from prev to calculate current iteration.

        m = k - 2 if k > 1 else 0  # Base case k = 1, ignore: used for check subsets are frequent itemsets.
        candidates = set()

        for candidate in prev_candidates:
            for i in singletons:
                mismatch = False
                new_candidate = frozenset(candidate).union(i)
                for combination in itertools.combinations(candidate, m):
                    frequent_tuple = frozenset(combination).union(i)
                    if frequent_tuple not in prev_candidates:
                        mismatch = True
                        break
                if not mismatch and len(new_candidate) == k: candidates.add(new_candidate)

        return candidates

    def prune_candidates(self, candidates, items_catalog):
        occurrences = collections.Counter()

        for candidate in candidates:
            if len(items_catalog[candidate]) > 0:
                occurrences[candidate] = len(items_catalog[candidate])
            else:
                baskets_intersection = []
                for item in candidate:
                    baskets_intersection.append(set(items_catalog[item]))
                occurrences[candidate] = len(set.intersection(*baskets_intersection))

        candidates_return = candidates.copy()
        support_return = dict()
        for candidate, occurrence in occurrences.items():
            support = occurrence/self.n
            if support < self.support_threshold:
                candidates_return.discard(candidate)
            support_return[candidate] = support

        return candidates_return, support_return

    def run(self, logging_level=logging.INFO, catalog_function=utility.create_items_catalog):
        self.logger.setLevel(logging_level)

        total_time = time.time()

        time_catalog = time.time()
        items_catalog = catalog_function(self.baskets)
        self.logger.debug("Generate catalog: {}".format(time.time()-time_catalog))

        k = 1
        frequent_itemsets = dict()
        support_itemsets = dict()

        time_c1 = time.time()
        c1 = {frozenset({x}) for x in set(filter(lambda x: len(x) == 1, items_catalog.keys()))}
        self.logger.debug('k={}: Candidates generation takes: {}'.format(k, time.time() - time_c1))

        time_l1 = time.time()
        l1, support_l1 = self.prune_candidates(c1, items_catalog)
        self.logger.debug('k={}: Prune takes: {}'.format(k, time.time() - time_l1))
        self.logger.debug('k={}: Ck={} and Lk={}'.format(k, len(c1), len(l1)))

        current = l1
        frequent_itemsets[k] = l1
        support_itemsets.update(support_l1)

        while len(current) > 0:
            k += 1
            time_ck = time.time()
            ck = self.generate_candidates(current, l1)
            self.logger.debug('k={}: Candidates generation takes: {}'.format(k, time.time()-time_ck))

            time_lk = time.time()
            lk, support_lk = self.prune_candidates(ck, items_catalog)
            self.logger.debug('k={}: Prune takes: {}'.format(k, time.time()-time_lk))
            self.logger.debug('k={}: Ck={} and Lk={}'.format(k, len(ck), len(lk)))

            frequent_itemsets[k] = lk
            support_itemsets.update(support_lk)
            current = lk

        self.logger.info('Total time: {}'.format(time.time()-total_time))
        return frequent_itemsets, support_itemsets
