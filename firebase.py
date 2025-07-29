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
    try:
        return auth.verify_id_token(id_token)

    except Exception as e:
        print(f"[verify_firebase_token ERROR] {type(e).__name__}: {e}")
        return None
    
