from datetime import timedelta
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status

from app.core.config import settings
from app.core.db import init_db, get_session
from app.core.security import verify_password, get_password_hash, create_access_token

from app.models.user import User, UserBase, UserCreate
from app.models.travel import Travel
from app.models.chat import ChatMessages
from app.models.itinerary import Itinerary


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 테이블 생성 (이미 있으면 생성 안 함)
    init_db()
    yield

app = FastAPI(title="Voyagent Backend API", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Voyagent Backend API!"}

@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where((User.user_id == user.user_id) | (User.email == user.email))).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID or email already exists"
        )
    
    hashed_password = get_password_hash(user.password)

    new_user = User(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    # DB에 사용자 정보 저장
    session.add(new_user)
    session.commit()
    session.refresh(new_user) # 새로 생성된 사용자 정보로 갱신
    
    return {"message": "User created successfully", "user_id": new_user.user_id}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.user_id == form_data.username)).first() # form_data는 username, password 속성을 가짐
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
