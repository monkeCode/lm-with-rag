import dataclasses
import datetime
@dataclasses.dataclass
class Message:
    id:int
    chat_id:int
    date:datetime.datetime
    author:str
    text:str

@dataclasses.dataclass
class Chat:
    id:int
    user_id:int
    messages:list[Message]

@dataclasses.dataclass
class User:
    id:int
    name:str
    chats:list[Chat]
