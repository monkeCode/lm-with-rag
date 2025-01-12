import database
from mysql.connector import connect, Error
import entities
from hash import generate_random_hash

class MysqlDatabase(database.Database):

    def __init__(self, host, database, user, password, drop_database=False):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

        if(not self.check_exists()):
            self.create_database()
        elif drop_database:
            self.drop_database()
            self.create_database()
    
    def check_exists(self) -> bool:
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT Exists (select * from INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' );)", (self.database,), multi=True)
            res = cursor.fetchone()
            cursor.close()
            return (res is not None and res == 1)
    
    def create_database(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            #cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database};")
            #cursor.execute(f"USE {self.database};")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    login VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    session_key VARCHAR(255)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    chat_id INT,
                    date DATETIME,
                    author VARCHAR(255),
                    text TEXT,
                    FOREIGN KEY (chat_id) REFERENCES chats(id)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                );
            """)
            connection.commit()
            cursor.close()


    def drop_database(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT GROUP_CONCAT('DROP TABLE IF EXISTS ', table_name, ';') FROM information_schema.tables WHERE table_schema = %s;", (self.database,))
            connection.commit()
            cursor.close()

    def connect(self):
        return connect(host=self.host, database=self.database, user=self.user, password=self.password)

    async def get_user(self, key):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("select id, name from users where session_key =%s", (key,))
            user = cursor.fetchone()
            if user is not None:
                chats = await self.get_chats(user_id=user[0])
                return entities.User(id=user[0], name=user[1], chats=chats)
            cursor.close()
            return None

    async def get_chat(self, chat_id):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("select user_id from chats where id = %s", (chat_id,))
            chat_data = cursor.fetchone()
            if chat_data is None:
                return None
            
            cursor.execute("select id, date, author, text from messages where chat_id = %s", (chat_id,))
            data = cursor.fetchall()
            messages = [entities.Message(id = mes[0], chat_id=chat_id, date = mes[1], author=mes[2], text=mes[3]) for mes in data]
            cursor.close()
            return entities.Chat(id=chat_id, user_id = chat_data[0], messages=messages)
    
    async def get_chats(self, user_id):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("select id from chats where user_id = %s", (user_id,))
            chats = []
            for chat_data in cursor.fetchall():
                chat_id = chat_data[0]
                cursor.execute("select id, date, author, text from messages where chat_id = %s", (chat_id,))
                data = cursor.fetchall()
                messages = [entities.Message(id = mes[0], chat_id=chat_id, date = mes[1], author=mes[2], text=mes[3]) for mes in data]
                chats.append(entities.Chat(id=chat_id, user_id = user_id, messages=messages))
            cursor.close()
            return chats
    
    async def add_message(self, message:entities.Message):
            with self.connect() as connection:
                cursor = connection.cursor()
                cursor.execute("insert into messages (chat_id, date, author, text) values (%s, %s, %s, %s)", (message.chat_id, message.date, message.author, message.text))
                connection.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")
                id = cursor.fetchone()[0]
                cursor.close()
                return entities.Message(id=id, chat_id=message.chat_id, date=message.date, author=message.author, text=message.text)

    async def create_chat(self, user_id) -> entities.Chat:
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO chats (user_id) VALUES (%s)", (user_id,))
            connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            chat_id = cursor.fetchone()[0]
            cursor.close()
            return entities.Chat(id=chat_id, user_id=user_id, messages=[])

    
    async def delete_chat(self, chat_id) -> bool:
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("DElete from chats where id= %s ", (chat_id,))
            connection.commit()
            cursor.close()
        return True
    
    async def register(self, name, login, password) -> tuple[entities.User, str]:
        with self.connect() as connection:
            cursor = connection.cursor()
            hash = generate_random_hash()
            cursor.execute("INSERT INTO users (name, login, password, session_key) VALUES (%s, %s, %s, %s)", (name, login, password, hash))
            connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            user_id = cursor.fetchone()[0]
            cursor.close()
            return entities.User(id=user_id, name=name, chats=[]), hash

    
    async def login(self, login, password) -> tuple[entities.User, str]:
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, session_key FROM users WHERE login = %s AND password = %s", (login, password))
            user = cursor.fetchone()
            cursor.close()
            if user is not None:
                chats = await self.get_chats(user_id=user[0])
                return entities.User(id=user[0], name=user[1], chats=chats), user[2]
            return None, None

    
    async def logout(self, user_id) -> bool:
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE users SET session_key = NULL WHERE id = %s", (user_id,))
            connection.commit()
            cursor.close()
        return True

