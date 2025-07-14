from main import embed
import PyPDF2 
import uuid
from main import embed
from database import index

def extractPDF(file: str, index) -> None: 
    with open(file, 'rb') as pdf: 
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pages = [] 

        for page in reader.pages:
            content = page.extract_text()
            vec = embed(content)
            id = str(uuid.uuid4())
            index.upsert(vectors=[{"id": id, "values": vec, "metadata": {"content": content}}])

extractPDF("Attention-Research.pdf", index)           