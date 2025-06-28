# SQLAlchemy 엔진과 세션을 정의
# SQLAlchemy는 파이썬의 ORM(Object-Relational Mapping) 라이브러리
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# .env 파일 읽어옴
load_dotenv() 

# 1) DATABASE_URL 은 .env 혹은 환경변수로 설정
DATABASE_URL = os.getenv("DATABASE_URL")

# 2) SQLAlchemy 엔진과 세션팩토리 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, # DB 연결이 끊어져도 자동 복구 시도
)


# 세션 팩토리 생성 (FastAPI 의존성으로 주입할 예정)
# SessionLocal을 FastAPI 경로에 주입(Dependency Injection)하여, API 호출 시마다 DB 세션을 열고 닫음
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3) FastAPI 의존성으로 쓰일 get_db
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()