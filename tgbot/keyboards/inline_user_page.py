# - *- coding: utf- 8 - *-
import math

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.database.db_category import Categoryx
from tgbot.database.db_item import Itemx
from tgbot.database.db_position import Positionx
from tgbot.utils.const_functions import ikb


# fp - flip page

#Заказы клиента
def prod_item_category_client(remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_categories = Categoryx.get_all()
    if 10 - (len(get_categories) % 10) != 10:
        remover_page = len(get_categories) + (10 - (len(get_categories) % 10))
    else:
        remover_page = len(get_categories)

    if remover >= len(get_categories):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.row(
                ikb(
                    get_categories[a].category_name,
                    data=f"buy_category_open:{get_categories[a].category_id}:0",
                )
            )

    if len(get_categories) <= 10:
        ...
    elif len(get_categories) > 10 and remover < 10:
        if len(get_categories) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"buy_category_swipe:{remover + 10}"),
                ikb("⏩", data=f"buy_category_swipe:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"buy_category_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if len(get_categories) > 20:
            keyboard.row(
                ikb("⏪", data=f"buy_category_swipe:0"),
                ikb("⬅️", data=f"buy_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"buy_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_categories) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"buy_category_swipe:0"),
                    ikb("⬅️", data=f"buy_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"buy_category_swipe:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"buy_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"buy_category_swipe:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"buy_category_swipe:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"buy_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"buy_category_swipe:{remover + 10}"),
            )

    return keyboard.as_markup()
################################################################################
################################ ВЫПОЛНЕНИЕ ЗАКАЗОВ ###############################
# Страницы категорий при выполнении заказа
def prod_item_category_swipe_fp(remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_categories = Categoryx.get_all()
    if 10 - (len(get_categories) % 10) != 10:
        remover_page = len(get_categories) + (10 - (len(get_categories) % 10))
    else:
        remover_page = len(get_categories)

    if remover >= len(get_categories):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            keyboard.row(
                ikb(
                    get_categories[a].category_name,
                    data=f"buy_category_open:{get_categories[a].category_id}:0",
                )
            )

    if len(get_categories) <= 10:
        ...
    elif len(get_categories) > 10 and remover < 10:
        if len(get_categories) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"buy_category_swipe:{remover + 10}"),
                ikb("⏩", data=f"buy_category_swipe:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"buy_category_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if len(get_categories) > 20:
            keyboard.row(
                ikb("⏪", data=f"buy_category_swipe:0"),
                ikb("⬅️", data=f"buy_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"buy_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_categories) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"buy_category_swipe:0"),
                    ikb("⬅️", data=f"buy_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"buy_category_swipe:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"buy_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"buy_category_swipe:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"buy_category_swipe:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"buy_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"buy_category_swipe:{remover + 10}"),
            )

    return keyboard.as_markup()


# Страницы позиций для выполнения заказов
def prod_item_position_swipe_fp(remover, category_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_positions = Positionx.gets(category_id=category_id)
    if 10 - (len(get_positions) % 10) != 10:
        remover_page = len(get_positions) + (10 - (len(get_positions) % 10))
    else:
        remover_page = len(get_positions)

    if remover >= len(get_positions):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = 1

            keyboard.row(
                ikb(
                    f"{get_positions[a].position_name} | {get_positions[a].position_price}₽",
                    data=f"buy_position_open:{get_positions[a].position_id}:{get_positions[a].position_unix}:{remover}",
                )
            )

    if len(get_positions) <= 10:
        ...
    elif len(get_positions) > 10 and remover < 10:
        if len(get_positions) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_positions) / 10)}", data="..."),
                ikb("➡️", data=f"buy_position_swipe:{category_id}:{remover + 10}"),
                ikb("⏩", data=f"buy_position_swipe:{category_id}:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_positions) / 10)}", data="..."),
                ikb("➡️", data=f"buy_position_swipe:{category_id}:{remover + 10}"),
            )
    elif remover + 10 >= len(get_positions):
        if len(get_positions) > 20:
            keyboard.row(
                ikb("⏪", data=f"buy_position_swipe:{category_id}:0"),
                ikb("⬅️", data=f"buy_position_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"buy_position_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_positions) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"buy_position_swipe:{category_id}:0"),
                    ikb("⬅️", data=f"buy_position_swipe:{category_id}:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"buy_position_swipe:{category_id}:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"buy_position_swipe:{category_id}:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"buy_position_swipe:{category_id}:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"buy_position_swipe:{category_id}:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"buy_position_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"buy_position_swipe:{category_id}:{remover + 10}"),
            )

    keyboard.row(ikb("🔙 Вернуться", data=f"buy_category_swipe:0"))

    return keyboard.as_markup()


################################################################################
################################ НАЛИЧИЕ ЗАКАЗОВ ###############################
# Страницы наличия заказов
def prod_available_swipe_fp(remover_now: int, remover_max: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    if remover_max > 1:
        if remover_now > 1 and remover_max >= 3:
            keyboard.add(
                ikb("⏪", data=f"user_available_swipe:{0}"),
            )

        if remover_now >= 1:
            keyboard.add(
                ikb("⬅️", data=f"user_available_swipe:{remover_now - 1}"),
            )

        keyboard.add(ikb(f"{remover_now + 1}/{remover_max}", data="..."))

        if remover_now + 1 < remover_max:
            keyboard.add(
                ikb("➡️", data=f"user_available_swipe:{remover_now + 1}"),
            )

        if remover_now + 1 < remover_max - 1 and remover_max >= 3:
            keyboard.add(
                ikb("⏩", data=f"user_available_swipe:{remover_max - 1}"),
            )

        keyboard.adjust(5)

    return keyboard.as_markup()
