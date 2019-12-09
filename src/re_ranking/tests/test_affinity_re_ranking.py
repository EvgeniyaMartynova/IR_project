from unittest import TestCase
import affinity_ranking as ar

class TestAffinityReRanking(TestCase):

    def test_affinity_measure(self):
        ar.affinity([1,2,3], [4,5,6])
        self.assertEqual(1, 2)
