# app/firebase.py
import logging
import os
import firebase_admin
from firebase_admin import credentials, auth

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")

# 중복 초기화 방지
if not firebase_admin._apps:
    try:
        if os.path.exists(KEY_PATH):
            cred = credentials.Certificate(KEY_PATH)
            firebase_admin.initialize_app(cred)
        else:
            logger.error(f"Firebase key file not found at: {KEY_PATH}")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")

def verify_firebase_token(id_token: str):
    try:
        # check_revoked=True 옵션을 사용하면 
        # 사용자가 로그아웃하거나 비밀번호를 변경한 경우 토큰을 무효화할 수 있어 보안이 강화됩니다.
        return auth.verify_id_token(id_token, check_revoked=True) 
    except auth.RevokedIdTokenError:
            logger.warning("Token revoked")
            return None
    except Exception as e:
        logger.error(f"[verify_firebase_token ERROR] {type(e).__name__}: {e}")
        return None
    
