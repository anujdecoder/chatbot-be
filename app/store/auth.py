from firebase_admin import firestore

from app.models.messages import Message
from app.models.users import User
from app.store.constants import BASE_COLLECTION, MESSAGE_COLLECTION
from firebase.config import db


def signup(user: User, message: Message):
    batch = db.batch()

    user_ref = db.collection(BASE_COLLECTION).document(user.id)
    batch.set(user_ref, user.model_dump())

    message_ref = user_ref.collection(MESSAGE_COLLECTION).document(message.id)
    message_dict = message.model_dump()
    message_dict['created_on'] = firestore.SERVER_TIMESTAMP
    batch.set(message_ref, message_dict)

    batch.commit()


def get_user(user_id: str):
    doc_ref = db.collection(BASE_COLLECTION).document(user_id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        return User(**data)
