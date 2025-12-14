# backend/weaviate_client.py
import weaviate
import os

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")

client = weaviate.Client(url=WEAVIATE_URL)

CLASS_NAME = "DocumentChunk"

def create_schema():
    schema = {
        "classes": [
            {
                "class": CLASS_NAME,
                "description": "Text chunks from uploaded documents",
                "properties": [
                    {"name": "text", "dataType": ["text"]},
                    {"name": "source", "dataType": ["text"]},
                ],
            }
        ]
    }
    # حذف کلاس اگر وجود دارد (برای توسعه)
    if client.schema.contains({"class": CLASS_NAME}):
        try:
            client.schema.delete_class(CLASS_NAME)
        except Exception:
            pass
    client.schema.create_class(schema["classes"][0])
    print("Schema created.")

def index_chunks(chunks):
    """
    chunks: list of dicts: {"id":str, "text":str, "vector": list[float], "source":str}
    """
    with client.batch as batch:
        batch.batch_size = 50
        for c in chunks:
            props = {"text": c["text"], "source": c.get("source","")}
            client.batch.add_data_object(data_object=props, class_name=CLASS_NAME, vector=c["vector"])
    print("Indexed", len(chunks))

def query_top_k(query_vector, k=5):
    result = client.query.get(CLASS_NAME, ["text", "source"]).with_near_vector({"vector": query_vector}).with_limit(k).do()
    # parse
    hits = []
    try:
        for h in result["data"]["Get"][CLASS_NAME]:
            # score not directly returned if we pass explicit vector; weaviate supports with_distance
            hits.append({"text": h["text"], "source": h.get("source","")})
    except Exception:
        pass
    return hits
