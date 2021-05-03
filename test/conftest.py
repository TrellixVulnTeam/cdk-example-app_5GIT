import os
import tarfile

import requests
from pytest_dynamodb import factories
from pytest_dynamodb.port import get_port


def download_dynamodb_local(target_dir):
    url = 'https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz'
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    with tarfile.open(local_filename, 'r:gz') as tar:
        tar.extractall(path=target_dir)
    os.remove(local_filename)
    print(f'downloaded local dynamodb to {target_dir}')


dynamo_dir = os.path.join(os.path.dirname(__file__), "../.dynamodb")
if not os.path.exists(f"{dynamo_dir}/DynamoDBLocal.jar"):
    download_dynamodb_local(dynamo_dir)
# find a free port and start local dynamodb
port = get_port(None)
dynamodb_proc = factories.dynamodb_proc(dynamo_dir, port=port)
