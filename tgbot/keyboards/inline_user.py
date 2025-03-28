# - *- coding: utf- 8 - *-
from typing import Union

from aiogram import Router, Bot, F
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import requests
from aiogram.types import CallbackQuery, Message
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from aiogram.filters.state import StateFilter

from tgbot.data.config import SECRET_KEY, SHOP_ID
from tgbot.database.db_payments import Paymentsx
from tgbot.payment import create_payment
from tgbot.utils.const_functions import ikb

router = Router(name=__name__)


################################################################################
#################################### ПРОЧЕЕ ####################################
# Открытие своего профиля
def user_profile_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💰 Вывести", data="user_withdraw"),
        ikb("💸 Пополнить", data="user_refill"),
    )

    return keyboard.as_markup()


def client_profile_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💰 Вывести", data="client_withdraw"),
    ).row(
        ikb("💸 Пополнить баланс", data="client_refill"),
    )

    return keyboard.as_markup()


@router.callback_query(F.data == "client_refill")
async def start_refill(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите сумму пополнения в рублях:")
    await state.set_state("waiting_for_amount")


@router.message(StateFilter("waiting_for_amount"))
async def process_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount <= 0:
            await message.answer("Введите корректную сумму (больше 0).")
            return

        # Создаём платёж через ЮKassa
        payment_data = create_payment(amount, user_id=message.from_user.id)
        confirmation_url = payment_data["confirmation"]["confirmation_url"]

        # Кнопка для оплаты
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Оплатить 💳", url=confirmation_url))

        # Отправляем пользователю
        await message.answer(
            f"Для оплаты {amount:.2f} RUB нажмите на кнопку ниже:",
            reply_markup=keyboard,
        )
        await state.clear()  # Сбрасываем состояние
    except ValueError:
        await message.answer("Введите числовое значение суммы.")


# Ссылка на поддержку
def user_support_finl(support_login: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💌 Написать в поддержку", url=f"https://t.me/{support_login}"),
    )

    return keyboard.as_markup()


def user_client_finl(chat_link) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("☎️ Ссылка на чат с заказчиком", url=f"tg://user?id={chat_link}"),
    )

    return keyboard.as_markup()


################################################################################
################################### ПЛАТЕЖИ ####################################
# Выбор способов пополнения
def refill_method_finl() -> Union[InlineKeyboardMarkup, None]:
    keyboard = InlineKeyboardBuilder()

    get_payments = Paymentsx.get()

    keyboard.row(ikb("🔮 Юkassa", data="user_refill_method:YooKassa"))

    keyboard.row(ikb("🔙 Вернуться", data="user_profile"))

    return keyboard.as_markup()

def withdraw_method_finl() -> Union[InlineKeyboardMarkup, None]:
    keyboard = InlineKeyboardBuilder()

    get_payments = Paymentsx.get()

    keyboard.row(ikb("🔮 Юkassa", data="user_withdraw_method:YooKassa"))

    keyboard.row(ikb("🔙 Вернуться", data="user_profile"))

    return keyboard.as_markup()

def client_withdraw_method_finl() -> Union[InlineKeyboardMarkup, None]:
    keyboard = InlineKeyboardBuilder()

    get_payments = Paymentsx.get()

    keyboard.row(ikb("🔮 Юkassa", data="client_withdraw_method:YooKassa"))

    keyboard.row(ikb("🔙 Вернуться", data="user_profile"))

    return keyboard.as_markup()

# Проверка платежа
def refill_bill_finl(
    pay_link: str, pay_receipt: Union[str, int], pay_way: str
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(ikb("🌀 Перейти к оплате", url=pay_link)).row(
        ikb("🔄 Проверить оплату", data=f"Pay:{pay_way}:{pay_receipt}")
    )

    return keyboard.as_markup()


################################################################################
#################################### ЗАКАЗЫ ####################################
# Открытие позиции для просмотра
def products_open_finl(position_id, category_id,position_unix) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(ikb("💰 Выполнить заказ", data=f"buy_item_open:{position_id}:{position_unix}")).row(
        ikb("🔙 Вернуться", data=f"buy_category_open:{category_id}")
    )

    return keyboard.as_markup()


# Подтверждение выполнения заказа
def products_confirm_finl(position_id, category_id, position_unix) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Подтвердить", data=f"buy_item_confirm:{position_id}:{position_unix}"),
        ikb("❌ Отменить", data=f"buy_position_open:{position_id}:{position_unix}"),
    )

    return keyboard.as_markup()


# Возврат к позиции при отмене ввода
def products_return_finl(position_id, category_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(ikb("🔙 Вернуться", data=f"buy_position_open:{position_id}:0"))

    return keyboard.as_markup()
