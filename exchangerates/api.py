# -*- coding: utf-8 -*-

import os
import json

from django.conf import settings

import requests

from .const import CURRENCIES


class OpenExchangeRates():

    BASE_PATH = 'https://api.exchangeratesapi.io/latest'



    def format_params_for_request(self, base_currency):
        return {'base': base_currency,
                'symbols': ','.join([symb for symb in CURRENCIES if symb != base_currency])
                }

    def get_last_one_rate(self, base_currency):
        try:
            response = requests.get(self.BASE_PATH, params=self.format_params_for_request(base_currency))
        except:
            # TODO:
            pass
        return response.json()

    def get_last_rates(self):

        currency_rates = []
        for base_currency in CURRENCIES:
            currency_rates.append(self.get_last_one_rate(base_currency))
        return currency_rates

    def transform_rates(self, currency_rates):
        '''
        :currency_rates: List
        f.e.
        [
            {u'base': u'USD',
            u'date': u'2018-10-19',
            u'rates': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278}},
            ]

        :return: Dict
                {"USD": {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278},
                 "CZK": {},
                 "EUR": {},
                 "PLN": {}
                }
        '''
        res = {}
        for rate in currency_rates:
            res[rate['base']] = rate['rates']
        return res

    def save_json_to_file(self, rates_json):
        with open(settings.RATES_FNAME, 'w') as f:
            json.dump(rates_json, f, indent=2)

    def get_and_save_last_rates(self):
        currency_rates = self.get_last_rates()
        rates_json = self.transform_rates(currency_rates)
        self.save_json_to_file(rates_json)


    # end