import time
from typing import Union

from fastapi import FastAPI
from firebase_admin import auth

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
    message.id = str(time.time())
    return create_message(message)


@app.put("/messages/{message_id}")
def read_item(message_id: str, message: Message):
    return update_message(message_id, message.body, 'user-2')


@app.delete("/messages/{message_id}")
def delete_item(message_id: str, ):
    return delete_message(message_id, 'user-2')


@app.get('/claims')
def read_claims():
    return auth.verify_id_token(
        'eyJhbGciOiJSUzI1NiIsImtpZCI6IjFkYmUwNmI1ZDdjMmE3YzA0NDU2MzA2MWZmMGZlYTM3NzQwYjg2YmMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQW51aiAxIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0o4ZEE4aDNGdnpvdXVJdzN6THFYZ3ZIbGMtWkdWeGx4Q0FLdUcwOEVveTVMbUVQUT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9hdmEtY2hhdGJvdC1mMjU1MSIsImF1ZCI6ImF2YS1jaGF0Ym90LWYyNTUxIiwiYXV0aF90aW1lIjoxNzIyNzQ1NDcxLCJ1c2VyX2lkIjoiVW1CblRCTWJOWmcwSmY0VXhVRExFbUNhZDMxMyIsInN1YiI6IlVtQm5UQk1iTlpnMEpmNFV4VURMRW1DYWQzMTMiLCJpYXQiOjE3MjI3NDU0NzEsImV4cCI6MTcyMjc0OTA3MSwiZW1haWwiOiJsdWRpY3JvdXM2NDRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMTA1NzIzMjM2NDc4MTI5NjQ2NTgiXSwiZW1haWwiOlsibHVkaWNyb3VzNjQ0QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.KcEcSKJedgRoHh3MxdbcggEi5SH180lGO_RstpbmE-qQAWTVx2yiFqgwG0YzRI4RZAKN5M_XDCH78epDBY_QO5BaSNgXm6H3Lj5__VI7qio1JM5l2wMX-7yPdUxu8LPiIh9TSa3kSXlsskuw0DpIfSeTisrTF1uMQxdX5T9NmKBkblGBplFTWcNjYjkv3tnA5PgCv-ddXLpcDnVtXdk0kUrIik9QwM_cu0pvG1KdqKvaK-Xs9rBOFkHPAUjPGMKDeZOj0vF_pB1Qt9UTYDquNnIsrsoaI49xMpxKmcPaj5sA7fpIBwlJobbKhAd_Qbkiq-Nxwo8sc1QAFuxG2gXt-A')
