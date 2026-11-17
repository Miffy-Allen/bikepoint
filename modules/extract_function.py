import requests
import json
import os
from datetime import datetime, time
import logging 

#appends log with filename
logger = logging.getLogger(__name__)


# Creating a function for modularizing

def extract_to_json(url: str, data_dir: str, timestamp: str, max_attempts: int, delay: int):
    """Function to extract JSON files from a URL and save to a destination.

    Args:
        url (str): URL to pull data from
        data_dir (str): filepath to save data to
        timestamp (str): timestamp to append to file name
        max_retry (int): no of times to retry calls
        delay (int): how long to wait between call
    """    
    #Make directory if not exist
    os.makedirs(data_dir, exist_ok = True)
    #Want filename to make in function (contains data dir/timestamp)
    filename = f'{data_dir}/{timestamp}.json' 

    attempt = 1

    while attempt <= max_attempts:
        response = requests.get(url)
        status_code = response.status_code

        if 200 <= status_code <300:
            try:
                data = response.json()

                with open(filename, 'w') as file:
                    json.dump(data, file)
                print(f'File {filename} saved successfully')
                logger.info(f'File {filename} saved successfully')

                return True # if data return true - flag that iwas saved successfully
            
            except Exception as e:
                print(f'An error occured when saving the JSON: {e}')
                logger.error(f'An error occured when saving the JSON: {e}')
            break 

        elif 300 <=status_code < 500:

            print(f'API call failed, status code {status_code}')
            logger.error(f'API call failed, status code {status_code}')

            break

        else:
            if attempt == max_attempts:
                print(f'Max number of attempts reached. Status code {status_code}. Investigate further 👀')
                logger.warning(f'Max number of attempts reached. Status code {status_code}. Investigate further 👀')
            else: 
                print(f'Attempt {attempt} failed, ststus code {status_code}. Try again')
                logger.error(f'Attempt {attempt} failed, ststus code {status_code}. Try again')

            attempt += 1

            time.sleep(delay = 30)

    # return false value if goes wrong aka no data
    return False