import os
import boto3
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
load_dotenv('.env') 


aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")
bucket_name = os.getenv("BUCKET_NAME")
s3_client = boto3.client('s3',
                         aws_access_key_id=aws_access_key,
                         aws_secret_access_key=aws_secret_key)
# initialize s3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key,
                  aws_secret_access_key=aws_secret_key)

# This is the prefix of the folder you want to access
folder_prefix = 'summary_statistics/'


# def update_s3_file(bucket_name, file_path):
#     # Get the object from the bucket
#     obj = s3.get_object(Bucket=bucket_name, Key=file_path)

#     # Check if the file is not empty
#     if obj['ContentLength'] > 0:
#         # Load the data into a pandas dataframe
#         try:
#             df = pd.read_csv(obj['Body'])
            
#             # Drop the unnecessary columns
#             df = df.drop(columns=['Unnamed: 0', 'Open', 'High', 'Low', 'TP', 'TP_SMA', 'MD', 'Pos', 'Balance', 'Return rate'])

#             # Use StringIO to convert the dataframe to csv format, it returns a file-like object that can be used as a file object
#             csv_buffer = StringIO()
#             df.to_csv(csv_buffer)

#             # Overwrite the object in the bucket
#             s3.put_object(Bucket=bucket_name, Key=file_path, Body=csv_buffer.getvalue())
#         except pd.errors.EmptyDataError:
#             print(f"File {file_path} is empty. Skipping.")
#     else:
#         print(f"File {file_path} is empty. Skipping.")


def update_s3_file(bucket_name, file_path):
    # Get the object from the bucket
    obj = s3.get_object(Bucket=bucket_name, Key=file_path)

    # Check if the file is not empty
    if obj['ContentLength'] > 0:
        # Load the data into a pandas dataframe
        try:
            df = pd.read_csv(obj['Body'])
            
            # Drop the unnecessary columns
            df = df.drop(columns=['Positive trading days'])

            # calculate average trade duration

            # Use StringIO to convert the dataframe to csv format, it returns a file-like object that can be used as a file object
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)

            # Overwrite the object in the bucket
            s3.put_object(Bucket=bucket_name, Key=file_path, Body=csv_buffer.getvalue())
        except pd.errors.EmptyDataError:
            print(f"File {file_path} is empty. Skipping.")
    else:
        print(f"File {file_path} is empty. Skipping.")

response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)

# Iterate through all your files in the specific folder and update
for obj in response['Contents']:
    file_path = obj['Key']
    update_s3_file(bucket_name, file_path)
