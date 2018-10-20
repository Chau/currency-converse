# -*- coding: utf-8 -*-

import os
import json

from django.conf import settings

import requests


from .const import CZECH_KRONA, POLISH_ZLOTY, EURO, US_DOLLAR

'''
u'AED': 3.673072,
  u'AFN': 75.999759,
  u'ALL': 108.55,
  u'AMD': 483.993889,
  u'ANG': 1.774556,
  u'AOA': 302.4385,
  u'ARS': 36.491,
  u'AUD': 1.4045,
  u'AWG': 1.800506,
  u'AZN': 1.7025,
  u'BAM': 1.705902,
  u'BBD': 2,
  u'BDT': 83.82,
  u'BGN': 1.701245,
  u'BHD': 0.377085,
  u'BIF': 1810,
  u'BMD': 1,
  u'BND': 1.410258,
  u'BOB': 6.911803,
  u'BRL': 3.712909,
  u'BSD': 1,
  u'BTC': 0.000155694547,
  u'BTN': 73.394096,
  u'BWP': 10.642022,
  u'BYN': 2.109496,
  u'BZD': 2.009512,
  u'CAD': 1.311501,
  u'CDF': 1625,
  u'CHF': 0.99595,
  u'CLF': 0.02338,
  u'CLP': 679.9,
  u'CNH': 6.936989,
  u'CNY': 6.9296,
  u'COP': 3073.657843,
  u'CRC': 592.933454,
  u'CUC': 1,
  u'CUP': 25.75,
  u'CVE': 96.3135,
  u'CZK': 22.4564,
  u'DJF': 178.05,
  u'DKK': 6.4798,
  u'DOP': 50.01,
  u'DZD': 118.66,
  u'EGP': 17.8915,
  u'ERN': 14.99774,
  u'ETB': 27.96,
  u'EUR': 0.86744,
  u'FJD': 2.142745,
  u'FKP': 0.764995,
  u'GBP': 0.764995,
  u'GEL': 2.44699,
  u'GGP': 0.764995,
  u'GHS': 4.84,
  u'GIP': 0.764995,
  u'GMD': 49.495,
  u'GNF': 9100,
  u'GTQ': 7.738117,
  u'GYD': 209.090351,
  u'HKD': 7.842132,
  u'HNL': 24.11005,
  u'HRK': 6.437929,
  u'HTG': 71.283974,
  u'HUF': 280.61,
  u'IDR': 15180.07,
  u'ILS': 3.6581,
  u'IMP': 0.764995,
  u'INR': 73.473469,
  u'IQD': 1191,
  u'IRR': 42495.975464,
  u'ISK': 117.070027,
  u'JEP': 0.764995,
  u'JMD': 134.56,
  u'JOD': 0.709506,
  u'JPY': 112.55,
  u'KES': 101.011175,
  u'KGS': 68.533355,
  u'KHR': 4069,
  u'KMF': 429.101075,
  u'KPW': 900,
  u'KRW': 1132.12,
  u'KWD': 0.303276,
  u'KYD': 0.833167,
  u'KZT': 366.11,
  u'LAK': 8541,
  u'LBP': 1513.937693,
  u'LKR': 171.458902,
  u'LRD': 157.125087,
  u'LSL': 14.4025,
  u'LYD': 1.38,
  u'MAD': 9.47596,
  u'MDL': 17.019918,
  u'MGA': 3515,
  u'MKD': 53.589064,
  u'MMK': 1591.184708,
  u'MNT': 2483.764134,
  u'MOP': 8.072848,
  u'MRO': 357,
  u'MRU': 35.9,
  u'MUR': 34.678,
  u'MVR': 15.450044,
  u'MWK': 727.192725,
  u'MXN': 19.269877,
  u'MYR': 4.158006,
  u'MZN': 60.64916,
  u'NAD': 14.425,
  u'NGN': 363.5,
  u'NIO': 32.275,
  u'NOK': 8.223347,
  u'NPR': 117.430825,
  u'NZD': 1.51653,
  u'OMR': 0.384873,
  u'PAB': 1,
  u'PEN': 3.32965,
  u'PGK': 3.355,
  u'PHP': 53.643753,
  u'PKR': 133.345,
  u'PLN': 3.7312,
  u'PYG': 5975.011193,
  u'QAR': 3.640999,
  u'RON': 4.055176,
  u'RSD': 102.866287,
  u'RUB': 65.4974,
  u'RWF': 871,
  u'SAR': 3.751235,
  u'SBD': 7.959857,
  u'SCR': 13.640868,
  u'SDG': 47.05,
  u'SEK': 8.9891,
  u'SGD': 1.377339,
  u'SHP': 0.764995,
  u'SLL': 8390,
  u'SOS': 580.25,
  u'SRD': 7.458,
  u'SSP': 130.2634,
  u'STD': 21117.219904,
  u'STN': 21.325,
  u'SVC': 8.747503,
  u'SYP': 515.000106,
  u'SZL': 14.425,
  u'THB': 32.5485,
  u'TJS': 9.422892,
  u'TMT': 3.499986,
  u'TND': 2.836894,
  u'TOP': 2.305893,
  u'TRY': 5.647492,
  u'TTD': 6.74175,
  u'TWD': 30.9025,
  u'TZS': 2290.6,
  u'UAH': 28.043,
  u'UGX': 3759.040139,
  u'USD': 1,
  u'UYU': 32.799887,
  u'UZS': 8220,
  u'VEF': 248471.708907,
  u'VES': 63.3213,
  u'VND': 23252.792672,
  u'VUV': 111.042095,
  u'WST': 2.624527,
  u'XAF': 569.00334,
  u'XAG': 0.06832703,
  u'XAU': 0.00081534,
  u'XCD': 2.70255,
  u'XDR': 0.717081,
  u'XOF': 569.00334,
  u'XPD': 0.00092297,
  u'XPF': 103.513126,
  u'XPT': 0.00120121,
  u'YER': 250.350747,
  u'ZAR': 14.403006,
  u'ZMW': 11.796963,
  u'ZWL': 322.355011
'''

class OpenExchangeRates():

    # BASE_PATH = 'https://openexchangerates.org/api/'
    BASE_PATH = 'https://api.exchangeratesapi.io/latest'
    CURRENCIES = [CZECH_KRONA, EURO, POLISH_ZLOTY, US_DOLLAR]
    RATES_FNAME = os.path.join(settings.BASE_DIR, 'rates_data', 'last_rates.json')

    # def full_url(self, endpoint):
    #     return '{base_path}{endpoint}'.format(base_path=self.BASE_PATH, endpoint=endpoint)

    def format_params_for_request(self, base_currency):
        return {'base': base_currency,
                'symbols': ','.join([symb for symb in self.CURRENCIES if symb != base_currency])
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
        for base_currency in self.CURRENCIES:
            currency_rates.append(self.get_last_one_rate(base_currency))
        return currency_rates

    def transform_rates(self, currency_rates):
        '''
        :currency_rates: List
        [
            {u'base': u'USD',
            u'date': u'2018-10-19',
            u'rates': {u'CZK': 22.5518744551, u'EUR': 0.8718395815, u'PLN': 3.7503923278}}, ]

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
        return

    def save_json_to_file(self, rates_json):
        with open(self.RATES_FNAME, 'w') as f:
            json.load(f, rates_json)

    def get_and_save_last_rates(self):
        currency_rates = self.get_last_rates()
        rates_json = self.transform_rates(currency_rates)
        self.save_json_to_file(rates_json)


    # end