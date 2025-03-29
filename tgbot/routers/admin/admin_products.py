# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from tgbot.database.db_category import Categoryx
from tgbot.utils.const_functions import ikb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.database.db_item import Itemx
from tgbot.database.db_position import Positionx
from tgbot.database.db_purchases import Purchasesx
from tgbot.database.db_purchases_clients import Purchasesclientx
from tgbot.database.db_users import Clientx, Userx
from tgbot.keyboards.inline_admin import close_finl
from tgbot.keyboards.inline_admin_page import (
    admin_position_edit_swipe_fp,
    category_edit_swipe_fp,
    position_add_swipe_fp,
    position_edit_category_swipe_fp,
    position_edit_swipe_fp,
    item_add_position_swipe_fp,
    item_add_category_swipe_fp,
    item_delete_swipe_fp,
)
from tgbot.keyboards.inline_admin_prod import (
    category_edit_delete_finl,
    position_edit_clear_finl,
    position_edit_delete_finl,
    position_edit_cancel_finl,
    category_edit_cancel_finl,
    position_edit_done_finl,
    position_edit_open_finl_dindon,
    products_removes_finl,
    products_removes_categories_finl,
    products_removes_positions_finl,
    products_removes_items_finl,
    item_add_finish_finl,
)
from tgbot.keyboards.reply_main import menu_second_start_clients
from tgbot.utils.const_functions import (
    clear_list,
    gen_id,
    is_number,
    to_number,
    del_message,
    ded,
    get_unix,
    clear_html,
)

from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import upload_text, upload_photo
from tgbot.utils.text_functions import (
    category_open_admin,
    position_open_admin,
    item_open_admin,
)

router = Router(name=__name__)


# Создание новой категории
@router.message(F.text == "🗃 Создать категорию")
async def prod_category_add(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await state.set_state("here_category_name")
    await message.answer("<b>🗃 Введите название для категории</b>")


# Выбор категории для редактирования
@router.message(F.text == "🖍 Изменить категорию")
async def prod_category_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            "<b>🗃 Выберите категорию для изменения</b>",
            reply_markup=category_edit_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Отсутствуют категории для изменения категорий</b>")


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


# Страницы заказов для добавления
@router.message(F.text == "➕ Добавить заказы")
async def prod_item_add(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            "<b>➕ Выберите заказ для заказа ➕</b>",
            reply_markup=item_add_category_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Отсутствуют заказ для добавления заказа</b>")


# Удаление категорий, позиций или закзов
@router.message(F.text == "❌ Удаление")
async def prod_removes(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b> Выберите раздел который хотите удалить ❌</b>\n",
        reply_markup=products_removes_finl(),
    )


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
            "🗃 Введите название для категории",
        )

    await state.clear()

    category_id = get_unix()
    Categoryx.add(category_id, clear_html(message.text))

    await category_open_admin(bot, message.from_user.id, category_id, 0)


################################################################################
############################### ИЗМЕНЕНИЕ КАТЕГОРИИ ############################
# Страница выбора категорий для редактирования
@router.callback_query(F.data.startswith("catategory_edit_swipe:"))
async def prod_category_edit_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>🗃 Выберите категорию для изменения 🖍</b>",
        reply_markup=category_edit_swipe_fp(remover),
    )


# Выбор текущей категории для редактирования
@router.callback_query(F.data.startswith("category_edit_open:"))
async def prod_category_edit_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await state.clear()

    await del_message(call.message)
    await category_open_admin(bot, call.from_user.id, category_id, remover)


############################ САМО ИЗМЕНЕНИЕ КАТЕГОРИИ ##########################
# Изменение названия категории
@router.callback_query(F.data.startswith("category_edit_name:"))
async def prod_category_edit_name(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await state.update_data(here_category_id=category_id)
    await state.update_data(here_remover=remover)
    await state.set_state("here_category_edit_name")

    await del_message(call.message)

    await call.message.answer(
        "<b>🗃 Введите новое название для категории</b>",
        reply_markup=category_edit_cancel_finl(category_id, remover),
    )


# Принятие нового названия для категории
@router.message(F.text, StateFilter("here_category_edit_name"))
async def prod_category_edit_name_get(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    category_id = (await state.get_data())["here_category_id"]
    remover = (await state.get_data())["here_remover"]

    if len(message.text) > 50:
        return await message.answer(
            "<b>❌ Название не может превышать 50 символов.</b>\n"
            "🗃 Введите новое название для категории",
            reply_markup=category_edit_cancel_finl(category_id, remover),
        )

    await state.clear()

    Categoryx.update(category_id, category_name=clear_html(message.text))
    await category_open_admin(bot, message.from_user.id, category_id, remover)


# Окно с уточнением удалить категорию
@router.callback_query(F.data.startswith("category_edit_delete:"))
async def prod_category_edit_delete(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await call.message.edit_text(
        "<b>❗ Вы действительно хотите удалить категорию и все её данные?</b>",
        reply_markup=category_edit_delete_finl(category_id, remover),
    )


# Отмена удаления категории
@router.callback_query(F.data.startswith("category_edit_delete_confirm:"))
async def prod_category_edit_delete_confirm(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    Categoryx.delete(category_id=category_id)
    Positionx.delete(category_id=category_id)
    Itemx.delete(category_id=category_id)

    await call.answer("🗃 Категория и все её данные были успешно удалены ✅")

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await call.message.edit_text(
            "<b>🗃 Выберите категорию для изменения 🖍</b>",
            reply_markup=category_edit_swipe_fp(remover),
        )
    else:
        await del_message(call.message)


################################################################################
############################### ДОБАВЛЕНИЕ ПОЗИЦИИ #############################
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.state import StateFilter


# Создаем клавиатуру с кнопкой отмены
def cancel_order_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌ Отменить создание заказа и вернуться в меню",
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

    await state.update_data(here_position_price=to_number(message.text))
    await state.set_state("here_position_desc")

    await message.answer(
        "<b>📁 Введите описание для заказа</b>\n"
        "❕ Отправьте <code>0</code> чтобы пропустить.",
        reply_markup=cancel_order_button(),
    )


# Принятие описания позиции для её создания
@router.message(F.text, StateFilter("here_position_desc"))
async def prod_position_add_desc_get(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    if len(message.text) > 400:
        return await message.answer(
            "<b>❌ Описание не может превышать 400 символов.</b>\n"
            "📁 Введите новое описание для позиции\n",
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
            "📁 Введите описание для позиции\n",
            reply_markup=cancel_order_button(),
        )

    await state.update_data(here_position_desc=position_desc)

    state_data = await state.get_data()

    category_id = state_data["here_category_id"]
    position_name = clear_html(state_data["here_position_name"])
    position_price = to_number(state_data["here_position_price"])
    position_desc = state_data["here_position_desc"]
    position_id = get_unix()
    await state.clear()

    Positionx.add(
        category_id,
        position_id,
        position_name,
        position_price,
        position_desc,
    )
    get_position = Positionx.get(position_id=position_id)
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
    await menu_second_start_clients(call.message.chat.id, bot)


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
        "<b>📁 Выберите заказ для изменения 🖍</b>",
        reply_markup=position_edit_category_swipe_fp(remover),
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
            f"📁 Позиции в категории {get_category.category_name} отсутствуют"
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
            f"📁 Orders в категории {get_category.category_name} отсутствуют"
        )


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
        "<b>📁 Введите новое название для позиции</b>",
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
            "📁 Введите новое название для позиции",
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
        "<b>📁 Введите новую цену для позиции</b>",
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
            "<b>❌ Данные были введены неверно.</b>\n" "📁 Введите цену для позиции",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    if to_number(message.text) > 10_000_000 or to_number(message.text) < 0:
        await message.answer(
            "<b>❌ Цена не может быть меньше 0₽ или больше 10 000 000₽.</b>\n"
            "📁 Введите цену для позиции",
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
        "<b>📁 Введите новое описание для позиции</b>\n",
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
            "📁 Введите новое описание для позиции\n"
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
            "📁 Введите новое описание для позиции\n"
            "❕ Отправьте <code>0</code> чтобы пропустить.",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    await state.clear()
    get_position = Positionx.get(position_id=position_id)
    position_unix = get_position.position_unix
    Positionx.update(position_id, position_desc=position_desc)
    await position_open_admin(bot, message.from_user.id, position_id, position_unix)


# Изменение изображения позиции
@router.callback_query(F.data.startswith("position_edit_photo:"))
async def prod_position_edit_photo(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_position_id=position_id)
    await state.update_data(here_category_id=category_id)
    await state.update_data(here_remover=remover)
    await state.set_state("here_position_edit_photo")

    await del_message(call.message)

    state_data = await state.get_data()
    await state.clear()

    position_id = state_data["here_position_id"]
    category_id = state_data["here_category_id"]
    remover = state_data["here_remover"]

    await call.message.answer(
        "❕ Готово",
        reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
    )


# Выгрузка заказов
@router.callback_query(F.data.startswith("position_edit_items:"))
async def prod_position_edit_items(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    get_position = Positionx.get(position_id=position_id)
    get_items = Itemx.gets(position_id=position_id)

    if len(get_items) >= 1:
        save_items = "\n\n".join([item.item_data for item in get_items])
        save_items = await upload_text(arSession, save_items)

        await call.message.answer(
            f"<b>📥 Все заказы типа: <code>{get_position.position_name}</code>\n"
            f"🔗 Ссылка: <a href='{save_items}'>кликабельно</a></b>",
            reply_markup=close_finl(),
        )
        await call.answer(cache_time=5)
    else:
        await call.answer("❕ В данном типе отсутствуют заказы", True)


# Удаление позиции
@router.callback_query(F.data.startswith("position_edit_delete:"))
async def prod_position_edit_delete(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Вы действительно хотите удалить заказ? ❌</b>",
        reply_markup=position_edit_delete_finl(position_id, category_id, remover),
    )


# Удаление позиции
@router.callback_query(F.data.startswith("position_edit_confirm:"))
async def prod_position_edit_delete(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])
    position_unix = call.data.split(":")[4]

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Вы действительно хотите подтвердить заказ? ✔️</b>",
        reply_markup=position_edit_done_finl(position_id, category_id, remover, position_unix),
    )


@router.callback_query(F.data.startswith("position_done_dindon:"))
async def prod_position_edit_delete(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])
    position_unix = call.data.split(":")[4]
    position = Positionx.get(position_unix=position_unix)
    name = position.position_name
    await del_message(call.message)

    # Отправка сообщения конкретному пользователю
    await bot.send_message(
        position_id,  # Указание ID пользователя
        text=(
            f"<b>📁 Исполнитель отправил вам на проверку заказ: <u>{name}</u></b>\n\n"
        ),reply_markup = position_edit_open_finl_dindon(position_id, category_id, remover, position_unix)
    )

    # Информирование отправителя, что сообщение отправлено
    await call.message.answer("<b>Заказчик уведомлен!</b>")


# Подтверждение удаления позиции
@router.callback_query(F.data.startswith("position_edit_delete_confirm:"))
async def prod_position_edit_delete_confirm(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    Itemx.delete(position_id=position_id)
    Positionx.delete(position_id=position_id)

    await call.answer("📁 Вы успешно удалили заказы ✅")

    if len(Positionx.gets(category_id=category_id)) >= 1:
        await call.message.edit_text(
            "<b>📁 Выберите заказы для изменения 🖍</b>",
            reply_markup=position_edit_swipe_fp(remover, category_id, call),
        )
    else:
        await del_message(call.message)


# Подтверждение заказа
@router.callback_query(F.data.startswith("position_edit_done_confirm:"))
async def prod_position_edit_delete_confirm(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = int(call.data.split(":")[1])
    position_unix = int(call.data.split(":")[4])
    get_items = Itemx.gets(position_id=position_id)
    worker_id = Positionx.get_worker_id(position_id=position_id)
    position = Positionx.get(position_id=position_id)

    await call.message.edit_text("<b>🔄 Ждите</b>")

    get_position = Positionx.get(position_unix=position_unix)
    get_category = Categoryx.get(category_id=get_position.category_id)
    get_client = Clientx.get(client_id=call.from_user.id)

    get_user = Userx.get(user_id=worker_id)

    purchase_price = round(get_position.position_price, 2)

    save_items, save_len = Itemx.buy(get_items, 1)
    save_count = len(save_items)

    Userx.update(
        get_user.user_id,
        user_balance=round(get_user.user_balance + purchase_price, 2),
    )

    purchase_receipt = gen_id()
    purchase_unix = get_unix()
    purchase_data = "\n".join(save_items)

    Purchasesx.add(
        get_user.user_id,
        get_user.user_balance,
        round(get_user.user_balance - purchase_price, 2),
        purchase_receipt,
        purchase_data,
        purchase_price,
        get_position.position_price,
        get_position.position_id,
        get_position.position_name,
        get_category.category_id,
        get_category.category_name,
    )

    purchase_price = round(get_position.position_price, 2)

    save_items, save_len = Itemx.buy(get_items, 1)
    save_count = len(save_items)

    Clientx.update(
        get_client.client_id,
        client_balance=round(get_client.client_balance - purchase_price, 2),
    )

    purchase_receipt = gen_id()
    purchase_unix = get_unix()
    purchase_data = "\n".join(save_items)

    Purchasesclientx.add(
        get_client.client_id,
        get_client.client_balance,
        round(get_client.client_balance - purchase_price, 2),
        purchase_receipt,
        purchase_data,
        purchase_price,
        get_position.position_price,
        get_position.position_id,
        get_position.position_name,
        get_category.category_id,
        get_category.category_name,
    )

    # Positionx.update_gpt(
    #    field_name="position_unix",  # Обновляем по полю position_unix
    #    field_value=get_position.position_unix,
    #    position_status=1,
    # )

    Positionx.delete(position_unix=get_position.position_unix)

    Itemx.delete(position_id=position_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1 ⭐️", callback_data=f"rate_worker:{worker_id}:1"
                ),
                InlineKeyboardButton(
                    text="2 ⭐️", callback_data=f"rate_worker:{worker_id}:2"
                ),
                InlineKeyboardButton(
                    text="3 ⭐️", callback_data=f"rate_worker:{worker_id}:3"
                ),
                InlineKeyboardButton(
                    text="4 ⭐️", callback_data=f"rate_worker:{worker_id}:4"
                ),
                InlineKeyboardButton(
                    text="5 ⭐️", callback_data=f"rate_worker:{worker_id}:5"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Пропустить", callback_data=f"skip_rating:{worker_id}"
                )
            ],
        ]
    )

    await call.message.answer(
        ded(
            f"""
            <b>✅ Заказ успешно подтверждён!</b>
            ➖➖➖➖➖➖➖➖➖➖
            ▪️ Заказ: <code>{position.position_name} - {position.position_price}₽</code>
            ▪️ Оцените работу исполнителя:
        """
        ),
        reply_markup=keyboard,
    )


@router.callback_query(F.data.startswith("rate_worker:"))
async def rate_worker(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    """
    Обработка оценки работы исполнителя.
    """
    try:
        # Разделение callback_data
        data = call.data.split(":")
        worker_id = int(data[1])  # worker_id == user_id
        rating = int(data[2])

        # Обновление средней оценки
        Userx.update_rating(worker_id, rating)
        await call.message.edit_text("<b>Спасибо за вашу оценку!</b>")
    except ValueError as e:
        await call.message.edit_text(f"<b>Ошибка: {str(e)}</b>")
    except Exception as e:
        await call.message.edit_text("<b>Произошла ошибка при сохранении оценки.</b>")
        print(e)


@router.callback_query(F.data.startswith("skip_rating:"))
async def skip_rating(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    """
    Обработка пропуска оценки.
    """
    worker_id = int(call.data.split(":")[1])
    await call.message.edit_text("<b>Вы пропустили оценку исполнителя.</b>")


# Очистка позиции
@router.callback_query(F.data.startswith("position_edit_clear:"))
async def prod_position_edit_clear(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Вы хотите удалить все заказы позиции?</b>",
        reply_markup=position_edit_clear_finl(position_id, category_id, remover),
    )


# Согласие очистики позиции
@router.callback_query(F.data.startswith("position_edit_clear_confirm:"))
async def prod_position_edit_clear_confirm(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    Itemx.delete(position_id=position_id)
    await call.answer("📁 Вы успешно удалили все заказы в позиции ✅")

    await del_message(call.message)
    await position_open_admin(bot, call.from_user.id, position_id)


################################################################################
############################### ДОБАВЛЕНИЕ ЗАКАЗОВ #############################
# Перемещение по страницам категорий для добавления заказов
@router.callback_query(F.data.startswith("item_add_category_swipe:"))
async def prod_item_add_category_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>➕ Выберите позицию для заказов ➕</b>",
        reply_markup=item_add_category_swipe_fp(remover),
    )


# Выбор категории с нужной позицией
@router.callback_query(F.data.startswith("item_add_category_open:"))
async def prod_item_add_category_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    get_category = Categoryx.get(category_id=category_id)
    get_positions = Positionx.gets(category_id=category_id)

    await del_message(call.message)

    if len(get_positions) >= 1:
        await call.message.answer(
            "<b>➕ Выберите позицию для заказов ➕</b>",
            reply_markup=item_add_position_swipe_fp(0, category_id),
        )
    else:
        await call.answer(
            f"➕ Позиции в категории {get_category.category_name} отсутствуют"
        )


# Перемещение по страницам позиций для добавления заказов
@router.callback_query(F.data.startswith("item_add_position_swipe:"))
async def prod_item_add_position_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await call.message.edit_text(
        "<b>🔎 Выберите позицию для заказов ➕</b>",
        reply_markup=item_add_position_swipe_fp(remover, category_id),
    )


# Выбор позиции для добавления заказов
@router.callback_query(F.data.startswith("item_add_position_open:"), flags={"rate": 0})
async def prod_item_add_position_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]

    await state.update_data(here_add_item_category_id=category_id)
    await state.update_data(here_add_item_position_id=position_id)
    await state.update_data(here_add_item_count=0)
    await state.set_state("here_add_items")

    await del_message(call.message)

    await call.message.answer(
        ded(
            f"""
            <b>📤 Отправьте данные заказов.</b>
            ❗ Orders разделяются одной пустой строчкой. Пример:
            <code>Данные заказа...

            Данные заказа...

            Данные заказа...</code>
        """
        ),
        reply_markup=item_add_finish_finl(position_id),
    )


# Завершение загрузки заказов
@router.callback_query(
    F.data.startswith("item_add_position_finish:"), flags={"rate": 0}
)
async def prod_item_add_finish(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]

    try:
        count_items = (await state.get_data())["here_add_item_count"]
    except:
        count_items = 0

    await state.clear()

    await call.message.edit_reply_markup()
    await call.message.answer(
        "<b>📥 Загрузка заказов была успешно завершена ✅\n"
        f"🔎 Загружено заказов: <code>{count_items}шт</code></b>",
    )   

    get_position = Positionx.get(position_id=position_id)
    position_unix = get_position.position_unix

    await position_open_admin(bot, call.from_user.id, position_id, position_unix)


# Принятие данных товара
@router.message(F.text, StateFilter("here_add_items"), flags={"rate": 0})
async def prod_item_add_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    cache_message = await message.answer("<b>⌛ Ждите, заказы добавляются...</b>")

    get_items = clear_list(message.text.split("\n\n"))

    count_item = (await state.get_data())["here_add_item_count"]
    category_id = (await state.get_data())["here_add_item_category_id"]
    position_id = (await state.get_data())["here_add_item_position_id"]

    await state.update_data(here_add_item_count=count_item)

    get_user = Userx.get(user_id=message.from_user.id)
    Itemx.add(
        get_user.user_id,
        category_id,
        position_id,
        get_items,
    )

    await cache_message.edit_text(
        f"<b>📥 Заказ был успешно добавлен ✅</b>",
        reply_markup=item_add_finish_finl(position_id),
    )


################################################################################
############################### УДАЛЕНИЕ ЗАКАЗОВ ###############################
# Страницы удаления заказов
@router.callback_query(F.data.startswith("item_delete_swipe:"))
async def prod_item_delete_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    get_items = Itemx.gets(position_id=position_id)
    get_position = Positionx.get(position_id=position_id)

    await del_message(call.message)

    if len(get_items) >= 1:
        await call.message.answer(
            "<b>❌ Выберите закакз для удаления</b>",
            reply_markup=item_delete_swipe_fp(remover, position_id, category_id),
        )
    else:
        await call.answer(
            f"❌ Orders в позиции {get_position.position_name} отсутствуют"
        )


# Удаление товара
@router.callback_query(F.data.startswith("item_delete_open:"))
async def prod_item_delete_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    item_id = call.data.split(":")[1]

    await del_message(call.message)
    await item_open_admin(bot, call.from_user.id, item_id, 0)


# Подтверждение удаления товара
@router.callback_query(F.data.startswith("item_delete_confirm:"))
async def prod_item_delete_confirm_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    item_id = call.data.split(":")[1]

    get_item = Itemx.get(item_id=item_id)
    get_items = Itemx.gets(position_id=get_item.position_id)

    Itemx.delete(item_id=item_id)

    await call.message.edit_text(
        f"<b>✅ Заказ был успешно удалён</b>\n"
        f"➖➖➖➖➖➖➖➖➖➖\n"
        f"🧑🏻‍💻️ Заказ: <code>{get_item.item_data}</code>"
    )

    if len(get_items) >= 1:
        await call.message.answer(
            "<b>🧑🏻‍💻 Выберите заказ для удаления</b>",
            reply_markup=item_delete_swipe_fp(
                0, get_item.position_id, get_item.category_id
            ),
        )


################################################################################
############################### УДАЛЕНИЕ РАЗДЕЛОВ ##############################
# Возвращение к меню удаления разделов
@router.callback_query(F.data == "prod_removes_return")
async def prod_removes_return(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    await state.clear()

    await call.message.edit_text(
        "<b>🧑🏻‍💻 Выберите раздел который хотите удалить ❌</b>\n",
        reply_markup=products_removes_finl(),
    )


# Удаление всех категорий
@router.callback_query(F.data == "prod_removes_categories")
async def prod_removes_categories(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    get_categories = len(Categoryx.get_all())
    get_positions = len(Positionx.get_all())

    await call.message.edit_text(
        f"<b>❌ Вы действительно хотите удалить все категории, позиции и заказы?</b>\n"
        f"🗃 Категорий: <code>{get_categories}шт</code>\n"
        f"📁 Заказов: <code>{get_positions}шт</code>\n",
        reply_markup=products_removes_categories_finl(),
    )


# Подтверждение удаления всех категорий (позиций и заказов включительно)
@router.callback_query(F.data == "prod_removes_categories_confirm")
async def prod_removes_categories_confirm(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    get_categories = len(Categoryx.get_all())
    get_positions = len(Positionx.get_all())

    Categoryx.clear()
    Positionx.clear()
    Itemx.clear()

    await call.message.edit_text(
        f"<b>✅ Вы успешно удалили все категории</b>\n"
        f"🗃 Категорий: <code>{get_categories}шт</code>\n"
        f"📁 Заказов: <code>{get_positions}шт</code>\n"
    )


# Удаление всех позиций
@router.callback_query(F.data == "prod_removes_positions")
async def prod_removes_positions(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    get_positions = len(Positionx.get_all())

    await call.message.edit_text(
        f"<b>❌ Вы действительно хотите удалить все заказы?</b>\n"
        f"📁 Позиций: <code>{get_positions}шт</code>\n",
        reply_markup=products_removes_positions_finl(),
    )


# Подтверждение удаления всех позиций (заказов включительно)
@router.callback_query(F.data == "prod_removes_positions_confirm")
async def prod_position_remove(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    get_positions = len(Positionx.get_all())

    Positionx.clear()

    await call.message.edit_text(
        f"<b>✅ Вы успешно удалили все заказы</b>\n"
        f"📁 Заказов: <code>{get_positions}шт</code>\n"
    )
