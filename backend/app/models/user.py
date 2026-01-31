from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from sqlmodel import SQLModel, Field
from typing import Optional


KST = timezone(timedelta(hours=9))  # 한국 표준시 (KST)

class User(SQLModel, table=True):
    # Primary Key로 UUID 사용
    id: UUID = Field(default_factory=uuid4, primary_key=True)  # default_factory: 실행 시점에 동적으로 값 생성

    user_id: str = Field(unique=True, index=True, nullable=False)
    password_hash: str = Field(nullable=False)
    name: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False)

    is_verifieid: bool = Field(default=False)  # default: 고정된 값
    created_at: datetime = Field(default_factory=lambda: datetime.now(KST))
    updated_at: Optional[datetime] = Field(default=None)