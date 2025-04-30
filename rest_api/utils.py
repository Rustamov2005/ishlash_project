from django.conf import settings

from backend.services.s3_client import S3Client

_s3_client = None


def get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = MinIOClient(
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
            region_name=settings.AWS_S3_REGION_NAME
        )
    return _s3_client
