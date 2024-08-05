import os
import time
from typing import Annotated, Union

import uvicorn
from fastapi import Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import src.store.messages
from src.config.api import app
from src.middlewares.auth import validate_request
from src.models.messages import Message, MessageBody, ListMessagesResponse, PageInfo, convert_message
from src.services.responses import generate_response

origins = [
    "http://localhost:3000",
    "https://ava-chatbot-f2551.web.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/messages')
def list_messages(
        x_user_id: Annotated[str, Header()],
        x_token: Annotated[str, Header()],
        first: int,
        after: Union[str, None] = None,
):
    try:
        validate_request(x_token, x_user_id)
    except Exception as e:
        raise e

    if after is None:
        after = ''

    try:
        messages = src.store.messages.list_messages(x_user_id, first + 1, after)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    page_params = PageInfo(hasMore=False, cursor="")
    target = messages
    if len(messages) > first:
        page_params.hasMore = True
        target = messages[:len(messages) - 1]

    edges = []
    for m in target:
        edges.append(convert_message(m))
    if len(edges) > 0:
        page_params.cursor = edges[len(edges) - 1].id

    return ListMessagesResponse(pages=edges, pageParams=page_params)


@app.post('/messages')
def send_message(
        x_user_id: Annotated[str, Header()],
        x_token: Annotated[str, Header()],
        request: MessageBody,
):
    try:
        validate_request(x_token, x_user_id)
    except Exception as e:
        raise e

    sent = Message(
        id=str(time.time()) + 'user',
        body=request.body,
        user_sent=True,
        user_id=x_user_id,
    )
    received = Message(
        id=str(time.time()) + 'bot',
        body=generate_response(request.body),
        user_sent=False,
        user_id=x_user_id,
    )

    try:
        src.store.messages.create_message(sent, received)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    return [convert_message(sent), convert_message(received)]


@app.put("/messages/{message_id}")
def update_message(
        x_user_id: Annotated[str, Header()],
        x_token: Annotated[str, Header()],
        message_id: str,
        message: MessageBody,
):
    try:
        validate_request(x_token, x_user_id)
    except Exception as e:
        raise e

    try:
        return src.store.messages.update_message(message_id, message.body, x_user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/messages/{message_id}")
def delete_message(
        x_user_id: Annotated[str, Header()],
        x_token: Annotated[str, Header()],
        message_id: str,
):
    try:
        validate_request(x_token, x_user_id)
    except Exception as e:
        raise e

    try:
        return src.store.messages.delete_message(message_id, x_user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="localhost", port=port)
