import time
from typing import Annotated, Union

from fastapi import Header, HTTPException
from firebase_admin import auth

from src.config.api import app
from src.config.logger import logger
from src.middlewares.auth import validate_request
from src.models.messages import Message, MessageBody, ListMessagesResponse, PageInfo, MessageEdge
from src.services.responses import generate_response
from src.store.messages import list_messages, update_message, create_message, delete_message


@app.get('/messages')
def get_messages(
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
        messages = list_messages(x_user_id, first + 1, after)
    except Exception as e:
        logger.error("Error while reading messages", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

    page_params = PageInfo(hasMore=False, cursor="")
    target = messages
    if len(messages) > first:
        page_params.hasMore = True
        target = messages[:len(messages) - 1]

    edges = []
    for m in target:
        edges.append(MessageEdge(
            id=m.id,
            body=m.body,
            userId=m.user_id,
            userSent=m.user_sent,
        ))
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
        create_message(sent, received)
    except Exception as e:
        logger.error("Error while creating messages", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

    return received


@app.put("/messages/{message_id}")
def read_item(
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
        return update_message(message_id, message.body, x_user_id)
    except Exception as e:
        logger.error("Error while updating messages", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/messages/{message_id}")
def delete_item(
        x_user_id: Annotated[str, Header()],
        x_token: Annotated[str, Header()],
        message_id: str,
):
    try:
        validate_request(x_token, x_user_id)
    except Exception as e:
        raise e

    try:
        return delete_message(message_id, x_user_id)
    except Exception as e:
        logger.error("Error while deleting messages", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get('/claims')
def read_claims():
    return auth.verify_id_token(
        'eyJhbGciOiJSUzI1NiIsImtpZCI6IjFkYmUwNmI1ZDdjMmE3YzA0NDU2MzA2MWZmMGZlYTM3NzQwYjg2YmMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQW51aiAxIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0o4ZEE4aDNGdnpvdXVJdzN6THFYZ3ZIbGMtWkdWeGx4Q0FLdUcwOEVveTVMbUVQUT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9hdmEtY2hhdGJvdC1mMjU1MSIsImF1ZCI6ImF2YS1jaGF0Ym90LWYyNTUxIiwiYXV0aF90aW1lIjoxNzIyNzU5Mjk0LCJ1c2VyX2lkIjoiVW1CblRCTWJOWmcwSmY0VXhVRExFbUNhZDMxMyIsInN1YiI6IlVtQm5UQk1iTlpnMEpmNFV4VURMRW1DYWQzMTMiLCJpYXQiOjE3MjI3ODQ3NTMsImV4cCI6MTcyMjc4ODM1MywiZW1haWwiOiJsdWRpY3JvdXM2NDRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMTA1NzIzMjM2NDc4MTI5NjQ2NTgiXSwiZW1haWwiOlsibHVkaWNyb3VzNjQ0QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.kVXt4MN49AzweyfEpuvUFVIndEMIrVgfPg3dbPxXm_bvISJM7qcPQlM-9r4PrKAv_bAAPGudeGOVPWY74WVPD1sjBWETZs2J0P0VLmT9WAVVu_WGXWQCbLQMqIFx4DHygOB1ixWVFwqvybgco2doFkBtG9lDKKxbpLCMn6rD1fdKyjKv_rshFeM05TLP43s6-QRa2Gml_X6eqkz-XMpXjs6NEkzXzb_iaH9zt0Bxb1GdItM8WC3BQtt_XGhT4QQyc1FPAIbYXGQ1LbrCow7M7uW8kAfzZh3x8FQmRCp7FmIwuQFiCbv4Vrz6ljKKv9WrxuHoeNSb4a9aIdYk7zwFag')
