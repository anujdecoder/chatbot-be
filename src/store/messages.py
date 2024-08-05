import time

from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter

from src.config.firebase import db
from src.models.messages import Message
from src.store.constants import BASE_COLLECTION, MESSAGE_COLLECTION, ID_KEY


def create_message(s: Message, r: Message):
    coll_ref = db.collection(BASE_COLLECTION).document(s.user_id).collection(MESSAGE_COLLECTION)

    batch = db.batch()

    message_ref = coll_ref.document(s.id)
    dump = s.model_dump()
    dump['created_on'] = time.time()
    batch.set(message_ref, dump)

    message_ref = coll_ref.document(r.id)
    dump = r.model_dump()
    dump['created_on'] = time.time()
    batch.set(message_ref, dump)

    batch.commit()


def update_message(message_id: str, message_body: str, user_id: str):
    message_ref = db.collection(BASE_COLLECTION).document(user_id).collection(MESSAGE_COLLECTION).document(
        message_id)
    message_ref.update({'body': message_body, 'updated_on': time.time()})


def delete_message(message_id: str, user_id: str):
    message_ref = db.collection(BASE_COLLECTION).document(user_id).collection(MESSAGE_COLLECTION).document(
        message_id)
    message_ref.update({'body': 'This message has been deleted', 'deleted_on': time.time(), 'deleted': True})


def list_messages(user_id: str, page_size: int, cursor: str = ''):
    messages_ref = db.collection(BASE_COLLECTION).document(user_id).collection(MESSAGE_COLLECTION)
    query = (messages_ref
             .order_by(ID_KEY, direction=firestore.Query.DESCENDING)
             .limit(page_size))
    if cursor != '':
        query = query.where(filter=FieldFilter("id", "<", cursor))

    docs = query.stream()
    messages = []
    for doc in docs:
        dd = doc.to_dict()
        m = Message(**dd)
        messages.append(m)

    return messages
