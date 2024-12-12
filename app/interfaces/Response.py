class Response:
    def __init__(self, success, message, data):
        self.success = success
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }

    @classmethod
    def create(cls, success, message, data=None):
        res = Response(success, message, data)
        return res.to_dict()
