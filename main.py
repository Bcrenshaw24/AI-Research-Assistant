from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

from extraction import queryDB
from LLM import generate
from pydantic import BaseModel, Field
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI() 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


class Query(BaseModel): 
    query: str 



@app.post("/question") 
async def root(query: Query): 
    query_embed = model.encode(query.query).tolist()
    result = queryDB(query_embed)
    return StreamingResponse(generate(query, result), media_type="text/plain")


