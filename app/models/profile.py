from database.db import db


class Profile(db.Model):
    __tablename__ = 'profile'

    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(50))
    point = db.Column(db.Integer, default=0)
    level_id = db.Column(db.Integer, db.ForeignKey('level.level_id'))

    def __init__(self, fullname, email, phone=None, point=0, level_id=None):
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.point = point
        self.level_id = level_id

    def to_dict(self):
        return {
            "profile_id": self.profile_id,
            "fullname": self.fullname,
            "email": self.email,
            "phone": self.phone,
            "point": self.point,
            "level_id": self.level_id,
        }
