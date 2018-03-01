# noinspection PyUnusedLocal
# skus = unicode string

import unittest

PRICES = {'A': 50, 'B': 30, 'C': 20, 'D': 15, 'E': 40, 'F': 10,
          'G': 20, 'H': 10, 'I': 35, 'J': 60, 'K': 70, 'L': 90,
          'M': 15, 'N': 40, 'O': 10, 'P': 50, 'Q': 30, 'R': 50,
          'S': 20, 'T': 20, 'U': 40, 'V': 50, 'W': 20, 'X': 17, 'Y': 20,
          'Z': 21}
MULTIBUY = {'A': [[5, 200], [3, 130]], 'B': [2, 45], 'H': [[10, 80], [5, 45]],
            'K': [2, 120], 'P': [5, 200], 'Q': [3, 80], 'V': [[3, 130], [2,
                                                                         90]]}
FREEDEALS = {'E': [2, ['B', 1]], 'F': [3, ['F', 1]], 'N': [3, ['M', 1]],
             'R': [3, ['Q', 1]], 'U': [4, ['U', 1]]}

GROUPDEALS = {'ZSTYX': [3, 45]}


def check_and_apply_freedeals(cart):

    for item in FREEDEALS:
        if item in cart and cart[item]>= FREEDEALS[item][0]:
            num = cart[item]
            while num >= FREEDEALS[item][0]:
                if FREEDEALS[item][1][0] in cart:
                    cart[FREEDEALS[item][1][0]] -= FREEDEALS[item][1][1]
                num -= FREEDEALS[item][0]
    return cart

def check_and_apply_groupdeals(cart, total):

    for groupitems in GROUPDEALS:
        tmpcart = {item: quantity for item, quantity in cart.iteritems() if
                   item in groupitems}
        if tmpcart:
            itemsum = sum(tmpcart.values())
            if itemsum >= GROUPDEALS[groupitems][0]:
                count = 0
                amount = 0
                for i in groupitems:
                    if i in tmpcart:
                        while tmpcart[i] and itemsum >= GROUPDEALS[groupitems][0]:
                            if (amount + tmpcart[i]) > GROUPDEALS[groupitems][0]:
                                tmpcart[i] = amount + tmpcart[i] - 3
                                count += 1
                                amount = 0
                                itemsum = sum(tmpcart.values())
                            else:
                                amount += tmpcart[i]
                                tmpcart[i] = 0
                total += count * GROUPDEALS[groupitems][1]
                for item, quantity in tmpcart.iteritems():
                    cart[item]= quantity
    return cart, total

def calculate_cart_cost(cart):
    total = 0
    cart, total = check_and_apply_groupdeals(cart, total)
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

    def test_group_deals_skus(self):
        self.assertEqual(checkout('STX'), 45)
        self.assertEqual(checkout('STXSTX'), 90)
        self.assertEqual(checkout('SSS'), 45)


    def test_empty_and_single_skus(self):

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
        self.assertEqual(checkout('K'), 70)
        self.assertEqual(checkout('L'), 90)
        self.assertEqual(checkout('M'), 15)
        self.assertEqual(checkout('N'), 40)
        self.assertEqual(checkout('O'), 10)
        self.assertEqual(checkout('P'), 50)
        self.assertEqual(checkout('Q'), 30)
        self.assertEqual(checkout('R'), 50)
        self.assertEqual(checkout('S'), 20)
        self.assertEqual(checkout('T'), 20)
        self.assertEqual(checkout('U'), 40)
        self.assertEqual(checkout('V'), 50)
        self.assertEqual(checkout('W'), 20)
        self.assertEqual(checkout('X'), 17)
        self.assertEqual(checkout('Y'), 20)
        self.assertEqual(checkout('Z'), 21)



    def test_multibuy_skus(self):
        self.assertEqual(checkout('BB'), 45)
        self.assertEqual(checkout('VV'), 90)
        self.assertEqual(checkout('VVV'), 130)
        self.assertEqual(checkout('QQQ'), 80)
        self.assertEqual(checkout('PPPPP'), 200)
        self.assertEqual(checkout('KK'), 120)
        self.assertEqual(checkout('HHHHH'), 45)
        self.assertEqual(checkout('HHHHHHHHHH'), 80)
        self.assertEqual(checkout('AAA'), 130)
        self.assertEqual(checkout('AAAAA'), 200)
        self.assertEqual(checkout('UUU'), 120)


    def test_freedeals_skus(self):
        self.assertEqual(checkout('UUUU'), 120)
        self.assertEqual(checkout('FFF'), 20)
        self.assertEqual(checkout('EBBE'), 110)
        self.assertEqual(checkout('EEEEBBB'), 190)
        self.assertEqual(checkout('RRRQQ'), 180)
        self.assertEqual(checkout('NNNM'), 120)

    def test_multibuy_and_free_deals_skus(self):
        self.assertEqual(checkout('AAAAABBEE'), 310)
