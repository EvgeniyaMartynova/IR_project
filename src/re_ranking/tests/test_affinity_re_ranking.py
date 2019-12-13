from unittest import TestCase
import affinity_ranking as ar
import numpy as np
import math
import os

class TestAffinityReRanking(TestCase):

    def get_documents(self):
        docs = []
        for the_file in os.listdir("docs"):
            if the_file.endswith(".txt"):
                file = open(os.path.join("docs", the_file), mode='r')
                doc = ar.InputDocument(the_file.replace(".txt", ""), file.read().strip(), 0)
                docs.append(doc)
                file.close()

        return docs

    def test_affinity_measure(self):
        a = np.array([1, 0, 0, 2, 3])
        b = np.array([3, 4, 0, 7, 0])
        self.assertEqual(ar.affinity(a, b), 17 / math.sqrt(14))
        self.assertEqual(ar.affinity(b, a), 17 / math.sqrt(74))

        c = np.array([0, 4, 5, 0, 0])
        self.assertAlmostEqual(ar.affinity(c, a), 0)
        self.assertAlmostEqual(ar.affinity(a, c), 0)

    def test_get_affinity_matrix(self):
        a0 = np.array([6, 4, 10, 2, 3, 9, 2, 20, 3, 13])
        a1 = np.array([1, 0, 0, 6, 9, 0, 0, 8, 3, 0])
        a2 = np.array([4, 0, 0, 12, 13, 0, 0, 20, 31, 0])
        a3 = np.array([0, 2, 6, 0, 0, 1, 1, 0, 0, 17])
        a4 = np.array([0, 5, 3, 0, 0, 25, 7, 0, 0, 1])
        a5 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        test_vectors = [a0, a1, a2, a3, a4, a5]
        affinity_matrix = ar.get_affinity_matrix(test_vectors)

        expected_matrix = np.array([[0, ar.affinity(a0, a1), ar.affinity(a0, a2), ar.affinity(a0, a3), ar.affinity(a0, a4), 0],
                                    [ar.affinity(a1, a0), 0, ar.affinity(a1, a2), 0, 0, 0],
                                    [ar.affinity(a2, a0), ar.affinity(a2, a1), 0, 0, 0, 0],
                                    [ar.affinity(a3, a0), 0, 0, 0, ar.affinity(a3, a4), 0],
                                    [ar.affinity(a4, a0), 0, 0, ar.affinity(a4, a3), 0, 0],
                                    [0, 0, 0, 0, 0, 0]
                                    ])
        expected_matrix /= np.amax(expected_matrix)

        self.assertTrue(np.allclose(affinity_matrix, expected_matrix))

    def test_get_adjacency_matrix(self):
        affinity_matrix = np.array([[0, 0.9, 0.4, 0.1, 0.02, 0.5],
                                    [1, 0, 0.8, 0.05, 0, 0.03],
                                    [0.09, 0.7, 0, 0.6, 0.099, 0.3],
                                    [0.03, 0.01, 0.04, 0, 0.06, 0.07],
                                    [0.7, 0.4, 0.6, 0.9, 0, 0.8],
                                    [0.003, 0.07, 0.101, 0.5, 0.004, 0]
                                    ])
        adjacency_matrix = ar.get_adjacency_matrix(affinity_matrix, 0.1)

        expected_matrix = np.array([[0, 0.9/1.9, 0.4/1.9, 0.1/1.9, 0, 0.5/1.9],
                                    [1/1.8, 0, 0.8/1.8, 0, 0, 0],
                                    [0, 0.7/1.6, 0, 0.6/1.6, 0, 0.3/1.6],
                                    [0, 0, 0, 0, 0, 0],
                                    [0.7/3.4, 0.4/3.4, 0.6/3.4, 0.9/3.4, 0, 0.8/3.4],
                                    [0, 0, 0.101/0.601, 0.5/0.601, 0, 0]
                                    ])

        self.assertTrue(np.allclose(adjacency_matrix, expected_matrix))

    def test_get_transition_matrix(self):
        dumping_factor = 0.85
        adjacency_matrix = np.array([[0, 0.8, 0.2],
                                    [1, 0, 0],
                                    [0.3, 0.7, 0],
                                    ])
        transition_matrix = ar.get_transition_matrix(adjacency_matrix, dumping_factor)

        expected_matrix = np.array([[(1 - dumping_factor)/9, dumping_factor + (1 - dumping_factor)/9, 0.3*dumping_factor + (1 - dumping_factor)/9],
                                    [0.8*dumping_factor + (1 - dumping_factor)/9, (1 - dumping_factor)/9, 0.7*dumping_factor + (1 - dumping_factor)/9],
                                    [0.2*dumping_factor + (1 - dumping_factor)/9, (1 - dumping_factor)/9, (1 - dumping_factor)/9],
                                    ])

        self.assertTrue(np.allclose(transition_matrix, expected_matrix))

    def test_get_document_rank(self):
        matrix = np.array([[1, 0, 0],
                           [0, 2, 0],
                           [0, 0, 3],
                          ])

        rank = ar.get_document_rank(matrix)
        # what we check here is that principal eigen vector is returned
        self.assertTrue(np.allclose(rank, np.array([0, 0, 1])))

    def test_get_document_rank(self):
        adjacency_matrix = np.array([[0, 0.75, 0.25],
                                     [0.2, 0, 0.8],
                                     [0.9, 0.1, 0],
                                     ])

        documents = [ar.RankedDocument("2", "2", 0.4, 7.8, 0), ar.RankedDocument("3", "3", 0.1, 6.6, 2), ar.RankedDocument("1", "1", 0.5, 7.6, 1)]
        diversity_penalized_ranking = ar.diversity_penalty(documents, adjacency_matrix)

        self.assertAlmostEqual(diversity_penalized_ranking[0].score, 0.5)
        self.assertAlmostEqual(diversity_penalized_ranking[0].docid, "1")
        self.assertAlmostEqual(diversity_penalized_ranking[1].score, 0.05)
        self.assertAlmostEqual(diversity_penalized_ranking[1].docid, "3")
        self.assertAlmostEqual(diversity_penalized_ranking[2].score, 0)
        self.assertAlmostEqual(diversity_penalized_ranking[2].docid, "2")

        # shifting of negative scores
        adjacency_matrix = np.array([[0, 0.75, 0.25],
                                     [0.2, 0, 0.8],
                                     [0, 1, 0],
                                     ])

        diversity_penalized_ranking = ar.diversity_penalty(documents, adjacency_matrix)

        self.assertAlmostEqual(diversity_penalized_ranking[0].score, 0.9)
        self.assertEqual(diversity_penalized_ranking[0].docid, "1")
        self.assertAlmostEqual(diversity_penalized_ranking[1].score, 0.425)
        self.assertEqual(diversity_penalized_ranking[1].docid, "2")
        self.assertAlmostEqual(diversity_penalized_ranking[2].score, 0)
        self.assertEqual(diversity_penalized_ranking[2].docid, "3")


    def test_affinity_ranking(self):
        docs = self.get_documents()
        affinity_ranking = ar.get_affinity_ranking(docs)

        self.assertEqual(affinity_ranking[0].docid, "9a3e7247-41e4-430e-8a30-db3d23f02a7f")
        self.assertEqual(affinity_ranking[1].docid, "33b4ba7c-7974-430f-9845-096f421a0fcc")
        self.assertEqual(affinity_ranking[2].docid, "f09a0a30-7a8d-483f-8b41-618a72dcc1f5")
        self.assertEqual(affinity_ranking[3].docid, "ed063488-a849-49a4-b608-c527ecb5d7c1")
        self.assertEqual(affinity_ranking[4].docid, "3017af48-cec7-45bb-ba6a-706c938b2d08")
        self.assertEqual(affinity_ranking[5].docid, "07bbf821-ae5e-4e9b-a066-9f36bbdbe4dd")






