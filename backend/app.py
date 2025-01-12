from fastapi import FastAPI, Body, Query, Request, Cookie, Depends, Header
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, RedirectResponse, Response
from fastapi.exceptions import HTTPException
from consts import *
import entities
from database import Database
from rag_api import Rag
from lm_api import Lm
from typing import Union
from hash import hash_str
from dataclasses import asdict
import mysql_database
import datetime

db = mysql_database.MysqlDatabase("mysql", DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD)
rag = Rag(RAG_ADDR, RAG_PORT)
model = Lm(MODEL_ADDR, MODEL_PORT)
app = FastAPI()


async def auth(session_key: Union[str, None] = Cookie(alias="session_key")) -> entities.User:
    user = await db.get_user(session_key) if session_key is not None else None
    if user is None:
        raise HTTPException(401, "Unauthorized")
    return user

async def generate_text(chat_id, documents):
    total_msg = ""
    for s in model.generate_text(documents):
        yield s
        total_msg += s
    await db.add_message(entities.Message(id=0, chat_id=chat_id, author="assistant", date= datetime.datetime.now(), text=total_msg))


@app.get("/api/chat/{chat_id}",)
async def chat_get(chat_id:int, user = Depends(auth)):
    if len(list(filter(lambda x: x.id == chat_id, user.chats))) == 0:
        raise HTTPException(403, "this chat isn't your")
    chat = await db.get_chat(chat_id)
    if chat is not None:
        return chat
    raise HTTPException(detail="chat not found", status_code=404)

@app.post("/api/chat/",)
async def chat_post(user:entities.User = Depends(auth)):
    chat = await db.create_chat(user.id)
    return JSONResponse(asdict(chat), status_code=201)

@app.delete("/api/chat/{chat_id}",)
async def chat_delete(chat_id:int, user:entities.User = Depends(auth)):
    if len(list(filter(lambda x: x.id == chat_id, user.chats))) == 0:
        raise HTTPException(403, "this chat isn't your")
    
    res = await db.delete_chat(chat_id)
    return Response(status_code= 200 if res else 400 )

@app.post("/api/rag_search/")
async def rag_serarh(data = Body()):
    answers = await rag.get_answers(data["text"])
    return answers

@app.get("/api/chat/")
async def get_chats(user:entities.User = Depends(auth)):
    return user.chats

@app.post("/api/send_message/{chat_id}")
async def send_message(chat_id:int, data = Body(), user:entities.User = Depends(auth)):
    if len(list(filter(lambda x: x.id == chat_id, user.chats))) == 0:
        raise HTTPException(403, "this chat isn't your")
    chat = await db.get_chat(chat_id)
    if chat is None:
        return Response("chat not found", status_code=404)
    messages = list()
    if "preamble" in data:
        preambule = data["preamble"]
        messages.append(entities.Message(id=0, author="system", date=datetime.datetime.now(), text=preambule))
    message = await db.add_message(entities.Message(id=0, chat_id=chat_id, author="user", date=datetime.datetime.now(), text = data["text"]))
    messages.extend(chat.messages)
    messages.append(message)
    return StreamingResponse(generate_text(chat_id, messages))

@app.get("/api/login")
async def login(body = Body()):
    login = body["login"]
    password = body["password"]
    user, key = await db.login(login, hash_str(password))
    if user is None:
        raise HTTPException(400, "login or password is incorect")
    resp = JSONResponse(asdict(user))
    resp.set_cookie("session_key", key)
    return resp

@app.post("/api/register")
async def register(body=Body()):
    login = body["login"]
    password = body["password"]
    name = body["name"]
    try:
        user, secret_key = await db.register(name, login,  hash_str(password))
        resp = JSONResponse(asdict(user), status_code=201)
        resp.set_cookie("session_key", secret_key)
        return resp
    except Exception as e:
        print(e)
        return HTTPException(status_code= 400, detail="user already exists")
