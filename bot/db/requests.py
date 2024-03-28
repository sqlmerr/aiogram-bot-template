from .models import User


async def get_user(user_id: int):
    return await User.find_one(User.user_id == user_id)
