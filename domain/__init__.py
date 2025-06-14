#declarative_base()가 반환하는 Base 클래스는
#메타데이터(MetaData)를 모아 테이블 스키마를 관리하고,
#ORM 모델 클래스들이 이 Base를 상속받음으로써 자동으로 테이블 매핑 정보(__tablename__, 컬럼, 관계 등)를 SQLAlchemy에 등록하게 해 줍니다.

from sqlalchemy.ext.declarative import declarative_base

Base= declarative_base()
