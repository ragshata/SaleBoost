# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from tgbot.data.config import get_admins
from tgbot.utils.const_functions import ikb, rkb


# Кнопки главного меню
def menu_frep(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    if user_id in get_admins():
        keyboard.row(
            rkb("🧑🏻‍💻 Управление заказами"),
            rkb("📊 Статистика"),
        ).row(
            rkb("⚙️ Настройки"),
            rkb("🔆 Общие функции"),
        ).row(
            rkb("🗂 Список пользователей"),
        )

    if not (user_id in get_admins()):
        keyboard.row(
            rkb("🧑🏻‍💻 I am a performer"),
        ).row(rkb("🔎 I am the customer"))

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки главного меню клиентов
def menu_second_start_clients(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(rkb("📝 Order Management"), rkb("💡 My orders")).row(
        rkb("👤 My Profile"), rkb("📍 Help")
    ).row(rkb("📖 Legal information"))

    return keyboard.as_markup(resize_keyboard=True)


def menu_second_start(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🧑🏻‍💻 Orders"),
        rkb("🪄 My Orders"),
    ).row(
        rkb("👤 Profile"), rkb("➕ Help")
    ).row(rkb("📗 Legal information"))

    return keyboard.as_markup(resize_keyboard=True)


def client_functions_codexk(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🗣 User Agreement"),
        rkb("👤 Privacy Policy"),
    ).row(rkb("📚 Help")).row(rkb("🔙 Back"))

    return keyboard.as_markup(resize_keyboard=True)


def user_functions_codexk(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🗣 User Agreement"),
        rkb("👤 Privacy Policy"),
    ).row(rkb("📚 База знаний")).row(rkb("◀️ Back"))

    return keyboard.as_markup(resize_keyboard=True)


def menu_help_clients(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🛎 Support"),
        rkb("❓ FAQ"),
    ).row(rkb("🔙 Back"))

    return keyboard.as_markup(resize_keyboard=True)


def menu_help_users(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🛎 Support"),
        rkb("❓ FAQ"),
    ).row(rkb("◀️ Back"))

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки платежных систем
def payments_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(rkb("🔙 Main menu"), rkb("🖲 Способы пополнений"))

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки общих функций
def functions_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🔍 Поиск"),
        rkb("📢 Рассылка"),
    ).row(rkb("🔙 Main menu"))

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки настроек
def settings_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🖍 Изменить данные"),
        rkb("🕹 Выключатели"),
    ).row(rkb("🔙 Main menu"))

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки настроек
def who_get_mail() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🚨 Всем"),
    ).row(rkb("🧑🏻‍💻 Исполнителям"), rkb("💰 Заказчикам")).row(
        rkb("🔙 Main menu"),
    )

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки изменения заказов
def items_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(rkb("📦 Все заказы")).row(
        rkb("📁 Создать заказ"),
        rkb("🗃 Создать категорию"),
    ).row(rkb("🖍 Изменить заказ"), rkb("🖍 Изменить категорию")).row(
        rkb("🔙 Main menu"), rkb("❌ Удаление")
    )

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки изменения заказов для клиента
def items_frep_client() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(rkb("📁 Создать заказ")).row(rkb("🔙 Back"))

    return keyboard.as_markup(resize_keyboard=True)


def order_category() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(rkb("📁 Все заказы"), rkb("👤 В работе")).row(
        rkb("✅ Выполненные"), rkb("🔙 Back")
    )

    return keyboard.as_markup(resize_keyboard=True)
