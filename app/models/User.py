from mongoengine import Document, StringField, DateTimeField, EnumField, IntField
from enum import Enum
from datetime import datetime

class UserRole(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"

class Users(Document):
    user_id = IntField(required=True)
    first_name = StringField(required=True)
    user_name = StringField(null=True)
    role = EnumField(UserRole, default=UserRole.USER)
    timestamp = DateTimeField(default=datetime.utcnow)