from firebase_admin import auth


def validate_request(token: str, user_id: str):
    resp = auth.verify_id_token(token)
    if resp['uid'] != user_id:
        raise Exception("Not authorized")
