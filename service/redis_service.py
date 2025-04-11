from contextlib import asynccontextmanager

# Заглушка для Redis
@asynccontextmanager
async def redis_connection():
    # Возвращаем "пустой" клиент
    yield None

# Функция для добавления задачи в поток (заглушка)
async def add_to_stream(stream_name: str, message: dict):
    pass

# Функция для получения сообщений из потока (заглушка)
async def get_messages_from_stream(stream_name: str, count: int = 10):
    return []

# Проверка лимита частоты через Redis (заглушка)
async def check_rate_limit(account_id: int, limit: int = 5, window: int = 60):
    return True

# Пинг Redis (заглушка)
async def ping():
    pass