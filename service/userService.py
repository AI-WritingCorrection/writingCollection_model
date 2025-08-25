from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from domain.user import User


def create_user(db: Session, **kwargs) -> User:
    try:
        user = User(**kwargs)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError:
        db.rollback()
        raise  # 혹은 적절한 커스텀 예외로 변환


def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None

    for key, value in kwargs.items():
        setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError:
        db.rollback()
        raise


def get_user_by_firebase_uid(db: Session, uid: str) -> Optional[User]:
    return db.query(User).filter(User.firebase_uid == uid).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.user_id == user_id).first()


def update_profile_pic(db: Session, user_id: int, url: str) -> Optional[User]:
    """
    User.profile_pic 전용 업데이트 함수.
    성공 시 갱신된 User를 반환하고, 대상이 없으면 None을 반환합니다.
    트랜잭션 에러 시 SQLAlchemyError를 상위로 전파합니다.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    user.profile_pic = url
    try:
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError:
        db.rollback()
        raise
