from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Dict, List


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class QuoteBase(BaseModel):
    quote: str
    character: str
    season: int
    episode: int


class QuoteCreate(QuoteBase):
    pass


class QuoteResponse(QuoteBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
