from pydantic import BaseModel


class Message(BaseModel):
    id: str
    user_id: str
    user_sent: bool
    body: str


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


class ListMessagesResponse(BaseModel):
    pages: list[MessageEdge]
    pageParams: PageInfo
