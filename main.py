from typing import Union

from fastapi import FastAPI

from app.models.messages import Message
from app.models.users import User
from app.store.auth import get_user, signup
from app.store.messages import list_messages, update_message, create_message, delete_message

app = FastAPI()


@app.get("/")
async def read_root():
    user = get_user('user-1')
    return user


@app.post("/signup")
async def read_item(user: User):
    return signup(user, Message(**{
        'id': 'message-1',
        'user_id': user.id,
        'user_sent': False,
        'body': 'Hello! How may I help you today?'
    }))


@app.get('/messages')
def get_messages(first: int, after: Union[str, None] = None):
    if after is None:
        after = ''
    return list_messages('user-2', first, after)


@app.post('/messages')
def send_message(message: Message):
    return create_message(message)


@app.put("/messages/{message_id}")
def read_item(message_id: str, message: Message):
    return update_message(message_id, message.body, 'user-2')


@app.delete("/messages/{message_id}")
def delete_item(message_id: str, ):
    return delete_message(message_id, 'user-2')
