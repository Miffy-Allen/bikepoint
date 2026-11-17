from datetime import datetime
from modules.extract_function import extract_to_json # adding the extract_function in
from modules.load_function import load_to_s3 # adding load_function
import logging
import os
from dotenv import load_dotenv

# Authentication

load_dotenv()

AWS_ACCESS_KEY =os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# add the logging in - modularize this 
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_filename = f'{log_dir}/{timestamp}.log'

logging.basicConfig(
    filename=log_filename,
    format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO  
)

logger = logging.getLogger()
logger.info('Logger was successfully initialised')

#add the url/data directory for extract_function
url = 'https://api.tfl.gov.uk/BikePoint/'
data_dir = 'data'

extract_result = extract_to_json(url, data_dir, timestamp, max_attempts= 3, delay =10)

if extract_result:
    #run load to s3
    load_to_s3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, data_dir)
else:
    logger.info('Extract saved no data, nothing to attempt to upload so aborted')
