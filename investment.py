from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from nbp_api import NbpApi

class Investment():
    def __init__(self, currency_dict, start_date, nbp_api):
        self.start_date = start_date
        self.nbp_api = nbp_api
        self.start_money = 1000
        self.first_currency = currency_dict.get('first')
        self.second_currency = currency_dict.get('second')
        self.third_currency = currency_dict.get('third')
        self.end_date = (datetime.strptime(self.start_date, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d')

    def analyze_investment(self):
        ...

