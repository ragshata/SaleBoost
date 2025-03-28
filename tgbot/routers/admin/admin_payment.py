# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from tgbot.database.db_payments import Paymentsx
from tgbot.keyboards.inline_admin import (
    payment_method_finl,
    payment_yoomoney_finl,
    close_finl,
)
from tgbot.services.api_yoomoney import YoomoneyAPI
from tgbot.utils.const_functions import ded
from tgbot.utils.misc.bot_models import FSM, ARS

router = Router(name=__name__)


################################################################################
############################ ВЫБОР СПОСОБА ПОПОЛНЕНИЯ ##########################
# Открытие способов пополнения
@router.message(F.text == "🖲 Способы пополнений")
async def payment_methods(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🖲 Выберите способы пополнений</b>",
        reply_markup=payment_method_finl(),
    )


# Включение/выключение самих способов пополнения
@router.callback_query(F.data.startswith("payment_method:"))
async def payment_methods_edit(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    way_pay = call.data.split(":")[1]
    way_status = call.data.split(":")[2]

    get_payment = Paymentsx.get()

    if way_pay == "Yoomoney":
        if way_status == "True" and get_payment.yoomoney_token == "None":
            return await call.answer(
                "❗ Добавьте Юkassa кошелёк перед включением Способов пополнений", True
            )

        Paymentsx.update(way_yoomoney=way_status)

    await call.message.edit_text(
        "<b>🖲 Выберите способы пополнений</b>",
        reply_markup=payment_method_finl(),
    )


# Открытие Юkassa
@router.message(F.text == "🔮 Юkassa")
async def payment_yoomoney_open(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🔮 Управление - Юkassa</b>",
        reply_markup=payment_yoomoney_finl(),
    )


################################################################################
#################################### Юkassa ####################################
# Баланс Юkassa
@router.callback_query(F.data == "payment_yoomoney_balance")
async def payment_yoomoney_balance(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    response = await YoomoneyAPI(
        bot=bot,
        arSession=arSession,
        update=call,
        skipping_error=True,
    ).balance()

    await call.message.answer(
        response,
        reply_markup=close_finl(),
    )


# Проверка Юkassa
@router.callback_query(F.data == "payment_yoomoney_check")
async def payment_yoomoney_check(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    response = await YoomoneyAPI(
        bot=bot,
        arSession=arSession,
        update=call,
        skipping_error=True,
    ).check()

    await call.message.answer(
        response,
        reply_markup=close_finl(),
    )


# Изменение Юkassa
@router.callback_query(F.data == "payment_yoomoney_edit")
async def payment_yoomoney_edit(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    response = await YoomoneyAPI(bot=bot, arSession=arSession).authorization_get()

    await state.set_state("here_yoomoney_token")
    await call.message.edit_text(
        ded(
            f"""
            <b>🔮 Для изменения Юkassa кошелька</b>
            ▪️ Перейдите по ссылке ниже и авторизуйте приложение.
            ▪️ После авторизации, отправьте ссылку или код из адресной строки.
            🔗 {response}
        """
        ),
        disable_web_page_preview=True,
    )


################################ ПРИНЯТИЕ Юkassa ###############################
# Принятие токена Юkassa
@router.message(StateFilter("here_yoomoney_token"))
async def payment_yoomoney_edit_token(
    message: Message, bot: Bot, state: FSM, arSession: ARS
):
    await state.clear()

    cache_message = await message.answer(
        "<b>🔮 Проверка введённых Юkassa данных... 🔄</b>"
    )

    get_code = message.text

    try:
        get_code = get_code[get_code.index("code=") + 5 :].replace(" ", "")
    except:
        ...

    status, response, token = await YoomoneyAPI(
        bot=bot,
        arSession=arSession,
    ).authorization_enter(get_code)

    if status:
        Paymentsx.update(yoomoney_token=token)

    await cache_message.edit_text(response)

    await message.answer(
        "<b>🔮 Управление - Юkassa</b>",
        reply_markup=payment_yoomoney_finl(),
    )
