import unittest
from naive_bayes import NaiveBayesClassifier

class NaiveBayesTestCase(unittest.TestCase):

    def test_can_create(self):
        obj = NaiveBayesClassifier()
        self.assertTrue(obj)
        

if __name__ == '__main__':
    unittest.main()