from database.db import db
from datetime import datetime

class UserNotification(db.Model):
    __tablename__ = 'user_notification'

    user_notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID duy nhất cho mỗi bản ghi
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)  # Liên kết với người dùng
    notification_id = db.Column(db.Integer, db.ForeignKey('notification.notification_id', ondelete='CASCADE'), nullable=False)  # Liên kết với thông báo
    status = db.Column(db.Boolean, default=False)  # Trạng thái thông báo (đã đọc hoặc chưa đọc)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Thời gian tạo
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Thời gian cập nhật

    # Quan hệ với bảng User và Notification
    user = db.relationship('User', backref='user_notifications', lazy=True)
    notification = db.relationship('Notification', backref='user_notifications', lazy=True)

    def __init__(self, user_id, notification_id, status=False):
        self.user_id = user_id
        self.notification_id = notification_id
        self.status = status

    def to_dict(self):
        return {
            "user_notification_id": self.user_notification_id,
            "user_id": self.user_id,
            "notification_id": self.notification_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
