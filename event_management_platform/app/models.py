from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base


class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True)
    company = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    registrations = relationship('Registration', back_populates='participant', cascade='all, delete-orphan')


class Trainer(Base):
    __tablename__ = 'trainers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    expertise = Column(String(200), nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    events = relationship('Event', back_populates='trainer')


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(150), nullable=False)
    date = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False, default=30)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    trainer = relationship('Trainer', back_populates='events')
    registrations = relationship('Registration', back_populates='event', cascade='all, delete-orphan')


class Registration(Base):
    __tablename__ = 'registrations'
    __table_args__ = (
        UniqueConstraint('participant_id', 'event_id', name='uq_participant_event'),
    )

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey('participants.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    status = Column(String(30), nullable=False, default='registered')
    created_at = Column(DateTime, default=datetime.utcnow)

    participant = relationship('Participant', back_populates='registrations')
    event = relationship('Event', back_populates='registrations')
