import os
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg') #not a windowed application, must set this to generate graphs
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Investment():
    def __init__(self, currency_dict, start_date, nbp_api):
        self.start_date = start_date
        self.nbp_api = nbp_api
        self.start_money = 1000
        self.first_currency_dict = currency_dict.get('first')
        self.second_currency_dict = currency_dict.get('second')
        self.third_currency_dict = currency_dict.get('third')
        self.end_date = (datetime.strptime(self.start_date, '%Y-%m-%d') + timedelta(days=29)).strftime('%Y-%m-%d') #days=29 because start date + 29days = 30 days
        self.graph_directory = os.path.join('static', 'graphs') #set path to graphs
        self.value_for_first = []
        self.value_for_second = []
        self.value_for_third = []
        self.total_value = []

    def _get_currency_rates(self):
        #first currency
        first_currency = self.nbp_api.get_currency_rates(self.first_currency_dict.get('currency'), self.start_date, self.end_date)

        #second currency
        second_currency = self.nbp_api.get_currency_rates(self.second_currency_dict.get('currency'), self.start_date, self.end_date)

        #third currency
        third_currency = self.nbp_api.get_currency_rates(self.third_currency_dict.get('currency'), self.start_date, self.end_date)

        return first_currency, second_currency, third_currency
    
    def _get_currency_percentage(self):
        first_percent = self.first_currency_dict.get('percentage')

        second_percent = self.second_currency_dict.get('percentage')

        third_percent = self.third_currency_dict.get('percentage')

        return first_percent, second_percent, third_percent
    
    def _get_dates_and_mid(self):
        first_currency, second_currency, third_currency = self._get_currency_rates()
        
        dates = []
        first_rate_value = []
        second_rate_value = []
        third_rate_value = []

        for first, second, third in zip(first_currency, second_currency, third_currency):
            dates.append(datetime.strptime(first.get('effectiveDate'), '%Y-%m-%d'))
            first_rate_value.append(first.get('mid'))
            second_rate_value.append(second.get('mid'))
            third_rate_value.append(third.get('mid'))

        return dates, first_rate_value, second_rate_value, third_rate_value

    def analyze_investment(self):
        ...

    def draw_start_pie(self, start_values):
        currencies = list(start_values.keys())
        values = list(start_values.values())
        
        self._configure_pie_chart('Procentowy podział walut na początku inwestycji', values, currencies, 'pie_chart_start.png')

    def draw_end_pie(self):
        last_total = round(self.total_value[-1], 2)
        last_first_value = round(self.value_for_first[-1], 2)
        last_second_value = round(self.value_for_second[-1], 2)
        last_third_value = round(self.value_for_third[-1], 2)

        first_percentage = (last_first_value / last_total) * 100
        second_percentage = (last_second_value / last_total) * 100
        third_percentage = (last_third_value / last_total) * 100

        first_percentage = round(first_percentage, 4)
        second_percentage = round(second_percentage, 4)
        third_percentage = round(third_percentage, 4)

        currencies = [self.first_currency_dict.get('currency'), self.second_currency_dict.get('currency'), self.third_currency_dict.get('currency')]
        values = [first_percentage, second_percentage, third_percentage]

        self._configure_pie_chart('Procentowy podział walut na koniec inwestycji', values, currencies, 'pie_chart_end.png')

    def when_to_leave(self):
        dates, _, _, _ = self._get_dates_and_mid()

        best_date = None
        highest_value = 0

        for date, value in zip(dates, self.total_value):
            if value > highest_value:
                highest_value = value
                best_date = date

        highest_value = round(highest_value, 2)
        best_date = best_date.strftime('%Y-%m-%d')

        return highest_value, best_date

    def draw_investment_pln(self):
        first_percent, second_percent, third_percent = self._get_currency_percentage()

        first_investment_value = self.start_money * (float(first_percent)*0.01)
        second_investment_value = self.start_money * (float(second_percent)*0.01)
        third_investment_value = self.start_money * (float(third_percent)*0.01)

        dates, first_rate_values, second_rate_values, third_rate_values = self._get_dates_and_mid()

        first_bought = first_investment_value / first_rate_values[0] 
        second_bought = second_investment_value / second_rate_values[0]
        third_bought = third_investment_value / third_rate_values[0]

        for first_rate, second_rate, third_rate in zip(first_rate_values, second_rate_values, third_rate_values):
            first_to_pln = first_bought * first_rate
            second_to_pln = second_bought * second_rate
            third_to_pln = third_bought * third_rate

            self.value_for_first.append(first_to_pln)
            self.value_for_second.append(second_to_pln)
            self.value_for_third.append(third_to_pln)

        for value_first, value_second, value_third in zip(self.value_for_first, self.value_for_second, self.value_for_third):
            self.total_value.append(value_first + value_second + value_third)

        plt.plot(dates, self.value_for_first, marker ='.', linestyle = '-', color = 'r', label=f"{self.first_currency_dict.get('currency')} {first_percent}%")
        plt.plot(dates, self.value_for_second, marker ='.', linestyle = '-', color = 'g', label=f"{self.second_currency_dict.get('currency')} {second_percent}%")
        plt.plot(dates, self.value_for_third, marker ='.', linestyle = '-', color = 'b', label=f"{self.third_currency_dict.get('currency')} {third_percent}%")

        self._configure_graph('przebieg inwestycji w PLN w ciągu inwestycji (30 dni)', 'Cena waluty', dates, 'investment_in_pln.png')

        last_total = self.total_value[-1]
        last_total = round(last_total, 2)
        return last_total
    
    def draw_currency_rates(self):
        dates, first_rate_value, second_rate_value, third_rate_value = self._get_dates_and_mid()

        plt.plot(dates, first_rate_value, marker = '.', linestyle = '-', color = 'r', label = self.first_currency_dict.get('currency'))
        plt.plot(dates, second_rate_value, marker = '.', linestyle = '-', color = 'g', label = self.second_currency_dict.get('currency'))
        plt.plot(dates, third_rate_value, marker = '.', linestyle = '-', color = 'b', label = self.third_currency_dict.get('currency'))

        self._configure_graph('Cena za wybrane waluty w ciągu inwestycji (30 dni)', 'Cena waluty', dates, 'currency_rates.png')    
            
    def _configure_graph(self, title, ylabel, dates, file_name):
        plt.xlabel('Data')
        plt.ylabel(ylabel)
        plt.title(title)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.xticks(rotation=90)
        plt.xlim(dates[0], dates[-1])
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        if not os.path.exists(self.graph_directory): #if no graph dir - make one
            os.makedirs(self.graph_directory)

        plt.savefig(os.path.join(self.graph_directory, file_name), bbox_inches='tight')
        plt.close()

    def _configure_pie_chart(self, title, values, currencies, file_name):
        plt.figure(figsize=(7, 7))
        plt.pie(values, labels = currencies, autopct='%1.1f%%', startangle=140)
        plt.title(title)

        if not os.path.exists(self.graph_directory): #if no graph dir - make one
            os.makedirs(self.graph_directory)

        plt.savefig(os.path.join(self.graph_directory, file_name), bbox_inches='tight')
        plt.close()

    def plot_currency_allocation_over_time(self):
        dates, _, _, _ = self._get_dates_and_mid()

        first_percentage_alloc = []
        second_percentage_alloc = []
        third_percentage_alloc = []

        for first, second, third, total in zip(self.value_for_first, self.value_for_second, self.value_for_third, self.total_value):
            first_percentage_alloc.append((first / total) * 100)
            second_percentage_alloc.append((second / total) * 100)
            third_percentage_alloc.append((third / total) * 100)

        plt.plot(dates, first_percentage_alloc, marker = '.', linestyle = '-', color = 'r', label = self.first_currency_dict.get('currency'))
        plt.plot(dates, second_percentage_alloc, marker = '.', linestyle = '-', color = 'g', label = self.second_currency_dict.get('currency'))
        plt.plot(dates, third_percentage_alloc, marker = '.', linestyle = '-', color = 'b', label = self.third_currency_dict.get('currency'))

        self._configure_graph('Procentowy udział walut w czasie', '%', dates, 'percentage_allocation_chart.png')