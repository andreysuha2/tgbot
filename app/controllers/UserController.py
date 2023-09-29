from app.models import User, UserRole
from aiogram import types
from app.core.telegram import tg_bot
from app.core.config import config
from app.callbacks_factorys.user_callbacks import AcсeptModeratorCallbackFactory

class UserController:
    SUPER_ADMINS = config.env.get("BOT_SUPER_ADMINS", "").split(",")

    def _get_acceped_mod_keyboard(self, user_id: int) -> types.InlineKeyboardMarkup:
        buttons = [
            [
                types.InlineKeyboardButton(
                    text='Підтвердити',
                    callback_data=AcсeptModeratorCallbackFactory(action="accept", user_id=user_id).pack()
                ),
                types.InlineKeyboardButton(
                    text='Відхилити',
                    callback_data=AcсeptModeratorCallbackFactory(action="decline", user_id=user_id).pack()
                )
            ]
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=buttons)

    async def start_admin(self, message: types.Message):
        data = message.from_user
        admin = User.objects(user_id=data.id).first()
        if not admin:
            admin = User(user_id=data.id, first_name=data.first_name, user_name=data.username, role=UserRole.ADMIN)
        else:
            admin.first_name = data.first_name
            admin.user_name = data.username
            admin.role = UserRole.ADMIN
        admin.save()
        await message.answer(f'Hello, {admin.first_name}. Welcome to tgbot as admin!')

    async def start_guest(self, message: types.Message):
        user = User.objects(user_id = message.from_user.id).first()
        if not user:
            data = message.from_user
            user = User(user_id=data.id, first_name=data.first_name, user_name=data.username)
            user.save()
        for id in self.SUPER_ADMINS:
            await tg_bot.send_message(
                id, 
                f"Користувач: {user.first_name} хоче бути модератором",
                reply_markup=self._get_acceped_mod_keyboard(user.user_id)
                )
        await message.answer("Очікуйте підтвердження адміністратором")

    async def accept_moderator(self, clb, id):
        user = User.objects(user_id=id).first()
        if user:
            user.role = UserRole.MODERATOR
            user.save()
            await clb.answer(f"Користувача {user.first_name} підтверджено як модератора")
            await tg_bot.send_message(id, text="Вітаю, Вас схвалено як модератора!")
        else:
            await clb.answer(f"Користувача з id: {id}, не знайдено в системі")

    async def decline_moderator(self, clb, id):
        user = User.objects(user_id=id).first()
        if user:
            user.delete()
            await clb.answer(f"Користувача {user.first_name} відхилено як модератора")
        else:
            await clb.answer(f"Користувача з id: {id}, не знайдено в системі")

user_controller = UserController()
