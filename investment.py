from nbp_api import NbpApi

def main():
    print('start NBP API test')
    api = NbpApi()
    output = api.get_currency_rates('USD', '2024-08-01', '2024-08-31')
    print(f'Response: {output}')

if __name__ == "__main__":
    main()