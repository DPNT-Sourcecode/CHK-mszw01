# noinspection PyShadowingBuiltins,PyUnusedLocal

import unittest


class Sum:

    def sum(self, x, y):
        return x + y


class TestSum(unittest.TestCase):

    def test_sum(self):
        sum_object = Sum()
        self.assertEqual(sum_object.sum(5,5), 10)
        self.assertEqual(sum_object.sum(5, 10), 15)
        self.assertEqual(sum_object.sum(0, 20), 20)