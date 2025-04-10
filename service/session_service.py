from telethon import TelegramClient, functions
from settings import settings

api_id = settings.API_ID
api_hash = settings.API_HASH

# Имя сессии
session_name = '6281373146649.session'

# Создайте клиент
client = TelegramClient(session_name, api_id, api_hash)

try:

    client.start()


    result = client(functions.contacts.ResolveUsernameRequest(username='some_username'))

    print(result.stringify())
except Exception as e:
    print(f'Ошибка: {e}')
finally:

    client.disconnect()
