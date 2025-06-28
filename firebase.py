# app/firebase.py
import os
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv

load_dotenv()

cred_path = os.getenv("FIREBASE_CREDENTIAL_PATH")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)


def verify_firebase_token(id_token: str):
    """
    Firebase ID 토큰을 검증하고, 
    유효하면 decoded_token(dict)을 반환, 
    유효하지 않으면 None을 반환합니다.
    """
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception:
        return None
    


