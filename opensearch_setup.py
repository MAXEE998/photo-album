from opensearchpy import OpenSearch, RequestsHttpConnection

host = "search-assignment2-m3x5c4zswkalnoqpcpjqv47apm.us-east-1.es.amazonaws.com"  # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com


index_name = "photos"

client = OpenSearch(
    hosts=[{"host": host, "port": 443}],
    http_auth=("maxee998", "Admin1234!"),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)


def create_index():
    # Create an index with non-default settings.
    index_body = {"settings": {"index": {"number_of_shards": 1}}}

    response = client.indices.create(index_name, body=index_body)
    print("\nCreating index:")
    print(response)

if __name__ == "__main__":
    create_index()
