from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..mongo import safe_log

router = APIRouter(prefix='/trainers', tags=['Trainers'])


@router.post('', response_model=schemas.TrainerOut, status_code=status.HTTP_201_CREATED)
def create_trainer(payload: schemas.TrainerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Trainer).filter(models.Trainer.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Trainer email already exists')

    trainer = models.Trainer(**payload.model_dump())
    db.add(trainer)
    db.commit()
    db.refresh(trainer)
    safe_log('user_activity_logs', {'action': 'trainer_created', 'trainer_id': trainer.id, 'email': trainer.email})
    return trainer


@router.get('', response_model=list[schemas.TrainerOut])
def list_trainers(db: Session = Depends(get_db)):
    return db.query(models.Trainer).order_by(models.Trainer.id.desc()).all()


@router.put('/{trainer_id}', response_model=schemas.TrainerOut)
def update_trainer(trainer_id: int, payload: schemas.TrainerUpdate, db: Session = Depends(get_db)):
    trainer = db.query(models.Trainer).filter(models.Trainer.id == trainer_id).first()
    if not trainer:
        raise HTTPException(status_code=404, detail='Trainer not found')

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(trainer, key, value)
    db.commit()
    db.refresh(trainer)
    safe_log('user_activity_logs', {'action': 'trainer_updated', 'trainer_id': trainer.id})
    return trainer


@router.get('/sessions')
def view_sessions(db: Session = Depends(get_db)):
    events = db.query(models.Event).order_by(models.Event.date.asc()).all()
    sessions = []
    for event in events:
        sessions.append({
            'event_id': event.id,
            'title': event.title,
            'date': event.date,
            'location': event.location,
            'trainer': event.trainer.name if event.trainer else None,
            'capacity': event.capacity,
        })
    return sessions
