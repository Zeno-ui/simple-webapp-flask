import pytest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from models import db


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ── CREATE tests ──────────────────────────────

def test_create_note_success(client):
    r = client.post('/api/notes',
        data=json.dumps({'data': 'Buy milk'}),
        content_type='application/json')
    assert r.status_code == 201
    assert r.get_json()['note']['data'] == 'Buy milk'

def test_create_note_missing_field(client):
    r = client.post('/api/notes',
        data=json.dumps({'wrong': 'oops'}),
        content_type='application/json')
    assert r.status_code == 400

def test_create_note_empty_string(client):
    r = client.post('/api/notes',
        data=json.dumps({'data': '   '}),
        content_type='application/json')
    assert r.status_code == 400


# ── READ tests ────────────────────────────────

def test_get_all_notes_empty(client):
    r = client.get('/api/notes')
    assert r.status_code == 200
    assert r.get_json()['notes'] == []

def test_get_all_notes_with_data(client):
    client.post('/api/notes',
        data=json.dumps({'data': 'Note 1'}),
        content_type='application/json')
    client.post('/api/notes',
        data=json.dumps({'data': 'Note 2'}),
        content_type='application/json')
    r = client.get('/api/notes')
    assert len(r.get_json()['notes']) == 2

def test_get_single_note_success(client):
    client.post('/api/notes',
        data=json.dumps({'data': 'Hello'}),
        content_type='application/json')
    r = client.get('/api/notes/1')
    assert r.status_code == 200
    assert r.get_json()['data'] == 'Hello'

def test_get_single_note_not_found(client):
    r = client.get('/api/notes/999')
    assert r.status_code == 404


# ── UPDATE tests ──────────────────────────────

def test_update_note_success(client):
    client.post('/api/notes',
        data=json.dumps({'data': 'Old text'}),
        content_type='application/json')
    r = client.put('/api/notes/1',
        data=json.dumps({'data': 'New text'}),
        content_type='application/json')
    assert r.status_code == 200
    assert r.get_json()['note']['data'] == 'New text'

def test_update_note_not_found(client):
    r = client.put('/api/notes/999',
        data=json.dumps({'data': 'x'}),
        content_type='application/json')
    assert r.status_code == 404

def test_update_note_missing_field(client):
    client.post('/api/notes',
        data=json.dumps({'data': 'Original'}),
        content_type='application/json')
    r = client.put('/api/notes/1',
        data=json.dumps({}),
        content_type='application/json')
    assert r.status_code == 400


# ── DELETE tests ──────────────────────────────

def test_delete_note_success(client):
    client.post('/api/notes',
        data=json.dumps({'data': 'Delete me'}),
        content_type='application/json')
    r = client.delete('/api/notes/1')
    assert r.status_code == 200
    assert client.get('/api/notes/1').status_code == 404

def test_delete_note_not_found(client):
    r = client.delete('/api/notes/999')
    assert r.status_code == 404

def test_update_note_empty_string(client):
    client.post('/api/notes',
        data=json.dumps({'data': 'Original'}),
        content_type='application/json')
    r = client.put('/api/notes/1',
        data=json.dumps({'data': '   '}),
        content_type='application/json')
    assert r.status_code == 400