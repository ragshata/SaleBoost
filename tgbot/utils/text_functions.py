# - *- coding: utf- 8 - *-
from typing import Union

from aiogram import Bot

from tgbot.database.db_category import Categoryx
from tgbot.database.db_item import Itemx
from tgbot.database.db_position import Positionx
from tgbot.database.db_purchases import Purchasesx, PurchasesModel
from tgbot.database.db_purchases_clients import Purchasesclientx
from tgbot.database.db_refill import Refillx, RefillModel
from tgbot.database.db_settings import Settingsx
from tgbot.database.db_users import ClientModel, Clientx, Userx, UserModel
from tgbot.keyboards.inline_admin import profile_search_finl, profile_search_finl_client
from tgbot.keyboards.inline_admin_prod import (
    position_edit_open_finl,
    category_edit_open_finl,
    item_delete_finl,
    user_position_edit_open_finl,
)
from tgbot.keyboards.inline_user import (
    client_profile_finl,
    products_open_finl,
    user_profile_finl,
)
from tgbot.utils.const_functions import ded, get_unix, convert_day, convert_date
from tgbot.utils.misc.bot_models import ARS


################################################################################
################################# ПОЛЬЗОВАТЕЛЬ #################################
# Открытие профиля пользователем
async def open_profile_user(bot: Bot, user_id: Union[int, str]):
    get_purchases = Purchasesx.gets(user_id=user_id)
    get_user = Userx.get(user_id=user_id)

    how_days = int(get_unix() - get_user.user_unix) // 60 // 60 // 24

    # Получение средней оценки пользователя
    user_rating = (
        round(get_user.user_rating_avg, 2) if get_user.user_rating_avg else "Нет оценок"
    )

    send_text = ded(
        f"""
        <b>👤 Ваш профиль:</b>
        ➖➖➖➖➖➖➖➖➖➖
        🆔 <code>{get_user.user_rlname}</code> <code>{get_user.user_surname}</code>
        💰 Баланс: <code>{get_user.user_balance}₽</code>
        ⭐ Средняя оценка: <code>{user_rating}</code>

        🕰 Регистрация: <code>{convert_date(get_user.user_unix, False, False)} ({convert_day(how_days)})</code>
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
        reply_markup=user_profile_finl(),
    )


# Открытие профиля клиентом
async def open_profile_client(bot: Bot, user_id: Union[int, str]):
    get_purchases = Purchasesclientx.gets(client_id=user_id)
    get_client = Clientx.get(client_id=user_id)

    how_days = int(get_unix() - get_client.client_unix) // 60 // 60 // 24
    #!count_items = sum([purchase.purchase_count for purchase in get_purchases])
    #!🧑🏻‍💻 Дано заказов: <code>{count_items}шт</code>
    send_text = ded(
        f"""
        <b>👤 Ваш профиль:</b>
        ➖➖➖➖➖➖➖➖➖➖
        🆔 <code>{get_client.client_rlname}</code> <code>{get_client.client_surname}</code>
        💰 Баланс: <code>{get_client.client_balance}₽</code>

        🕰 Регистрация: <code>{convert_date(get_client.client_unix, False, False)} ({convert_day(how_days)})</code>
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
        reply_markup=client_profile_finl(),
    )


# Открытие позиции пользователем
async def position_open_user(
    bot: Bot, user_id: int, position_id: Union[str, int], position_unix
):
    get_items = Itemx.gets(position_id=position_id)
    get_position = Positionx.get(position_unix=position_unix)
    get_category = Categoryx.get(category_id=get_position.category_id)

    if get_position.position_desc != "None":
        text_desc = f"\n▪️ Описание: {get_position.position_desc}"
    else:
        text_desc = ""

    send_text = ded(
        f"""
        <b>🧑🏻‍💻 Выполнение заказа:</b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ Название: <code>{get_position.position_name}</code>
        ▪️ Категория: <code>{get_category.category_name}</code>
        ▪️ Время на выполнение: <code>{get_position.position_time}ч</code>
        ▪️ Стоимость: <code>{get_position.position_price}₽</code>
        {text_desc}
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
        reply_markup=products_open_finl(
            position_id, get_position.category_id, get_position.position_unix
        ),
    )


################################################################################
#################################### АДМИН #####################################
# Открытие профиля админом
async def open_profile_admin(bot: Bot, user_id: int, get_user: UserModel):
    get_purchases = Purchasesx.gets(user_id=get_user.user_id)

    how_days = int(get_unix() - get_user.user_unix) // 60 // 60 // 24
    #!count_items = sum([purchase.purchase_count for purchase in get_purchases])
    #!▪️ Выполнено заказов: <code>{count_items}шт</code>

    send_text = ded(
        f"""
        <b>👤 Профиль пользователя: <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a></b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ ID: <code>{get_user.user_id}</code>
        ▪️ Логин: <b>@{get_user.user_login}</b>
        ▪️ Имя: <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>
        ▪️ Регистрация: <code>{convert_date(get_user.user_unix, False, False)} ({convert_day(how_days)})</code>

        ▪️ Баланс: <code>{get_user.user_balance}₽</code>
        ▪️ Всего выдано: <code>{get_user.user_give}₽</code>
        ▪️ Всего пополнено: <code>{get_user.user_refill}₽</code>
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
        reply_markup=profile_search_finl(get_user.user_id),
    )


async def open_profile_admin_client(bot: Bot, user_id: int, get_user: ClientModel):
    get_purchases = Purchasesclientx.gets(client_id=get_user.client_id)

    how_days = int(get_unix() - get_user.client_unix) // 60 // 60 // 24
    #!count_items = sum([purchase.purchase_count for purchase in get_purchases])
    #!▪️ Выполнено заказов: <code>{count_items}шт</code>

    send_text = ded(
        f"""
        <b>👤 Профиль пользователя: <a href='tg://user?id={get_user.client_id}'>{get_user.client_name}</a></b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ ID: <code>{get_user.client_id}</code>
        ▪️ Логин: <b>@{get_user.client_login}</b>
        ▪️ Имя: <a href='tg://user?id={get_user.client_id}'>{get_user.client_name}</a>
        ▪️ Регистрация: <code>{convert_date(get_user.client_unix, False, False)} ({convert_day(how_days)})</code>

        ▪️ Баланс: <code>{get_user.client_balance}₽</code>
        ▪️ Всего выдано: <code>{get_user.client_give}₽</code>
        ▪️ Всего пополнено: <code>{get_user.client_refill}₽</code>
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
        reply_markup=profile_search_finl_client(get_user.client_id),
    )


# Открытие пополнения админом
async def refill_open_admin(bot: Bot, user_id: int, get_refill: RefillModel):
    get_user = Userx.get(user_id=get_refill.user_id)

    if get_refill.refill_method == "Yoomoney":
        pay_way = "Юkassa 🔮"
    else:
        pay_way = f"{get_refill.refill_method}"

    send_text = ded(
        f"""
        <b>🧾 Чек: <code>#{get_refill.refill_receipt}</code></b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ Пользователь: <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a> | <code>{get_user.user_id}</code>
        ▪️ Сумма пополнения: <code>{get_refill.refill_amount}₽</code>
        ▪️ Способ пополнения: <code>{pay_way}</code>
        ▪️ Комментарий: <code>{get_refill.refill_comment}</code>
        ▪️ Дата пополнения: <code>{convert_date(get_refill.refill_unix)}</code>
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
    )


# Открытие пополнения админом
async def refill_open_admin_client(bot: Bot, user_id: int, get_refill: RefillModel):
    get_user = Clientx.get(user_id=get_refill.user_id)

    if get_refill.refill_method == "Yoomoney":
        pay_way = "Юkassa 🔮"
    else:
        pay_way = f"{get_refill.refill_method}"

    send_text = ded(
        f"""
        <b>🧾 Чек: <code>#{get_refill.refill_receipt}</code></b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ Пользователь: <a href='tg://user?id={get_user.client_id}'>{get_user.client_name}</a> | <code>{get_user.client_id}</code>
        ▪️ Сумма пополнения: <code>{get_refill.refill_amount}₽</code>
        ▪️ Способ пополнения: <code>{pay_way}</code>
        ▪️ Комментарий: <code>{get_refill.refill_comment}</code>
        ▪️ Дата пополнения: <code>{convert_date(get_refill.refill_unix)}</code>
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
    )


# Открытие Заказы админом
async def purchase_open_admin(
    bot: Bot, arSession: ARS, user_id: int, get_purchase: PurchasesModel
):
    from tgbot.utils.misc_functions import upload_text

    get_user = Userx.get(user_id=get_purchase.user_id)

    link_items = await upload_text(arSession, get_purchase.purchase_data)

    # ▪️ Выполнено заказов: <code>{get_purchase.purchase_count}шт</code>

    send_text = ded(
        f"""
        <b>🧾 Чек: <code>#{get_purchase.purchase_receipt}</code></b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ Пользователь: <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a> | <code>{get_user.user_id}</code>
        ▪️ Название заказа: <code>{get_purchase.purchase_position_name}</code>
        ▪️ Цена заказа: <code>{get_purchase.purchase_price_one}₽</code>
        ▪️ Баланс до Заказы: <code>{get_purchase.user_balance_before}₽</code>
        ▪️ Баланс после Заказы: <code>{get_purchase.user_balance_after}₽</code>
        ▪️ Дата Заказы: <code>{convert_date(get_purchase.purchase_unix)}</code>
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
    )


# Открытие Заказы админом
async def purchase_open_admin(
    bot: Bot, arSession: ARS, user_id: int, get_purchase: PurchasesModel
):
    from tgbot.utils.misc_functions import upload_text

    get_user = Userx.get(user_id=get_purchase.user_id)

    link_items = await upload_text(arSession, get_purchase.purchase_data)

    # ▪️ Выполнено заказов: <code>{get_purchase.purchase_count}шт</code>

    send_text = ded(
        f"""
        <b>🧾 Чек: <code>#{get_purchase.purchase_receipt}</code></b>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ Пользователь: <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a> | <code>{get_user.user_id}</code>
        ▪️ Название заказа: <code>{get_purchase.purchase_position_name}</code>
        ▪️ Цена заказа: <code>{get_purchase.purchase_price_one}₽</code>
        ▪️ Баланс до Заказы: <code>{get_purchase.user_balance_before}₽</code>
        ▪️ Баланс после Заказы: <code>{get_purchase.user_balance_after}₽</code>
        ▪️ Дата Заказы: <code>{convert_date(get_purchase.purchase_unix)}</code>
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
    )


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


# Открытие позиции админом
async def position_open_admin(
    bot: Bot, user_id: int, position_id: Union[str, int], position_unix
):
    get_items = Itemx.gets(position_id=position_id)
    get_position = Positionx.get(position_unix=position_unix)
    get_category = Categoryx.get(category_id=get_position.category_id)

    get_purchases = Purchasesx.gets(purchase_position_id=position_id)
    get_settings = Settingsx.get()

    profit_amount_all, profit_amount_day, profit_amount_week, profit_amount_month = (
        0,
        0,
        0,
        0,
    )
    profit_count_all, profit_count_day, profit_count_week, profit_count_month = (
        0,
        0,
        0,
        0,
    )

    position_desc = "<code>Отсутствует ❌</code>"

    if get_position.position_desc != "None":
        position_desc = f"{get_position.position_desc}"

    for purchase in get_purchases:
        profit_amount_all += purchase.purchase_price

        if purchase.purchase_unix - get_settings.misc_profit_day >= 0:
            profit_amount_day += purchase.purchase_price
        if purchase.purchase_unix - get_settings.misc_profit_week >= 0:
            profit_amount_week += purchase.purchase_price
        if purchase.purchase_unix - get_settings.misc_profit_month >= 0:
            profit_amount_month += purchase.purchase_price

    send_text = ded(
        f"""
        <b>📁 Редактирование заказа</b>
        ➖➖➖➖➖➖➖➖➖➖➖➖➖➖
        ▪️ Заказ: <code>{get_position.position_name}</code>
        ▪️ Категория: <code>{get_category.category_name}</code>
        ▪️ Стоимость: <code>{get_position.position_price}₽</code>
        ▪️ Дата создания: <code>{convert_date(get_category.category_unix)}</code>
        ▪️ Срок: {get_position.position_time} часов
        ▪️ Описание: {position_desc}
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
        reply_markup=position_edit_open_finl(position_id, get_position.category_id, 0, position_unix),
    )


# Открытие позиции userom
async def position_open_not_admin_user(
    bot: Bot, user_id: int, position_id: Union[str, int], position_unix
):
    get_items = Itemx.gets(position_id=position_id)
    get_position = Positionx.get(position_unix=position_unix)
    get_category = Categoryx.get(category_id=get_position.category_id)

    get_purchases = Purchasesx.gets(purchase_position_id=position_id)
    get_settings = Settingsx.get()

    profit_amount_all, profit_amount_day, profit_amount_week, profit_amount_month = (
        0,
        0,
        0,
        0,
    )
    profit_count_all, profit_count_day, profit_count_week, profit_count_month = (
        0,
        0,
        0,
        0,
    )

    position_desc = "<code>Отсутствует ❌</code>"

    if get_position.position_desc != "None":
        position_desc = f"{get_position.position_desc}"

    for purchase in get_purchases:
        profit_amount_all += purchase.purchase_price

        if purchase.purchase_unix - get_settings.misc_profit_day >= 0:
            profit_amount_day += purchase.purchase_price
        if purchase.purchase_unix - get_settings.misc_profit_week >= 0:
            profit_amount_week += purchase.purchase_price
        if purchase.purchase_unix - get_settings.misc_profit_month >= 0:
            profit_amount_month += purchase.purchase_price

    send_text = ded(
        f"""
        <b>📁 Заказ</b>
        ➖➖➖➖➖➖➖➖➖➖➖➖➖➖
        ▪️ Заказ: <code>{get_position.position_name}</code>
        ▪️ Категория: <code>{get_category.category_name}</code>
        ▪️ Стоимость: <code>{get_position.position_price}₽</code>
        ▪️ Дата создания: <code>{convert_date(get_category.category_unix)}</code>
        ▪️ Срок: {get_position.position_time} часов
        ▪️ Описание: {position_desc}
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
        reply_markup=user_position_edit_open_finl(
            position_id, get_position.category_id, 0, get_position.position_unix
        ),
    )


# Открытие товара админом
async def item_open_admin(
    bot: Bot, user_id: int, item_id: Union[str, int], remover: int
):
    get_item = Itemx.get(item_id=item_id)

    get_position = Positionx.get(position_id=get_item.position_id)
    get_category = Categoryx.get(category_id=get_item.category_id)

    send_text = ded(
        f"""
        <b>🧑🏻‍💻️ Редактирование заказа</b>
        ➖➖➖➖➖➖➖➖➖➖➖➖➖➖
        ▪️ Категория: <code>{get_category.category_name}</code>
        ▪️ Заказ: <code>{get_position.position_name}</code>
        ▪️ Дата добавления: <code>{convert_date(get_item.item_unix)}</code>
    """
    )

    await bot.send_message(
        chat_id=user_id,
        text=send_text,
        reply_markup=item_delete_finl(
            get_item.item_id, get_item.position_id, get_item.category_id
        ),
    )


# Статистика бота
def get_statistics() -> str:
    refill_amount_all, refill_amount_day, refill_amount_week, refill_amount_month = (
        0,
        0,
        0,
        0,
    )
    refill_count_all, refill_count_day, refill_count_week, refill_count_month = (
        0,
        0,
        0,
        0,
    )
    profit_amount_all, profit_amount_day, profit_amount_week, profit_amount_month = (
        0,
        0,
        0,
        0,
    )
    profit_count_all, profit_count_day, profit_count_week, profit_count_month = (
        0,
        0,
        0,
        0,
    )
    (
        users_all,
        users_day,
        users_week,
        users_month,
        users_money_have,
        users_money_give,
    ) = (0, 0, 0, 0, 0, 0)

    get_categories = Categoryx.get_all()
    get_positions = Positionx.get_all()
    get_purchases = Purchasesx.get_all()
    get_refill = Refillx.get_all()
    get_items = Itemx.get_all()
    get_users = Userx.get_all()

    get_settings = Settingsx.get()

    for purchase in get_purchases:
        profit_amount_all += purchase.purchase_price

        if purchase.purchase_unix - get_settings.misc_profit_day >= 0:
            profit_amount_day += purchase.purchase_price
        if purchase.purchase_unix - get_settings.misc_profit_week >= 0:
            profit_amount_week += purchase.purchase_price
        if purchase.purchase_unix - get_settings.misc_profit_month >= 0:
            profit_amount_month += purchase.purchase_price

    for refill in get_refill:
        refill_amount_all += refill.refill_amount
        refill_count_all += 1

        if refill.refill_unix - get_settings.misc_profit_day >= 0:
            refill_amount_day += refill.refill_amount
            refill_count_day += 1
        if refill.refill_unix - get_settings.misc_profit_week >= 0:
            refill_amount_week += refill.refill_amount
            refill_count_week += 1
        if refill.refill_unix - get_settings.misc_profit_month >= 0:
            refill_amount_month += refill.refill_amount
            refill_count_month += 1

    for user in get_users:
        users_money_have += user.user_balance
        users_money_give += user.user_give
        users_all += 1

        if user.user_unix - get_settings.misc_profit_day >= 0:
            users_day += 1
        if user.user_unix - get_settings.misc_profit_week >= 0:
            users_week += 1
        if user.user_unix - get_settings.misc_profit_month >= 0:
            users_month += 1

    return ded(
        f"""
        <b>📊 СТАТИСТИКА БОТА</b>
        ➖➖➖➖➖➖➖➖➖➖
        <b>👤 Пользователи</b>
        ┣ Юзеров за День: <code>{users_day}</code>
        ┣ Юзеров за Неделю: <code>{users_week}</code>
        ┣ Юзеров за Месяц: <code>{users_month}</code>
        ┗ Юзеров за Всё время: <code>{users_all}</code>

        <b>💰 Средства</b>
        ┣‒ Заказы (кол-во, сумма)
        ┣ За День: <code>{profit_count_day}шт</code> - <code>{profit_amount_day}₽</code>
        ┣ За Неделю: <code>{profit_count_week}шт</code> - <code>{profit_amount_week}₽</code>
        ┣ За Месяц: <code>{profit_count_month}шт</code> - <code>{profit_amount_month}₽</code>
        ┣ За Всё время: <code>{profit_count_all}шт</code> - <code>{profit_amount_all}₽</code>
        ┃
        ┣‒ Пополнения (кол-во, сумма)
        ┣ За День: <code>{refill_count_day}шт</code> - <code>{refill_amount_day}₽</code>
        ┣ За Неделю: <code>{refill_count_week}шт</code> - <code>{refill_amount_week}₽</code>
        ┣ За Месяц: <code>{refill_count_month}шт</code> - <code>{refill_amount_month}₽</code>
        ┣ За Всё время: <code>{refill_count_all}шт</code> - <code>{refill_amount_all}₽</code>
        ┃
        ┣‒ Прочее
        ┣ Средств выдано: <code>{users_money_give}₽</code>
        ┗ Средств в системе: <code>{users_money_have}₽</code>

        <b>🧑🏻‍💻 Заказы</b>
        ┣ Позиций: <code>{len(get_positions)}шт</code>
        ┗ Категорий: <code>{len(get_categories)}шт</code>
   """
    )
