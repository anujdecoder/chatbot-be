from typing import Union

from pydantic import BaseModel


class Message(BaseModel):
    id: str
    user_id: str
    user_sent: bool
    body: str
    deleted: Union[bool, None] = None


class MessageBody(BaseModel):
    body: str


class PageInfo(BaseModel):
    hasMore: bool
    cursor: str


class MessageEdge(BaseModel):
    id: str
    userId: str
    userSent: bool
    body: str
    deleted: Union[bool, None] = None


class ListMessagesResponse(BaseModel):
    pages: list[MessageEdge]
    pageParams: PageInfo


def convert_message(message: Message):
    return MessageEdge(
        id=message.id,
        body=message.body,
        userId=message.user_id,
        userSent=message.user_sent,
        deleted=message.deleted,
    )
