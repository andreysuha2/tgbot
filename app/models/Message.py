from mongoengine import Document, StringField, DateTimeField, EnumField
from enum import Enum
from datetime import datetime

class MessageStatus(Enum):
    PENDING_FOR_VALIDATE = "pendind_for_validate"
    ON_VALIDATE = "on_validate"
    PENDING_FOR_POST = "pending_for_post"
    POSTED = "posted"
    DECLINE = "decline"

class Messages(Document):
    source = StringField(required=True)
    source_id = StringField(required=True)
    message_id = StringField(required=True)
    text = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)
    status = EnumField(MessageStatus, default=MessageStatus.PENDING_FOR_VALIDATE)
