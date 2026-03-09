from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..mongo import safe_log

router = APIRouter(prefix='/participants', tags=['Participants'])


@router.post('', response_model=schemas.ParticipantOut, status_code=status.HTTP_201_CREATED)
def create_participant(payload: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Participant).filter(models.Participant.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Participant email already exists')

    participant = models.Participant(**payload.model_dump())
    db.add(participant)
    db.commit()
    db.refresh(participant)
    safe_log('user_activity_logs', {'action': 'participant_created', 'participant_id': participant.id, 'email': participant.email})
    return participant


@router.get('', response_model=list[schemas.ParticipantOut])
def list_participants(db: Session = Depends(get_db)):
    return db.query(models.Participant).order_by(models.Participant.id.desc()).all()


@router.put('/{participant_id}', response_model=schemas.ParticipantOut)
def update_participant(participant_id: int, payload: schemas.ParticipantUpdate, db: Session = Depends(get_db)):
    participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail='Participant not found')

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(participant, key, value)
    db.commit()
    db.refresh(participant)
    safe_log('user_activity_logs', {'action': 'participant_updated', 'participant_id': participant.id})
    return participant


@router.delete('/{participant_id}', status_code=status.HTTP_200_OK)
def delete_participant(participant_id: int, db: Session = Depends(get_db)):
    participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail='Participant not found')
    db.delete(participant)
    db.commit()
    safe_log('user_activity_logs', {'action': 'participant_deleted', 'participant_id': participant_id})
    return {'message': 'Participant deleted successfully'}


@router.post('/register', response_model=schemas.RegistrationOut, status_code=status.HTTP_201_CREATED)
def register_for_event(payload: schemas.RegistrationCreate, db: Session = Depends(get_db)):
    participant = db.query(models.Participant).filter(models.Participant.id == payload.participant_id).first()
    event = db.query(models.Event).filter(models.Event.id == payload.event_id).first()

    if not participant:
        raise HTTPException(status_code=404, detail='Participant not found')
    if not event:
        raise HTTPException(status_code=404, detail='Event not found')

    current_count = db.query(models.Registration).filter(models.Registration.event_id == payload.event_id).count()
    if current_count >= event.capacity:
        raise HTTPException(status_code=400, detail='Event capacity is full')

    existing_registration = db.query(models.Registration).filter(
        models.Registration.participant_id == payload.participant_id,
        models.Registration.event_id == payload.event_id,
    ).first()
    if existing_registration:
        raise HTTPException(status_code=400, detail='Participant already registered for this event')

    registration = models.Registration(**payload.model_dump())
    db.add(registration)
    db.commit()
    db.refresh(registration)
    safe_log('event_logs', {'action': 'participant_registered', 'participant_id': payload.participant_id, 'event_id': payload.event_id})
    return registration
