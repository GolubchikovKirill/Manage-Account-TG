import uvicorn
from fastapi import FastAPI
from handlers import routers
from fastapi.staticfiles import StaticFiles
import os


# Использование lifespan для управления жизненным циклом приложения
async def lifespan(_):
    # Инициализация при старте приложения
    yield  # Это место, где FastAPI будет работать


app = FastAPI(
    title="Telegram Account Manager",
    lifespan=lifespan
)

# Роутеры
for router in routers:
    app.include_router(router)

# Статика на уровне приложения
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# STATIC_DIR = os.path.join(BASE_DIR, "static")
# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)