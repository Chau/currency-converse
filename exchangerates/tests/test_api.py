# -*- coding: utf-8 -*-

import json
import os

from django.test import TestCase
from django.conf import settings

import mock

from exchangerates.api import OpenExchangeRates, ApiException
from exchangerates.const import *


class OpenExchangeRatesBaseTest(TestCase):

    def setUp(self):
        self.rate = OpenExchangeRates()


class GetOneRateTest(OpenExchangeRatesBaseTest):

    def test_access(self):
        for currency in CURRENCIES:
            currency_rate = self.rate.get_one_rate(base_currency=currency)
            self.assertTrue(currency_rate.get('base'))
            self.assertEqual(currency, currency_rate.get('base'))
            self.assertTrue(currency_rate.get('rates'))

    def test_wrong_base(self):
        with self.assertRaises(ApiException):
            self.rate.get_one_rate(base_currency='abrakadabra')

    def test_empty_base(self):
        with self.assertRaises(ApiException):
            self.rate.get_one_rate(base_currency='')


class FormatParamsTest(OpenExchangeRatesBaseTest):


    def test_usd(self):
        params = self.rate.format_params_for_request(US_DOLLAR)
        self.assertDictEqual({'symbols': 'CZK,EUR,PLN', 'base': US_DOLLAR}, params)

    def test_czk(self):
        params = self.rate.format_params_for_request(CZECH_KRONA)
        self.assertDictEqual({'symbols': 'EUR,PLN,USD', 'base': CZECH_KRONA}, params)

    def test_eur(self):
        params = self.rate.format_params_for_request(EURO)
        self.assertDictEqual({'symbols': 'CZK,PLN,USD', 'base': EURO}, params)

    def test_pln(self):
        params = self.rate.format_params_for_request(POLISH_ZLOTY)
        self.assertDictEqual({'symbols': 'CZK,EUR,USD', 'base': POLISH_ZLOTY}, params)

    def test_empty(self):
        with self.assertRaises(ApiException):
            self.rate.format_params_for_request('')

    def test_currency_not_in_list(self):

        with self.assertRaises(ApiException):
            self.rate.format_params_for_request('abrakadabra')


class TransformRatesTest(OpenExchangeRatesBaseTest):

    def test_success(self):
        currency_rates =  [
            {   u'base': u'USD',
                u'date': u'2018-10-19',
                u'rates': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'CZK',
             u'date': u'2018-10-19',
             u'rates': {u'USD': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'EUR',
             u'date': u'2018-10-19',
             u'rates': {u'CZK': 22.5518744551, u'USD': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'PLN',
             u'date': u'2018-10-19',
             u'rates': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'USD': 3.7503923278}
             },
            ]
        transformed_rates = self.rate.transform_rates(currency_rates)
        success_rates = {'USD': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278},
            u'CZK': {u'USD': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278},
            u'EUR': {u'CZK': 22.5518744551, u'USD': 0.8718395815, u'PLN': 3.7503923278},
            u'PLN': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'USD': 3.7503923278}
             }
        self.assertDictEqual(success_rates, transformed_rates)

    def test_wrong_structure(self):
        currency_rates = [
            {
             u'date': u'2018-10-19',
             u'rates': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'CZK',
             u'date': u'2018-10-19',
             u'rates': {u'USD': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'EUR',
             u'date': u'2018-10-19',
             u'rates': {u'CZK': 22.5518744551, u'USD': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'PLN',
             u'date': u'2018-10-19',
             u'rates': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'USD': 3.7503923278}
             },
        ]
        with self.assertRaises(KeyError):
            self.rate.transform_rates(currency_rates)

    def test_wrong_structure2(self):
        currency_rates = [
            {u'base': u'USD',
             u'date': u'2018-10-19',
             },
            {u'base': u'CZK',
             u'date': u'2018-10-19',
             u'rates': {u'USD': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'EUR',
             u'date': u'2018-10-19',
             u'rates': {u'CZK': 22.5518744551, u'USD': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'PLN',
             u'date': u'2018-10-19',
             u'rates': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'USD': 3.7503923278}
             },
        ]

        with self.assertRaises(KeyError):
            self.rate.transform_rates(currency_rates)

    def test_structure_wo_date(self):
        currency_rates = [
            {u'base': u'USD',
             u'rates': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'CZK',
             u'date': u'2018-10-19',
             u'rates': {u'USD': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'EUR',
             u'date': u'2018-10-19',
             u'rates': {u'CZK': 22.5518744551, u'USD': 0.8718395815, u'PLN': 3.7503923278}
             },
            {u'base': u'PLN',
             u'date': u'2018-10-19',
             u'rates': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'USD': 3.7503923278}
             },
        ]
        transformed_rates = self.rate.transform_rates(currency_rates)
        success_rates = {u'USD': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278},
                         u'CZK': {u'USD': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278},
                         u'EUR': {u'CZK': 22.5518744551, u'USD': 0.8718395815, u'PLN': 3.7503923278},
                         u'PLN': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'USD': 3.7503923278}
                         }
        self.assertDictEqual(success_rates, transformed_rates)

    def test_empty(self):
        transform_rates = self.rate.transform_rates([])
        self.assertFalse(transform_rates)

    def test_none(self):
        with self.assertRaises(TypeError):
            self.rate.transform_rates(None)


class RatesWMockBase(OpenExchangeRatesBaseTest):

    def setUp(self):
        super(RatesWMockBase, self).setUp()
        self.patcher_call = mock.patch('exchangerates.api.OpenExchangeRates.get_one_rate')
        self.test_rates =  [
            {u'date': u'2018-10-19', u'base': u'CZK',
             u'rates': {u'PLN': 0.166300692, u'USD': 0.0443422121, u'EUR': 0.0386592956}},
            {u'date': u'2018-10-19', u'base': u'EUR',
             u'rates': {u'CZK': 25.867, u'USD': 1.147, u'PLN': 4.3017}},
            {u'date': u'2018-10-19', u'base': u'PLN',
             u'rates': {u'CZK': 6.0132040821, u'USD': 0.2666387707, u'EUR': 0.2324662343}},
            {u'date': u'2018-10-19', u'base': u'USD',
             u'rates': {u'CZK': 22.5518744551, u'PLN': 3.7503923278, u'EUR': 0.8718395815}}
        ]

    def tearDown(self):
        try:
            self.patcher_call.stop()
        except RuntimeError:
            pass


class GetLastRatesTest(RatesWMockBase):


    def test_success(self):

        func_call = self.patcher_call.start()
        func_call.side_effect = self.test_rates
        last_rates = self.rate.get_last_rates()
        self.assertEquals(self.test_rates, last_rates)

    def test_empty(self):
        func_call = self.patcher_call.start()
        rates = [
            {}, {}, {}, {}
        ]

        func_call.side_effect = rates
        last_rates = self.rate.get_last_rates()
        self.assertEquals(rates, last_rates)

    def test_raise(self):

        func_call = self.patcher_call.start()
        rates = [ApiException('')]

        func_call.side_effect = rates
        with self.assertRaises(ApiException):
            self.rate.get_last_rates()


class GetAndSaveLastRatesTest(RatesWMockBase):

    def setUp(self):
        '''
        remove json file if it exists
        :return:
        '''
        super(GetAndSaveLastRatesTest, self).setUp()
        if os.path.exists(settings.RATES_FNAME):
            os.remove(settings.RATES_FNAME)

    def tearDown(self):
        '''
        remove json file after using
        :return:
        '''
        super(GetAndSaveLastRatesTest, self).tearDown()
        if os.path.exists(settings.RATES_FNAME):
            os.remove(settings.RATES_FNAME)

    def test_success(self):

        func_call = self.patcher_call.start()
        func_call.side_effect = self.test_rates
        self.rate.get_and_save_last_rates()
        with open(settings.RATES_FNAME) as f:
            file_content = json.load(f)
        success = {
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
        self.assertEquals(success, file_content)

    def test_raise(self):
        func_call = self.patcher_call.start()
        func_call.side_effect = [ApiException('')]

        self.rate.get_and_save_last_rates()
        self.assertFalse(os.path.exists(settings.RATES_FNAME))

