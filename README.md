# currency-converse

Technology stack:
backend: Django 1.11, Python 2.7
frontend: Bootstrap 4.1.3, Jquery 3.3.1

Testing:
python manage.py test --settings=currency_converse.settings_test

Command for daily updating rates should be inserted in cron:
python manage.py get_currency_rates

Daily currency rates is saved in rates_data/last_rates.json