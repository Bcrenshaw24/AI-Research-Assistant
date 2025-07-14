from together import Together
from dotenv import load_dotenv
import os 

load_dotenv() 

client = Together()
from database import queryDB
from LLM import generate
from pydantic import BaseModel
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio


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

def embed(text: str): 
    response = client.embeddings.create(
    model="togethercomputer/m2-bert-80M-32k-retrieval",
    input=text
)
    return response.data[0].embedding

@app.post("/") 
async def root(query: Query): 
    query_embed = embed(query.query)
    print(len(query_embed))
    result = queryDB(query_embed)
    asyncio.sleep(2)
    return StreamingResponse(generate(query.query, result), media_type="text/plain")


