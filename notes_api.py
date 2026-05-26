from flask import Blueprint, request, jsonify
from models import db, Note

notes_api = Blueprint('notes_api', __name__, url_prefix='/api')


# CREATE — POST /api/notes
@notes_api.route('/notes', methods=['POST'])
def create_note():
    """
    Create a note
    ---
    tags:
      - Notes
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [data]
          properties:
            data:
              type: string
              example: "Buy groceries"
    responses:
      201:
        description: Note created
      400:
        description: Bad request
    """
    body = request.get_json()

    if not body or 'data' not in body:
        return jsonify({'error': 'Missing "data" field.'}), 400

    text = body['data'].strip()
    if len(text) < 1:
        return jsonify({'error': 'Note cannot be empty.'}), 400

    note = Note(data=text)
    db.session.add(note)
    db.session.commit()

    return jsonify({
        'message': 'Note created.',
        'note': {'id': note.id, 'data': note.data}
    }), 201


# READ ALL — GET /api/notes
@notes_api.route('/notes', methods=['GET'])
def get_notes():
    """
    Get all notes
    ---
    tags:
      - Notes
    responses:
      200:
        description: List of notes
    """
    notes = Note.query.all()
    return jsonify({
        'notes': [{'id': n.id, 'data': n.data} for n in notes]
    }), 200


# READ ONE — GET /api/notes/<id>
@notes_api.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """
    Get a single note
    ---
    tags:
      - Notes
    parameters:
      - in: path
        name: note_id
        type: integer
        required: true
    responses:
      200:
        description: Note found
      404:
        description: Note not found
    """
    note = db.session.get(Note, note_id)
    if not note:
        return jsonify({'error': 'Note not found.'}), 404

    return jsonify({'id': note.id, 'data': note.data}), 200


# UPDATE — PUT /api/notes/<id>
@notes_api.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """
    Update a note
    ---
    tags:
      - Notes
    parameters:
      - in: path
        name: note_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [data]
          properties:
            data:
              type: string
              example: "Updated text"
    responses:
      200:
        description: Note updated
      400:
        description: Bad request
      404:
        description: Note not found
    """
    note = db.session.get(Note, note_id)
    if not note:
        return jsonify({'error': 'Note not found.'}), 404

    body = request.get_json()
    if not body or 'data' not in body:
        return jsonify({'error': 'Missing "data" field.'}), 400

    text = body['data'].strip()
    if len(text) < 1:
        return jsonify({'error': 'Note cannot be empty.'}), 400

    note.data = text
    db.session.commit()

    return jsonify({
        'message': 'Note updated.',
        'note': {'id': note.id, 'data': note.data}
    }), 200


# DELETE — DELETE /api/notes/<id>
@notes_api.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """
    Delete a note
    ---
    tags:
      - Notes
    parameters:
      - in: path
        name: note_id
        type: integer
        required: true
    responses:
      200:
        description: Note deleted
      404:
        description: Note not found
    """
    note = db.session.get(Note, note_id)
    if not note:
        return jsonify({'error': 'Note not found.'}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted.'}), 200