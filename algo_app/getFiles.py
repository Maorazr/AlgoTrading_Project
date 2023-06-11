import boto3
from botocore.exceptions import NoCredentialsError
from io import StringIO, BytesIO
import pandas as pd
import json

global bucket_name
global access_key
global secret_key
global s3_client
global s3_resource
global my_bucket
bucket_name = 'algotradingproject'
access_key = 'AKIA4C5ZLMSXGT5GGTTU'
secret_key = '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'

s3_client = boto3.client('s3',
                         aws_access_key_id=access_key,
                         aws_secret_access_key=secret_key)

s3_resource = boto3.resource('s3')
my_bucket = s3_resource.Bucket(bucket_name)


def get_names(dir_name):
    files_names = []
    s3 = boto3.resource('s3',
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key)
    my_bucket = s3.Bucket(bucket_name)
    for object_summary in my_bucket.objects.filter(Prefix=dir_name):
        files_names.append(object_summary.key.replace(dir_name + '/', ''))
    return files_names[1:]


def list_files_in_bucket():
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    all_objects = response['Contents']
    filenames = [obj['Key'] for obj in all_objects]

    return filenames


def get_files_from_folder(folder_name):
    s3 = boto3.resource('s3',
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key)
    my_bucket = s3.Bucket(bucket_name)

    files = {}
    try:
        for s3_file in my_bucket.objects.filter(Prefix=folder_name):
            # to ensure it's a file, not a 'folder'
            if not s3_file.key.endswith("/"):
                body = s3_file.get()['Body'].read()
                # read the file and store in a dictionary
                files[s3_file.key] = BytesIO(body)
    except Exception as e:
        print(f"Error occurred: {e}")

    return files


def open_files_from_object(files):
    files_dict = {}
    for file_name, file_content in files.items():
        if file_name.endswith('.csv'):
            df = pd.read_csv(file_content)
            files_dict[file_name] = df
        elif file_name.endswith('.json'):
            data = json.load(file_content)
            files_dict[file_name] = data

    return files_dict


def get_df_from_s3_folder(folder_name):

    df_dict = {}
    try:
        for s3_file in my_bucket.objects.filter(Prefix=folder_name):
            # to ensure it's a file, not a 'folder'
            if not s3_file.key.endswith("/") and s3_file.key.endswith(".csv"):
                body = s3_file.get()['Body'].read()
                # read the file and store in a dictionary
                df = pd.read_csv(BytesIO(body))
                df_dict[s3_file.key] = df
    except NoCredentialsError:
        print("Credentials not available")

    return df_dict


def get_json_from_s3_folder(folder_name):
    json_dict = {}
    try:
        for s3_file in my_bucket.objects.filter(Prefix=folder_name):
            # to ensure it's a file, not a 'folder'
            if not s3_file.key.endswith("/") and s3_file.key.endswith(".json"):
                body = s3_file.get()['Body'].read().decode('utf-8')
                # read the file and store in a dictionary
                json_content = json.loads(body)
                json_dict[s3_file.key] = json_content
    except NoCredentialsError:
        print("Credentials not available")

    return json_dict


def get_default_file(file_key, type):
    if (type == 'csv'):
        csv_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        csv_data = csv_obj['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data), parse_dates=['Date'])
        return df
    elif (type == 'json'):
        csv_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        csv_data = csv_obj['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))
        return df
        # json_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        # json_data = json_obj['Body'].read().decode('utf-8')
        # data = json.loads(json_data)
        # return data
