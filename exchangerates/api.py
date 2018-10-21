# -*- coding: utf-8 -*-

import os
import json

from logging import getLogger

from django.conf import settings

import requests

from .const import CURRENCIES

log = getLogger(__name__)

class ApiException(Exception):
    pass


class OpenExchangeRates():

    BASE_PATH = 'https://api.exchangeratesapi.io/latest'

    def get_one_rate(self, base_currency):

        self.check_currency_param(base_currency)

        response = requests.get(self.BASE_PATH, params=self.format_params_for_request(base_currency))
        return response.json()

    def check_currency_param(self, base_currency):

        if not base_currency:
            raise ApiException('"base_currency" param can\'t be empty.')

        if base_currency not in CURRENCIES:
            raise ApiException('"base_currency" param must be on of "{}" values. Not {}'
                               .format(','.join(CURRENCIES), base_currency))

        return True

    def format_params_for_request(self, base_currency):

        self.check_currency_param(base_currency)

        return {'base': base_currency,
                'symbols': ','.join([symb for symb in CURRENCIES if symb != base_currency])
                }

    def get_last_rates(self):

        currency_rates = []
        for base_currency in CURRENCIES:
            currency_rates.append(self.get_one_rate(base_currency))
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
        if not os.path.exists(os.path.basename(settings.RATES_FNAME)):
            os.makedirs(os.path.basename(settings.RATES_FNAME))
        with open(settings.RATES_FNAME, 'w') as f:
            json.dump(rates_json, f, indent=2)

    def get_and_save_last_rates(self):
        try:
            currency_rates = self.get_last_rates()
        except ApiException as e:
            log.error(str(e))
            return
        except Exception as e:
            log.error(str(e))
            return

        rates_json = self.transform_rates(currency_rates)
        self.save_json_to_file(rates_json)


    # end