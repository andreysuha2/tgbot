from aiogram.filters.callback_data import CallbackData

class AcceptMessageCallbackFactory(CallbackData, prefix="accept_message"):
    action: str
    message_id: str