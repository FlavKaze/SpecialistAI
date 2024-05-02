import os
from typing import List

import pickle
from pydantic import BaseModel
from fastapi import APIRouter, File, UploadFile

import config
from app.utils import database
from app.utils.tools import rag_inference, make_embeddings
from app.utils.create_context import generate_contexts_from_file, generate_contexts_from_sites, load_data_to_db


router = APIRouter()

class Message(BaseModel):
    message_id: str
    message: str
    site: str

class Chat(BaseModel):
    chat_id: str
    messages: List[Message]
    
class keyword(BaseModel):
    keyword: str 

@router.post("/create_context_from_file")
async def create_context(file: UploadFile = File(None)) -> str:
    """Create context from image or keyword."""
    file_bytes = await file.read()
    generate_contexts_from_file(file_bytes) 
    return "Context created successfully!"
    
    
@router.post("/create_context_from_text")
async def create_context_from_text(keyword: keyword) -> str:
    """Create context from keyword."""
    generate_contexts_from_sites(keyword.keyword)
    return "Context created successfully!"


@router.get("/list_knowledge_base")
def list_knowledge_base():
    return database.list_tables(uri=config.db_name)

@router.post("/query")
async def query(chat: Chat) -> Message:
    message = chat.messages[-1]
    chat_id = chat.chat_id

    embeddings = make_embeddings(message.message)
    result = database.search(
        table_name=chat_id,
        uri=config.db_name, 
        vector=embeddings["embedding"], 
        limit=10
    )

    response = rag_inference(message=message.message, context=result.get("text").tolist())
    site = result.get("site")[0] or ""
    return Message(message_id="None", message=response, site=site)
