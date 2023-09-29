from aiogram import Router, types, F
from app.controllers import message_controller
from app.callbacks_factorys.message_callbacks import AcceptMessageCallbackFactory

router = Router()

@router.callback_query(AcceptMessageCallbackFactory.filter(F.action == "accept"))
async def accept_message_callback(callback: types.CallbackQuery, callback_data: AcceptMessageCallbackFactory):
    await message_controller.accept_message(callback, callback_data.message_id)

@router.callback_query(AcceptMessageCallbackFactory.filter(F.action == "decline"))
async def decline_message_callback(callback: types.CallbackQuery, callback_data: AcceptMessageCallbackFactory):
    await message_controller.decline_message(callback, callback_data.message_id)