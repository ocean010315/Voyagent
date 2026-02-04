from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    """사용자 기본 정보 모델"""
    
    user_id: str = Field(index=True)
    name: str
    email: str = Field(index=True)


class User(UserBase, table=True):
    """사용자 테이블 모델"""
    
    # Primary Key로 UUID 사용
    id: UUID = Field(default_factory=uuid4, primary_key=True)  # default_factory: 실행 시점에 동적으로 값 생성

    # user_id: str = Field(unique=True, index=True, nullable=False)
    password_hash: str = Field(nullable=False)
    # name: str = Field(nullable=False)
    # email: str = Field(unique=True, nullable=False)

    is_verified: bool = Field(default=False)  # default: 고정된 값
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserCreate(UserBase):
    """사용자 생성 시 필요한 입력 모델"""
    
    password: str


class UserRead(UserBase):
    """사용자 조회 시 반환 모델"""
    
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]