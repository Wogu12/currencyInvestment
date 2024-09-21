from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_values():
    api_url = 'https://api.nbp.pl/api/exchangerates/rates/A/USD/2024-08-01/2024-08-31/?format=json'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from API: {response.status_code}")
        return None
    
def get_table():
    api_url = 'https://api.nbp.pl/api/exchangerates/tables/A/?format=json'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]
    else:
        print(f"Error fetching data from API: {response.status_code}")
        return None

@app.route('/')
def index():
    data = get_values()
    curr = get_table()
    if data:
        return render_template('index.html', data=data, curr=curr)
    else:
        return "Error fetching data", 500

if __name__ == '__main__':
    app.run(debug=True)
