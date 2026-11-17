# Libraries and Packages

import os
import json
import logging
import boto3
from dotenv import load_dotenv

# Authentication

load_dotenv()

AWS_ACCESS_KEY =os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Getting the file we want to upload

##test_file = '2026-11-11 15-36-09.json' - this was the undynamic hardcoded file to test##
data_dir = 'data'
file_location = os.listdir(data_dir) # Finds the data directory with all the json files in it - makes it dynamic

# Connecting to AWS 

s3_client = boto3.client(
    's3', # Specifically connects to s3 within AWS
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

# Upload the file to AWS

## s3_client.upload_file(file_location, # Is the local connection
                    ## AWS_BUCKET_NAME, # Where we want to save file 
                    ## test_file)  # The specific file we want to upload

#-----------------------------------------------------------🎀---------------------------------------------------------#

# Loop through each json file in data folder

for file in file_location: 
    to_upload = f'{data_dir}/{file}'
    try:
        s3_client.upload_file(
            to_upload, # goes through each file locally
            AWS_BUCKET_NAME, # bucket we want to put it in
            file) #what the file will be called in bucket
        print(f'{file} successfully uploaded')
        os.remove(to_upload) # removing files in local after
    except Exception as e:
        print(f'Something went wrong. Error: {e}')

#-------------------------------------
