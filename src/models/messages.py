from pydantic import BaseModel


class Message(BaseModel):
    id: str
    user_id: str
    user_sent: bool
    body: str


class MessageBody(BaseModel):
    body: str
