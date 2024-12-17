class Content:
    def __init__(self, content_id, content, status):
        self.content_id = content_id
        self.content = content
        self.status = status

    def to_dict(self):
        return {
            "content_id": self.content_id,
            "content": self.content,
            "status": self.status
        }

    @classmethod
    def create(cls, content):
        content_dict = cls(content[0], content[1], content[2]).to_dict()
        return content_dict
