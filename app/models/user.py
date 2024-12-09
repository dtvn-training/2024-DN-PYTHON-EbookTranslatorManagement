from database.db import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(100), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey(
        'profile.profile_id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Relationship với bảng Profile và Role
    profile = db.relationship('Profile', backref='users', lazy=True)
    role = db.relationship('Role', backref='users', lazy=True)

    def __init__(self, username, user_password, profile_id=None, role_id=None):
        self.username = username
        self.user_password = user_password
        self.profile_id = profile_id
        self.role_id = role_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "profile_id": self.profile_id,
            "role_id": self.role_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
