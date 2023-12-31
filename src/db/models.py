from beanie import Document, Indexed


class User(Document):
    user_id: Indexed(int, unique=True)
