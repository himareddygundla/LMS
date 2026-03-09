def test_full_workflow(client):
    participant = client.post('/api/participants', json={
        'name': 'Rajashekar', 'email': 'rajashekar@example.com', 'phone': '9999999999', 'company': 'Capstone'
    })
    assert participant.status_code == 201
    participant_id = participant.json()['id']

    trainer = client.post('/api/trainers', json={
        'name': 'Anita Rao', 'email': 'anita@example.com', 'expertise': 'AI & Cloud', 'bio': 'Senior trainer'
    })
    assert trainer.status_code == 201
    trainer_id = trainer.json()['id']

    event = client.post('/api/events', json={
        'title': 'AI Bootcamp',
        'description': 'Hands-on event',
        'location': 'Hyderabad',
        'date': '2026-04-10 10:00 AM',
        'capacity': 2,
        'trainer_id': trainer_id,
    })
    assert event.status_code == 201
    event_id = event.json()['id']

    registration = client.post('/api/participants/register', json={
        'participant_id': participant_id,
        'event_id': event_id,
    })
    assert registration.status_code == 201
    assert registration.json()['status'] == 'registered'

    summary = client.get('/api/dashboard-summary')
    assert summary.status_code == 200
    data = summary.json()
    assert data['participants'] == 1
    assert data['trainers'] == 1
    assert data['events'] == 1
    assert data['registrations'] == 1


def test_capacity_validation(client):
    p1 = client.post('/api/participants', json={'name': 'P1', 'email': 'p1@example.com', 'phone': '1', 'company': 'A'})
    p2 = client.post('/api/participants', json={'name': 'P2', 'email': 'p2@example.com', 'phone': '2', 'company': 'A'})
    event = client.post('/api/events', json={
        'title': 'ML Workshop', 'description': 'desc', 'location': 'Online', 'date': 'tomorrow', 'capacity': 1
    })
    event_id = event.json()['id']

    assert client.post('/api/participants/register', json={'participant_id': p1.json()['id'], 'event_id': event_id}).status_code == 201
    blocked = client.post('/api/participants/register', json={'participant_id': p2.json()['id'], 'event_id': event_id})
    assert blocked.status_code == 400
    assert blocked.json()['detail'] == 'Event capacity is full'
