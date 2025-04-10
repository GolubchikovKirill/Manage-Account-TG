from typing import List
from fastapi import APIRouter, HTTPException, Depends

from depends.depends import get_repo
from repository.repository_channel import ChannelRepository
from schema_pydantic.schemas import ChannelCreate, ChannelOut

router = APIRouter(prefix="/channels", tags=["channels"])


@router.get("/", response_model=List[ChannelOut])
async def get_channels(channel_name: str, repo: ChannelRepository = Depends(get_repo)):
    channel = await repo.get_channel(channel_name)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return [channel]


@router.post("/", response_model=str)
async def create_channel(
        channel: ChannelCreate, repo: ChannelRepository = Depends(get_repo)
):
    result = await repo.add_channel(channel.name)
    if "уже существует" in result:
        raise HTTPException(status_code=400, detail=result)
    return result


@router.delete("/by-name/{channel_name}", response_model=str)
async def delete_channel_by_name(
        channel_name: str, repo: ChannelRepository = Depends(get_repo)
):
    result = await repo.remove_channel(channel_name)
    if "не найден" in result:
        raise HTTPException(status_code=404, detail=result)
    return result
