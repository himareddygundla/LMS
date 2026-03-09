import os
from pathlib import Path
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .mongo import count_documents
from . import models
from .routers import participants, trainers, events, logs

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Event Management Platform', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

BASE_DIR = Path(__file__).resolve().parent
app.mount('/static', StaticFiles(directory=str(BASE_DIR / 'static')), name='static')
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

app.include_router(participants.router, prefix='/api')
app.include_router(trainers.router, prefix='/api')
app.include_router(events.router, prefix='/api')
app.include_router(logs.router, prefix='/api')


def render_page(request: Request, template_name: str, title: str, subtitle: str):
    return templates.TemplateResponse(template_name, {
        'request': request,
        'app_name': 'EventSphere',
        'page_title': title,
        'page_subtitle': subtitle,
    })


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/api/dashboard-summary')
def dashboard_summary(db: Session = Depends(get_db)):
    return {
        'participants': db.query(models.Participant).count(),
        'trainers': db.query(models.Trainer).count(),
        'events': db.query(models.Event).count(),
        'registrations': db.query(models.Registration).count(),
        'logs': count_documents('event_logs') + count_documents('user_activity_logs'),
        'feedback': list(),
    }


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return render_page(request, 'index.html', 'Control Center', 'Track the overall platform and jump into each module.')


@app.get('/participants', response_class=HTMLResponse)
def participants_page(request: Request):
    return render_page(request, 'participants.html', 'Participants Module', 'Register, update, delete, view participants, and register them for events.')


@app.get('/trainers', response_class=HTMLResponse)
def trainers_page(request: Request):
    return render_page(request, 'trainers.html', 'Trainers Module', 'Add trainers, update their profiles, assign them to events, and review sessions.')


@app.get('/events', response_class=HTMLResponse)
def events_page(request: Request):
    return render_page(request, 'events.html', 'Events Module', 'Create, update, delete events, and manage event capacity cleanly.')
