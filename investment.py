import os
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

matplotlib.use('Agg') #not a windowed application, must set this to generate graphs

class Investment():
    def __init__(self, currency_dict: dict[str, dict[str, str]], start_date: str, nbp_api):
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

    def _get_currency_rates(self) -> tuple[list[dict[str, float]], list[dict[str, float]], list[dict[str, float]]]:
        """
        Get rates for each currency from NbpApi
        """
        #first currency
        first_currency = self.nbp_api.get_currency_rates(self.first_currency_dict.get('currency'), self.start_date, self.end_date)

        #second currency
        second_currency = self.nbp_api.get_currency_rates(self.second_currency_dict.get('currency'), self.start_date, self.end_date)

        #third currency
        third_currency = self.nbp_api.get_currency_rates(self.third_currency_dict.get('currency'), self.start_date, self.end_date)

        return first_currency, second_currency, third_currency
    
    def _get_currency_percentage(self) -> tuple[float, float, float]:
        """
        Get percentage share for each currency
        """
        first_percent = self.first_currency_dict.get('percentage')

        second_percent = self.second_currency_dict.get('percentage')

        third_percent = self.third_currency_dict.get('percentage')

        return first_percent, second_percent, third_percent
    
    def _get_dates_and_mid(self) -> tuple[list[datetime], list[float], list[float], list[float]]:
        """
        Get dates and values for each currency
        """
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
    
    def when_to_leave(self) -> tuple[float, str]:
        """
        Calculate when user should leave investment to get the best outcome
        """
        dates, _, _, _ = self._get_dates_and_mid() #get only dates

        best_date = None
        highest_value = 0

        for date, value in zip(dates, self.total_value):
            if value > highest_value: #if current value is better than previous higheset -> take current
                highest_value = value
                best_date = date

        highest_value = round(highest_value, 2) #round highest value
        best_date = best_date.strftime('%Y-%m-%d') #assure good format of date

        return highest_value, best_date

    def analyze_investment(self, start_values: dict[str, float]) -> tuple[float, float, str, float, float]:
        """
        Pack all needed function to carry out analysis into one function
        """
        self.draw_currency_rates()

        last_total = self.draw_investment_pln()
        bilance = last_total - 1000.0
        bilance = round(bilance, 2)

        self.draw_start_pie(start_values)

        self.draw_end_pie()
        highest_value, best_date = self.when_to_leave()

        best_bilance = round((highest_value - 1000), 2)

        self.plot_currency_allocation_over_time()

        return last_total, highest_value, best_date, bilance, best_bilance

    def draw_start_pie(self, start_values: dict[str, float]) -> None:
        """
        Draw pie chart for percentage share of currencies in the investment at the beginning
        """
        currencies = list(start_values.keys())
        values = list(start_values.values())
        
        self._configure_pie_chart('Procentowy podział walut na początku inwestycji', values, currencies, 'pie_chart_start.png')

    def draw_end_pie(self) -> None:
        """
        Draw pie chart for percentage share of currencies in the investment at the end
        """
        #rounded last values 
        last_total = round(self.total_value[-1], 2)
        last_first_value = round(self.value_for_first[-1], 2)
        last_second_value = round(self.value_for_second[-1], 2)
        last_third_value = round(self.value_for_third[-1], 2)

        #calculate percentages
        first_percentage = round(((last_first_value / last_total) * 100), 2)
        second_percentage = round(((last_second_value / last_total) * 100), 2)
        third_percentage = round(((last_third_value / last_total) * 100), 2)

        currencies = [self.first_currency_dict.get('currency'), self.second_currency_dict.get('currency'), self.third_currency_dict.get('currency')] #get currencies codes
        values = [first_percentage, second_percentage, third_percentage] #pack in array for drawing pie chart

        self._configure_pie_chart('Procentowy podział walut na koniec inwestycji', values, currencies, 'pie_chart_end.png')

    def draw_investment_pln(self) -> float:
        """
        Draw line chart to show how investment proceeds in PLN
        """
        first_percent, second_percent, third_percent = self._get_currency_percentage()

        #calculate how much user bought with given percentages
        first_investment_value = self.start_money * (float(first_percent)*0.01)
        second_investment_value = self.start_money * (float(second_percent)*0.01)
        third_investment_value = self.start_money * (float(third_percent)*0.01)

        #get dates with mid value
        dates, first_rate_values, second_rate_values, third_rate_values = self._get_dates_and_mid()

        #calculate how much of currency user bought
        first_bought = first_investment_value / first_rate_values[0] 
        second_bought = second_investment_value / second_rate_values[0]
        third_bought = third_investment_value / third_rate_values[0]

        #change from currencies to PLN
        for first_rate, second_rate, third_rate in zip(first_rate_values, second_rate_values, third_rate_values):
            first_to_pln = first_bought * first_rate
            second_to_pln = second_bought * second_rate
            third_to_pln = third_bought * third_rate

            self.value_for_first.append(first_to_pln)
            self.value_for_second.append(second_to_pln)
            self.value_for_third.append(third_to_pln)

        #calculate sum of all currencies for each day
        for value_first, value_second, value_third in zip(self.value_for_first, self.value_for_second, self.value_for_third):
            self.total_value.append(value_first + value_second + value_third)

        plt.plot(dates, self.value_for_first, marker ='.', linestyle = '-', color = 'r', label=f"{self.first_currency_dict.get('currency')} {first_percent}%")
        plt.plot(dates, self.value_for_second, marker ='.', linestyle = '-', color = 'g', label=f"{self.second_currency_dict.get('currency')} {second_percent}%")
        plt.plot(dates, self.value_for_third, marker ='.', linestyle = '-', color = 'b', label=f"{self.third_currency_dict.get('currency')} {third_percent}%")

        self._configure_graph('przebieg inwestycji w PLN w ciągu inwestycji (30 dni)', 'Cena waluty', dates, 'investment_in_pln.png')

        #get total value of last day and round
        last_total = self.total_value[-1]
        last_total = round(last_total, 2)
        return last_total
    
    def draw_currency_rates(self) -> None:
        """
        Draw line chart to show how much did each currency cost for each day
        """
        dates, first_rate_value, second_rate_value, third_rate_value = self._get_dates_and_mid()

        plt.plot(dates, first_rate_value, marker = '.', linestyle = '-', color = 'r', label = self.first_currency_dict.get('currency'))
        plt.plot(dates, second_rate_value, marker = '.', linestyle = '-', color = 'g', label = self.second_currency_dict.get('currency'))
        plt.plot(dates, third_rate_value, marker = '.', linestyle = '-', color = 'b', label = self.third_currency_dict.get('currency'))

        self._configure_graph('Cena za wybrane waluty w ciągu inwestycji (30 dni)', 'Cena waluty', dates, 'currency_rates.png')    
            
    def _configure_graph(self, title: str, ylabel: str, dates: list[datetime], file_name: str) -> None:
        """
        Modularize repeatable elements of code for drawing line charts
        """
        plt.xlabel('Data')
        plt.ylabel(ylabel)
        plt.title(title)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1)) #set grid to show everyday
        plt.xticks(rotation=90)
        plt.xlim(dates[0], dates[-1]) #ensure that first dot starts on Y axis
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        if not os.path.exists(self.graph_directory): #if no graph dir - make one
            os.makedirs(self.graph_directory)

        plt.savefig(os.path.join(self.graph_directory, file_name), bbox_inches='tight')
        plt.close()

    def _configure_pie_chart(self, title: str, values: list[float], currencies: list[str], file_name: str) -> None:
        """
        Modularize repeatable elements of code for drawing pie charts
        """
        plt.figure(figsize=(7, 7))
        plt.pie(values, labels = currencies, autopct='%1.1f%%', startangle=140) #autopct -> decimal places
        plt.title(title)

        if not os.path.exists(self.graph_directory): #if no graph dir - make one
            os.makedirs(self.graph_directory)

        plt.savefig(os.path.join(self.graph_directory, file_name), bbox_inches='tight')
        plt.close()

    def plot_currency_allocation_over_time(self) -> None:
        """
        Draw line chart for how percentage share of currencies changed over dates
        """
        dates, _, _, _ = self._get_dates_and_mid() #get only dates

        #placeholders
        first_percentage_alloc = []
        second_percentage_alloc = []
        third_percentage_alloc = []

        #calculate percentage share for each day
        for first, second, third, total in zip(self.value_for_first, self.value_for_second, self.value_for_third, self.total_value):
            first_percentage_alloc.append((first / total) * 100)
            second_percentage_alloc.append((second / total) * 100)
            third_percentage_alloc.append((third / total) * 100)

        plt.plot(dates, first_percentage_alloc, marker = '.', linestyle = '-', color = 'r', label = self.first_currency_dict.get('currency'))
        plt.plot(dates, second_percentage_alloc, marker = '.', linestyle = '-', color = 'g', label = self.second_currency_dict.get('currency'))
        plt.plot(dates, third_percentage_alloc, marker = '.', linestyle = '-', color = 'b', label = self.third_currency_dict.get('currency'))

        self._configure_graph('Procentowy udział walut w czasie', '%', dates, 'percentage_allocation_chart.png')
