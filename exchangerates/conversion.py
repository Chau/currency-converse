# -*- coding: utf-8 -*-

import json

from django.conf import settings
from logging import getLogger

log = getLogger(__name__)


class ConvertRate():

    def __init__(self, from_currency, to_currency, amount):

        self.from_currency = from_currency
        self.to_currency = to_currency
        self.amount = amount
        self.rate = None

    def get_last_rate_from_file(self):
        with open(settings.RATES_FNAME) as f:
            rates_json = json.load(f)
        return rates_json

    def find_rate(self, rates_json):
        from_currency_rates = rates_json.get(self.from_currency)
        self.rate = from_currency_rates.get(self.to_currency)
        return self.rate

    def format_amount(self, amount):
        return '{:,.2f}'.format(amount).replace(',', ' ')

    def convert(self):
        try:
            rates_json = self.get_last_rate_from_file()
            rate = float(self.find_rate(rates_json))
            return self.format_amount(self.amount * rate)
        except Exception as e:
            log.error(str(e))
            raise type(e)

# end
