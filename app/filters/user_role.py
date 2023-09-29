from app.core.config import config
from typing import Union
from app.models import User, UserRole
from aiogram.filters import BaseFilter
from aiogram.types import Message


class UserRoleFilter(BaseFilter):
    def __init__(self, user_roles: Union[str, list]):
        self.user_roles = user_roles

    async def __call__(self, message: Message) -> bool:
        roles = {
            UserRole.ADMIN: [ int(id) for id in config.env.get("BOT_SUPER_ADMINS", "").split(",") ],
            UserRole.MODERATOR: [ user.user_id for user in User.objects(role=UserRole.MODERATOR) ],
            UserRole.USER: [ user.user_id for user in User.objects(role=UserRole.USER) ]
        }
        result = False 
        for role in self.user_roles:
            if role in roles:
                result = message.from_user.id in roles[role]
                if result:
                    break
        return result or (UserRole.GUEST in self.user_roles and not result)
        