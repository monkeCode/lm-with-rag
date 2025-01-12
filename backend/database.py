import entities

class Database:

    async def get_chat(self, chat_id:int) -> entities.Chat:
        return entities.Chat(id=0, user_id=0, messages = list())
    
    async def get_chats(self, user_id:int) -> list[entities.Chat]:
        return []
    
    async def create_chat(self, user_id) -> entities.Chat:
        return entities.Chat(id=0, user_id=0, messages = list())
    
    async def delete_chat(self, chat_id) -> bool:
        return True

    async def add_message(self, message:entities.Message) -> entities.Message:
        return entities.Message(id=0, chat_id= 0, date= entities.datetime.datetime.now(), author = message.author, text=message.text)

    async def get_user(self, key) -> entities.User:
        return entities.User(0, name="test", chats=[entities.Chat(0, 0, [entities.Message(0, 0,entities.datetime.datetime.now(), "user", "text")])])
    
    async def register(self, name, login, password) -> tuple[entities.User, str]:
        return entities.User(0, name, []), "fjgfdglj"
    
    async def login(self, login, password) -> tuple[entities.User, str]:
        return entities.User(0, "test_name", []), "fdgfdgfdg"
    
    async def logout(self, user_id) -> bool:
        return True