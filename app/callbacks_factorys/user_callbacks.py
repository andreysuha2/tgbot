from aiogram.filters.callback_data import CallbackData

class AcceptModeratorCallbackFactory(CallbackData, prefix="accept_moderator"):
    action: str
    user_id: int