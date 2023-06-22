# from io import StringIO
from io import BytesIO
from tqdm import tqdm
import boto3
# from tqdm import tqdm

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

    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    progress = tqdm(total=df.size, unit='B', unit_scale=True)

    def progress_callback(sent):
        progress.update(sent)

    s3_client.upload_fileobj(
        csv_buffer, bucket_name, f'{folder_name}/{file_name}', Callback=progress_callback)

    progress.close()
