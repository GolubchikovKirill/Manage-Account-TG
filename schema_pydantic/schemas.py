from pydantic import BaseModel

class ChannelCreate(BaseModel):
    name: str
    account_id: int
    comment: str

class ChannelOut(BaseModel):
    id: int
    name: str
    account_id: int
    comment: str

    class Config:
        from_attributes = True