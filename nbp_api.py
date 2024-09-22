import requests
import logging
from datetime import datetime, timedelta


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NbpApi:
    """
    Class for getting values from NBP API
    """
    def __init__(self):
        self.base_url = 'https://api.nbp.pl/api/exchangerates/'

    def _make_request(self, url, clean_func):
        """
        Make API request and clean the response
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return clean_func(response.json())
        except requests.exceptions.RequestException as e:
            logging.error(f'Error while connecting to API: {e}')
            return []
        except ValueError as json_error:
            logging.error(f'Error while parsing JSON: {json_error}')
            return []
        except Exception as e:
            logging.error(f'Error: {e}')
            return []

    def _validate_dates(self, start_date, end_date):
        """
        Validate date format and if date exist
        """ 
        for date in (start_date, end_date):
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                logging.error(f'Invalid date format')
                raise
        
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        yesterday = datetime.today() - timedelta(days=1)

        if end_date_obj > yesterday:
            logging.error(f'End date {end_date} is in the future')
            raise ValueError(f'End date {end_date} is in the future')
        
    def adjust_start_date(self, start_date):
        """
        Adjust start date if it falls on a weekend
        """
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()

        if start_date_obj.weekday() == 5:
            start_date_obj -= timedelta(days=1)
        elif start_date_obj.weekday() == 6:
            start_date_obj -= timedelta(days=2)

        return start_date_obj.strftime('%Y-%m-%d')

    def get_currency_list(self):
        """
        Get list of currencies and their codes
        """
        full_url = f'{self.base_url}tables/A/?format=json'
        return self._make_request(full_url, self.clean_currency_list)
        
        
    def get_currency_rates(self, curr_code, start_date, end_date):
        """
        Get list of certain currency rates from start_date to end_date
        """
        self._validate_dates(start_date, end_date)
        valid_start_date = self.adjust_start_date(start_date)
        
        full_url = f'{self.base_url}rates/A/{curr_code}/{valid_start_date}/{end_date}/?format=json'
        api_response = self._make_request(full_url, self.clean_currency_rates)
        refactored_response = self.fill_missing_dates(api_response, start_date, end_date)
        return refactored_response

    def clean_currency_list(self, api_response):
        """
        Clean API response to get only currency name and its code
        """
        if api_response:
            rates = api_response[0].get('rates', [])
            return [{'currency': rate['currency'], 'code': rate['code']} for rate in rates]
        return []
    
    def clean_currency_rates(self, api_response):
        """
        Delete unnecessary "no" key
        """
        if api_response:
            rates = api_response.get('rates', [])
            for rate in rates:
                if "no" in rate:
                    del rate["no"]
            return rates
        return []

    def fill_missing_dates(self, data, start_date, end_date):
        """
        NBP API does not provide data on weekends.
        Rates on weekends will be replaced with friday rates.
        """

        data_dict = {entry['effectiveDate']: entry['mid'] for entry in data}
        
        complete_data = []
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        last_mid = None  

        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            if date_str in data_dict:
                last_mid = data_dict[date_str]
                complete_data.append({'effectiveDate': date_str, 'mid': last_mid})
            else:
                if current_date.weekday() < 5: 
                    if last_mid is not None:
                        complete_data.append({'effectiveDate': date_str, 'mid': last_mid})
                else:
                    backtrack_date = current_date
                    while backtrack_date.weekday() >= 5:
                        backtrack_date -= timedelta(days=1)
                    
                    backtrack_date_str = backtrack_date.strftime('%Y-%m-%d')
                    if backtrack_date_str in data_dict:
                        last_mid = data_dict[backtrack_date_str]
                        complete_data.append({'effectiveDate': date_str, 'mid': last_mid})

            current_date += timedelta(days=1)

        complete_data = [
            entry for entry in complete_data 
            if start_date <= datetime.strptime(entry['effectiveDate'], '%Y-%m-%d').date() <= end_date
        ]

        return complete_data