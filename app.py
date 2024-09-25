from flask import Flask, render_template, request
from nbp_api import NbpApi
from investment import Investment

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

nbp_api = NbpApi()

@app.route('/')
def index():

    currency_list = nbp_api.get_currency_list()
    
    return render_template('index.html', currency_list = currency_list)

@app.route('/analyze', methods=['POST'])
def analyze():
    curr_first = request.form.get('curr_first')
    percentage_first = request.form.get('percentage_first')
    
    curr_second = request.form.get('curr_second')
    percentage_second = request.form.get('percentage_second')
    
    curr_third = request.form.get('curr_third')
    percentage_third = request.form.get('percentage_third')

    start_date = request.form.get('start_date')

    currency_dict = {
        'first': {'currency': curr_first, 'percentage': percentage_first},
        'second': {'currency': curr_second, 'percentage': percentage_second},
        'third': {'currency': curr_third, 'percentage': percentage_third},
    }

    investment = Investment(currency_dict, start_date, nbp_api)

    investment.draw_currency_rates()

    last_total = investment.draw_investment_pln()
    bilance = last_total - 1000.0
    bilance = round(bilance, 2)

    start_values = {curr_first: percentage_first, curr_second: percentage_second, curr_third: percentage_third}
    investment.draw_start_pie(start_values)

    investment.draw_end_pie()
    highest_value, best_date = investment.when_to_leave()

    best_bilance = round((highest_value - 1000), 2)

    investment.plot_currency_allocation_over_time()
    
    
    return render_template('investmentResult.html', 
                           last_total = last_total, 
                           bilance = bilance, 
                           highest_value = highest_value, 
                           best_date = best_date, 
                           best_bilance = best_bilance, 
                           curr_first = curr_first, 
                           curr_second = curr_second, 
                           curr_third = curr_third,
                           percentage_first = percentage_first,
                           percentage_second = percentage_second,
                           percentage_third = percentage_third)

if __name__ == '__main__':
    app.run(debug=True)
