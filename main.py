from typing import Union

from fastapi import FastAPI

from app.store.auth import get_user

app = FastAPI()


@app.get("/")
async def read_root():
    user = get_user('user-1')
    return user


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
