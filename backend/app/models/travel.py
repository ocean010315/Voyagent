from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.itinerary import Itinerary
    from app.models.chat import ChatMessages


KST = timezone(timedelta(hours=9)) # 한국 표준시 (KST)

class Travel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    user_id: UUID = Field(foreign_key="user.id")
    
    title: str = Field(nullable=False, max_length=255)
    destination: str = Field(nullable=False, max_length=100)
    start_date: datetime
    end_date: datetime

    created_at: datetime = Field(default_factory=lambda: datetime.now(KST))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(KST))

    # travel.itineraries, travel.chats 로 접근 가능
    itineraries: List["Itinerary"] = Relationship(back_populates="travel") # back_populates: 양방향 관계 설정
    chats: List["ChatMessages"] = Relationship(back_populates="travel")