# - *- coding: utf- 8 - *-
import sqlite3
from typing import Union

from pydantic import BaseModel

from tgbot.data.config import PATH_DATABASE
from tgbot.database.db_helper import dict_factory, update_format_where, update_format
from tgbot.utils.const_functions import ded, get_unix


# Модель таблицы
class PurchasesModelClient(BaseModel):
    increment: int
    client_id: int
    client_balance_before: float
    client_balance_after: float
    purchase_receipt: Union[str, int]
    purchase_data: str
    purchase_price: float
    purchase_price_one: float
    purchase_position_id: int
    purchase_position_name: str
    purchase_category_id: int
    purchase_category_name: str
    purchase_unix: int


# Работа с категориями
class Purchasesclientx:
    storage_name = "storage_purchases_clients"

    # Добавление записи
    @staticmethod
    def add(
            client_id: int,
            client_balance_before: float,
            client_balance_after: float,
            purchase_receipt: Union[str, int],
            purchase_data: str,
            purchase_price: float,
            purchase_price_one: float,
            purchase_position_id: int,
            purchase_position_name: str,
            purchase_category_id: int,
            purchase_category_name: str,
    ):
        purchase_unix = get_unix()

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(f"""
                    INSERT INTO {Purchasesclientx.storage_name} (
                        client_id,
                        client_balance_before,
                        client_balance_after,
                        purchase_receipt,
                        purchase_data,
                        purchase_price,
                        purchase_price_one,
                        purchase_position_id,
                        purchase_position_name,
                        purchase_category_id,
                        purchase_category_name,
                        purchase_unix
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """),
                [
                    client_id,
                    client_balance_before,
                    client_balance_after,
                    purchase_receipt,
                    purchase_data,
                    purchase_price,
                    purchase_price_one,
                    purchase_position_id,
                    purchase_position_name,
                    purchase_category_id,
                    purchase_category_name,
                    purchase_unix,
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> PurchasesModelClient:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Purchasesclientx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = PurchasesModelClient(**response)

            return response

    # Получение записей
    @staticmethod
    def gets(**kwargs) -> list[PurchasesModelClient]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Purchasesclientx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [PurchasesModelClient(**cache_object) for cache_object in response]

            return response

    # Получение всех записей
    @staticmethod
    def get_all() -> list[PurchasesModelClient]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Purchasesclientx.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [PurchasesModelClient(**cache_object) for cache_object in response]

            return response

    # Редактирование записи
    @staticmethod
    def update(purchase_receipt, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Purchasesclientx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(purchase_receipt)

            con.execute(sql + "WHERE purchase_receipt = ?", parameters)

    # Удаление записи
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Purchasesclientx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Очистка всех записей
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Purchasesclientx.storage_name}"

            con.execute(sql)