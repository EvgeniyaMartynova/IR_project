from unittest import TestCase
import affinity_ranking as ar

class TestAffinityReRanking(TestCase):

    def test_affinity_measure(self):
        doc_trump = "Mr. Trump became president after winning the political election. Though he lost the support of some republican friends, Trump is friends with President Putin"
        doc_election = "President Trump says Putin had no political interference is the election outcome. He says it was a witchhunt by political parties. He claimed President Putin is a friend who had nothing to do with the election"
        doc_putin = "Post elections, Vladimir Putin became President of Russia. President Putin had served as the Prime Minister earlier in his political career"
        documents = [doc_trump, doc_election, doc_putin]
        ar.affinity([1,2,3], [4,5,6])
        self.assertEqual(1, 2)
