from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os 

load_dotenv()
PINE = os.environ.get("PINE")
pc = Pinecone(api_key=PINE) 
index_name = "papers"
if index_name not in [idx.name for idx in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=768,          # embedding dimension
        metric="cosine",        # similarity metric
        spec=ServerlessSpec( 
            cloud="aws",
            region="us-east-1"
        )
    ) 
index = pc.Index(index_name)


            
def queryDB(query, index=index): 
    result = index.query( 
        vector=query, 
        top_k=8,
        include_metadata=True
    )
    return result
