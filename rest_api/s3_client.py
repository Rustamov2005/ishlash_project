import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class S3Client:
    def __init__(self, access_key, secret_key, bucket_name, region_name):
        self.s3_client = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)  # MinIO's URL
        self.bucket_name = bucket_name

    def upload_file(self, file_path, object_name):
        try:
            with open(file_path, "rb") as file_obj:
                self.s3_client.upload_fileobj(file_obj, self.bucket_name, object_name)
            return True
        except (NoCredentialsError, ClientError) as e:
            print(f"Failed to upload file to MinIO: {e}")
            return False

    def download_file(self, object_name, download_path):
        try:
            self.s3_client.download_file(self.bucket_name, object_name, download_path)
            return True
        except (NoCredentialsError, ClientError) as e:
            print(f"Failed to download file from MinIO: {e}")
            return False

    def get_permanent_file_url(self, object_name):
        return f"{self.s3_client.meta.endpoint_url}/{self.bucket_name}/{object_name}"

    def get_temporary_file_url(self, object_name, expiration=3600):
        try:
            url = self.s3_client.generate_presigned_url("get_object", Params={"Bucket": self.bucket_name, "Key": object_name}, ExpiresIn=expiration)
            return url
        except Exception as ex:
            raise Exception(f"Error: {ex}")

    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
            print(f'Bucket "{bucket_name}" created successfully.')
        except Exception as e:
            print(f"Error creating bucket: {str(e)}")

    def delete_object(self, object_name):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except Exception as ex:
            raise Exception(f"Error: {ex}")
