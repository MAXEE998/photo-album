import logging
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
rekognition = boto3.client('rekognition')
bucket = "assignment2-nyu-photos"

openSearchHost = "search-assignment2-m3x5c4zswkalnoqpcpjqv47apm.us-east-1.es.amazonaws.com" 
openSearch = OpenSearch(
    hosts=[{"host": openSearchHost, "port": 443}],
    http_auth=("maxee998", "Admin1234!"),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

def print2(m):
    logger.debug(m)

def create(key, doc):
    response = openSearch.index(
        index = "photos",
        body=doc,
        refresh=True,
        id=key,
    )
    return response


def lambda_handler(event, context):
    # TODO implement
    file_key = event["Records"][0]["s3"]["object"]["key"]
    creation_time = event["Records"][0]["eventTime"]
    
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': file_key
            },
            
        },
        MinConfidence=70,
    )
    labels = ";".join([label["Name"] for label in response["Labels"]])
    doc = {
        "objectKey": file_key,
        "bucket": bucket,
        "createdTimestamp": creation_time,
        "labels": labels,
    }

    return create(file_key, doc)