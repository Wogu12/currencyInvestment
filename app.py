from flask import Flask, render_template, request
import requests
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
    
    return('hello world!')

if __name__ == '__main__':
    app.run(debug=True)
