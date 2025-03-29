# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F, types
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from tgbot.database.db_users import Clientx, Userx
from tgbot.database.db_settings import Settingsx
from tgbot.database.db_users import UserModel
from tgbot.keyboards.inline_user import user_support_finl
from tgbot.keyboards.reply_main import menu_frep, menu_second_start, menu_second_start_clients
from tgbot.utils.const_functions import ded
from tgbot.utils.misc.bot_filters import IsBuy, IsRefill, IsWork
from tgbot.utils.misc.bot_models import FSM, ARS

# Игнор-колбэки покупок
prohibit_buy = [
    "buy_category_swipe",
    "buy_category_open",
    "buy_position_swipe",
    "buy_position_open",
    "buy_item_open",
    "buy_item_confirm",
]

# Игнор-колбэки пополнений
prohibit_refill = [
    "user_refill",
    "user_refill_method",
    "Pay:",
    "Pay:Yoomoney",
]

router = Router(name=__name__)


################################################################################
########################### СТАТУС ТЕХНИЧЕСКИХ РАБОТ ###########################
# Фильтр на технические работы - сообщение
@router.message(IsWork())
async def filter_work_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_settings = Settingsx.get()

    if get_settings.misc_support != "None":
        return await message.answer(
            "<b>⛔ Бот находится на технических работах.</b>",
            reply_markup=user_support_finl(get_settings.misc_support),
        )

    await message.answer("<b>⛔ Бот находится на технических работах.</b>")


# Фильтр на технические работы - колбэк
@router.callback_query(IsWork())
async def filter_work_callback(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    await state.clear()

    await call.answer("⛔ Бот находится на технических работах.", True)


################################################################################
################################# СТАТУС ПОКУПОК ###############################
# Фильтр на доступность покупок - сообщение
@router.message(IsBuy(), F.text == "🧑🏻‍💻 Выполнить заказ")
@router.message(IsBuy(), StateFilter("here_item_count"))
async def filter_buy_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer("<b>⛔ Orders временно отключены.</b>")


# Фильтр на доступность покупок - колбэк
@router.callback_query(IsBuy(), F.text.startswith(prohibit_buy))
async def filter_buy_callback(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    await state.clear()

    await call.answer("⛔ Orders временно отключены.", True)


################################################################################
############################### СТАТУС ПОПОЛНЕНИЙ ##############################
# Фильтр на доступность пополнения - сообщение
@router.message(IsRefill(), StateFilter("here_pay_amount"))
async def filter_refill_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer("<b>⛔ Пополнение временно отключено.</b>")


# Фильтр на доступность пополнения - колбэк
@router.callback_query(IsRefill(), F.text.startswith(prohibit_refill))
async def filter_refill_callback(
    call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS
):
    await state.clear()

    await call.answer("⛔ Пополнение временно отключено.", True)


################################################################################
#################################### ПРОЧЕЕ ####################################
# Открытие главного меню
@router.message(F.text.in_(("🔙 Main menu", "/start")))
async def main_start(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        ded(
            """
            🚀 Bee — Your assistant in the world of freelancing! 🚀

            Welcome! This bot will help you:

            ➡️ Quickly find performers for your projects.
            ➡️ Easily start earning money by offering your services.

            What do you want to do?

            1️⃣ Become a performer: Registration and start working in just a few steps!

            2️⃣ Find a performer: Find the perfect specialist for your task.

        """
        ),
        reply_markup=menu_frep(message.from_user.id),
    )

# FSM состояния
class RegisterStates(StatesGroup):
    user_rlname = State()
    user_surname = State()
    user_number = State()


@router.message(F.text.in_(("🧑🏻‍💻 I am a performer")))
async def enter_registr(message: Message, state: FSMContext):
    # Проверяем, существует ли пользователь в базе
    user = Userx.get(user_id=message.from_user.id)
    if user:  # Если пользователь существует
        if user.user_number == 0:  # Если имя еще не указано
            # Убираем инлайн-кнопки и начинаем регистрацию
            await message.answer(
                "📝It looks like you are not registered yet. Enter your name:",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await state.set_state(RegisterStates.user_rlname)
        else:
            # Если пользователь уже зарегистрирован
            await message.answer(
                f"Добро пожаловать обратно, {user.user_rlname}!",
                reply_markup=menu_second_start(message.from_user.id)
            )
    else:
        # Если пользователя нет в базе, начинаем регистрацию
        await message.answer(
            "📝 Введите свое имя:",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(RegisterStates.user_rlname)


@router.message(RegisterStates.user_rlname)
async def set_name(message: Message, state: FSMContext):
    # Сохраняем имя
    await state.update_data(user_rlname=message.text)

    await message.answer(
        "📝 Enter your last name:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RegisterStates.user_surname)


@router.message(RegisterStates.user_surname)
async def set_surname(message: Message, state: FSMContext):
    # Сохраняем фамилию
    await state.update_data(user_surname=message.text)

    await message.answer(
        "📝 Enter your phone number:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RegisterStates.user_number)


@router.message(RegisterStates.user_number)
async def set_phone(message: Message, state: FSMContext):
    phone = message.text

    # Проверяем формат телефона
    if not phone.startswith("+") or not phone[1:].isdigit():
        await message.answer(
            "❌ Пожалуйста, введите корректный номер телефона в формате +123456789:",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return

    # Сохраняем телефон
    await state.update_data(user_number=phone)

    # Получаем данные из FSM
    data = await state.get_data()
    user_rlname = data["user_rlname"]
    user_surname = data["user_surname"]
    user_number = data["user_number"]

    # Добавляем пользователя в базу
    Userx.update(
        user_id=message.from_user.id,
        user_login=message.from_user.username or "unknown",
        user_name=message.from_user.first_name or "unknown",
        user_rlname=user_rlname,
        user_surname=user_surname,
        user_number=user_number,
    )

    # Завершаем FSM
    await state.clear()

    # Отправляем приветственное сообщение и меню
    await message.answer(
        ded(
            f"""
            ✅ Registration completed!
            Your name: {user_rlname}
            Your last name: {user_surname}
            Your phone number: {user_number}
            """
        ),
        reply_markup=menu_second_start(message.from_user.id),
    )

class RegisterStatesClients(StatesGroup):
    client_rlname = State()
    client_surname = State()
    client_number = State()


@router.message(F.text.in_(("🔎 I am the customer")))
async def enter_registr(message: Message, state: FSMContext):
    client = Clientx.get(client_id=message.from_user.id)
    if client:  # Если пользователь существует
        if client.client_number == 0:  # Если имя еще не указано
            # Убираем инлайн-кнопки и начинаем регистрацию
            await message.answer(
                "📝It looks like you are not registered yet. Enter your name:",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await state.set_state(RegisterStatesClients.client_rlname)
        else:
            # Если пользователь уже зарегистрирован
            await message.answer(
                f"Добро пожаловать обратно, {client.client_rlname}!",
                reply_markup=menu_second_start_clients(message.from_user.id)
            )
    else:
        # Если пользователя нет в базе, начинаем регистрацию
        await message.answer(
            "📝 Введите свое имя:",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(RegisterStatesClients.client_rlname)


@router.message(RegisterStatesClients.client_rlname)
async def set_name(message: Message, state: FSMContext):
    # Сохраняем имя
    await state.update_data(client_rlname=message.text)

    await message.answer(
        "📝 Enter your last name:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RegisterStatesClients.client_surname)


@router.message(RegisterStatesClients.client_surname)
async def set_surname(message: Message, state: FSMContext):
    # Сохраняем фамилию
    await state.update_data(client_surname=message.text)

    await message.answer(
        "📝 Enter your phone number:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(RegisterStatesClients.client_number)


@router.message(RegisterStatesClients.client_number)
async def set_phone(message: Message, state: FSMContext):
    phone = message.text

    # Проверяем формат телефона
    if not phone.startswith("+") or not phone[1:].isdigit():
        await message.answer(
            "❌ Пожалуйста, введите корректный номер телефона в формате +123456789:",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return

    # Сохраняем телефон
    await state.update_data(client_number=phone)

    # Получаем данные из FSM
    data = await state.get_data()
    client_rlname = data["client_rlname"]
    client_surname = data["client_surname"]
    client_number = data["client_number"]

    # Добавляем пользователя в базу
    Clientx.update(
        client_id=message.from_user.id,
        client_login=message.from_user.username or "unknown",
        client_name=message.from_user.first_name or "unknown",
        client_rlname=client_rlname,
        client_surname=client_surname,
        client_number=client_number,
    )

    # Завершаем FSM
    await state.clear()

    # Отправляем приветственное сообщение и меню
    await message.answer(
        ded(
            f"""
            ✅ Registration completed!
            Your name: {client_rlname}
            Your last name: {client_surname}
            Your phone number: {client_number}
            """
        ),reply_markup=menu_second_start_clients(message.from_user.id),
    )