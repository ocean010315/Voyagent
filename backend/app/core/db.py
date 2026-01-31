import os
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

from app.core.config import settings


# DB engine 생성 (echo=True를 통해 개발단에서 보내는 쿼리 로깅 가능)
engine = create_engine(settings.DATABASE_URL, echo=True)

def init_db():
    """DB 초기화 함수: 모델 기반으로 테이블 생성"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """DB 세션 생성 함수: 의존성 주입에 사용, API에서 DB를 쓸 때 세션을 빌려줌"""
    with Session(engine) as session:
        yield session