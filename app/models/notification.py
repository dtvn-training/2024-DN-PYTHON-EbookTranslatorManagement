from database.db import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notification'

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)  # Tiêu đề thông báo
    message = db.Column(db.Text, nullable=False)  # Nội dung thông báo
    target_url = db.Column(db.String(200))  # Đường dẫn mục tiêu
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Thời gian tạo thông báo
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Thời gian cập nhật thông báo
    deleted_at = db.Column(db.DateTime)  # Thời gian xóa thông báo (nếu có)

    def __init__(self, title, message, target_url=None):
        self.title = title
        self.message = message
        self.target_url = target_url

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "title": self.title,
            "message": self.message,
            "target_url": self.target_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
