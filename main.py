import firebase_admin

from typing import Union
from fastapi import FastAPI
from firebase_admin import credentials
from firebase_admin import firestore


app = FastAPI()

cred = credentials.Certificate("keys.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.get("/")
async def read_root():
    doc_ref = db.collection('chats').document('user-1')
    doc = doc_ref.get()
    if doc.exists:
        return {
            "name": doc.to_dict().get("name")
        }

    return {"error": "not-exists"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
