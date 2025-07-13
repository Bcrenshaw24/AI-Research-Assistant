import PyPDF2
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from main import model 
import os 
import uuid

PINE = os.environ.get("PINE")
pc = Pinecone(api_key=PINE) 
index_name = "papers"
if index_name not in [idx.name for idx in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=384,          # embedding dimension
        metric="cosine",        # similarity metric
        spec=ServerlessSpec( 
            cloud="aws",
            region="us-east-1"
        )
    ) 
index = pc.Index(index_name)
def extractPDF(file: str, index) -> None: 
    with open(file, 'rb') as pdf: 
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pages = [] 

        for page in reader.pages:
            content = page.extract_text()
            vec = model.encode(content)
            id = str(uuid.uuid4())
            index.upsert(vectors=[{"id": id, "values": vec, "metadata": {"content": content}}])
            
            
def queryDB(query, index=index): 
    result = index.query( 
        vector=query, 
        top_k=5,
        include_metadata=True
    )
    return result
