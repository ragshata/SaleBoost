# - *- coding: utf- 8 - *-
from typing import Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.database.db_settings import Settingsx
from tgbot.utils.const_functions import ikb


################################### КАТЕГОРИИ ##################################
# Изменение категории
def category_edit_open_finl(category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("▪️ Изм. Название", data=f"category_edit_name:{category_id}:{remover}"),
        ikb("▪️ Добавить заказ", data=f"position_add_open:{category_id}"),
    ).row(
        ikb("🔙 Вернуться", data=f"catategory_edit_swipe:{remover}"),
        ikb("▪️ Удалить", data=f"category_edit_delete:{category_id}:{remover}"),
    )

    return keyboard.as_markup()


# Подтверждение удаления категории
def category_edit_delete_finl(category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(
            "✅ Да, удалить",
            data=f"category_edit_delete_confirm:{category_id}:{remover}",
        ),
        ikb("❌ Нет, отменить", data=f"category_edit_open:{category_id}:{remover}"),
    )

    return keyboard.as_markup()


# Отмена изменения категории и возвращение
def category_edit_cancel_finl(category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("❌ Отменить", data=f"category_edit_open:{category_id}:{remover}"),
    )

    return keyboard.as_markup()


#################################### ПОЗИЦИИ ###################################
# Кнопки при открытии позиции для изменения
def position_edit_open_finl_all(position_id, remover, position_unix) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(
            "▪️ Изм. Название",
            data=f"position_edit_name:{position_id}:{remover}",
        ),
        ikb(
            "▪️ Изм. цену",
            data=f"position_edit_price:{position_id}:{remover}",
        ),
    ).row(
        ikb(
            "▪️ Изм. Описание",
            data=f"position_edit_desc:{position_id}:{remover}",
        ),
    ).row(
        ikb(
            "✅ Завершить Заказ",
            data=f"position_edit_confirm:{position_id}:{remover}:{position_unix}",
        ),
    ).row(
        ikb(
            "▪️ Удалить Заказ",
            data=f"position_edit_delete:{position_id}:{remover}",
        ),
    ).row(
        ikb("🔙 Вернуться", data=f"position_edit_swipe:{remover}"),
        ikb(
            "▪️ Обновить",
            data=f"position_edit_open:{position_id}:{remover}",
        ),
    )

    return keyboard.as_markup()

def position_edit_open_finl_dindon(position_id, category_id, remover, position_unix) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(
            "✅ Завершить Заказ",
            data=f"position_edit_confirm:{position_id}:{category_id}:{remover}:{position_unix}",
        ))
    return keyboard.as_markup()

# Кнопки при открытии позиции для изменения
def position_edit_open_finl(position_id, category_id, remover, position_unix) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(
            "▪️ Изм. Название",
            data=f"position_edit_name:{position_id}:{category_id}:{remover}",
        ),
        ikb(
            "▪️ Изм. цену",
            data=f"position_edit_price:{position_id}:{category_id}:{remover}",
        ),
    ).row(
        ikb(
            "▪️ Изм. Описание",
            data=f"position_edit_desc:{position_id}:{category_id}:{remover}",
        ),
    ).row(
        ikb(
            "✅ Завершить Заказ",
            data=f"position_edit_confirm:{position_id}:{category_id}:{remover}:{position_unix}",
        ),
    ).row(
        ikb(
            "▪️ Удалить Заказ",
            data=f"position_edit_delete:{position_id}:{category_id}:{remover}",
        ),
    ).row(
        ikb("🔙 Вернуться", data=f"position_edit_swipe:{category_id}:{remover}"),
        ikb(
            "▪️ Обновить",
            data=f"position_edit_open:{position_id}:{category_id}:{remover}",
        ),
    )

    return keyboard.as_markup()


# Кнопки при открытии позиции для изменения
def user_position_edit_open_finl(
    position_id, category_id, remover, position_unix
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    get_settings = Settingsx.get()
    keyboard.row(
        ikb(
            "✅ Отправить на проверку",
            data=f"position_done_dindon:{position_id}:{category_id}:{remover}:{position_unix}",
        ),
    ).row(
        ikb(
            "▪️ Написать в арбитраж",
            url=f"https://t.me/{get_settings.misc_support}",
        ),
    )

    return keyboard.as_markup()


# Подтверждение удаления позиции
def position_edit_delete_finl(
    position_id, category_id, remover
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(
            "✅ Да, удалить",
            data=f"position_edit_delete_confirm:{position_id}:{category_id}:{remover}",
        ),
        ikb(
            "❌ Нет, отменить",
            data=f"position_edit_open:{position_id}:{category_id}:{remover}",
        ),
    )

    return keyboard.as_markup()


def position_edit_done_finl(position_id, category_id, remover, position_unix) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(
            "✅ Да, подтвердить",
            data=f"position_edit_done_confirm:{position_id}:{category_id}:{remover}:{position_unix}",
        ),
        ikb(
            "❌ Нет",
            data=f"position_edit_open:{position_id}:{category_id}:{remover}:{position_unix}",
        ),
    )

    return keyboard.as_markup()


# Подтверждение очистики позиции
def position_edit_clear_finl(position_id, category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(
            "✅ Да, очистить",
            data=f"position_edit_clear_confirm:{position_id}:{category_id}:{remover}",
        ),
        ikb(
            "❌ Нет, отменить",
            data=f"position_edit_open:{position_id}:{category_id}:{remover}",
        ),
    )

    return keyboard.as_markup()


# Отмена изменения позиции и возвращение
def position_edit_cancel_finl(
    position_id, category_id, remover
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(
            "❌ Отменить",
            data=f"position_edit_open:{position_id}:{category_id}:{remover}",
        ),
    )

    return keyboard.as_markup()


##################################### ЗАКАЗЫ ###################################
# Отмена изменения позиции и возвращение
def item_add_finish_finl(position_id: Union[int, str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Завершить загрузку", data=f"item_add_position_finish:{position_id}"),
    )

    return keyboard.as_markup()


# Удаление заказа
def item_delete_finl(item_id, position_id, category_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("▪️ Удалить заказ", data=f"item_delete_confirm:{item_id}"),
    ).row(
        ikb("🔙 Вернуться", data=f"item_delete_swipe:{position_id}:{category_id}:0"),
    )

    return keyboard.as_markup()


############################### УДАЛЕНИЕ РАЗДЕЛОВ ##############################
# Выбор раздела для удаления
def products_removes_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🗃 Удалить все категории", data=f"prod_removes_categories"),
    ).row(
        ikb("📁 Удалить все заказы", data=f"prod_removes_positions"),
    )

    return keyboard.as_markup()


def users_admire() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(" ✉️ ", url="https://telegra.ph/POLZOVATELSKOE-SOGLASHENIE-01-10-9"),
    )

    return keyboard.as_markup()


def privacy_policy() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(" ✉️ ", url="https://telegra.ph/POLITIKA-KONFIDENCIALNOSTI-01-10-10"),
    )

    return keyboard.as_markup()


def knowledge_base() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(" ✉️ ", url="https://telegra.ph/Pomoshch-01-10-3"),
    )

    return keyboard.as_markup()


# Удаление всех категорий
def products_removes_categories_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Да, удалить все", data="prod_removes_categories_confirm"),
        ikb("❌ Нет, отменить", data="prod_removes_return"),
    )

    return keyboard.as_markup()


# Удаление всех позиций
def products_removes_positions_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Да, удалить все", data="prod_removes_positions_confirm"),
        ikb("❌ Нет, отменить", data="prod_removes_return"),
    )

    return keyboard.as_markup()


# Удаление всех заказов
def products_removes_items_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Да, удалить все", data="prod_removes_items_confirm"),
        ikb("❌ Нет, отменить", data="prod_removes_return"),
    )

    return keyboard.as_markup()
