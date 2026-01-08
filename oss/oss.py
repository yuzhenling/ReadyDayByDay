import base64
from io import BytesIO

import oss2

access_key_id = ''
access_key_secret = ''
endpoint = ''



auth = oss2.Auth(access_key_id, access_key_secret)


# 上传文件
def upload_file(bucket_name, file_path, object_name):
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    return bucket.put_object_from_file(object_name, file_path)

# 下载文件
def download_file(bucket_name,object_name, file_path):
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    return bucket.get_object_to_file(object_name, file_path)
# 下载文件
def delete_file(bucket_name,object_name):
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    return bucket.delete_object(object_name)


def sign_url( object_name,bucket_name="oss-igc", method='GET', expires=3600):
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    return bucket.sign_url(method, object_name, expires)

