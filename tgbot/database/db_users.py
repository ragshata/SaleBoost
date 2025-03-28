# - *- coding: utf- 8 - *-
import sqlite3

from pydantic import BaseModel

from tgbot.data.config import PATH_DATABASE
from tgbot.database.db_helper import dict_factory, update_format_where, update_format
from tgbot.utils.const_functions import get_unix, ded


# Модель таблицы
class UserModel(BaseModel):
    increment: int
    user_id: int
    user_login: str
    user_name: str
    user_balance: float
    user_refill: float
    user_give: float
    user_unix: int
    user_rlname: str
    user_surname: str
    user_number: int
    user_rating_avg: float


# Работа с юзером
class Userx:
    storage_name = "storage_users"

    # Добавление записи
    @staticmethod
    def add(
        user_id: int,
        user_login: str,
        user_name: str,
        user_rlname: str,
        user_surname: str,
        user_number: int,
    ):
        user_balance = 0
        user_refill = 0
        user_give = 0
        user_unix = get_unix()
        user_rating_avg = 0.0

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(
                    f"""
                    INSERT INTO {Userx.storage_name} (
                        user_id,
                        user_login,
                        user_name,
                        user_balance,
                        user_refill,
                        user_give,
                        user_unix,
                        user_rlname,
                        user_surname,
                        user_number,
                        user_rating_avg
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                ),
                [
                    user_id,
                    user_login,
                    user_name,
                    user_balance,
                    user_refill,
                    user_give,
                    user_unix,
                    user_rlname,
                    user_surname,
                    user_number,
                    user_rating_avg,
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> UserModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Userx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = UserModel(**response)

            return response

    # Получение записей
    @staticmethod
    def gets(**kwargs) -> list[UserModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Userx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [UserModel(**cache_object) for cache_object in response]

            return response

    # Получение всех записей
    @staticmethod
    def get_all() -> list[UserModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Userx.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [UserModel(**cache_object) for cache_object in response]

            return response

    # Редактирование записи
    @staticmethod
    def update(user_id, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Userx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(user_id)

            con.execute(sql + "WHERE user_id = ?", parameters)

    # Удаление записи
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Userx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Очистка всех записей
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Userx.storage_name}"

            con.execute(sql)

    # Метод для обновления средней оценки
    # Метод для обновления средней оценки
    @staticmethod
    def update_rating(user_id: int, new_rating: float):
        user = Userx.get(user_id=user_id)
        if user is None:
            raise ValueError("Пользователь (worker_id) не найден")

        # Получение текущей средней оценки
        current_avg = user.user_rating_avg if user.user_rating_avg else 0.0

        # Расчёт новой средней оценки
        new_avg = (current_avg + new_rating) / 2

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = (
                f"UPDATE {Userx.storage_name} SET user_rating_avg = ? WHERE user_id = ?"
            )
            con.execute(sql, [new_avg, user_id])


# Модель таблицы
class ClientModel(BaseModel):
    increment: int
    client_id: int
    client_login: str
    client_name: str
    client_balance: float
    client_refill: float
    client_give: float
    client_unix: int
    client_rlname: str
    client_surname: str
    client_number: int


# Работа с юзером-заказчиком
class Clientx:
    storage_name = "storage_clients"

    # Добавление записи
    @staticmethod
    def add(
        client_id: int,
        client_login: str,
        client_name: str,
        client_rlname: str,
        client_surname: str,
        client_number: int,
    ):
        client_balance = 0
        client_refill = 0
        client_give = 0
        client_unix = get_unix()

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(
                    f"""
                    INSERT INTO {Clientx.storage_name} (
                        client_id,
                        client_login,
                        client_name,
                        client_balance,
                        client_refill,
                        client_give,
                        client_unix,
                        client_rlname,
                        client_surname,
                        client_number
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                ),
                [
                    client_id,
                    client_login,
                    client_name,
                    client_balance,
                    client_refill,
                    client_give,
                    client_unix,
                    client_rlname,
                    client_surname,
                    client_number,
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> ClientModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Clientx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = ClientModel(**response)

            return response

    # Получение записей
    @staticmethod
    def gets(**kwargs) -> list[ClientModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Clientx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [ClientModel(**cache_object) for cache_object in response]

            return response

    # Получение всех записей
    @staticmethod
    def get_all() -> list[ClientModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Clientx.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [ClientModel(**cache_object) for cache_object in response]

            return response

    # Редактирование записи
    @staticmethod
    def update(client_id, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Clientx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(client_id)

            con.execute(sql + "WHERE client_id = ?", parameters)

    # Удаление записи
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Clientx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Очистка всех записей
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Clientx.storage_name}"

            con.execute(sql)
