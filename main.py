from fastapi import FastAPI

from app.models.messages import Message
from app.models.users import User
from app.store.auth import get_user, signup

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
