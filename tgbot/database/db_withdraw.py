# - *- coding: utf- 8 - *-
import sqlite3
from typing import Union

from pydantic import BaseModel

from tgbot.data.config import PATH_DATABASE
from tgbot.database.db_helper import dict_factory, update_format_where, update_format
from tgbot.utils.const_functions import get_unix, ded


# Модель таблицы
class WithdrawModel(BaseModel):
    increment: int
    user_id: int
    withdraw_comment: str
    withdraw_amount : float
    withdraw_details  : Union[str, int]
    withdraw_status : str
    withdraw_unix: int


# Работа с пополнениями
class Withdrawx:
    storage_name = "storage_withdraw"

    # Добавление записи
    @staticmethod
    def add(
            user_id: int,
            withdraw_comment: str,
            withdraw_amount : float,
            withdraw_details  : Union[str, int],
            withdraw_status : str,
    ):
        withdraw_unix = get_unix()

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(f"""
                    INSERT INTO {Withdrawx.storage_name} (
                        user_id,
                        withdraw_comment,
                        withdraw_amount,
                        withdraw_details,
                        withdraw_status,
                        withdraw_unix
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """),
                [
                    user_id,
                    withdraw_comment,
                    withdraw_amount ,
                    withdraw_details  ,
                    withdraw_status,
                    withdraw_unix,
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> WithdrawModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Withdrawx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = WithdrawModel(**response)

            return response

    # Получение записей
    @staticmethod
    def gets(**kwargs) -> list[WithdrawModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Withdrawx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [WithdrawModel(**cache_object) for cache_object in response]

            return response

    # Получение всех записей
    @staticmethod
    def get_all() -> list[WithdrawModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Withdrawx.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [WithdrawModel(**cache_object) for cache_object in response]

            return response

    # Редактирование записи
    @staticmethod
    def update(withdraw_details  , **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Withdrawx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(withdraw_details  )

            con.execute(sql + "WHERE withdraw_details   = ?", parameters)

    # Удаление записи
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Withdrawx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Очистка всех записей
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Withdrawx.storage_name}"

            con.execute(sql)
