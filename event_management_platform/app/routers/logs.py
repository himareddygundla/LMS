from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from ..deps import get_logs_db

router = APIRouter(prefix='/logs', tags=['Logs'])


def normalize(doc: dict):
    doc['id'] = str(doc.pop('_id'))
    if 'created_at' in doc:
        doc['created_at'] = str(doc['created_at'])
    return doc


@router.get('/event')
def get_event_logs(db=Depends(get_logs_db)):
    return [normalize(item) for item in db['event_logs'].find().sort('_id', -1)]


@router.get('/activity')
def get_activity_logs(db=Depends(get_logs_db)):
    return [normalize(item) for item in db['user_activity_logs'].find().sort('_id', -1)]


@router.post('/feedback', status_code=status.HTTP_201_CREATED)
def create_feedback(payload: dict, db=Depends(get_logs_db)):
    if not payload.get('name') or not payload.get('comment'):
        raise HTTPException(status_code=400, detail='name and comment are required')
    result = db['feedback_comments'].insert_one(payload)
    return {'message': 'Feedback saved', 'id': str(result.inserted_id)}


@router.get('/feedback')
def get_feedback(db=Depends(get_logs_db)):
    return [normalize(item) for item in db['feedback_comments'].find().sort('_id', -1)]


@router.delete('/feedback/{feedback_id}')
def delete_feedback(feedback_id: str, db=Depends(get_logs_db)):
    result = db['feedback_comments'].delete_one({'_id': ObjectId(feedback_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail='Feedback not found')
    return {'message': 'Feedback deleted'}
