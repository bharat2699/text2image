from botocore.client import Config
import boto3
from botocore.exceptions import ClientError
from text2image import settings
from rest_framework import exceptions
from datetime import datetime
import os
from hashlib import md5

from common.helpers.constants import StatusCodes


class AwsS3Client:
    def __init__(self, bucket: str):
        self.bucket = bucket
        self.writer = boto3.resource(
            "s3", config=Config(signature_version="s3v4")
        ).Bucket(bucket)
        self.client = boto3.client(
            "s3",
            config=Config(signature_version="s3v4", region_name=settings.AWS_REGION),
        )

    def upload(self, bytes: bytes, mime: str, path: str):
        res = self.writer.put_object(Key=path, Body=bytes, ContentType=mime)
        return res

    def build_path(self, b: bytes):
        md5_hash = md5(b).hexdigest()
        return f"{md5_hash}"

    def get_presigned_url(self, path: str, expiration=604700):
        try:
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": path},
                ExpiresIn=expiration,
            )
            assert isinstance(
                url, str
            ), f"response from generate_presigned_url method is not string : {path}"
            return url
        except ClientError:
            raise exceptions.APIException(
                "Something went wrong", StatusCodes().BAD_REQUEST
            )

    def put_presigned_url(self, path: str, expiration=60470):
        try:
            url = self.client.generate_presigned_url(
                "put_object",
                Params={"Bucket": self.bucket, "Key": path},
                ExpiresIn=expiration,
            )
            assert isinstance(
                url, str
            ), f"response from generate_presigned_url method is not string : {path}"
            return url
        except ClientError:
            raise exceptions.APIException(
                "Something went wrong", StatusCodes().BAD_REQUEST
            )


class UploadFilesBase64:
    def __init__(self, bucket_name, folder_name):
        self.AWS_BUCKET_NAME = bucket_name
        self.BUCKET_REGION_NAME = settings.AWS_REGION
        self.s3_conn = boto3.client(
            "s3",
            config=Config(signature_version="s3v4", region_name=settings.AWS_REGION),
        )
        self.base_url = f"https://{self.AWS_BUCKET_NAME}.s3.{self.BUCKET_REGION_NAME}.amazonaws.com/"
        self.folder_name = folder_name

    def upload_file(self, file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        file_name = f"{file_name}_{timestamp}{file_extension}"
        object_key = f"{self.folder_name}/{file_name}"
        content_type = (
            "image/*"
            if file_extension in [".jpeg", ".jpg", ".png", ".gif"]
            else "application/pdf"
        )
        self.s3_conn.upload_file(
            file_path,
            self.AWS_BUCKET_NAME,
            object_key,
            ExtraArgs={"ContentType": content_type},
        )

        return self.get_file_link(file_name)

    def get_file_link(self, file_name):
        file_name = file_name.replace(" ", "+").replace(":", "%3A")
        file_link = self.base_url + self.folder_name + "/" + file_name

        return file_link
