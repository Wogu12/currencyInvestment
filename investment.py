from nbp_api import NbpApi

def main():
    print('start NBP API test')
    api = NbpApi()
    output = api.get_currency_rates('EUR', '2024-06-01', '2024-06-30')
    print(f'Response: {output}')

if __name__ == "__main__":
    main()