from opensearchpy import OpenSearch, RequestsHttpConnection
import os
import cfnresponse

index_name = "photos"
openSearchHost = os.environ['openSearchHost']
openSearch = OpenSearch(
    hosts=[{"host": openSearchHost, "port": 443}],
    http_auth=("maxee998", "Admin1234!"),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)

def create_index():
    # Create an index with non-default settings.
    index_body = {"settings": {"index": {"number_of_shards": 1}}}
    try:
        response = openSearch.indices.create(index_name, body=index_body)
    except Exception as e:
        response = e
    return response

def lambda_handler(event, context):
    if event["RequestType"] == "Create":
        create_index()
    cfnresponse.send(event, context, cfnresponse.SUCCESS, {"result": "ok"})
    return "ok"
