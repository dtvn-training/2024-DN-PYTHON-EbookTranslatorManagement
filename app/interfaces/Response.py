class Response:
    def __init__(self, is_success, message, data):
        self.is_success = is_success
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "is_success": self.is_success,
            "message": self.message,
            "data": self.data
        }

    @classmethod
    def create(cls, is_success, message, data=None):
        res = cls(is_success, message, data)
        return res.to_dict()
