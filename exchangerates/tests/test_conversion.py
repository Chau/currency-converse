# -*- coding: utf-8 -*-

import json
import os


from django.test import TestCase
from django.conf import settings

from exchangerates.conversion import ConvertRate
from exchangerates.const import *


class ConvertRateTestBase(TestCase):

    def setUp(self):
        self.rates = {
              "CZK": {
                "PLN": 0.166300692,
                "USD": 0.0443422121,
                "EUR": 0.0386592956
              },
              "PLN": {
                "CZK": 6.0132040821,
                "USD": 0.2666387707,
                "EUR": 0.2324662343
              },
              "USD": {
                "CZK": 22.5518744551,
                "PLN": 3.7503923278,
                "EUR": 0.8718395815
              },
              "EUR": {
                "CZK": 25.867,
                "USD": 1.147,
                "PLN": 4.3017
              }
            }

        if os.path.exists(settings.RATES_FNAME):
            os.remove(settings.RATES_FNAME)

    def tearDown(self):
        '''
        remove json file after using
        :return:
        '''
        if os.path.exists(settings.RATES_FNAME):
            os.remove(settings.RATES_FNAME)


class GetRateFromFileTest(ConvertRateTestBase):

    def setUp(self):
        super(GetRateFromFileTest, self).setUp()
        self.converse = ConvertRate(from_currency=CZECH_KRONA, to_currency=US_DOLLAR, amount=1000)

    def test_success(self):
        with open(settings.RATES_FNAME, 'w') as f:
            json.dump(self.rates, f, indent=2)

        last_rates = self.converse.get_last_rate_from_file()
        self.assertEquals(self.rates, last_rates)

    def test_file_not_exist(self):
        with self.assertRaises(IOError):
            self.converse.get_last_rate_from_file()


class FindRateTest(ConvertRateTestBase):

    def test_usd_czk(self):
        converse = ConvertRate(from_currency=US_DOLLAR, to_currency=CZECH_KRONA, amount=1000)
        finded_rate = converse.find_rate(self.rates)
        self.assertEqual(22.5518744551, finded_rate)

    def test_pln_eur(self):
        converse = ConvertRate(from_currency=POLISH_ZLOTY, to_currency=EURO, amount=1000)
        finded_rate = converse.find_rate(self.rates)
        self.assertEqual(0.2324662343, finded_rate)

    def test_empty(self):
        converse = ConvertRate(from_currency=POLISH_ZLOTY, to_currency=EURO, amount=1000)
        with self.assertRaises(AttributeError):
            converse.find_rate({})

    def test_empty_to(self):
        '''
        in the rates does not info about rate for to_currency
        :return:
        '''
        converse = ConvertRate(from_currency=US_DOLLAR, to_currency=CZECH_KRONA, amount=1000)
        del self.rates[US_DOLLAR][CZECH_KRONA]
        finded_rate = converse.find_rate(self.rates)
        self.assertIsNone(finded_rate)

    def test_empty_from(self):
        '''
        ther is no info about from_currency in the rates
        :return:
        '''
        converse = ConvertRate(from_currency=US_DOLLAR, to_currency=CZECH_KRONA, amount=1000)
        del self.rates[US_DOLLAR]
        with self.assertRaises(AttributeError):
            converse.find_rate(self.rates)


class ConvertTest(ConvertRateTestBase):

    def test_success_czk_usd(self):
        self.__create_rate_file()
        converse = ConvertRate(from_currency=CZECH_KRONA, to_currency=US_DOLLAR, amount=1000)
        converted_amount = converse.convert()
        self.assertEqual('44.34', converted_amount)

    def test_success_eur_usd(self):
        self.__create_rate_file()
        converse = ConvertRate(from_currency=EURO, to_currency=US_DOLLAR, amount=1000)
        converted_amount = converse.convert()
        self.assertEqual('1 147.00', converted_amount)

    def test_success_pln_czk(self):
        self.__create_rate_file()
        converse = ConvertRate(from_currency=POLISH_ZLOTY, to_currency=CZECH_KRONA, amount=1234.89)
        converted_amount = converse.convert()
        self.assertEqual('7 425.65', converted_amount)

    def test_no_data(self):
        '''
        rate file is empty
        :return:
        '''
        converse = ConvertRate(from_currency=POLISH_ZLOTY, to_currency=CZECH_KRONA, amount=1234.89)
        with self.assertRaises(IOError):
            converse.convert()

    def test_wrong_json(self):
        with open(settings.RATES_FNAME, 'w') as f:
            pass
        converse = ConvertRate(from_currency=POLISH_ZLOTY, to_currency=CZECH_KRONA, amount=1234.89)
        with self.assertRaises(ValueError):
            converse.convert()

    def test_wrong_amount(self):
        self.__create_rate_file()
        converse = ConvertRate(from_currency=POLISH_ZLOTY, to_currency=CZECH_KRONA, amount='kjhkjg')
        with self.assertRaises(TypeError):
            converse.convert()

    def __create_rate_file(self):

        with open(settings.RATES_FNAME, 'w') as f:
            json.dump(self.rates, f, indent=2)


class FormatAmountTest(ConvertRateTestBase):
    def setUp(self):
        super(FormatAmountTest, self).setUp()
        self.converse = ConvertRate(from_currency=CZECH_KRONA, to_currency=US_DOLLAR, amount=1000)


    def test_double_digit(self):
        formated_amount = self.converse.format_amount(23.45)
        self.assertEqual('23.45', formated_amount)

    def test_int_double_digit(self):
        formated_amount = self.converse.format_amount(23)
        self.assertEqual('23.00', formated_amount)

    def test_four_digit(self):
        formated_amount = self.converse.format_amount(2323.7634)
        self.assertEqual('2 323.76', formated_amount)

    def test_seven_digit(self):
        formated_amount = self.converse.format_amount(2345872.4587)
        self.assertEqual('2 345 872.46', formated_amount)

    def test_none(self):
        with self.assertRaises(ValueError):
            self.converse.format_amount(None)

    def test_string(self):
        with self.assertRaises(ValueError):
            self.converse.format_amount('abra')

    def test_null(self):

        formated_amount = self.converse.format_amount(0)
        self.assertEqual('0.00', formated_amount)

