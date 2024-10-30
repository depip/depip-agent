import os
from dotenv import load_dotenv
import boto3
load_dotenv()

class Boto3Client:
    def __init__(self) -> None:
        self.client = boto3.client(
            service_name=os.getenv('AWS_SERVICE_NAME'),
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
        )