from aiogram import Router, types, F
from aiogram.filters import Command
from app.controllers import user_controller
from app.filters.user_role import UserRoleFilter
from app.models import UserRole
from app.callbacks_factorys.user_callbacks import AcceptModeratorCallbackFactory

router = Router()

@router.message(Command("start"), UserRoleFilter([UserRole.ADMIN]))
async def start_command_admin(message: types.Message):
    await user_controller.start_admin(message)

@router.message(Command("start"), UserRoleFilter([UserRole.GUEST]))
async def start_command_guest(message: types.Message):
    await user_controller.start_guest(message)

@router.callback_query(AcceptModeratorCallbackFactory.filter(F.action == "accept"))
async def accept_modarator_callback(callback: types.CallbackQuery, callback_data: AcceptModeratorCallbackFactory):
    await user_controller.accept_moderator(callback, callback_data.user_id)

@router.callback_query(AcceptModeratorCallbackFactory.filter(F.action == "decline"))
async def decline_moderator_callback(callback: types.CallbackQuery, callback_data: AcceptModeratorCallbackFactory):
    await user_controller.decline_moderator(callback, callback_data.user_id)