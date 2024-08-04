from fastapi import HTTPException
from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError


def validate_request(token: str, user_id: str):
    try:
        resp = auth.verify_id_token(token)
    except InvalidIdTokenError:
        raise HTTPException(status_code=403, detail="Please login again")
    if resp['uid'] != user_id:
        raise HTTPException(status_code=403, detail="You do not have access to this resource")
