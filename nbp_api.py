import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NbpApi:
    """
    Class for getting values from NBP API
    """
    def __init__(self) -> None:
        self.base_url = 'https://api.nbp.pl/api/exchangerates/'

    def _make_request(self, url: str, clean_func: callable) -> list[dict]:
        """
        Make API request and clean the response
        """
        try:
            response = requests.get(url, timeout=120)
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

    def _validate_dates(self, start_date: str, end_date: str) -> None:
        """
        Validate date format and if is in right format and if end_date is not in the future
        """ 
        for date in (start_date, end_date):
            # Check format
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                logging.error(f'Invalid date format')
                raise
        
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        yesterday = datetime.today() - timedelta(days=1)
        
        # Check if end_date is not in the future
        if end_date_obj > yesterday:
            logging.error(f'End date {end_date} is in the future')
            raise ValueError(f'End date {end_date} is in the future')
        
    def adjust_start_date(self, start_date: str) -> str:
        """
        Adjust start date if it falls on a weekend
        """
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()

        if start_date_obj.weekday() == 5:  # 5 -> Saturday
            start_date_obj -= timedelta(days=1)  # Take Friday date
        elif start_date_obj.weekday() == 6:  # If Sunday -> take Friday date
            start_date_obj -= timedelta(days=2)

        return start_date_obj.strftime('%Y-%m-%d')

    def get_currency_list(self) -> list[dict]:
        """
        Get list of currencies and their codes
        """
        full_url = f'{self.base_url}tables/A/?format=json'  
        return self._make_request(full_url, self.clean_currency_list)  # Get currencies and their codes from API
        
    def get_currency_rates(self, curr_code: str, start_date: str, end_date: str) -> list[dict]:
        """
        Get list of certain currency rates from start_date to end_date
        """
        self._validate_dates(start_date, end_date)  # Validate dates
        valid_start_date = self.adjust_start_date(start_date)  # Check if start_date is not on the weekend
        
        full_url = f'{self.base_url}rates/A/{curr_code}/{valid_start_date}/{end_date}/?format=json'
        api_response = self._make_request(full_url, self.clean_currency_rates)  # Get rates for specific currency
        refactored_response = self.fill_missing_dates(api_response, start_date, end_date)  # Fill missing dates
        return refactored_response

    def clean_currency_list(self, api_response: dict) -> list[dict]:
        """
        Clean API response to get only currency name and its code
        """
        if api_response:
            rates = api_response[0].get('rates', [])
            return [{'currency': rate['currency'], 'code': rate['code']} for rate in rates]  # New dict with only needed keys and codes
        return []
    
    def clean_currency_rates(self, api_response: dict) -> list[dict]:
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

    def fill_missing_dates(self, data: list[dict], start_date: str, end_date: str) -> list[dict]:
        """
        NBP API does not provide data on weekends and holidays.
        Rates on missing days will be replaced with previous day rates or Friday rates if the missing day is weekend.
        """
        data_dict = {entry['effectiveDate']: entry['mid'] for entry in data}
        
        complete_data = []
        
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        last_mid  = None  # Empty placeholder

        current_date = start_date_obj
        while current_date <= end_date_obj:
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

            current_date += timedelta(days=1)  # To start next day

        complete_data = [
            # Leaves only dates from between start_date and end_date
            entry for entry in complete_data 
                if start_date_obj <= datetime.strptime(entry['effectiveDate'], '%Y-%m-%d').date() <= end_date_obj
        ]

        return complete_data
