from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from settings import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % DATABASE_FILE
db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    path = db.Column(db.String(512), unique=True)
    hash = db.Column(db.String(40), unique=True)
    root = db.Column(db.String(40), nullable=True)
    is_dir = db.Column(db.Boolean(), default=False)

    def __init__(self, name, path, hash, root=None, is_dir=False):
        self.name = name
        self.path = path
        self.hash = hash
        self.root = root
        self.is_dir = is_dir

    def __repr__(self):
        return '<File %r, hash: %r>' % (self.name, self.hash)

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'hash' : self.hash,
            'is_dir': self.is_dir
        }