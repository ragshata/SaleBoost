# - *- coding: utf- 8 - *-
import math

from aiogram.types import CallbackQuery
from aiogram import Bot, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from tgbot.database.db_category import Categoryx
from tgbot.database.db_item import Itemx
from tgbot.database.db_position import Positionx
from tgbot.database.db_users import Clientx
from tgbot.utils.const_functions import ikb


# fp - flip page





################################################################################
############################## ИЗМЕНЕНИЕ КАТЕГОРИИ #############################
# Cтраницы выбора категории для изменения
def category_edit_swipe_fp(remover) -> InlineKeyboardMarkup:
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
                    data=f"category_edit_open:{get_categories[a].category_id}:{remover}",
                )
            )

    if len(get_categories) <= 10:
        ...
    elif len(get_categories) > 10 and remover < 10:
        if len(get_categories) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"catategory_edit_swipe:{remover + 10}"),
                ikb("⏩", data=f"catategory_edit_swipe:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"catategory_edit_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if len(get_categories) > 20:
            keyboard.row(
                ikb("⏪", data=f"catategory_edit_swipe:0"),
                ikb("⬅️", data=f"catategory_edit_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"catategory_edit_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_categories) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"catategory_edit_swipe:0"),
                    ikb("⬅️", data=f"catategory_edit_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"catategory_edit_swipe:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"catategory_edit_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"catategory_edit_swipe:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"catategory_edit_swipe:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"catategory_edit_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"catategory_edit_swipe:{remover + 10}"),
            )

    return keyboard.as_markup()


################################################################################
################################ СОЗДАНИЕ ЗАКАЗА ##############################
# Страницы выбора категории для заказа
def position_add_swipe_fp(remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_categories = Categoryx.get_all()
    if (10 - (len(get_categories) % 10)) != 10:
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
                    data=f"position_add_open:{get_categories[a].category_id}",
                )
            )

    if len(get_categories) <= 10:
        ...
    elif len(get_categories) > 10 and remover < 10:
        if len(get_categories) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"position_add_swipe:{remover + 10}"),
                ikb("⏩", data=f"position_add_swipe:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"position_add_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if len(get_categories) > 20:
            keyboard.row(
                ikb("⏪", data=f"position_add_swipe:0"),
                ikb("⬅️", data=f"position_add_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"position_add_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_categories) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"position_add_swipe:0"),
                    ikb("⬅️", data=f"position_add_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"position_add_swipe:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"position_add_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"position_add_swipe:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"position_add_swipe:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"position_add_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"position_add_swipe:{remover + 10}"),
            )

    return keyboard.as_markup()


 #######################################################################################
############################### ИЗМЕНЕНИЕ ЗАКАЗА КЛИЕНТОМ ##############################
def client_position_edit_swipe_fp(remover, category_id, source) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    # Определяем user_id исходя из типа source
    client_id = source.from_user.id if isinstance(source, CallbackQuery) else source.from_user.id

    # Получаем позиции пользователя
    get_positions = Positionx.gets(position_id=client_id)
    
    if 10 - (len(get_positions) % 10) != 10:
        remover_page = len(get_positions) + (10 - (len(get_positions) % 10))
    else:
        remover_page = len(get_positions)

    if remover >= len(get_positions):
        remover -= 10

    try:
        for count, a in enumerate(range(remover, len(get_positions))):
            if count < 10:
                keyboard.row(
                    ikb(
                        f"{get_positions[a].position_name} | {get_positions[a].position_price}₽",
                        data=f"client_position_edit_open:{get_positions[a].position_unix}:{get_positions[a].position_id}:{remover}",
                    )
                )
    except Exception:
        pass

    if len(get_positions) > 10:
        if remover < 10:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_positions) / 10)}", data="..."),
                ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
            )
        elif remover + 10 >= len(get_positions):
            keyboard.row(
                ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
            )

    return keyboard.as_markup()

#######################################################################################
############################### ИЗМЕНЕНИЕ ЗАКАЗА ЮЗЕРОМ ##############################
# Cтраницы категорий для изменения заказа
def user_position_edit_category_swipe_fp(remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_categories = Categoryx.get_all()
    if (10 - (len(get_categories) % 10)) != 10:
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
                    data=f"user_position_edit_category_open:{get_categories[a].category_id}",
                )
            )

    if len(get_categories) <= 10:
        ...
    elif len(get_categories) > 10 and remover < 10:
        if len(get_categories) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"user_position_edit_category_swipe:{remover + 10}"),
                ikb("⏩", data=f"user_position_edit_category_swipe:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"user_position_edit_category_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if len(get_categories) > 20:
            keyboard.row(
                ikb("⏪", data=f"user_position_edit_category_swipe:0"),
                ikb("⬅️", data=f"user_position_edit_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"user_position_edit_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_categories) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"user_position_edit_category_swipe:0"),
                    ikb("⬅️", data=f"user_position_edit_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"user_position_edit_category_swipe:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"user_position_edit_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"user_position_edit_category_swipe:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"user_position_edit_category_swipe:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"user_position_edit_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"user_position_edit_category_swipe:{remover + 10}"),
            )

    return keyboard.as_markup()

# Cтраницы выбора заказа для изменения
def user_position_edit_swipe_fp(source, category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    # Определяем user_id исходя из типа source
    user_id = source.from_user.id if isinstance(source, CallbackQuery) else source.from_user.id
    
    # Получаем позиции пользователя
    get_positions = Positionx.gets(worker_id=user_id)

    if 10 - (len(get_positions) % 10) != 10:
        remover_page = len(get_positions) + (10 - (len(get_positions) % 10))
    else:
        remover_page = len(get_positions)

    if remover >= len(get_positions):
        remover -= 10

    try:
        for count, a in enumerate(range(remover, len(get_positions))):
            if count < 10:
                keyboard.row(
                    ikb(
                        f"{get_positions[a].position_name} | {get_positions[a].position_price}₽",
                        data=f"user_position_edit_open:{get_positions[a].position_id}:{get_positions[a].position_unix}:{category_id}:{remover}",
                    )
                )

    except Exception:
        pass

    if len(get_positions) > 10:
        if remover < 10:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_positions) / 10)}", data="..."),
                ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
            )
        elif remover + 10 >= len(get_positions):
            keyboard.row(
                ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
            )

    return keyboard.as_markup()

#######################################################################################
############################### ИЗМЕНЕНИЕ ЗАКАЗА АДМИНОМ ##############################
def admin_position_edit_category_swipe_fp(remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_categories = Categoryx.get_all()
    if (10 - (len(get_categories) % 10)) != 10:
        remover_page = len(get_categories) + (10 - (len(get_categories) % 10))
    else:
        remover_page = len(get_categories)

    if remover >= len(get_categories):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_categories))):
        if count < 10:
            # Подсчет количества заказов в категории
            category_id = get_categories[a].category_id
            order_count = Positionx.count_by_category(category_id)  # Подсчет заказов в категории

            keyboard.row(
                ikb(
                    f"{get_categories[a].category_name} ({order_count})",  # Добавляем количество в скобках
                    data=f"admin_position_edit_category_open:{category_id}",
                )
            )

    # Пагинация
    if len(get_categories) <= 10:
        pass
    elif len(get_categories) > 10 and remover < 10:
        if len(get_categories) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"admin_position_edit_category_swipe:{remover + 10}"),
                ikb("⏩", data=f"admin_position_edit_category_swipe:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"admin_position_edit_category_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if len(get_categories) > 20:
            keyboard.row(
                ikb("⏪", data=f"admin_position_edit_category_swipe:0"),
                ikb("⬅️", data=f"admin_position_edit_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"admin_position_edit_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_categories) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"admin_position_edit_category_swipe:0"),
                    ikb("⬅️", data=f"admin_position_edit_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"admin_position_edit_category_swipe:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"admin_position_edit_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"admin_position_edit_category_swipe:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"admin_position_edit_category_swipe:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"admin_position_edit_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"admin_position_edit_category_swipe:{remover + 10}"),
            )

    return keyboard.as_markup()


# Cтраницы выбора заказа для изменения
def admin_position_edit_swipe_fp(remover, category_id, call: CallbackQuery) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    user_id = call.from_user.id
    get_positions = Positionx.gets(category_id=category_id)
    if 10 - (len(get_positions) % 10) != 10:
        remover_page = len(get_positions) + (10 - (len(get_positions) % 10))
    else:
        remover_page = len(get_positions)

    if remover >= len(get_positions):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = Itemx.gets(position_id=get_positions[a].position_id)

            keyboard.row(
                ikb(
                    f"{get_positions[a].position_name} | {get_positions[a].position_price}₽",
                    data=f"position_edit_open:{get_positions[a].position_unix}:{get_positions[a].position_id}:{category_id}:{remover}",
                )
            )

    if len(get_positions) <= 10:
        ...
    elif len(get_positions) > 10 and remover < 10:
        if len(get_positions) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_positions) / 10)}", data="..."),
                ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
                ikb("⏩", data=f"position_edit_swipe:{category_id}:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_positions) / 10)}", data="..."),
                ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
            )
    elif remover + 10 >= len(get_positions):
        if len(get_positions) > 20:
            keyboard.row(
                ikb("⏪", data=f"position_edit_swipe:{category_id}:0"),
                ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_positions) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"position_edit_swipe:{category_id}:0"),
                    ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"position_edit_swipe:{category_id}:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
            )


    return keyboard.as_markup()

################################################################################
############################### ИЗМЕНЕНИЕ ЗАКАЗА ##############################
# Cтраницы категорий для изменения заказа
def position_edit_category_swipe_fp(remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_categories = Categoryx.get_all()
    if (10 - (len(get_categories) % 10)) != 10:
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
                    data=f"position_edit_category_open:{get_categories[a].category_id}",
                )
            )

    if len(get_categories) <= 10:
        ...
    elif len(get_categories) > 10 and remover < 10:
        if len(get_categories) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"position_edit_category_swipe:{remover + 10}"),
                ikb("⏩", data=f"position_edit_category_swipe:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"position_edit_category_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if len(get_categories) > 20:
            keyboard.row(
                ikb("⏪", data=f"position_edit_category_swipe:0"),
                ikb("⬅️", data=f"position_edit_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"position_edit_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_categories) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"position_edit_category_swipe:0"),
                    ikb("⬅️", data=f"position_edit_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"position_edit_category_swipe:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"position_edit_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"position_edit_category_swipe:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"position_edit_category_swipe:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"position_edit_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"position_edit_category_swipe:{remover + 10}"),
            )

    return keyboard.as_markup()


# Cтраницы выбора заказа для изменения
def position_edit_swipe_fp(remover, category_id, call: CallbackQuery) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    user_id = call.from_user.id
    get_positions = Positionx.gets(position_id=user_id)
    if 10 - (len(get_positions) % 10) != 10:
        remover_page = len(get_positions) + (10 - (len(get_positions) % 10))
    else:
        remover_page = len(get_positions)

    if remover >= len(get_positions):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_positions))):
        if count < 10:
            get_items = Itemx.gets(position_id=get_positions[a].position_id)

            keyboard.row(
                ikb(
                    f"{get_positions[a].position_name} | {get_positions[a].position_price}₽",
                    data=f"position_edit_open:{get_positions[a].position_unix}:{get_positions[a].position_id}:{remover}",
                )
            )

    if len(get_positions) <= 10:
        ...
    elif len(get_positions) > 10 and remover < 10:
        if len(get_positions) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_positions) / 10)}", data="..."),
                ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
                ikb("⏩", data=f"position_edit_swipe:{category_id}:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_positions) / 10)}", data="..."),
                ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
            )
    elif remover + 10 >= len(get_positions):
        if len(get_positions) > 20:
            keyboard.row(
                ikb("⏪", data=f"position_edit_swipe:{category_id}:0"),
                ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_positions) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"position_edit_swipe:{category_id}:0"),
                    ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"position_edit_swipe:{category_id}:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"position_edit_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"position_edit_swipe:{category_id}:{remover + 10}"),
            )

    keyboard.row(ikb("🔙 Вернуться", data="position_edit_category_swipe:0"))

    return keyboard.as_markup()


################################################################################
############################### ДОБАВЛЕНИЕ ЗАКАЗОВ #############################
# Страницы категорий для добавления заказов
def item_add_category_swipe_fp(remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_categories = Categoryx.get_all()
    if (10 - (len(get_categories) % 10)) != 10:
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
                    data=f"item_add_category_open:{get_categories[a].category_id}:{remover}",
                )
            )

    if len(get_categories) <= 10:
        ...
    elif len(get_categories) > 10 and remover < 10:
        if len(get_categories) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"item_add_category_swipe:{remover + 10}"),
                ikb("⏩", data=f"item_add_category_swipe:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_categories) / 10)}", data="..."),
                ikb("➡️", data=f"item_add_category_swipe:{remover + 10}"),
            )
    elif remover + 10 >= len(get_categories):
        if len(get_categories) > 20:
            keyboard.row(
                ikb("⏪", data=f"item_add_category_swipe:0"),
                ikb("⬅️", data=f"item_add_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"item_add_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_categories) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"item_add_category_swipe:0"),
                    ikb("⬅️", data=f"item_add_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"item_add_category_swipe:{remover + 10}"),
                )
            else:
                keyboard.row(
                    ikb("⬅️", data=f"item_add_category_swipe:{remover - 10}"),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                        data="...",
                    ),
                    ikb("➡️", data=f"item_add_category_swipe:{remover + 10}"),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb("⏩", data=f"item_add_category_swipe:{remover_page}"),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"item_add_category_swipe:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_categories) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"item_add_category_swipe:{remover + 10}"),
            )

    return keyboard.as_markup()


# Страницы позиций для добавления заказов
def item_add_position_swipe_fp(remover, category_id) -> InlineKeyboardMarkup:
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
                    data=f"item_add_position_open:{get_positions[a].position_id}:{category_id}",
                )
            )

    if len(get_positions) <= 10:
        ...
    elif len(get_positions) > 10 and remover < 10:
        if len(get_positions) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_positions) / 10)}", data="..."),
                ikb("➡️", data=f"item_add_position_swipe:{category_id}:{remover + 10}"),
                ikb("⏩", data=f"item_add_position_swipe:{category_id}:{remover_page}"),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_positions) / 10)}", data="..."),
                ikb("➡️", data=f"item_add_position_swipe:{category_id}:{remover + 10}"),
            )
    elif remover + 10 >= len(get_positions):
        if len(get_positions) > 20:
            keyboard.row(
                ikb("⏪", data=f"item_add_position_swipe:{category_id}:0"),
                ikb("⬅️", data=f"item_add_position_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb("⬅️", data=f"item_add_position_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_positions) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"item_add_position_swipe:{category_id}:0"),
                    ikb(
                        "⬅️",
                        data=f"item_add_position_swipe:{category_id}:{remover - 10}",
                    ),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                        data="...",
                    ),
                    ikb(
                        "➡️",
                        data=f"item_add_position_swipe:{category_id}:{remover + 10}",
                    ),
                )
            else:
                keyboard.row(
                    ikb(
                        "⬅️",
                        data=f"item_add_position_swipe:{category_id}:{remover - 10}",
                    ),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                        data="...",
                    ),
                    ikb(
                        "➡️",
                        data=f"item_add_position_swipe:{category_id}:{remover + 10}",
                    ),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb(
                        "⏩",
                        data=f"item_add_position_swipe:{category_id}:{remover_page}",
                    ),
                )
        else:
            keyboard.row(
                ikb("⬅️", data=f"item_add_position_swipe:{category_id}:{remover - 10}"),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_positions) / 10)}",
                    data="...",
                ),
                ikb("➡️", data=f"item_add_position_swipe:{category_id}:{remover + 10}"),
            )

    keyboard.row(ikb("🔙 Вернуться", data="products_add_category_swipe:0"))

    return keyboard.as_markup()


################################################################################
################################ УДАЛЕНИЕ ЗАКАЗОВ ##############################
# Страницы заказов для удаления
def item_delete_swipe_fp(remover, position_id, category_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_items = Itemx.gets(position_id=position_id)
    if 10 - (len(get_items) % 10) != 10:
        remover_page = len(get_items) + (10 - (len(get_items) % 10))
    else:
        remover_page = len(get_items)

    if remover >= len(get_items):
        remover -= 10

    for count, a in enumerate(range(remover, len(get_items))):
        if count < 10:
            keyboard.row(
                ikb(
                    get_items[a].item_data,
                    data=f"item_delete_open:{get_items[a].item_id}",
                )
            )

    if len(get_items) <= 10:
        ...
    elif len(get_items) > 10 and remover < 10:
        if len(get_items) > 20:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_items) / 10)}", data="..."),
                ikb(
                    "➡️",
                    data=f"item_delete_swipe:{position_id}:{category_id}:{remover + 10}",
                ),
                ikb(
                    "⏩",
                    data=f"item_delete_swipe:{position_id}:{category_id}:{remover_page}",
                ),
            )
        else:
            keyboard.row(
                ikb(f"1/{math.ceil(len(get_items) / 10)}", data="..."),
                ikb(
                    "➡️",
                    data=f"item_delete_swipe:{position_id}:{category_id}:{remover + 10}",
                ),
            )
    elif remover + 10 >= len(get_items):
        if len(get_items) > 20:
            keyboard.row(
                ikb("⏪", data=f"item_delete_swipe:{position_id}:{category_id}:0"),
                ikb(
                    "⬅️",
                    data=f"item_delete_swipe:{position_id}:{category_id}:{remover - 10}",
                ),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_items) / 10)}",
                    data="...",
                ),
            )
        else:
            keyboard.row(
                ikb(
                    "⬅️",
                    data=f"item_delete_swipe:{position_id}:{category_id}:{remover - 10}",
                ),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_items) / 10)}",
                    data="...",
                ),
            )
    else:
        if len(get_items) > 20:
            if remover >= 20:
                keyboard.row(
                    ikb("⏪", data=f"item_delete_swipe:{position_id}:{category_id}:0"),
                    ikb(
                        "⬅️",
                        data=f"item_delete_swipe:{position_id}:{category_id}:{remover - 10}",
                    ),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_items) / 10)}",
                        data="...",
                    ),
                    ikb(
                        "➡️",
                        data=f"item_delete_swipe:{position_id}:{category_id}:{remover + 10}",
                    ),
                )
            else:
                keyboard.row(
                    ikb(
                        "⬅️",
                        data=f"item_delete_swipe:{position_id}:{category_id}:{remover - 10}",
                    ),
                    ikb(
                        f"{str(remover + 10)[:-1]}/{math.ceil(len(get_items) / 10)}",
                        data="...",
                    ),
                    ikb(
                        "➡️",
                        data=f"item_delete_swipe:{position_id}:{category_id}:{remover + 10}",
                    ),
                )

            if remover_page - 20 > remover:
                keyboard.add(
                    ikb(
                        "⏩",
                        data=f"item_delete_swipe:{position_id}:{category_id}:{remover_page}",
                    ),
                )
        else:
            keyboard.row(
                ikb(
                    "⬅️",
                    data=f"item_delete_swipe:{position_id}:{category_id}:{remover - 10}",
                ),
                ikb(
                    f"{str(remover + 10)[:-1]}/{math.ceil(len(get_items) / 10)}",
                    data="...",
                ),
                ikb(
                    "➡️",
                    data=f"item_delete_swipe:{position_id}:{category_id}:{remover + 10}",
                ),
            )

    keyboard.row(
        ikb("🔙 Вернуться", data=f"position_edit_open:{position_id}:{category_id}:0")
    )

    return keyboard.as_markup()
