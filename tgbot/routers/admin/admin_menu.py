# - *- coding: utf- 8 - *-
import os

import aiofiles
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from tgbot.data.config import PATH_LOGS, PATH_DATABASE
from tgbot.database.db_users import Clientx, Userx
from tgbot.keyboards.reply_main import (
    payments_frep,
    settings_frep,
    functions_frep,
    items_frep,
)
from tgbot.utils.const_functions import get_date
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import get_statistics

router = Router(name=__name__)


# Платежные системы
@router.message(F.text == "🔑 Платежные системы")
async def admin_payments(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🔑 Настройка платежных системы.</b>",
        reply_markup=payments_frep(),
    )


# Настройки бота
@router.message(F.text == "⚙️ Настройки")
async def admin_settings(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>⚙️ Основные настройки бота.</b>",
        reply_markup=settings_frep(),
    )


# Общие функции
@router.message(F.text == "🔆 Общие функции")
async def admin_functions(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🔆 Выберите нужную функцию.</b>",
        reply_markup=functions_frep(),
    )


from tgbot.utils.const_functions import ikb
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Общие функции
@router.message(F.text == "🗂 Список пользователей")
async def admin_functions(message: Message, bot: Bot, state: FSM, arSession: ARS):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(ikb("🧑🏻‍💻 Исполнитель", data="find_all_user")).row(
        ikb("💰 Клиент", data="find_all_client")
    )

    await message.answer(
        "Выберите категорию поиска:", reply_markup=keyboard.as_markup()
    )


from aiogram.types import CallbackQuery


# Обработчик для отображения всех пользователей или клиентов
@router.callback_query(F.data.in_({"find_all_user", "find_all_client"}))
async def show_user_list(callback: CallbackQuery, bot: Bot):
    # Проверяем, какая кнопка была нажата
    if callback.data == "find_all_user":
        users = Userx.get_all()  # Получаем всех пользователей
        user_type = "пользователей"
    elif callback.data == "find_all_client":
        users = Clientx.get_all()  # Получаем всех клиентов
        user_type = "клиентов"

    # Формируем текст ответа
    if not users:
        text = f"Список {user_type} пуст."
    else:
        text = f"Список {user_type}:\n\n"
        for user in users:
            text += (
                f"ID: {user.user_id if hasattr(user, 'user_id') else user.client_id}\n"
                f"Логин: {user.user_login if hasattr(user, 'user_login') else user.client_login}\n"
                f"Имя: {user.user_name if hasattr(user, 'user_name') else user.client_name}\n"
                f"Баланс: {user.user_balance if hasattr(user, 'user_balance') else user.client_balance} руб.\n"
                f"Номер: {user.user_number if hasattr(user, 'user_number') else user.client_number}\n"
                f"----------------------\n"
            )

    # Отправляем сообщение с результатами
    await callback.message.edit_text(text)


# Управление товарами
@router.message(F.text == "🧑🏻‍💻 Управление заказами")
async def admin_products(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🧑🏻‍💻 Редактирование заданий.</b>",
        reply_markup=items_frep(),
    )


# Cтатистики бота
@router.message(F.text == "📊 Статистика")
async def admin_statistics(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(get_statistics())


# Получение БД
@router.message(Command(commands=["db", "database"]))
async def admin_database(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer_document(
        FSInputFile(PATH_DATABASE),
        caption=f"<b>📦 #BACKUP | <code>{get_date(full=False)}</code></b>",
    )


# Получение Логов
@router.message(Command(commands=["log", "logs"]))
async def admin_log(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    media_group = MediaGroupBuilder(
        caption=f"<b>🖨 #LOGS | <code>{get_date(full=False)}</code></b>",
    )

    if os.path.isfile(PATH_LOGS):
        media_group.add_document(media=FSInputFile(PATH_LOGS))

    if os.path.isfile("tgbot/data/sv_log_err.log"):
        media_group.add_document(media=FSInputFile("tgbot/data/sv_log_err.log"))

    if os.path.isfile("tgbot/data/sv_log_out.log"):
        media_group.add_document(media=FSInputFile("tgbot/data/sv_log_out.log"))

    await message.answer_media_group(media=media_group.build())


# Очистка логов
@router.message(
    Command(commands=["clear_log", "clear_logs", "log_clear", "logs_clear"])
)
async def admin_log_clear(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    if os.path.isfile(PATH_LOGS):
        async with aiofiles.open(PATH_LOGS, "w") as file:
            await file.write(f"{get_date()} | LOGS WAS CLEAR")

    if os.path.isfile("tgbot/data/sv_log_err.log"):
        async with aiofiles.open("tgbot/data/sv_log_err.log", "w") as file:
            await file.write(f"{get_date()} | LOGS ERR WAS CLEAR")

    if os.path.isfile("tgbot/data/sv_log_out.log"):
        async with aiofiles.open("tgbot/data/sv_log_out.log", "w") as file:
            await file.write(f"{get_date()} | LOGS OUT WAS CLEAR")

    await message.answer("<b>🖨 Логи были успешно очищены</b>")
