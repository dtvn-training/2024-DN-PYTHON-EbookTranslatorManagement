class Comment:
    def __init__(self, comment_id, fullname, role, content, status):
        self.comment_id = comment_id
        self.fullname = fullname
        self.role = role
        self.status = status
        self.content = content

    def to_dict(self):
        return {
            "comment_id": self.comment_id,
            "fullname": self.fullname,
            "role": self.role,
            "status": self.status,
            "content": self.content,

        }

    @classmethod
    def create(cls, comment):
        comment_dict = cls(comment[0], comment[1],
                           comment[2], comment[3], comment[4]).to_dict()
        return comment_dict
