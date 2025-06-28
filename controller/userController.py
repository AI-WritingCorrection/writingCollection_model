from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.user import User
from dto.userDTO import UserResponse


router=APIRouter()

# DB에서 해당 유저의 정보를 가져오는 함수
@router.get("/getProfile/{user_id}", response_model=UserResponse)
def get_userProfile_from_db(user_id:int, db: Session = Depends(get_db)):

    try:
        records = (
            db.query(User)
              .filter(User.user_id == user_id)
              .first()
        )
        return records
    except Exception as e:
        print(f"Error fetching mission records for user {user_id}: {e}")
        return []