# -*- coding:utf-8 -*-

from django.core.management.base import BaseCommand

from exchangerates.api import OpenExchangeRates


class Command(BaseCommand):

    help = "Get last currency rates from https://api.exchangeratesapi.io"

    def handle(self, **options):

        rate = OpenExchangeRates()
        rate.get_and_save_last_rates()