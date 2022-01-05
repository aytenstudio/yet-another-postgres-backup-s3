import os
import boto3
from botocore.client import Config
from datetime import datetime


class UploadHandler:
    def __init__(self):
        """
            in order to set environment variables.
        """
        try:
            # AWS related environment variables
            self.__AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
            self.__AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
            
            # endpint, file name & path , bucket name and signature version environment variables
            self.__ENDPOINT_URL = os.environ['ENDPOINT_URL']
            self.__UPLOADING_FILE_PATH = os.environ['UPLOADING_FILE_PATH']
            self.__DESTINATION_BUCKET_NAME = os.environ['DESTINATION_BUCKET_NAME']
            self.__SIGNATURE_VERSION = os.environ['SIGNATURE_VERSION']
            self.__MAX_NUMBER_BACKUPS = int(os.environ['MAX_NUMBER_BACKUPS'])

            # set resource client
            self.s3_resource_client = boto3.resource('s3',
                                endpoint_url=self.__ENDPOINT_URL,
                                aws_access_key_id=self.__AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=self.__AWS_SECRET_ACCESS_KEY,
                                config=Config(signature_version=self.__SIGNATURE_VERSION))

        except Exception as error:
            print(f'can not continue the process due to : {error} is None')
            exit(0)


    def upload_file(self):
        """
            upload files to destination bucket.
        """
        try:
            bucket = self.s3_resource_client.Bucket(self.__DESTINATION_BUCKET_NAME)

            # reverse sorting objects by their last_modified date so the last object in the list is the oldest one.
            all_objects = [obj for obj in sorted(bucket.objects.all(), key=lambda obj: obj.last_modified, reverse=True)]

            # if number of objects in the bucket reached to the maximum number of objects, delete the oldest objects.
            while len(all_objects) >= self.__MAX_NUMBER_BACKUPS:
                all_objects.pop().delete()

            # objects are saved with their uploading utc date time. 
            result = bucket.upload_file(self.__UPLOADING_FILE_PATH, f'{datetime.utcnow()}.dump')

            print(f'current objects in the bucket : {[obj.key for obj in bucket.objects.all()]}')

                

        except Exception as error:
            print(f'can not continue the process due to : {error}')
            exit(0)

        else:
            # remove temporary files after uploading them to bucket.
            os.remove(self.__UPLOADING_FILE_PATH)
            return result
