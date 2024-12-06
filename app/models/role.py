from database.db import db

class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "role_id": self.role_id,
            "name": self.name,
        }
