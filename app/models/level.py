from database.db import db

class Level(db.Model):
    __tablename__ = 'level'

    level_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level_type = db.Column(db.String(15), default="begin", nullable=False)
    level_limit = db.Column(db.Integer, default=5, nullable=False)

    def __init__(self, level_type="begin", level_limit=5):
        self.level_type = level_type
        self.level_limit = level_limit

    def to_dict(self):
        return {
            "level_id": self.level_id,
            "level_type": self.level_type,
            "level_limit": self.level_limit
        }
