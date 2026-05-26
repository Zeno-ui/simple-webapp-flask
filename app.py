from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from models import db
from notes_api import notes_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)
Swagger(app)

app.register_blueprint(notes_api)

@app.route("/")
def main():
    return "Welcome!"

@app.route('/how-are-you')
def hello():
    return 'I am good, how about you?'

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)