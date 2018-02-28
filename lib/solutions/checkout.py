# noinspection PyUnusedLocal
# skus = unicode string

import unittest

PRICES = {'A': 50, 'B': 30, 'C': 20, 'D': 15}
OFFERS = {'A': [3, 130], 'B': [2,45]}


def calculate_cart_cost(cart):
    total = 0

    for item, quantity in cart.iteritems():
        num = quantity
        while num:
            if item in OFFERS and num >= OFFERS[item][0]:
                total += OFFERS[item][1]
                num -= OFFERS[item][0]
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
            return "%s ::: %s " % (item, PRICES)
        else:
            if item in cart:
                cart[item] = cart[item] + 1
            else:
                cart[item] = 1

    total = calculate_cart_cost(cart)
    return total


class TestCheckout(unittest.TestCase):

    def test_checkout(self):
        self.assertEqual(checkout(unicode('AA')), 100)

        self.assertEqual(checkout(''), 0)
        self.assertEqual(checkout('A'), 50)
        self.assertEqual(checkout("B"), 30)
        self.assertEqual(checkout('AA'), 100)
        self.assertEqual(checkout('AAA'), 130)
