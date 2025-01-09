import dataclasses

@dataclasses.dataclass
class Message:
    id:int
    author:str
    text:str

@dataclasses.dataclass
class Chat:
    id:int
    messages:list[Message]

@dataclasses.dataclass
class User:
    id:int
    chats:list[Chat]
