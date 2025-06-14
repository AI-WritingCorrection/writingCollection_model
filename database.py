# SQLAlchemy 엔진과 세션을 정의
# SQLAlchemy는 파이썬의 ORM(Object-Relational Mapping) 라이브러리
#ORM (Declarative)
#– 클래스(모델)와 테이블을 1:1 대응시켜, 파이썬 객체를 생성·조회·수정·삭제하면 내부적으로 SQL이 자동으로 실행되게 해줍니다.
#– 예: User 클래스를 정의해 두면, session.add(User(...)) → session.commit() 같은 방식으로 편하게 데이터를 조작할 수 있습니다.
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv() # .env 파일 읽어옴

DATABASE_URL = os.getenv("DATABASE_URL")

#SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, # DB 연결이 끊어져도 자동 복구 시도
)

# 세션 팩토리 생성 (FastAPI 의존성으로 주입할 예정)
# SessionLocal을 FastAPI 경로에 주입(Dependency Injection)하여, API 호출 시마다 DB 세션을 열고 닫음
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

