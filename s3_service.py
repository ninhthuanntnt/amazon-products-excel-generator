import datetime
import mimetypes
import threading
import traceback
from logging import Logger

import boto3
import logging
import time

from random_util import RandomUtil

class S3Service:
    s3_client: object
    bucket_name: str
    retries: int
    logger: Logger

    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.session.Session().client("s3")
        self.retries = 3
        self.logger = logging.getLogger(self.__class__.__name__)

    def upload(self, file_path: str, key: str) -> str:
        count: int = self.retries

        while (count > 0):
            self.logger.info("Start upload s3 file: {0} with target key: {1}".format(file_path, key));
            content_type, content_encoding = mimetypes.guess_type(file_path)
            response = self.s3_client.upload_file(file_path, self.bucket_name, key, ExtraArgs = {"ContentType": content_type})
            self.logger.info("Uploaded successfully")
            print("Thread ID:", threading.get_ident())

            return response
