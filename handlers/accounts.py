from fastapi import APIRouter, HTTPException, Depends
from depends.depends import get_session_service
from service.session_service import TelegramSessionService

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/login")
async def login(account_id: int, session_service: TelegramSessionService = Depends(get_session_service)):
    client = await session_service.create_client(account_id)
    if not client:
        raise HTTPException(status_code=400, detail="Ошибка авторизации")
    return {"message": "Успешно авторизовано", "account_id": account_id}

@router.post("/logout")
async def logout(account_id: int, session_service: TelegramSessionService = Depends(get_session_service)):
    await session_service.logout(account_id)
    return {"message": f"Аккаунт {account_id} успешно разлогинен."}

@router.get("/me")
async def get_me(account_id: int, session_service: TelegramSessionService = Depends(get_session_service)):
    client = await session_service.get_client(account_id)
    if not client:
        raise HTTPException(status_code=404, detail="Аккаунт не найден")
    me = await client.get_me()
    return {"username": me.username, "name": me.first_name}