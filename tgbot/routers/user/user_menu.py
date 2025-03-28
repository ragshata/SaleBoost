# - *- coding: utf- 8 - *-
import asyncio
from typing import Union

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from tgbot.database.db_category import Categoryx
from aiogram.types import ReplyKeyboardRemove

from tgbot.data.config import BOT_VERSION, get_desc
from tgbot.database.db_purchases import Purchasesx
from tgbot.database.db_settings import Settingsx
from tgbot.database.db_users import Clientx
from tgbot.keyboards.inline_admin_page import (
    admin_position_edit_category_swipe_fp,
    admin_position_edit_swipe_fp,
    client_position_edit_swipe_fp,
    position_add_swipe_fp,
    position_edit_category_swipe_fp,
    position_edit_swipe_fp,
    user_position_edit_category_swipe_fp,
    user_position_edit_swipe_fp,
)
from tgbot.keyboards.inline_admin_prod import (
    category_edit_open_finl,
    knowledge_base,
    position_edit_cancel_finl,
    privacy_policy,
    users_admire,
)
from tgbot.keyboards.inline_user import user_support_finl
from tgbot.keyboards.inline_user_page import *
from tgbot.keyboards.reply_main import (
    client_functions_codexk,
    items_frep_client,
    menu_help_clients,
    menu_help_users,
    menu_second_start,
    menu_second_start_clients,
    order_category,
    user_functions_codexk,
)
from tgbot.utils.const_functions import (
    clear_html,
    ded,
    del_message,
    convert_date,
    get_unix,
    is_number,
    to_number,
)
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import (
    upload_photo,
    upload_text,
    insert_tags,
    get_items_available,
)
from tgbot.utils.text_functions import (
    category_open_admin,
    open_profile_client,
    open_profile_user,
    position_open_admin,
    position_open_not_admin_user,
)

router = Router(name=__name__)


# Открытие заказов
@router.message(F.text == "🧑🏻‍💻 Заказы")
async def user_shop(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            "<b>🔎 Выберите нужную вам категорию:</b>",
            reply_markup=prod_item_category_swipe_fp(0),
        )
    else:
        await message.answer("<b>🔎 Увы, заказы в данное время отсутствуют.</b>")


# Следующая страница выбора категорий для расположения позиции
@router.callback_query(F.data.startswith("position_add_swipe:"))
async def prod_position_add_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>📁 Выберите категорию для заказа ➕</b>",
        reply_markup=position_add_swipe_fp(remover),
    )


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.state import StateFilter


# Создаем клавиатуру с кнопкой отмены
def cancel_order_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Прервать создание заказа",
                    callback_data="cancel_create_order",
                )
            ]
        ]
    )


# Выбор категории для создания позиции
@router.callback_query(F.data.startswith("position_add_open:"))
async def prod_position_add_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]

    await state.update_data(here_category_id=category_id)
    await state.set_state("here_position_name")

    await call.message.edit_text(
        "<b>📁 Введите название для заказа</b>",
        reply_markup=cancel_order_button(),
    )


# Принятие названия для создания позиции
@router.message(F.text, StateFilter("here_position_name"))
async def prod_position_add_name_get(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    if len(message.text) > 50:
        return await message.answer(
            "<b>❌ Название не может превышать 50 символов.</b>\n"
            "📁 Введите название для заказа",
            reply_markup=cancel_order_button(),
        )

    await state.update_data(here_position_name=clear_html(message.text))
    await state.set_state("here_position_price")

    await message.answer(
        "<b>📁 Введите цену для заказа</b>",
        reply_markup=cancel_order_button(),
    )


# Принятие цены позиции для её создания
@router.message(F.text, StateFilter("here_position_price"))
async def prod_position_add_price_get(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    if not is_number(message.text):
        return await message.answer(
            "<b>❌ Данные были введены неверно. Введите число</b>\n"
            "📁 Введите цену для заказа",
            reply_markup=cancel_order_button(),
        )

    if to_number(message.text) > 10_000_000 or to_number(message.text) < 0:
        return await message.answer(
            "<b>❌ Цена не может быть меньше 0₽ или больше 10 000 000₽.</b>\n"
            "📁 Введите цену для заказа",
            reply_markup=cancel_order_button(),
        )

    user_id = message.from_user.id
    get_user = Clientx.get(client_id=user_id)

    if to_number(message.text) == None:
        return await message.answer(
            "<b>❌ Цена не может меньше чем есть у вас на балансе.</b>\n"
            "📁 Введите цену для заказа",
            reply_markup=cancel_order_button(),
        )

    if to_number(message.text) > get_user.client_balance:
        return await message.answer(
            "<b>❌ Цена не может меньше чем есть у вас на балансе.</b>\n"
            "📁 Введите цену для заказа",
            reply_markup=cancel_order_button(),
        )

    await state.update_data(here_position_price=to_number(message.text))
    await state.set_state("here_position_desc")

    await message.answer(
        "<b>📁 Введите описание для заказа</b>\n"
        "❕ Отправьте <code>0</code> чтобы пропустить.",
        )


# Принятие описания позиции для её создания
@router.message(F.text, StateFilter("here_position_desc"))
async def prod_position_add_desc_get(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    if len(message.text) > 400:
        return await message.answer(
            "<b>❌ Описание не может превышать 400 символов.</b>\n"
            "📁 Введите новое описание для позиции\n"
            "❕ Отправьте <code>0</code> чтобы пропустить.",
            reply_markup=cancel_order_button(),
        )

    try:
        if message.text != "0":
            await (await message.answer(message.text)).delete()

            position_desc = message.text
        else:
            position_desc = "None"
    except:
        return await message.answer(
            "<b>❌ Ошибка синтаксиса HTML.</b>\n"
            "📁 Введите описание для позиции\n"
            "❕ Отправьте <code>0</code> чтобы пропустить.",
            reply_markup=cancel_order_button(),
        )

    await state.update_data(here_position_desc=position_desc)
    await state.set_state("here_position_time")

    await message.answer(
        "<b>📁 Введите срок для выполнения задания (в часах)</b>\n",
        reply_markup=cancel_order_button(),
    )


# Принятие срока позиции для её создания
@router.message(F.text, StateFilter("here_position_time"))
async def prod_position_add_time_get(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    if not is_number(message.text):
        return await message.answer(
            "<b>❌ Данные были введены неверно.</b>\n"
            "📁 Введите срок для выполнения задания",
        )

    if to_number(message.text) > 10_000 or to_number(message.text) < 0:
        return await message.answer(
            "<b>❌ Срок не может быть меньше 0 или больше 10 000.</b>\n"
            "📁 Введите срок для выполнения задания",
        )

    await state.update_data(here_position_time=to_number(message.text))

    state_data = await state.get_data()

    category_id = state_data["here_category_id"]
    position_name = clear_html(state_data["here_position_name"])
    position_price = to_number(state_data["here_position_price"])
    position_desc = state_data["here_position_desc"]
    position_time = to_number(state_data["here_position_time"])
    position_id = message.from_user.id
    worker_id = 0
    position_status = 0

    await state.clear()

    Positionx.add(
        category_id,
        position_id,
        position_name,
        position_price,
        position_desc,
        position_time,
        worker_id,
        position_status,
    )
    get_position = Positionx.get(position_name=position_name)
    position_unix = get_position.position_unix
    
    await position_open_admin(bot, message.from_user.id, position_id, position_unix)


# Обработка нажатия на кнопку "Отменить создание заказа"
@router.callback_query(F.data == "cancel_create_order")
async def cancel_create_order(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    await state.clear()  # Прерываем создание заказа и очищаем состояние
    await call.message.edit_text("<b>Вы вернулись в меню</b>", reply_markup=None)

    # Здесь вызываем функцию для отображения меню второго уровня
    await menu_second_start_clients(call.message.chat.id)


################################################################################
############################### ИЗМЕНЕНИЕ ПОЗИЦИИ ##############################
# Перемещение по страницам категорий для редактирования позиции
@router.callback_query(F.data.startswith("position_edit_category_swipe:"))
async def prod_position_edit_category_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>📁 Выберите заказ для изменения 🖍</b>",
        reply_markup=position_edit_category_swipe_fp(remover),
    )

# Перемещение по страницам категорий для редактирования позиции
@router.callback_query(F.data.startswith("admin_position_edit_category_swipe:"))
async def prod_position_edit_category_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>📁 Выберите заказ </b>",
        reply_markup=position_edit_category_swipe_fp(remover),
    )

# Перемещение по страницам категорий для редактирования позиции
@router.callback_query(F.data.startswith("user_position_edit_category_swipe:"))
async def prod_position_edit_category_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>📁 Выберите заказ </b>",
        reply_markup=user_position_edit_category_swipe_fp(remover),
    )

# Выбор категории с нужной позицией
@router.callback_query(F.data.startswith("position_edit_category_open:"))
async def prod_position_edit_category_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]

    get_category = Categoryx.get(category_id=category_id)
    get_positions = Positionx.gets(category_id=category_id)

    if len(get_positions) >= 1:
        await call.message.edit_text(
            "<b>📁 Выберите заказ для изменения 🖍</b>",
            reply_markup=position_edit_swipe_fp(0, category_id, call),
        )
    else:
        await call.answer(
            f"📁 Заказы в категории {get_category.category_name} отсутствуют"
        )

# Выбор категории с нужной позицией
@router.callback_query(F.data.startswith("user_position_edit_category_open:"))
async def prod_position_edit_category_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]

    get_category = Categoryx.get(category_id=category_id)
    get_positions = Positionx.gets(category_id=category_id)

    if len(get_positions) >= 1:
        await call.message.edit_text(
            "<b>📁 Выберите заказ</b>",
            reply_markup=user_position_edit_swipe_fp(0, category_id, call),
        )
    else:
        await call.answer(
            f"📁 Заказы в категории {get_category.category_name} отсутствуют"
        )

# Выбор категории с нужной позицией
@router.callback_query(F.data.startswith("admin_position_edit_category_open:"))
async def prod_position_edit_category_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]

    get_category = Categoryx.get(category_id=category_id)
    get_positions = Positionx.gets(category_id=category_id)

    if len(get_positions) >= 1:
        await call.message.edit_text(
            "<b>📁 Выберите заказ для изменения 🖍</b>",
            reply_markup=admin_position_edit_swipe_fp(0, category_id, call),
        )
    else:
        await call.answer(
            f"📁 Заказы в категории {get_category.category_name} отсутствуют"
        )



@router.message(F.text == "🗣 Пользовательское соглашение")
async def prod_removes(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b> Пользовательское соглашение</b>\n",
        reply_markup=users_admire(),
    )


@router.message(F.text == "👤 Политика конфиденциальности")
async def prod_removes(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b> Политика конфиденциальности</b>\n",
        reply_markup=privacy_policy(),
    )


@router.message(F.text == "📚 Помощь")
async def prod_removes(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b> Помощь </b>\n",
        reply_markup=knowledge_base(),
    )


'''# Открытие профиля
@router.message(F.text == "💡 Мои заказы")
async def user_profile(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await message.answer(
        "<b>📁 Куда хотите перейте дальше?</b>",
        reply_markup=order_category(),
    )

@router.message(F.text == "📁 Все заказы")
async def user_all_orders(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_positions = Positionx.gets(position_id=message.from_user.id)
    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            """
            <b>Ваши заказы:</b>
            """,
            reply_markup=position_edit_category_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Отсутствуют категории для изменения позиций</b>")


@router.message(F.text == "👤 В работе")
async def user_profile(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    # Получаем заказы пользователя со статусом 0
    get_positions = Positionx.get_by_id_and_status(message.from_user.id, position_status=0)
    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            """
            <b>Ваши заказы:</b>
            """,
            reply_markup=position_edit_category_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Отсутствуют категории для изменения позиций</b>")




@router.message(F.text == "✅ Выполненные")
async def user_profile(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()
    get_positions = Positionx.get_by_id_and_status(message.from_user.id, position_status=1)

    if len(get_categories) >= 1:
        await message.answer(
            """
            <b>Ваши заказы:</b>
            """,
            reply_markup=position_edit_category_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Отсутствуют категории для изменения позиций</b>")'''

#! Открытие заказов
@router.message(F.text == "📦 Все заказы")
async def prod_position_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            """
            <b>Ваши заказы:</b>
            """,
            reply_markup=admin_position_edit_category_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Отсутствуют категории для изменения позиций</b>")

#? Открытие заказов
@router.message(F.text == "🪄 Мои Заказы")
async def prod_position_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    
    # Получение заказов пользователя
    user_id = message.from_user.id
    get_positions = Positionx.gets(worker_id=user_id)  # Получаем позиции пользователя

    # Если заказы есть
    if len(get_positions) > 0:
        # Первая страница заказов (remover = 0)
        await message.answer(
            "<b>📁 Ваши заказы:</b>",
            reply_markup=user_position_edit_swipe_fp(message, None, 0)
        )
    else:
        # Если заказов нет
        await message.answer("<b>❌ У вас нет активных заказов.</b>")


# Открытие заказов
@router.message(F.text == "💡 Мои заказы")
async def prod_position_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    
    # Получение заказов пользователя
    user_id = message.from_user.id
    get_positions = Positionx.gets(position_id=user_id)  # Получаем позиции пользователя

    # Если заказы есть
    if len(get_positions) > 0:
        # Первая страница заказов (remover = 0)
        await message.answer(
            "<b>📁 Ваши заказы:</b>",
            reply_markup=client_position_edit_swipe_fp(0, None, message)
        )
    else:
        # Если заказов нет
        await message.answer("<b>❌ У вас нет активных заказов.</b>")


# Перемещение по страницам позиций для редактирования позиции
@router.callback_query(F.data.startswith("position_edit_swipe:"))
async def prod_position_edit_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Выберите заказ для изменения 🖍</b>",
        reply_markup=position_edit_swipe_fp(remover, category_id, call),
    )

# Выбор позиции для редактирования
@router.callback_query(F.data.startswith("client_position_edit_open:"))
async def prod_position_edit_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[2]

    remover = int(call.data.split(":")[3])
    position_unix = call.data.split(":")[1]

    await state.clear()

    await del_message(call.message)
    await position_open_admin(bot, call.from_user.id, position_id, position_unix)

# Выбор позиции для редактирования
@router.callback_query(F.data.startswith("position_edit_open:"))
async def prod_position_edit_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[2]
    category_id = call.data.split(":")[3]
    remover = int(call.data.split(":")[4])
    position_unix = call.data.split(":")[1]

    await state.clear()

    await del_message(call.message)
    await position_open_admin(bot, call.from_user.id, position_id, position_unix)

    


# Выбор позиции для редактирования
@router.callback_query(F.data.startswith("user_position_edit_open:"))
async def prod_position_edit_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    data = call.data.split(":")
    position_id = int(data[1])  # ID позиции
    position_unix = int(data[2])  # ID категории
    remover = int(data[4])      # Параметр пагинации
    
    # Очистка состояния
    await state.clear()

    # Удаление старого сообщения
    await del_message(call.message)

    # Открытие информации по позиции
    await position_open_not_admin_user(bot, call.from_user.id, position_id, position_unix)


############################ САМО ИЗМЕНЕНИЕ ПОЗИЦИИ ############################
# Изменение названия позиции
@router.callback_query(F.data.startswith("position_edit_name:"))
async def prod_position_edit_name(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_position_id=position_id)
    await state.update_data(here_category_id=category_id)
    await state.update_data(here_remover=remover)
    await state.set_state("here_position_edit_name")

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Введите новое название для заказа</b>",
        reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
    )


# Принятие названия позиции для её изменения
@router.message(F.text, StateFilter("here_position_edit_name"))
async def prod_position_edit_name_get(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    state_data = await state.get_data()

    position_id = state_data["here_position_id"]
    category_id = state_data["here_category_id"]
    remover = state_data["here_remover"]

    if len(message.text) > 50:
        return await message.answer(
            "<b>❌ Название не может превышать 50 символов.</b>\n"
            "📁 Введите новое название для заказа",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    await state.clear()
    get_position = Positionx.get(position_id=position_id)
    position_unix = get_position.position_unix
    Positionx.update(position_id, position_name=clear_html(message.text))
    await position_open_admin(bot, message.from_user.id, position_id, position_unix)


# Изменение цены позиции
@router.callback_query(F.data.startswith("position_edit_price:"))
async def prod_position_edit_price(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_position_id=position_id)
    await state.update_data(here_category_id=category_id)
    await state.update_data(here_remover=remover)
    await state.set_state("here_position_edit_price")

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Введите новую цену для заказа</b>",
        reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
    )


# Принятие цены позиции для её изменения
@router.message(F.text, StateFilter("here_position_edit_price"))
async def prod_position_edit_price_get(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    state_data = await state.get_data()

    position_id = state_data["here_position_id"]
    category_id = state_data["here_category_id"]
    remover = state_data["here_remover"]

    if not is_number(message.text):
        await message.answer(
            "<b>❌ Данные были введены неверно. Введите число</b>\n"
            "📁 Введите цену для заказа",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    if to_number(message.text) > 10_000_000 or to_number(message.text) < 0:
        await message.answer(
            "<b>❌ Цена не может быть меньше 0₽ или больше 10 000 000₽.</b>\n"
            "📁 Введите цену для заказа",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    await state.clear()
    get_position = Positionx.get(position_id=position_id)
    position_unix = get_position.position_unix
    Positionx.update(position_id, position_price=to_number(message.text))
    await position_open_admin(bot, message.from_user.id, position_id, position_unix)


# Изменение описания позиции
@router.callback_query(F.data.startswith("position_edit_desc:"))
async def prod_position_edit_desc(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_position_id=position_id)
    await state.update_data(here_category_id=category_id)
    await state.update_data(here_remover=remover)
    await state.set_state("here_position_edit_desc")

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Введите новое описание для заказа</b>\n"
        "❕ Отправьте <code>0</code> чтобы пропустить.",
        reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
    )


# Принятие описания позиции для её изменения
@router.message(F.text, StateFilter("here_position_edit_desc"))
async def prod_position_edit_desc_get(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    state_data = await state.get_data()

    category_id = state_data["here_category_id"]
    position_id = state_data["here_position_id"]
    remover = state_data["here_remover"]

    if len(message.text) > 400:
        return await message.answer(
            "<b>❌ Описание не может превышать 400 символов.</b>\n"
            "📁 Введите новое описание для заказа\n"
            "❕ Отправьте <code>0</code> чтобы пропустить.",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    try:
        if message.text != "0":
            await (await message.answer(message.text)).delete()

            position_desc = message.text
        else:
            position_desc = "None"
    except:
        return await message.answer(
            "<b>❌ Ошибка синтаксиса HTML.</b>\n"
            "📁 Введите новое описание для заказа\n"
            "❕ Отправьте <code>0</code> чтобы пропустить.",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    await state.clear()
    get_position = Positionx.get(position_id=position_id)
    position_unix = get_position.position_unix
    Positionx.update(position_id, position_desc=position_desc)
    await position_open_admin(bot, message.from_user.id, position_id, position_unix)

@router.message(F.text == "📝 Управление заказами")
async def admin_products(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    await message.answer(
        "<b>🧑🏻‍💻 Создание и изменение заказов</b>",
        reply_markup=items_frep_client(),
    )


# Создание нового заказа
@router.message(F.text == "📁 Создать заказ")
async def prod_position_add(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            "<b>📁 Выберите категорию для создания заказа </b>",
            reply_markup=position_add_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Отсутствуют категории для создания заказа</b>")


################################################################################
############################### СОЗДАНИЕ ЗАКАЗОВ #############################
# Принятие названия категории для её создания
@router.message(F.text, StateFilter("here_category_name"))
async def prod_category_add_name_get(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    if len(message.text) > 50:
        return await message.answer(
            "<b>❌ Название не может превышать 50 символов.</b>\n"
            "🗃 Введите название для заказа",
        )

    await state.clear()

    category_id = get_unix()
    Categoryx.add(category_id, clear_html(message.text))

    await category_open_admin(bot, message.from_user.id, category_id, 0)


# Открытие категории админом
async def category_open_admin(
    bot: Bot, user_id: int, category_id: Union[str, int], remover: int
):
    get_category = Categoryx.get(category_id=category_id)
    get_positions = Positionx.gets(category_id=category_id)

    send_text = ded(
        f"""
        <b>🗃️ Редактирование категории</b>
        ➖➖➖➖➖➖➖➖➖➖➖➖➖➖
        ▪️ Заказ: <code>{get_category.category_name}</code>
        ▪️ Дата создания: <code>{convert_date(get_category.category_unix)}</code>
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
        reply_markup=category_edit_open_finl(category_id, remover),
    )


# Выбор позиции для редактирования
@router.message(F.text == "🖍 Изменить заказ")
async def prod_position_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            "<b>🖍 Выберите заказ для изменения </b>",
            reply_markup=position_edit_category_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Отсутствуют категории для изменения позиций</b>")


# Открытие профиля
@router.message(F.text == "👤 Профиль")
async def user_profile(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await open_profile_user(bot, message.from_user.id)


# Открытие профиля
@router.message(F.text == "👤 Мой профиль")
async def user_profile(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await open_profile_client(bot, message.from_user.id)


@router.message(F.text.in_(("📍 Помощь")))
async def client_help(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await message.answer(
        "<b>☎️ Не нашли, что искали? Мы поможем! Здесь вы можете найти FAQ или связаться с поддержкой?</b>",
        reply_markup=menu_help_clients(message.from_user.id),
    )


@router.message(F.text.in_(("➕ Помощь")))
async def user_help(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await message.answer(
        "<b>☎️ Не нашли, что искали? Мы поможем! Здесь вы можете найти FAQ или связаться с поддержкой?</b>",
        reply_markup=menu_help_users(message.from_user.id),
    )


@router.message(F.text.in_(("🔙 Назад")))
async def user_help(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await message.answer(
        "<b>Мы в главном меню</b>",
        reply_markup=menu_second_start_clients(message.from_user.id),
    )


@router.message(F.text.in_(("◀️ Назад")))
async def user_help(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await message.answer(
        "<b>Мы в главном меню</b>",
        reply_markup=menu_second_start(message.from_user.id),
    )


@router.message(F.text.in_(("📖 Правовая информация")))
async def user_help(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await message.answer(
        "<b>Что вас интересует?</b>",
        reply_markup=client_functions_codexk(message.from_user.id),
    )


@router.message(F.text.in_(("📗 Правовая информация")))
async def user_help(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await message.answer(
        "<b>Что вас интересует?</b>",
        reply_markup=user_functions_codexk(message.from_user.id),
    )


# Открытие FAQ
@router.message(F.text.in_(("❓ FAQ", "/faq")))
async def user_faq(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_settings = Settingsx.get()
    send_message = get_settings.misc_faq

    if send_message == "None":
        send_message = ded(
            f"""
            ❔ Информация. Измените её в настройках бота.
            ➖➖➖➖➖➖➖➖➖➖
            {get_desc()}
        """
        )

    await message.answer(
        insert_tags(message.from_user.id, send_message),
        disable_web_page_preview=True,
    )


# Открытие сообщения с ссылкой на поддержку
@router.message(F.text.in_(("🛎 Поддержка", "/support")))
async def user_support(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_settings = Settingsx.get()

    if get_settings.misc_support == "None":
        return await message.answer(
            ded(
                f"""
                🛎 Поддержка. Измените её в настройках бота.
                ➖➖➖➖➖➖➖➖➖➖
                {get_desc()}
            """
            ),
            disable_web_page_preview=True,
        )

    await message.answer(
        "<b>☎️ Нажмите кнопку ниже для связи с Администратором.</b>",
        reply_markup=user_support_finl(get_settings.misc_support),
    )


# Получение версии бота
@router.message(Command(commands=["version"]))
async def admin_version(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(f"<b>❇️ Текущая версия бота: <code>{BOT_VERSION}</code></b>")


# Получение информации о боте
@router.message(Command(commands=["dj_desc"]))
async def admin_desc(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(get_desc(), disable_web_page_preview=True)


################################################################################
# Возвращение к профилю
@router.callback_query(F.data == "user_profile")
async def user_profile_return(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    await state.clear()

    await del_message(call.message)
    await open_profile_user(bot, call.from_user.id)


# Просмотр истории покупок
@router.callback_query(F.data == "user_purchases")
async def user_purchases(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_purchases = Purchasesx.gets(user_id=call.from_user.id)
    get_purchases = get_purchases[-5:]

    if len(get_purchases) >= 1:
        await call.answer("✅ Последние 5 заказов")
        await del_message(call.message)

        for purchase in get_purchases:
            link_items = await upload_text(arSession, purchase.purchase_data)

            await call.message.answer(
                ded(
                    f"""
                    <b>🧾 Чек: <code>#{purchase.purchase_receipt}</code></b>
                    ▪️ Заказ: <code>{purchase.purchase_position_name} | {purchase.purchase_price}₽</code>
                    ▪️ Дата выполнения: <code>{convert_date(purchase.purchase_unix)}</code>
                    ▪️ Заказ: <a href='{link_items}'>кликабельно</a>
                """
                )
            )

            await asyncio.sleep(0.2)

        await open_profile_user(bot, call.from_user.id)
    else:
        await call.answer("❗ У вас отсутствуют выполненные заказы", True)


# Страницы наличия заказов
@router.callback_query(F.data.startswith("user_available_swipe:"))
async def user_available_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    remover = int(call.data.split(":")[1])

    items_available = get_items_available()

    if remover >= len(items_available):
        remover = len(items_available) - 1
    if remover < 0:
        remover = 0

    await call.message.edit_text(
        items_available[remover],
        reply_markup=prod_available_swipe_fp(remover, len(items_available)),
    )
