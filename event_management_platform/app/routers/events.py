from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..mongo import safe_log

router = APIRouter(prefix='/events', tags=['Events'])


@router.post('', response_model=schemas.EventOut, status_code=status.HTTP_201_CREATED)
def create_event(payload: schemas.EventCreate, db: Session = Depends(get_db)):
    if payload.trainer_id:
        trainer = db.query(models.Trainer).filter(models.Trainer.id == payload.trainer_id).first()
        if not trainer:
            raise HTTPException(status_code=404, detail='Trainer not found')

    event = models.Event(**payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    safe_log('event_logs', {'action': 'event_created', 'event_id': event.id, 'title': event.title})
    return event


@router.get('', response_model=list[schemas.EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(models.Event).order_by(models.Event.id.desc()).all()


@router.put('/{event_id}', response_model=schemas.EventOut)
def update_event(event_id: int, payload: schemas.EventUpdate, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')

    updates = payload.model_dump(exclude_unset=True)
    if 'trainer_id' in updates and updates['trainer_id'] is not None:
        trainer = db.query(models.Trainer).filter(models.Trainer.id == updates['trainer_id']).first()
        if not trainer:
            raise HTTPException(status_code=404, detail='Trainer not found')

    for key, value in updates.items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    safe_log('event_logs', {'action': 'event_updated', 'event_id': event.id})
    return event


@router.delete('/{event_id}', status_code=status.HTTP_200_OK)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')
    db.delete(event)
    db.commit()
    safe_log('event_logs', {'action': 'event_deleted', 'event_id': event_id})
    return {'message': 'Event deleted successfully'}


@router.post('/{event_id}/assign-trainer')
def assign_trainer(event_id: int, payload: schemas.AssignTrainerRequest, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    trainer = db.query(models.Trainer).filter(models.Trainer.id == payload.trainer_id).first()

    if not event:
        raise HTTPException(status_code=404, detail='Event not found')
    if not trainer:
        raise HTTPException(status_code=404, detail='Trainer not found')

    event.trainer_id = trainer.id
    db.commit()
    db.refresh(event)
    safe_log('event_logs', {'action': 'trainer_assigned', 'event_id': event.id, 'trainer_id': trainer.id})
    return {'message': 'Trainer assigned successfully', 'event_id': event.id, 'trainer_id': trainer.id}
