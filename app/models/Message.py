from mongoengine import Document, StringField, DateTimeField, EnumField
from enum import Enum
from datetime import datetime

class MessageStatus(Enum):
    PENDING_FOR_VALIDATE = "pendind_for_validate"
    ON_AI_VALIDATE = "on_ai_validate"
    ON_HUMAN_VALIDATE = "on_human_validate"
    PENDING_FOR_POST = "pending_for_post"
    POSTED = "posted"
    DECLINED_BY_AI = "declined_by_ai"
    DECLINED_BY_HUMAN = "declined_by_human"

class Messages(Document):
    source = StringField(required=True)
    source_id = StringField(required=True)
    message_id = StringField(required=True)
    text = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)
    status = EnumField(MessageStatus, default=MessageStatus.PENDING_FOR_VALIDATE)
