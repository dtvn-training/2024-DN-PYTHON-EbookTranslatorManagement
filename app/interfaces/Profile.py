class Profile:
    def __init__(self, full_name, username, avatar, email, phone_number, level, total_task, created_at):
        self.full_name = full_name
        self.username = username
        self.avatar = avatar
        self.email = email
        self.phone_number = phone_number
        self.level = level
        self.total_task = total_task
        self.created_at = created_at

    def to_dict(self):
        return {
            "full_name": self.full_name,
            "username": self.username,
            "avatar": self.avatar,
            "email": self.email,
            "phone_number": self.phone_number,
            "level": self.level,
            "total_task": self.total_task,
            "created_at": self.created_at,

        }

    @classmethod
    def create(cls, profile):
        profile = cls(profile[0], profile[1], profile[2], profile[3],
                      profile[4], profile[5], profile[6], profile[7])
        return profile.to_dict()
