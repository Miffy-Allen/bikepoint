import boto3
import logging
import os

# ensure logger will work in main:

logger = logging.getLogger(__name__)

# creating a function for modularizing

def load_to_s3(AWS_ACCESS_KEY: str, AWS_SECRET_ACCESS_KEY: str, AWS_BUCKET_NAME: str, data_dir: str): #dynamically changing things that need to be set before i call the function or in function - if used twice by diff functions needs to be outside
    """_summary_

    Args:
        AWS_ACCESS_KEY (str): Key Value - get value from your .env file
        AWS_SECRET_ACCESS_KEY (str): Secret Key - get value from your .env file
        AWS_BUCKET_NAME (str): Bucket Name - get value from your .env file
        data_dir (str): filepath to save data to
    """    

    s3_client = boto3.client(
        's3', # Specifically connects to s3 within AWS
        aws_access_key_id = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    
    file_location = os.listdir(data_dir) 

    for file in file_location: 
        to_upload = f'{data_dir}/{file}'
        try:
            s3_client.upload_file(
                to_upload, # goes through each file locally
                AWS_BUCKET_NAME, # bucket we want to put it in
                file) #what the file will be called in bucket
            print(f'{file} successfully uploaded')
            logger.info(f'{file} successfully uploaded')
            os.remove(to_upload) # removing files in local after
        except Exception as e:
            print(f'Something went wrong. Error: {e}')
            logger.error(f'Something went wrong. Error: {e}')