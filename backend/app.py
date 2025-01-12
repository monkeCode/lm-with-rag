from fastapi import FastAPI, Body, Query, Request, Cookie, Depends, Header
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, RedirectResponse, Response
from fastapi.exceptions import HTTPException
from consts import *
import entities
from database import Database
from rag_api import Rag
from lm_api import Lm
from typing import Union

db = Database()
rag = Rag(RAG_ADDR, RAG_PORT)
model = Lm(RAG_ADDR, RAG_PORT)
app = FastAPI()

def hash(password):
    return password

async def auth(session_key: Union[str, None] = Cookie(alias="session_key")) -> entities.User:
    user = await db.get_user(session_key) if session_key is not None else None
    print(user)
    if user is None:
        raise HTTPException(401, "Unauthorized")
    return user

def generate_text(chat_id, documents):
    total_msg = ""
    for s in model.generate_text(documents):
        yield s
        total_msg += s

    db.add_message(entities.Message(id=0, chat_id=chat_id, author="assistant", text=total_msg))


@app.get("/api/chat/{chat_id}",)
async def chat_get(chat_id:int, user = Depends(auth)):
    if len(filter(lambda x: x.id == chat_id, user.chats)) == 0:
        raise HTTPException(403, "this chat isn't your")
    chat = await db.get_chat(chat_id)
    if chat is not None:
        return chat
    raise HTTPException(detail="chat not found", status_code=404)

@app.post("/api/chat/",)
async def chat_post(user:entities.User = Depends(auth)):
    chat = db.create_chat(user.id)
    return JSONResponse(chat, status_code=201)

@app.delete("/api/chat/{chat_id}",)
async def chat_delete(chat_id:int, user:entities.User = Depends(auth)):
    if len(filter(lambda x: x.id == chat_id, user.chats)) == 0:
        raise HTTPException(403, "this chat isn't your")
    
    res = await db.delete_chat(chat_id)
    return Response(status_code= 200 if res else 400 )

@app.post("/api/rag_search/")
async def rag_serarh(data = Body()):
    answers = await rag.get_answers(data["text"])
    return answers

@app.get("/api/chats/")
async def get_chats(user:entities.User = Depends(auth)):
    return user.chats

@app.post("/api/send_message/{chat_id}")
async def send_message(chat_id:int, data = Body(), user:entities.User = Depends(auth)):
    if len(filter(lambda x: x.id == chat_id, user.chats)) == 0:
        raise HTTPException(403, "this chat isn't your")
    chat = await db.get_chat(chat_id)
    if chat is None:
        return Response("chat not found", status_code=404)
    messages = list()
    if "preamble" in data:
        preambule = data["preamble"]
        messages.append(entities.Message(id=0, author="system", text=preambule))
    message = await db.add_message(chat_id, entities.Message(id=0, chat_id=chat_id, author="user", text = data["text"]))
    messages.extend(chat.messages)
    messages.append(message)
    return StreamingResponse(generate_text(chat_id, messages))

@app.get("/api/login")
async def login(body = Body()):
    login = body["login"]
    password = body["password"]
    user, key = await db.login(login, hash(password))
    if user is None:
        raise HTTPException(400, "login or password is incorect")
    resp = JSONResponse(user)
    resp.set_cookie("session_key", key)
    return resp

@app.post("/api/register")
async def register(body=Body()):
    login = body["login"]
    password = body["password"]
    name = body["name"]
    try:
        user, secret_key = await db.register(name, login, password)
        resp = JSONResponse(user, status_code=201)
        resp.set_cookie("session_key", secret_key)
    except Exception as e:
        return HTTPException(status_code= 400, detail="user already exists")
