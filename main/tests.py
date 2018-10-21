# -*- coding: utf-8 -*-

import json
import os

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.conf import settings

from exchangerates.const import CZECH_KRONA, US_DOLLAR

# Create your tests here.

class IndexTest(TestCase):

    def test_success(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(200, response.status_code)


class ApiTest(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        '''
        remove json file after using
        :return:
        '''
        if os.path.exists(settings.RATES_FNAME):
            os.remove(settings.RATES_FNAME)

    def test_success(self):
        self.__create_rate_file()

        data = {'from_currency': CZECH_KRONA,
                'to_currency': US_DOLLAR,
                'amount': 1000}
        response = self.client.post(reverse('currency_converse',), data=data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({u'currency': u'USD', u'converted_amount': u'44.34'},
                             response.json() )

    def test_empty_from_currency(self):

        data = {'from_currency': '',
                'to_currency': US_DOLLAR,
                'amount': 1000}
        response = self.client.post(reverse('currency_converse', ), data=data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'status': 400,
                                 'error': {
                                     'code': 1,
                                     'message': ['Param "from_currency" can\'t be empty',
                                                 'Param "from_currency" must be one of "CZK,EUR,PLN,USD" values']
                                 }},
                             response.json())

    def test_wrong_from_currency(self):
        data = {'from_currency': 'lkjhklh',
                'to_currency': US_DOLLAR,
                'amount': 1000}
        response = self.client.post(reverse('currency_converse', ), data=data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'status': 400,
                              'error': {
                                  'code': 1,
                                  'message': [
                                              'Param "from_currency" must be one of "CZK,EUR,PLN,USD" values']
                              }},
                             response.json())

    def test_empty_to_currency(self):

        data = {'from_currency': CZECH_KRONA,
                'to_currency': '',
                'amount': 1000}
        response = self.client.post(reverse('currency_converse', ), data=data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'status': 400,
                                 'error': {
                                     'code': 1,
                                     'message': ['Param "to_currency" can\'t be empty',
                                                 'Param "to_currency" must be one of "CZK,EUR,PLN,USD" values']
                                 }},
                             response.json())

    def test_wrong_to_currency(self):

        data = {'from_currency': CZECH_KRONA,
                'to_currency': 'abra',
                'amount': 1000}
        response = self.client.post(reverse('currency_converse', ), data=data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'status': 400,
                              'error': {
                                  'code': 1,
                                  'message': [
                                              'Param "to_currency" must be one of "CZK,EUR,PLN,USD" values']
                              }},
                             response.json())

    def test_wrong_amount(self):

        data = {'from_currency': CZECH_KRONA,
                'to_currency': US_DOLLAR,
                'amount': 'sfa'}
        response = self.client.post(reverse('currency_converse', ), data=data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'status': 400,
                              'error': {
                                  'code': 1,
                                  'message': [
                                              'Bad type of "amount" param']
                              }},
                             response.json())

    def test_empty_amount(self):

        data = {'from_currency': CZECH_KRONA,
                'to_currency': US_DOLLAR,
                'amount': ''}
        response = self.client.post(reverse('currency_converse', ), data=data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'status': 400,
                              'error': {
                                  'code': 1,
                                  'message': [
                                              'Bad type of "amount" param']
                              }},
                             response.json())

    def test_internal_error(self):

        data = {'from_currency': CZECH_KRONA,
                'to_currency': US_DOLLAR,
                'amount': 1000}
        response = self.client.post(reverse('currency_converse', ), data=data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'status': 500,
                             'error':{
                                 'code': 2,
                                 'message': 'Internal error'
                             }},
                             response.json())

    def __create_rate_file(self):
        rates = {
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
        with open(settings.RATES_FNAME, 'w') as f:
            json.dump(rates, f, indent=2)