
import PyPDF2 
import uuid
from database import index
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')
def extractPDF(file: str, index) -> None: 
    try: 
        with open(file, 'rb') as pdf: 
            reader = PyPDF2.PdfReader(pdf, strict=False)
            pages = [] 

            for i, page in enumerate(reader.pages):
                try:
                    content = page.extract_text()
                    vec = model.encode(content).tolist()
                    id = str(uuid.uuid4())
                    index.upsert(vectors=[{"id": id, "values": vec, "metadata": {"content": content}}])
                except Exception as e: 
                    print(f"Error on chunk {i}: {e}")
                    continue
        print("Done")
    except Exception as e: 
        print(e)

extractPDF("./Data/Diff-Eqn.pdf", index)           