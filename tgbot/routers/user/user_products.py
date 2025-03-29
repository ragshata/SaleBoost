# - *- coding: utf- 8 - *-
import asyncio

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from tgbot.database.db_purchases import Purchasesx
from tgbot.database.db_users import Userx
from tgbot.keyboards.inline_user import (
    products_confirm_finl,
    products_return_finl,
    user_client_finl,
)
from tgbot.keyboards.inline_user_page import *
from tgbot.keyboards.reply_main import menu_frep, menu_second_start
from tgbot.utils.const_functions import (
    convert_day,
    split_messages,
    get_unix,
    ded,
    del_message,
    convert_date,
    gen_id,
)
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.text_functions import position_open_user

router = Router(name=__name__)


# Страницы категорий для Orders
@router.callback_query(F.data.startswith("buy_category_swipe:"))
async def user_buy_category_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>🔎 Выберите категорию:</b>",
        reply_markup=prod_item_category_swipe_fp(remover),
    )


@router.callback_query(F.data.startswith("buy_category_open:"))
async def user_buy_category_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    data_parts = call.data.split(":")  # Разбиваем данные
    category_id = data_parts[1]  # Получаем category_id

    # Проверяем наличие третьего элемента
    if len(data_parts) > 2:
        remover = int(data_parts[2])
    else:
        remover = (
            0  # Устанавливаем значение по умолчанию, если третий элемент отсутствует
        )

    get_category = Categoryx.get(category_id=category_id)
    get_positions = Positionx.gets(category_id=category_id)

    if len(get_positions) >= 1:
        await del_message(call.message)

        await call.message.answer(
            f"<b>🔎 Выберите нужный вам заказ</b>",
            reply_markup=prod_item_position_swipe_fp(remover, category_id),
        )
    else:
        if remover == 0:
            await call.message.edit_text(
                "<b>🔎 Увы, заказы в данное время отсутствуют.</b>"
            )
            await call.answer("❗ Orders были изменены или удалены")
        else:
            await call.answer(
                f"❕ Orders в категории {get_category.category_name} отсутствуют",
                True,
                cache_time=5,
            )


# Страницы позиций для Orders
@router.callback_query(F.data.startswith("buy_position_swipe:"))
async def user_buy_position_swipe(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    get_category = Categoryx.get(category_id=category_id)

    await del_message(call.message)
    await call.message.answer(
        f"<b>🔎 Выберите нужный вам заказ</b>",
        reply_markup=prod_item_position_swipe_fp(remover, category_id),
    )


# Открытие позиции для Orders
@router.callback_query(F.data.startswith("buy_position_open:"))
async def user_buy_position_open(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    position_id = call.data.split(":")[1]
    position_unix = call.data.split(":")[2]

    await state.clear()

    await del_message(call.message)
    await position_open_user(bot, call.from_user.id, position_id, position_unix)


#################################### ВЫПОЛНЕНИЕ ###################################
# Выбор количества заказов для выполнения
@router.callback_query(F.data.startswith("buy_item_open:"))
async def user_buy_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    position_unix = call.data.split(":")[2]

    get_position = Positionx.get(position_unix=position_unix)
    get_items = Itemx.gets(position_id=position_id)
    get_user = Userx.get(user_id=call.from_user.id)

    if True:
        await state.clear()

        await del_message(call.message)

        await call.message.answer(
            ded(
                f"""
                <b>❓ Вы действительно готовы выполнить заказ?</b>
                ➖➖➖➖➖➖➖➖➖➖
                ▪️ Заказ: <code>{get_position.position_name}</code>
                ▪️ После выполнения вы получите: <code>{get_position.position_price}₽</code>
            """
            ),
            reply_markup=products_confirm_finl(
                position_id, get_position.category_id, get_position.position_unix
            ),
        )


# Принятие количества заказов для Orders
@router.message(F.text, StateFilter("here_item_count"))
async def user_buy_count(message: Message, bot: Bot, state: FSM, arSession: ARS):
    position_id = (await state.get_data())["here_buy_position_id"]

    get_position = Positionx.get(position_id=position_id)
    get_user = Userx.get(user_id=message.from_user.id)
    client_id = get_position.position_id
    amount_pay = round(get_position.position_price, 2)
    get_purchases = Purchasesx.gets(user_id=message.from_user.id)
    how_days = int(get_unix() - get_user.user_unix) // 60 // 60 // 24
    count_items = sum([purchase.purchase_count for purchase in get_purchases])

    await state.clear()

    await message.answer(
        ded(
            f"""
            <b>🧑🏻‍💻 Вы действительно готовы выполнить заказ?</b>
            ➖➖➖➖➖➖➖➖➖➖
            ▪️ Заказ: <code>{get_position.position_name}</code>
            ▪️ Цена: <code>{amount_pay}₽</code>
        """
        ),
        reply_markup=products_confirm_finl(position_id, get_position.category_id),
    )


@router.callback_query(F.data.startswith("buy_item_confirm:"))
async def user_buy_confirm(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = int(call.data.split(":")[1])
    position_unix = int(call.data.split(":")[2])
    await call.message.edit_text("<b>🔄 Ждите ответа заказчика</b>")

    get_position = Positionx.get(position_unix=position_unix)
    get_user = Userx.get(user_id=call.from_user.id)
    client_id = get_position.position_id  # ID заказчика
    purchase_price = round(get_position.position_price, 2)
    user_rating = (
        round(get_user.user_rating_avg, 2) if get_user.user_rating_avg else "Нет оценок"
    )

    # Уведомление заказчика
    await bot.send_message(
        chat_id=client_id,
        text=ded(
            f"""
            <b>📦 Исполнитель отправил заявку на выполнение вашего заказа:</b>
            ➖➖➖➖➖➖➖➖➖➖
            ▪️ Заказ: <code>{get_position.position_name}</code>
            ▪️ Цена: <code>{purchase_price}₽</code>

            <b>👤 Profile исполнителя:</b>
            🆔 Имя: <code>{get_user.user_name} {get_user.user_surname}</code>
            ⭐ Средняя оценка: <code>{user_rating}</code>
            🕰 Регистрация: <code>{convert_date(get_user.user_unix, False, False)}</code>
            """
        ),
        reply_markup=confirm_tusk_button(
            position_id, purchase_price, call.from_user.id, position_unix
        ),
    )


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@router.callback_query(F.data.startswith("buy_item_confirm_fl:"))
async def client_accept_worker(call: CallbackQuery, bot: Bot):
    data = call.data.split(":")
    position_id = int(data[1])
    position_unix = int(data[4])
    user_id = int(data[3])
    get_position = Positionx.get(position_unix=position_unix)
    chat_link = get_position.position_id  # Пример ссылки

    # Уведомляем исполнителя
    await bot.send_message(
        chat_id=user_id,
        text=f"<b>Ваш запрос принят!</b>",
        reply_markup=user_client_finl(chat_link),
    )

    # Обновляем статус заказа
    Positionx.update_unix(position_unix, worker_id=user_id)

    # Уведомляем заказчика
    await call.message.edit_text("<b>Вы приняли заявку исполнителя</b>")


@router.callback_query(F.data.startswith("buy_item_confirm_cl:"))
async def client_reject_worker(call: CallbackQuery, bot: Bot):
    data = call.data.split(":")
    user_id = int(data[3])

    # Уведомляем исполнителя
    await bot.send_message(
        chat_id=user_id,
        text="<b>Заказчик отказал вам в выполнении заказа</b>",
    )

    # Уведомляем заказчика
    await call.message.edit_text("<b>Вы отклонили заявку исполнителя</b>")


def confirm_tusk_button(
    position_id: int, amount: float, user_id: int, position_unix
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data=f"buy_item_confirm_fl:{position_id}:{amount}:{user_id}:{position_unix}",
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"buy_item_confirm_cl:{position_id}:{amount}:{user_id}:{position_unix}",
                ),
            ]
        ]
    )


from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
