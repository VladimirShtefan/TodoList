from datetime import datetime

from pydantic import BaseModel, Field


class Chat(BaseModel):
    id: str
    first_name: str | None


class MessageFrom(BaseModel):
    id: int
    username: str | None
    first_name: str


class Message(BaseModel):
    message_id: int
    from_: MessageFrom = Field(..., alias='from') | None
    chat: Chat
    date: datetime
    text: str | None

    class Config:
        # чтобы использовать alias вместо имени поля
        allow_population_by_field_name = True


class MessageInfo(BaseModel):
    update_id: int
    message: Message | None


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[MessageInfo]


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message
