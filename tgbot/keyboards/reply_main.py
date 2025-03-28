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
            rkb("🧑🏻‍💻 Я исполнитель"),
        ).row(rkb("🔎 Я заказчик"))

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки главного меню клиентов
def menu_second_start_clients(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(rkb("📝 Управление заказами"), rkb("💡 Мои заказы")).row(
        rkb("👤 Мой профиль"), rkb("📍 Помощь")
    ).row(rkb("📖 Правовая информация"))

    return keyboard.as_markup(resize_keyboard=True)


def menu_second_start(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🧑🏻‍💻 Заказы"),
        rkb("🪄 Мои Заказы"),
    ).row(
        rkb("👤 Профиль"), rkb("➕ Помощь")
    ).row(rkb("📗 Правовая информация"))

    return keyboard.as_markup(resize_keyboard=True)


def client_functions_codexk(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🗣 Пользовательское соглашение"),
        rkb("👤 Политика конфиденциальности"),
    ).row(rkb("📚 Помощь")).row(rkb("🔙 Назад"))

    return keyboard.as_markup(resize_keyboard=True)


def user_functions_codexk(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🗣 Пользовательское соглашение"),
        rkb("👤 Политика конфиденциальности"),
    ).row(rkb("📚 База знаний")).row(rkb("◀️ Назад"))

    return keyboard.as_markup(resize_keyboard=True)


def menu_help_clients(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🛎 Поддержка"),
        rkb("❓ FAQ"),
    ).row(rkb("🔙 Назад"))

    return keyboard.as_markup(resize_keyboard=True)


def menu_help_users(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🛎 Поддержка"),
        rkb("❓ FAQ"),
    ).row(rkb("◀️ Назад"))

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки платежных систем
def payments_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(rkb("🔙 Главное меню"), rkb("🖲 Способы пополнений"))

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки общих функций
def functions_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🔍 Поиск"),
        rkb("📢 Рассылка"),
    ).row(rkb("🔙 Главное меню"))

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки настроек
def settings_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🖍 Изменить данные"),
        rkb("🕹 Выключатели"),
    ).row(rkb("🔙 Главное меню"))

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки настроек
def who_get_mail() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🚨 Всем"),
    ).row(rkb("🧑🏻‍💻 Исполнителям"), rkb("💰 Заказчикам")).row(
        rkb("🔙 Главное меню"),
    )

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки изменения заказов
def items_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(rkb("📦 Все заказы")).row(
        rkb("📁 Создать заказ"),
        rkb("🗃 Создать категорию"),
    ).row(rkb("🖍 Изменить заказ"), rkb("🖍 Изменить категорию")).row(
        rkb("🔙 Главное меню"), rkb("❌ Удаление")
    )

    return keyboard.as_markup(resize_keyboard=True)


# Кнопки изменения заказов для клиента
def items_frep_client() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(rkb("📁 Создать заказ")).row(rkb("🔙 Назад"))

    return keyboard.as_markup(resize_keyboard=True)


def order_category() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(rkb("📁 Все заказы"), rkb("👤 В работе")).row(
        rkb("✅ Выполненные"), rkb("🔙 Назад")
    )

    return keyboard.as_markup(resize_keyboard=True)
