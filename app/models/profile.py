from database.db import db


class Profile(db.Model):
    __tablename__ = 'profile'

    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100),default='Chưa có tên')
    email = db.Column(db.String(100), nullable=True, unique=True)
    phone = db.Column(db.String(50))
    point = db.Column(db.Integer, default=0)
    level_id = db.Column(db.Integer, db.ForeignKey('level.level_id'))
    task_quantity = db.Column(db.Integer, default=0)

    def __init__(self, email=None, fullname="Chưa có tên", phone=None, point=0, level_id=None,task_quantity=0):
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.point = point
        self.level_id = level_id
        self.task_quantity = task_quantity

    def to_dict(self):
        return {
            "profile_id": self.profile_id,
            "fullname": self.fullname,
            "email": self.email,
            "phone": self.phone,
            "point": self.point,
            "level_id": self.level_id,
            "task_quantity": self.task_quantity
        }
