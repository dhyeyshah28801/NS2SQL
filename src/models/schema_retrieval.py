from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

pc = Pinecone(api_key="pcsk_uQZa5_6sh7ivL9LdoTKHrz5BKiyan8VcR9QUfeB1R8eBnVj2nPnnpGJwJToBMW3BT2Dnb")
index = pc.Index("schema")

def get_schema_from_query(query):
    query_embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={
            "input_type": "query"
        }
    )

    # Search the index for the three most similar vectors
    results = index.query(
        namespace="example-namespace",
        vector=query_embedding[0].values,
        top_k=3,
        include_values=False,
        include_metadata=True
    )["matches"]
    i = 0
    schema = ''
    while i < 3 and i < len(results):
        schema += results[i]['metadata']['text']
        i+=1
    return schema
