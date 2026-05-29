# simple-webapp-flask

A simple Flask web application enhanced with a full REST API for Notes management.

## Original Application

Original repository: https://github.com/mmumshad/simple-webapp-flask

The original app was a minimal Flask application with only two routes:
- `GET /` → returns "Welcome!"
- `GET /how-are-you` → returns "I am good, how about you?"

---

## What I Added

I added a full **Notes REST API** with complete CRUD functionality on a new branch:
`feature/notes-rest-api`

### New Files
| File | Description |
|------|-------------|
| `models.py` | Note database model using SQLAlchemy |
| `notes_api.py` | REST API blueprint with all CRUD endpoints |
| `tests/test_notes_api.py` | 13 unit tests with 100% coverage |

### Changes to Existing Files
| File | Change |
|------|--------|
| `app.py` | Registered the API blueprint, added SQLAlchemy and Swagger |
| `requirements.txt` | Added new dependencies |

---

## API Endpoints

| Method | URL | Description | Status Code |
|--------|-----|-------------|-------------|
| POST | `/api/notes` | Create a new note | 201 |
| GET | `/api/notes` | Get all notes | 200 |
| GET | `/api/notes/<id>` | Get a single note | 200 / 404 |
| PUT | `/api/notes/<id>` | Update a note | 200 / 400 / 404 |
| DELETE | `/api/notes/<id>` | Delete a note | 200 / 404 |

---

## Example Requests

### Create a note
```bash
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"data": "Buy groceries"}'
```

### Get all notes
```bash
curl http://localhost:5000/api/notes
```

### Get one note
```bash
curl http://localhost:5000/api/notes/1
```

### Update a note
```bash
curl -X PUT http://localhost:5000/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"data": "Buy milk instead"}'
```

### Delete a note
```bash
curl -X DELETE http://localhost:5000/api/notes/1
```

---

## Swagger API Documentation

Run the app and visit:

## http://localhost:5000/apidocs

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/Zeno-ui/simple-webapp-flask.git
cd simple-webapp-flask
git checkout feature/notes-rest-api
```

### 2. Install dependencies
```bash
pip install "jsonschema==4.17.3" flask flask-sqlalchemy flasgger pytest pytest-cov
```

### 3. Run the app
```bash
python app.py
```

### 4. Run the tests
```bash
python -m pytest tests/ -v --cov=notes_api --cov-report=term-missing
```

---

## Test Results
    tests/test_notes_api.py::test_create_note_success        PASSED
    tests/test_notes_api.py::test_create_note_missing_field  PASSED
    tests/test_notes_api.py::test_create_note_empty_string   PASSED
    tests/test_notes_api.py::test_get_all_notes_empty        PASSED
    tests/test_notes_api.py::test_get_all_notes_with_data    PASSED
    tests/test_notes_api.py::test_get_single_note_success    PASSED
    tests/test_notes_api.py::test_get_single_note_not_found  PASSED
    tests/test_notes_api.py::test_update_note_success        PASSED
    tests/test_notes_api.py::test_update_note_not_found      PASSED
    tests/test_notes_api.py::test_update_note_missing_field  PASSED
    tests/test_notes_api.py::test_update_note_empty_string   PASSED
    tests/test_notes_api.py::test_delete_note_success        PASSED
    tests/test_notes_api.py::test_delete_note_not_found      PASSED
    Coverage: 100%

