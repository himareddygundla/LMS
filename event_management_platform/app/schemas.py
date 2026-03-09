from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class ParticipantBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=120)


class ParticipantCreate(ParticipantBase):
    pass


class ParticipantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    company: Optional[str] = Field(None, max_length=120)


class ParticipantOut(ParticipantBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TrainerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    expertise: str = Field(..., min_length=2, max_length=200)
    bio: Optional[str] = None


class TrainerCreate(TrainerBase):
    pass


class TrainerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    expertise: Optional[str] = Field(None, min_length=2, max_length=200)
    bio: Optional[str] = None


class TrainerOut(TrainerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EventBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: Optional[str] = None
    location: str = Field(..., min_length=2, max_length=150)
    date: str = Field(..., min_length=3, max_length=50)
    capacity: int = Field(..., ge=1, le=10000)


class EventCreate(EventBase):
    trainer_id: Optional[int] = None


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = None
    location: Optional[str] = Field(None, min_length=2, max_length=150)
    date: Optional[str] = Field(None, min_length=3, max_length=50)
    capacity: Optional[int] = Field(None, ge=1, le=10000)
    trainer_id: Optional[int] = None


class EventOut(EventBase):
    id: int
    trainer_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class RegistrationCreate(BaseModel):
    participant_id: int
    event_id: int


class RegistrationOut(BaseModel):
    id: int
    participant_id: int
    event_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AssignTrainerRequest(BaseModel):
    trainer_id: int


class DashboardSummary(BaseModel):
    participants: int
    trainers: int
    events: int
    registrations: int
    logs: int
    feedback: List[dict]
