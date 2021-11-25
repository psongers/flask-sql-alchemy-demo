from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQL_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/json')
def output_json():
    with open('./mount/ex.json') as f:
        return json.load(f)

# db setup
db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/load_db')
def create_all():
    db.create_all()
    db.session.add(User(username='admin', email="admin@email.com"))
    db.session.add(User(username='patrick', email="patrick@email.com"))
    db.session.commit()
    return f"db created for {app.config['SQLALCHEMY_DATABASE_URI']}"


@app.route('/db_query')
def test_db():
    return jsonify([str(u) for u in User.query.all()])


