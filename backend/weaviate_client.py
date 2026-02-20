# backend/weaviate_client.py
from urllib import response
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
import os

class WeaviateVectorDB:
    def __init__(self):
        self.client = weaviate.connect_to_local(port=8080, grpc_port=50051)
        self.class_name = "DocumentChunk"

    def create_schema(self):
        collections = self.client.collections.list_all()
        if self.class_name not in collections:
            self.client.collections.create(
                name=self.class_name,
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    Property(name="text", data_type=DataType.TEXT),
                    Property(name="source", data_type=DataType.TEXT),
                ]
            )
            print("Schema created")

    def add_chunks(self, chunks):
        collection = self.client.collections.get(self.class_name)
        with collection.batch.dynamic() as batch:
            for c in chunks:
                batch.add_object(
                    properties={
                        "text": c["text"],
                        "source": c["source"]
                    },
                    vector=c["vector"]
                )

    def search(self, query_vector, k=5):
        collection = self.client.collections.get(self.class_name)
        response = collection.query.near_vector(
            near_vector=query_vector,
            limit=k,
            return_properties=["text", "source"],
            return_metadata=MetadataQuery(distance=True)
        )
        return [
            {
                "text": obj.properties["text"],
                "source": obj.properties["source"],
                "distance": obj.metadata.distance
            } for obj in response.objects
        ]
        


    # def search(self, query_vector: list[float], k: int = 5,filter=None):
    #     collection = self.client.collections.get(self.class_name)
    #     query_builder = collection.query.near_vector(
    #         near_vector=query_vector,
    #         limit=k,
    #         return_properties=["text", "source"]
    # )
    #     if filter:
    #         query_builder = query_builder.with_where(filter)
    #         # response = collection.query.near_vector(
    #         # near_vector=query_vector,
    #         # limit=k,
    #         # return_properties=["text", "source"]
    #         # )
    #         response = query_builder.do()
    #         return [{"text": obj.properties["text"], "source": obj.properties["source"]} for obj in response.objects]

    def close(self):
        self.client.close()