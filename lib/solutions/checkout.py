# noinspection PyUnusedLocal
# skus = unicode string

import unittest

PRICES = {'A': 50, 'B': 30, 'C': 20, 'D': 15, 'E':40, 'F':10}
MULTIBUY = {'A': [[5, 200], [3, 130]], 'B': [2, 45]}
FREEDEALS = {'E': [2, ['B', 1]], 'F': [3, ['F', 1]]}


def check_and_apply_freedeals(cart):

    for item in FREEDEALS:
        if item in cart and cart[item]>= FREEDEALS[item][0]:
            num = cart[item]
            while num >= FREEDEALS[item][0]:
                if FREEDEALS[item][1][0] in cart:
                    cart[FREEDEALS[item][1][0]] -= FREEDEALS[item][1][1]
                num -= FREEDEALS[item][0]
    return cart


def calculate_cart_cost(cart):
    total = 0
    cart = check_and_apply_freedeals(cart)

    for item, quantity in cart.iteritems():
        num = quantity
        while num:

            if item in MULTIBUY and type(MULTIBUY[item][0]) is list:

                if num >= MULTIBUY[item][0][0]:
                    total += MULTIBUY[item][0][1]
                    num -= MULTIBUY[item][0][0]

                elif num >= MULTIBUY[item][1][0]:
                    total += MULTIBUY[item][1][1]
                    num -= MULTIBUY[item][1][0]

                else:
                    total += num * PRICES[item]
                    num -= num
            else:
                if item in MULTIBUY and num >= MULTIBUY[item][0]:
                    total += MULTIBUY[item][1]
                    num -= MULTIBUY[item][0]
                else:
                    total += num* PRICES[item]
                    num -= num
    return total


def checkout(skus):

    if type(skus) is list:
        skus = skus[0]
    #
    # if not isinstance(skus, str):
    #     return -1

    if skus == "":
        return 0

    cart = {}
    for item in skus:
        if item not in PRICES:
            return -1
        else:
            if item in cart:
                cart[item] = cart[item] + 1
            else:
                cart[item] = 1

    total = calculate_cart_cost(cart)
    return total


class TestCheckout(unittest.TestCase):

    def test_empty_and_single_skus(self):
        PRICES = {'A': 50, 'B': 30, 'C': 20, 'D': 15, 'E': 40, 'F': 10,
                  'G': 20, 'H':10, 'I': 35, 'J': 60, 'K': 80, 'L':90,
                  'M': 15, 'N': 40, 'O':10, 'P': 50}
        self.assertEqual(checkout(''), 0)
        self.assertEqual(checkout('A'), 50)
        self.assertEqual(checkout("B"), 30)
        self.assertEqual(checkout('C'), 20)
        self.assertEqual(checkout('D'), 15)
        self.assertEqual(checkout('E'), 40)
        self.assertEqual(checkout('F'), 10)
        self.assertEqual(checkout('FF'), 20)
        self.assertEqual(checkout('G'), 20)
        self.assertEqual(checkout('H'), 10)
        self.assertEqual(checkout('I'), 35)
        self.assertEqual(checkout('J'), 60)
        self.assertEqual(checkout('K'), 80)
        self.assertEqual(checkout('L'), 90)
        self.assertEqual(checkout('M'), 15)
        self.assertEqual(checkout('N'), 40)
        self.assertEqual(checkout('O'), 10)
        self.assertEqual(checkout('P'), 50)
        self.assertEqual(checkout('Q'), 30)
        self.assertEqual(checkout('R'), 50)
        self.assertEqual(checkout('S'), 30)
        self.assertEqual(checkout('T'), 20)
        self.assertEqual(checkout('U'), 40)
        self.assertEqual(checkout('V'), 50)
        self.assertEqual(checkout('W'), 20)
        self.assertEqual(checkout('X'), 90)
        self.assertEqual(checkout('Y'), 10)
        self.assertEqual(checkout('Z'), 50)



    def test_multibuy_skus(self):
        self.assertEqual(checkout('BB'), 45)
        self.assertEqual(checkout('AAA'), 130)
        self.assertEqual(checkout('AAAAA'), 200)

    def test_freedeals_skus(self):
        self.assertEqual(checkout('FFF'), 20)
        self.assertEqual(checkout('EBBE'), 110)
        self.assertEqual(checkout('EEEEBBB'), 190)

    def test_multibuy_and_free_deals_skus(self):
        self.assertEqual(checkout('AAAAABBEE'), 310)
