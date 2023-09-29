from aiogram.filters.callback_data import CallbackData

class AcсeptModeratorCallbackFactory(CallbackData, prefix="accept_moderator"):
    action: str
    user_id: int