import entities

class Database:

    async def get_chat(self, chat_id:int) -> entities.Chat:
        return entities.Chat(id=0, messages = list())
    
    async def create_chat(self) -> entities.Chat:
        return entities.Chat(id=0, messages = list())
    
    async def delete_chat(self, chat_id) -> bool:
        return True

    async def add_message(self, chat_id:int, message:entities.Message) -> entities.Message:
        return entities.Message(id=0, author= message.author, text=message.text)
