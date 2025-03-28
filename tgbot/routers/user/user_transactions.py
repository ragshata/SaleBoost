# - *- coding: utf- 8 - *-
from typing import Union

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from tgbot.data.config import SECRET_KEY, SHOP_ID, get_admins
from tgbot.database.db_payments import Paymentsx
from tgbot.database.db_refill import Refillx
from tgbot.database.db_users import Clientx, Userx
from tgbot.database.db_withdraw import Withdrawx
from tgbot.keyboards.inline_user import (
    client_withdraw_method_finl,
    refill_bill_finl,
    refill_method_finl,
    withdraw_method_finl,
)
from tgbot.payment import create_payment, create_payout
from tgbot.services.api_yoomoney import YoomoneyAPI
from tgbot.utils.const_functions import is_number, to_number, gen_id
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import send_admins

min_refill_rub = 10  # Минимальная сумма пополнения в рублях

router = Router(name=__name__)


# Выбор способа пополнения
@router.callback_query(F.data == "user_refill")
async def refill_method(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_payment = Paymentsx.get()

    await call.message.edit_text(
        "<b>💰 Выберите способ пополнения</b>",
        reply_markup=refill_method_finl(),
    )


# Выбор способа пополнения
@router.callback_query(F.data.startswith("user_refill_method:"))
async def refill_method_select(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    pay_method = call.data.split(":")[1]

    await state.update_data(here_pay_method=pay_method)

    await state.set_state("here_refill_amount")
    await call.message.edit_text("<b>💰 Введите сумму пополнения</b>")


################################################################################
################################### ВВОД СУММЫ #################################
# Принятие суммы для пополнения средств
@router.message(F.text, StateFilter("here_refill_amount"))
async def refill_amount_get(message: Message, bot, state: FSM):
    if not message.text.isdigit():
        return await message.answer("❌ Введите корректную сумму для пополнения.")

    amount = int(message.text)
    if amount < min_refill_rub or amount > 100_000:
        return await message.answer(
            f"❌ Сумма должна быть не менее {min_refill_rub}₽ и не более 100 000₽."
        )

    # Сохраняем сумму в состоянии
    await state.update_data(refill_amount=amount)

    # Переход к запросу email
    await state.set_state("here_refill_email")
    await message.answer("📧 Введите вашу электронную почту для получения квитанции:")


@router.message(F.text, StateFilter("here_refill_email"))
async def refill_email_get(message: Message, bot, state: FSM):
    email = message.text

    # Простейшая проверка на email
    if "@" not in email or "." not in email:
        return await message.answer("❌ Введите корректный email.")

    # Получаем номер телефона из базы данных
    user_id = message.from_user.id
    user = Userx.get(user_id=message.from_user.id)
    client = Clientx.get(client_id=message.from_user.id)
    phone_client = client.client_number
    phone = user.user_number  # Ваша функция для получения телефона

    if not phone:
        phone = phone_client

    # Получаем сумму из состояния
    data = await state.get_data()
    amount = data.get("refill_amount")

    # Создаём платёж через YooKassa
    try:
        payment_data = create_payment(
            amount=amount, user_id=user_id, email=email, phone=phone
        )
        payment_url = payment_data["confirmation"]["confirmation_url"]

        # Очистка состояния
        await state.clear()

        # Отправляем пользователю ссылку на оплату
        await message.answer(
            f"✅ Ваш платёж на сумму {amount}₽ создан.\n\n"
            f"💳 Для оплаты перейдите по ссылке:\n{payment_url}"
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка при создании платежа: {str(e)}")


################################################################################
############################### ПРОВЕРКА ПЛАТЕЖЕЙ ##############################
# Проверка оплаты - ЮKassa
@router.callback_query(F.data.startswith("Pay:YooKassa"))
async def refill_check_yookassa(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    pay_way = call.data.split(":")[1]
    payment_id = call.data.split(":")[2]

    try:
        # Проверка статуса платежа
        payment_data = check_payment_status(payment_id)
        pay_status = payment_data["status"]
        pay_amount = float(payment_data["amount"]["value"])

        if pay_status == "succeeded":
            # Проверяем, не был ли уже зачислен этот платёж
            get_refill = Refillx.get(refill_receipt=payment_id)

            if get_refill is None:
                await refill_success(
                    bot=bot,
                    call=call,
                    pay_way=pay_way,
                    pay_amount=pay_amount,
                    pay_receipt=payment_id,
                    pay_comment=payment_id,
                )
            else:
                await call.answer(
                    "❗ Ваше пополнение уже зачислено.", True, cache_time=60
                )
        elif pay_status == "pending":
            await call.answer(
                "❗️ Платёж ещё не завершён. Пожалуйста, попробуйте позже.",
                True,
                cache_time=5,
            )
        elif pay_status == "canceled":
            await call.answer("❗️ Платёж был отменён.", True, cache_time=5)
        else:
            await call.answer(
                f"❗ Неизвестный статус платежа: {pay_status}. Обратитесь в поддержку.",
                True,
                cache_time=5,
            )
    except Exception as e:
        await call.answer(
            f"❗ Ошибка при проверке платежа: {e}. Попробуйте позже.",
            True,
            cache_time=5,
        )


################################################################################
############################### Проверка статуса платежа #######################
def check_payment_status(payment_id: str) -> dict:
    """
    Проверяет статус платежа через API ЮKassa.
    :param payment_id: ID платежа
    :return: Данные о платеже
    """
    url = f"https://api.yookassa.ru/v3/payments/{payment_id}"

    # Аутентификация
    auth = (SHOP_ID, SECRET_KEY)

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка при проверке статуса платежа: {response.json()}")


################################################################################
################################### !КЛИЕНТ! #################################
################################################################################


# Выбор способа пополнения
@router.callback_query(F.data == "client_refill")
async def refill_method(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_payment = Paymentsx.get()

    await call.message.edit_text(
        "<b>💰 Выберите способ пополнения</b>",
        reply_markup=refill_method_finl(),
    )


# Выбор способа пополнения
@router.callback_query(F.data.startswith("client_refill_method:"))
async def refill_method_select(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    pay_method = call.data.split(":")[1]

    await state.update_data(here_pay_method=pay_method)

    await state.set_state("client_here_refill_amount")
    await call.message.edit_text("<b>💰 Введите сумму пополнения</b>")


################################################################################
################################### ВВОД СУММЫ #################################
# Принятие суммы для пополнения средств
@router.message(F.text, StateFilter("client_here_refill_amount"))
async def refill_amount_get(message: Message, bot, state: FSM):
    if not message.text.isdigit():
        return await message.answer("❌ Введите корректную сумму для пополнения.")

    amount = int(message.text)
    if amount < min_refill_rub or amount > 100_000:
        return await message.answer(
            f"❌ Сумма должна быть не менее {min_refill_rub}₽ и не более 100 000₽."
        )

    # Сохраняем сумму в состоянии
    await state.update_data(refill_amount=amount)

    # Переход к запросу email
    await state.set_state("client_here_refill_email")
    await message.answer("📧 Введите вашу электронную почту для получения квитанции:")


@router.message(F.text, StateFilter("client_here_refill_email"))
async def refill_email_get(message: Message, bot, state: FSM):
    email = message.text

    # Простейшая проверка на email
    if "@" not in email or "." not in email:
        return await message.answer("❌ Введите корректный email.")

    # Получаем номер телефона из базы данных
    client_id = message.from_user.id
    client = Clientx.get(client_id=message.from_user.id)
    phone = client.client_number  # Ваша функция для получения телефона

    if not phone:
        return await message.answer("❌ Не удалось найти номер телефона в базе данных.")

    # Получаем сумму из состояния
    data = await state.get_data()
    amount = data.get("refill_amount")

    # Создаём платёж через YooKassa
    try:
        payment_data = create_payment(
            amount=amount, user_id=client_id, email=email, phone=phone
        )
        payment_url = payment_data["confirmation"]["confirmation_url"]

        # Очистка состояния
        await state.clear()

        # Отправляем пользователю ссылку на оплату
        await message.answer(
            f"✅ Ваш платёж на сумму {amount}₽ создан.\n\n"
            f"💳 Для оплаты перейдите по ссылке:\n{payment_url}"
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка при создании платежа: {str(e)}")


################################################################################
#################################### ПРОЧЕЕ ####################################
# Зачисление средств
async def refill_success(
    bot: Bot,
    call: CallbackQuery,
    pay_way: str,
    pay_amount: float,
    pay_receipt: Union[str, int] = None,
    pay_comment: str = None,
):
    get_user = Userx.get(user_id=call.from_user.id)
    get_client = Clientx.get(user_id=call.from_user.id)

    if pay_receipt is None:
        pay_receipt = gen_id()
    if pay_comment is None:
        pay_comment = ""

    Refillx.add(
        user_id=get_user.user_id,
        refill_comment=pay_comment,
        refill_amount=pay_amount,
        refill_receipt=pay_receipt,
        refill_method=pay_way,
    )

    Userx.update(
        call.from_user.id,
        user_balance=round(get_user.user_balance + pay_amount, 2),
        user_refill=round(get_user.user_refill + pay_amount, 2),
    )

    Clientx.update(
        call.from_user.id,
        client_balance=round(get_client.client_balance + pay_amount, 2),
        client_refill=round(get_client.client_refill + pay_amount, 2),
    )

    await call.message.edit_text(
        f"<b>💰 Вы пополнили баланс на сумму <code>{pay_amount}₽</code>. Удачи ❤️\n"
        f"🧾 Чек: <code>#{pay_receipt}</code></b>",
    )

    await send_admins(
        bot,
        f"👤 Пользователь: <b>@{get_user.user_login}</b> | <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a> | <code>{get_user.user_id}</code>\n"
        f"💰 Сумма пополнения: <code>{pay_amount}₽</code>\n"
        f"🧾 Чек: <code>#{pay_receipt}</code>",
    )


################################################################################
############################### Проверка статуса платежа #######################
def check_payment_status(payment_id: str) -> dict:
    """
    Проверяет статус платежа через API ЮKassa.
    :param payment_id: ID платежа
    :return: Данные о платеже
    """
    url = f"https://api.yookassa.ru/v3/payments/{payment_id}"

    # Аутентификация
    auth = (SHOP_ID, SECRET_KEY)

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Ошибка при проверке статуса платежа: {response.json()}")


#!###############################################################################
################################### ! ВЫВОД ! ###################################
#!###############################################################################

min_withdraw_rub = 100  # Минимальная сумма для вывода в рублях


# Выбор способа вывода
@router.callback_query(F.data == "user_withdraw")
async def withdraw_method(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await call.message.edit_text(
        "<b>💸 Выберите способ вывода</b>",
        reply_markup=withdraw_method_finl(),  # Здесь должен быть клавиатура для выбора способа
    )


# Выбор способа вывода
@router.callback_query(F.data.startswith("user_withdraw_method:"))
async def withdraw_method_select(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    withdraw_method = call.data.split(":")[1]

    await state.update_data(here_withdraw_method=withdraw_method)

    await state.set_state("here_withdraw_amount")
    await call.message.edit_text("<b>💸 Введите сумму для вывода</b>")


################################################################################
################################### ВВОД СУММЫ #################################
# Принятие суммы для вывода
@router.message(F.text, StateFilter("here_withdraw_amount"))
async def withdraw_amount_get(message: Message, bot, state: FSM):
    if not message.text.isdigit():
        return await message.answer("❌ Введите корректную сумму для вывода.")

    amount = int(message.text)
    if amount < min_withdraw_rub or amount > 100_000:
        return await message.answer(
            f"❌ Сумма должна быть не менее {min_withdraw_rub}₽ и не более 100 000₽."
        )

    # Проверка доступного баланса
    user = Userx.get(user_id=message.from_user.id)  # Получаем данные пользователя
    if user.user_balance < amount:
        return await message.answer("❌ Недостаточно средств для вывода.")

    # Сохраняем сумму в состоянии
    await state.update_data(withdraw_amount=amount)

    # Переход к запросу имени
    await state.set_state("here_withdraw_name")
    await message.answer("👤 Введите ваше имя:")


@router.message(F.text, StateFilter("here_withdraw_name"))
async def withdraw_name_get(message: Message, bot, state: FSM):
    name = message.text

    # Сохраняем имя в состоянии
    await state.update_data(withdraw_name=name)

    # Переход к запросу фамилии
    await state.set_state("here_withdraw_surname")
    await message.answer("👤 Введите вашу фамилию:")


@router.message(F.text, StateFilter("here_withdraw_surname"))
async def withdraw_surname_get(message: Message, bot, state: FSM):
    surname = message.text

    # Сохраняем фамилию в состоянии
    await state.update_data(withdraw_surname=surname)

    # Переход к запросу номера телефона
    await state.set_state("here_withdraw_phone")
    await message.answer("📱 Введите ваш номер телефона:")


@router.message(F.text, StateFilter("here_withdraw_phone"))
async def withdraw_phone_get(message: Message, bot, state: FSM):
    phone = message.text

    # Простейшая проверка номера телефона
    if not phone.isdigit() or len(phone) < 10:
        return await message.answer("❌ Введите корректный номер телефона. Без '+ '")

    # Сохраняем номер телефона в состоянии
    await state.update_data(withdraw_phone=phone)

    # Переход к запросу названия банка
    await state.set_state("here_withdraw_bank")
    await message.answer("🏦 Введите название вашего банка:")


@router.message(F.text, StateFilter("here_withdraw_bank"))
async def withdraw_bank_get(message: Message, bot, state: FSM):
    bank_name = message.text

    # Сохраняем название банка в состоянии
    await state.update_data(withdraw_bank=bank_name)

    # Переход к запросу наличия СБП
    await state.set_state("here_withdraw_sbp")
    await message.answer("✅ У вас подключен СБП? (Да/Нет):")


@router.message(F.text, StateFilter("here_withdraw_sbp"))
async def withdraw_sbp_get(message: Message, bot, state: FSM):
    sbp_status = message.text.strip().lower()

    if sbp_status not in ["да", "нет"]:
        return await message.answer("❌ Пожалуйста, ответьте 'Да' или 'Нет'.")

    # Сохраняем статус СБП в состоянии
    await state.update_data(withdraw_sbp=(sbp_status == "да"))

    # Переход к запросу номера карты
    await state.set_state("here_withdraw_details")
    await message.answer("💳 Введите номер вашей банковской карты для вывода средств:")


@router.message(F.text, StateFilter("here_withdraw_details"))
async def withdraw_details_get(message: Message, bot: Bot, state: FSM):
    withdraw_details = message.text

    # Простейшая проверка номера карты
    if len(withdraw_details) < 16 or not withdraw_details.isdigit():
        return await message.answer("❌ Введите корректный номер карты.")

    # Получаем данные из состояния
    data = await state.get_data()
    amount = data.get("withdraw_amount")
    name = data.get("withdraw_name")
    surname = data.get("withdraw_surname")
    phone = data.get("withdraw_phone")
    bank_name = data.get("withdraw_bank")
    sbp_status = data.get("withdraw_sbp")
    user_id = message.from_user.id

    try:
        # Создание кнопки для подтверждения
        confirm_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Подтвердить",
                        callback_data=f"confirm_withdraw:{user_id}:{amount}",
                    )
                ]
            ]
        )

        # Уведомление администратора с кнопкой
        admins = get_admins()  # Получаем список ID администраторов
        for admin_id in admins:
            await bot.send_message(
                admin_id,
                (
                    f"📨 <b>Запрос на вывод средств</b>\n"
                    f"👤 Пользователь: {name} {surname}\n"
                    f"📱 Телефон: {phone}\n"
                    f"🏦 Банк: {bank_name}\n"
                    f"🔗 СБП: {'Подключен' if sbp_status else 'Не подключен'}\n"
                    f"💳 Счёт: {withdraw_details}\n"
                    f"💰 Сумма: {amount}₽"
                ),
                reply_markup=confirm_button,
            )

        # Уведомляем пользователя
        await message.answer(
            "✅ Ваш запрос на вывод средств отправлен администратору. Ожидайте подтверждения."
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке уведомления: {e}")

    # Очищаем состояние
    await state.clear()


@router.callback_query(F.data.startswith("confirm_withdraw:"))
async def confirm_withdraw(call: CallbackQuery, bot: Bot):
    try:
        # Извлечение данных из callback_data
        _, user_id, amount = call.data.split(":")
        user_id = int(user_id)
        amount = float(amount)

        # Получение пользователя и уменьшение баланса
        user = Userx.get(user_id=user_id)
        if user.user_balance >= amount:
            Userx.update(
                user_id=user_id,
                user_balance=round(user.user_balance - amount, 2),
            )

            # Уведомляем пользователя о подтверждении
            await bot.send_message(
                user_id,
                f"✅ Ваш запрос на вывод средств на сумму {amount}₽ подтверждён. Деньги скоро поступят на ваш счёт.",
            )

            # Уведомляем администратора о выполнении
            await call.message.edit_text(
                f"Запрос на вывод средств пользователя ID {user_id} на сумму {amount}₽ подтверждён."
            )
        else:
            await call.message.edit_text(
                f"❌ У пользователя недостаточно средств. Баланс: {user.user_balance}₽."
            )
    except Exception as e:
        await call.message.answer(f"❌ Ошибка при обработке запроса: {e}")


async def notify_admins_about_withdraw(
    bot: Bot, user_id: int, amount: float, card_number: str
):
    """
    Уведомляет администраторов о запросе на вывод средств.

    :param bot: экземпляр бота
    :param user_id: ID пользователя, запросившего вывод
    :param amount: сумма вывода
    :param card_number: номер банковской карты
    """
    admins = get_admins()  # Получаем список ID администраторов
    for admin_id in admins:
        await bot.send_message(
            admin_id,
            (
                f"📨 <b>Запрос на вывод средств</b>\n"
                f"👤 Пользователь: ID {user_id}\n"
                f"💳 Счёт: {card_number}\n"
                f"💰 Сумма: {amount}₽"
            ),
        )


##########################################################
##########################################################
#######################!КЛИЕНТ!###########################
##########################################################
##########################################################
# Выбор способа вывода
@router.callback_query(F.data == "client_withdraw")
async def withdraw_method(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await call.message.edit_text(
        "<b>💸 Выберите способ вывода</b>",
        reply_markup=client_withdraw_method_finl(),  # Здесь должен быть клавиатура для выбора способа
    )


# Выбор способа вывода
@router.callback_query(F.data.startswith("client_withdraw_method:"))
async def withdraw_method_select(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    withdraw_method = call.data.split(":")[1]

    await state.update_data(here_withdraw_method=withdraw_method)

    await state.set_state("client_here_withdraw_amount")
    await call.message.edit_text("<b>💸 Введите сумму для вывода</b>")


################################################################################
################################### ВВОД СУММЫ #################################
# Принятие суммы для вывода
@router.message(F.text, StateFilter("client_here_withdraw_amount"))
async def withdraw_amount_get(message: Message, bot, state: FSM):
    if not message.text.isdigit():
        return await message.answer("❌ Введите корректную сумму для вывода.")

    amount = int(message.text)
    if amount < min_withdraw_rub or amount > 100_000:
        return await message.answer(
            f"❌ Сумма должна быть не менее {min_withdraw_rub}₽ и не более 100 000₽."
        )

    # Проверка доступного баланса
    client = Clientx.get(client_id=message.from_user.id)  # Получаем данные пользователя
    if client.client_balance < amount:
        return await message.answer("❌ Недостаточно средств для вывода.")

    # Сохраняем сумму в состоянии
    await state.update_data(withdraw_amount=amount)

    # Переход к запросу имени
    await state.set_state("client_here_withdraw_name")
    await message.answer("👤 Введите ваше имя:")


@router.message(F.text, StateFilter("client_here_withdraw_name"))
async def withdraw_name_get(message: Message, bot, state: FSM):
    name = message.text

    # Сохраняем имя в состоянии
    await state.update_data(withdraw_name=name)

    # Переход к запросу фамилии
    await state.set_state("client_here_withdraw_surname")
    await message.answer("👤 Введите вашу фамилию:")


@router.message(F.text, StateFilter("client_here_withdraw_surname"))
async def withdraw_surname_get(message: Message, bot, state: FSM):
    surname = message.text

    # Сохраняем фамилию в состоянии
    await state.update_data(withdraw_surname=surname)

    # Переход к запросу номера телефона
    await state.set_state("client_here_withdraw_phone")
    await message.answer("📱 Введите ваш номер телефона:")


@router.message(F.text, StateFilter("client_here_withdraw_phone"))
async def withdraw_phone_get(message: Message, bot, state: FSM):
    phone = message.text

    # Простейшая проверка номера телефона
    if not phone.isdigit() or len(phone) < 10:
        return await message.answer("❌ Введите корректный номер телефона. Без '+' ")

    # Сохраняем номер телефона в состоянии
    await state.update_data(withdraw_phone=phone)

    # Переход к запросу названия банка
    await state.set_state("client_here_withdraw_bank")
    await message.answer("🏦 Введите название вашего банка:")


@router.message(F.text, StateFilter("client_here_withdraw_bank"))
async def withdraw_bank_get(message: Message, bot, state: FSM):
    bank_name = message.text

    # Сохраняем название банка в состоянии
    await state.update_data(withdraw_bank=bank_name)

    # Переход к запросу наличия СБП
    await state.set_state("client_here_withdraw_sbp")
    await message.answer("✅ У вас подключен СБП? (Да/Нет):")


@router.message(F.text, StateFilter("client_here_withdraw_sbp"))
async def withdraw_sbp_get(message: Message, bot, state: FSM):
    sbp_status = message.text.strip().lower()

    if sbp_status not in ["да", "нет"]:
        return await message.answer("❌ Пожалуйста, ответьте 'Да' или 'Нет'.")

    # Сохраняем статус СБП в состоянии
    await state.update_data(withdraw_sbp=(sbp_status == "да"))

    # Переход к запросу номера карты
    await state.set_state("client_here_withdraw_details")
    await message.answer("💳 Введите номер вашей банковской карты для вывода средств:")


@router.message(F.text, StateFilter("client_here_withdraw_details"))
async def withdraw_details_get(message: Message, bot: Bot, state: FSM):
    withdraw_details = message.text

    # Простейшая проверка номера карты
    if len(withdraw_details) < 16 or not withdraw_details.isdigit():
        return await message.answer("❌ Введите корректный номер карты.")

    # Получаем данные из состояния
    data = await state.get_data()
    amount = data.get("withdraw_amount")
    name = data.get("withdraw_name")
    surname = data.get("withdraw_surname")
    phone = data.get("withdraw_phone")
    bank_name = data.get("withdraw_bank")
    sbp_status = data.get("withdraw_sbp")
    client_id = message.from_user.id

    try:
        # Создание кнопки для подтверждения
        confirm_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Подтвердить",
                        callback_data=f"client_confirm_withdraw:{client_id}:{amount}",
                    )
                ]
            ]
        )

        # Уведомление администратора с кнопкой
        admins = get_admins()  # Получаем список ID администраторов
        for admin_id in admins:
            await bot.send_message(
                admin_id,
                (
                    f"📨 <b>Запрос на вывод средств</b>\n"
                    f"👤 Пользователь: {name} {surname}\n"
                    f"📱 Телефон: {phone}\n"
                    f"🏦 Банк: {bank_name}\n"
                    f"🔗 СБП: {'Подключен' if sbp_status else 'Не подключен'}\n"
                    f"💳 Счёт: {withdraw_details}\n"
                    f"💰 Сумма: {amount}₽"
                ),
                reply_markup=confirm_button,
            )

        # Уведомляем пользователя
        await message.answer(
            "✅ Ваш запрос на вывод средств отправлен администратору. Ожидайте подтверждения."
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке уведомления: {e}")

    # Очищаем состояние
    await state.clear()


@router.callback_query(F.data.startswith("client_confirm_withdraw:"))
async def client_confirm_withdraw(call: CallbackQuery, bot: Bot):
    try:
        # Извлечение данных из callback_data
        _, client_id, amount = call.data.split(":")
        client_id = int(client_id)
        amount = float(amount)

        # Получение пользователя и уменьшение баланса
        client = Clientx.get(client_id=client_id)
        if client.client_balance >= amount:
            Clientx.update(
                client_id=client_id,
                client_balance=round(client.client_balance - amount, 2),
            )

            # Уведомляем пользователя о подтверждении
            await bot.send_message(
                client_id,
                f"✅ Ваш запрос на вывод средств на сумму {amount}₽ подтверждён. Деньги скоро поступят на ваш счёт.",
            )

            # Уведомляем администратора о выполнении
            await call.message.edit_text(
                f"Запрос на вывод средств пользователя ID {client_id} на сумму {amount}₽ подтверждён."
            )
        else:
            await call.message.edit_text(
                f"❌ У пользователя недостаточно средств. Баланс: {client.client_balance}₽."
            )
    except Exception as e:
        await call.message.answer(f"❌ Ошибка при обработке запроса: {e}")
