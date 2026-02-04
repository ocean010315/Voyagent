from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from app.models.travel import Travel


KST = timezone(timedelta(hours=9))  # 한국 표준시 (KST)

class ChatMessages(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID = Field(foreign_key="user.id")
    travel_id: Optional[UUID] = Field(foreign_key="travel.id", default=None) # 대화 진행 시점이 여행 확정 전임

    role: str = Field(nullable=False, max_length=50)  # user, assistant
    content: str = Field(nullable=False, max_length=5000)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(KST))

    travel: Optional["Travel"] = Relationship(back_populates="chats")