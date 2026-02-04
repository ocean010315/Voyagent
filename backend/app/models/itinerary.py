from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

from app.models.travel import Travel


class Itinerary(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    travel_id: UUID = Field(foreign_key="travel.id")

    day_number: int = Field()
    visit_order: int = Field()
    category: str = Field(nullable=True, max_length=100) # 관광지, 음식점, 쇼핑, 숙박 등
    
    place_name: str = Field(nullable=False, max_length=255)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)

    memo: str = Field(nullable=True, max_length=1000) # AI가 생성한 설명 or 사용자 메모

    # 관계 설정
    travel: "Travel" = Relationship(back_populates="itineraries")  # back_populates: 양방향 관계 설정