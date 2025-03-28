# - *- coding: utf- 8 - *-
import sqlite3

from pydantic import BaseModel
from typing import Union

from tgbot.data.config import PATH_DATABASE
from tgbot.database.db_helper import dict_factory, update_format_where, update_format
from tgbot.utils.const_functions import ded, get_unix


# Модель таблицы
class PositionModel(BaseModel):
    increment: int
    category_id: int
    position_id: int
    position_name: str
    position_price: float
    position_desc: str
    position_time: float
    worker_id: int
    position_status: int
    position_unix: int


# Работа с категориями
class Positionx:
    storage_name = "storage_position"

    # Добавление записи
    @staticmethod
    def add(
        category_id: int,
        position_id: int,
        position_name: str,
        position_price: float,
        position_desc: str,
        position_time: float,
        worker_id: int,
        position_status: int,
    ):
        position_unix = get_unix()

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(
                    f"""
                    INSERT INTO {Positionx.storage_name} (
                        position_id,
                        position_name,
                        position_price,
                        position_desc,
                        position_time,
                        worker_id,
                        position_status,
                        position_unix,
                        category_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                ),
                [
                    position_id,
                    position_name,
                    position_price,
                    position_desc,
                    position_time,
                    worker_id,
                    position_status,
                    position_unix,
                    category_id,
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> PositionModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Positionx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = PositionModel(**response)

            return response

    # Получение worker_id
    @staticmethod
    def get_worker_id(**kwargs) -> Union[int, None]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT worker_id FROM {Positionx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                return response.get("worker_id")

            return None

    @staticmethod
    def count_by_category(category_id: int) -> int:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT COUNT(*) as count FROM {Positionx.storage_name} WHERE category_id = ?"
            result = con.execute(sql, (category_id,)).fetchone()
            return result["count"] if result else 0

    @staticmethod
    def update_unix(position_unix: int, **kwargs):
        """
        Обновление записи в таблице на основе значения position_unix.

        :param position_unix: Значение поля position_unix (идентификатор записи).
        :param kwargs: Поля и их значения для обновления.
        """
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Positionx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(position_unix)

            con.execute(sql + " WHERE position_unix = ?", parameters)

    @staticmethod
    def gets(**kwargs) -> list[PositionModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            # Проверяем, указан ли фильтр по position_id
            sql = f"SELECT * FROM {Positionx.storage_name}"
            if "position_id" in kwargs:
                sql += " WHERE position_id = :position_id"
                parameters = {"position_id": kwargs["position_id"]}
            else:
                sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [PositionModel(**cache_object) for cache_object in response]

            return response

    @staticmethod
    def get_by_id_and_status(
        position_id: int, position_status: int
    ) -> list[PositionModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            # Формируем SQL-запрос
            sql = f"""
                SELECT * FROM {Positionx.storage_name}
                WHERE position_id = ? AND position_status = ?
            """

            # Выполняем запрос с параметрами
            response = con.execute(sql, (position_id, position_status)).fetchall()

            # Преобразуем результат в список моделей
            if len(response) >= 1:
                response = [PositionModel(**cache_object) for cache_object in response]

            return response

    # Получение всех записей
    @staticmethod
    def get_all() -> list[PositionModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Positionx.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [PositionModel(**cache_object) for cache_object in response]

            return response

    @staticmethod
    def get_position_ids(**kwargs) -> list[int]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = lambda cursor, row: row[0]  # (position_id)
            sql = f"SELECT position_id FROM {Positionx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()
            return response if response else None

    # Редактирование записи
    @staticmethod
    def update(position_id, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Positionx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(position_id)

            con.execute(sql + "WHERE position_id = ?", parameters)

    @staticmethod
    def update_gpt(field_name: str, field_value, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Positionx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(field_value)

            con.execute(sql + f" WHERE {field_name} = ?", parameters)

    # Удаление записи
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Positionx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Очистка всех записей
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Positionx.storage_name}"

            con.execute(sql)
