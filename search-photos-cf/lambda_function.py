import logging
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
import inflect
import json
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
rekognition = boto3.client('rekognition')

lex = boto3.client('lexv2-runtime')
botId = os.environ['lexBotID']
botAliasId = 'TSTALIASID'
localeId = 'en_US'
sessionId = 'assignment2'

p = inflect.engine()

openSearchHost = os.environ['openSearchHost']
openSearch = OpenSearch(
    hosts=[{"host": openSearchHost, "port": 443}],
    http_auth=("maxee998", "Admin1234!"),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)


def print2(m):
    logger.debug(m)


def extractTags(query):
    lex.put_session(
        botId=botId,
        botAliasId=botAliasId,
        localeId=localeId,
        sessionId=sessionId,
        sessionState={},
    )
    response = lex.recognize_text(
        botId=botId,
        botAliasId=botAliasId,
        localeId=localeId,
        sessionId=sessionId,
        text=query,
    )
    slots = response["interpretations"][0]["intent"]["slots"]
    tags = []
    for v in slots.values():
        if v is not None:
            tags.append(v["value"]["interpretedValue"])
    return tags


def search(tags):
    for i in range(len(tags)):
        if p.singular_noun(tags[i]):
            tags[i] = p.singular_noun(tags[i])
    query_string = " OR ".join(tags)
    print(query_string)
    query = {
        'query': {
            "query_string": {
            "query": query_string
            }
        },
    }

    response = openSearch.search(
        body=query,
        index="photos"
    )
    return response["hits"]["hits"]


def lambda_handler(event, context):
    # TODO implement
    query = event["queryStringParameters"]["q"]
    tags = extractTags(query)
    body = json.dumps(search(tags))
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { 
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
         },
        "body": body
    }
