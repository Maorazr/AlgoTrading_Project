import boto3
from botocore.exceptions import NoCredentialsError
from io import StringIO, BytesIO
bucket_name = 'algotradingproject'
access_key = 'AKIA4C5ZLMSXGT5GGTTU'
secret_key = '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'


def list_files_in_bucket():
    s3 = boto3.client('s3',
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
    response = s3.list_objects_v2(Bucket=bucket_name)
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
