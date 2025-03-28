import requests
import uuid
from tgbot.data.config import SECRET_KEY, SHOP_ID

def create_payment(amount: float, user_id: int, email: str = None, phone: str = None) -> dict:
    url = "https://api.yookassa.ru/v3/payments"
    idempotence_key = str(uuid.uuid4())

    headers = {
        "Content-Type": "application/json",
        "Idempotence-Key": idempotence_key,
    }

    auth = (SHOP_ID, SECRET_KEY)

    data = {
        "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/ragshata_bot",
        },
        "capture": True,
        "description": f"Пополнение аккаунта пользователя {user_id}",
        "metadata": {"user_id": user_id},
        "receipt": {
            "customer": {
                "email": email,
                "phone": phone,
            },
            "items": [
                {
                    "description": "Пополнение аккаунта",  # Название услуги
                    "quantity": "1.00",                   # Количество
                    "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
                    "vat_code": 1,                        # Ставка НДС
                    "payment_subject": "payment",         # Тип: Платёж
                    "payment_mode": "full_payment",       # Режим расчёта: полный расчёт
                }
            ],
        },
    }

    response = requests.post(url, json=data, headers=headers, auth=auth)

    if response.status_code in [200, 201]:
        return response.json()
    else:
        print("Ошибка при создании платежа:", response.json())
        raise Exception(f"Ошибка при создании платежа: {response.json()}")



def create_payout(amount: float, user_id: int, card_number: str, description: str = "Выплата") -> dict:
    """
    Создаёт запрос на выплату через YooKassa.

    :param amount: Сумма выплаты
    :param user_id: ID пользователя
    :param card_number: Номер банковской карты
    :param description: Описание выплаты
    :return: Ответ API YooKassa
    """
    url = "https://api.yookassa.ru/v3/payouts"
    idempotence_key = str(uuid.uuid4())

    headers = {
        "Content-Type": "application/json",
        "Idempotence-Key": idempotence_key,
    }

    auth = (SHOP_ID, SECRET_KEY)

    data = {
        "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
        "payout_destination_data": {
            "type": "bank_card",
            "card": {"number": card_number}
        },
        "description": description,
        "metadata": {"user_id": user_id},
    }

    response = requests.post(url, json=data, headers=headers, auth=auth)

    if response.status_code in [200, 201]:
        return response.json()
    else:
        print("Ошибка при создании выплаты:", response.json())
        raise Exception(f"Ошибка при создании выплаты: {response.json()}")
