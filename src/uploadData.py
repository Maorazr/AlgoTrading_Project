from io import StringIO
import boto3

global bucket_name
global access_key
global secret_key
global s3_client
global my_bucket
bucket_name = 'algotradingproject'
access_key = 'AKIA4C5ZLMSXERDLI3HV'
secret_key = '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'


def upload_data_to_s3(df, folder_name, file_name):
    s3_client = boto3.client('s3',
                             aws_access_key_id='AKIA4C5ZLMSXERDLI3HV',
                             aws_secret_access_key='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')

    s3_resource = boto3.resource('s3', aws_access_key_id='AKIA4C5ZLMSXERDLI3HV',
                                 aws_secret_access_key='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')
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3_resource.Object(
        bucket_name, f'{folder_name}/{file_name}').put(Body=csv_buffer.getvalue())
