from flask_sqlalchemy import SQLAlchemy
import hashlib
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return{
            'username':self.username,
            'password':self.password
        }   