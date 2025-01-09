from fastapi import FastAPI, Body, Query
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, Response
import entities
from database import Database
from rag_api import Rag
from lm_api import Lm
import os

RAG_ADDR = os.getenv("rag_addr", "localhost")
RAG_PORT = os.getenv("rag_port", "50001")
MODEL_ADDR = os.getenv("model_addr", "localhost")
MODEL_PORT = os.getenv("model_port", "50001")

db = Database()
rag = Rag(RAG_ADDR, RAG_PORT)
model = Lm(RAG_ADDR, RAG_PORT)
app = FastAPI()


def generate_text(chat_id, documents):
    total_msg = ""
    for s in model.generate_text(documents):
        yield s
        total_msg += s

    db.add_message(chat_id, entities.Message(id=0, author="assistant", text=total_msg))


@app.get("/api/chat/{chat_id}",)
async def chat_get(chat_id:int):
    chat = await db.get_chat(chat_id)
    if chat is not None:
        return chat
    return Response("chat not found", status_code=404)

@app.post("/api/chat/",)
async def chat_post(chat_id:int):
    chat = db.create_chat(chat_id)
    return chat

@app.delete("/api/chat/{chat_id}",)
async def chat_delete(chat_id:int):
    await db.delete_chat(chat_id)
    return Response()

@app.post("/api/rag_search/")
async def rag_serarh(data = Body()):
    answers = await rag.get_answers(data["text"])
    return answers

@app.post("/api/send_message/{chat_id}")
async def send_message(chat_id:int, data = Body()):
    chat = await db.get_chat(chat_id)
    if chat is None:
        return Response("chat not found", status_code=404)
    messages = list()
    if "preamble" in data:
        preambule = data["preamble"]
        messages.append(entities.Message(id=0, author="system", text=preambule))
    message = await db.add_message(chat_id, entities.Message(id=0, author="user", text = data["text"]))
    messages.extend(chat.messages)
    messages.append(message)
    return StreamingResponse(generate_text(chat_id, messages))
