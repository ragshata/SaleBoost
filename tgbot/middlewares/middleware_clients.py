# - *- coding: utf- 8 - *-
from aiogram import BaseMiddleware
from aiogram.types import User

from tgbot.database.db_users import Clientx
from tgbot.routers.main_start import enter_registr
from tgbot.utils.const_functions import clear_html

   
class ExistsClientMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        this_user: User = data.get("event_from_user")

        if not this_user.is_bot:
            get_client = Clientx.get(client_id=this_user.id)

            client_id = this_user.id
            client_login = this_user.username
            client_name = clear_html(this_user.full_name)

            if client_name is None: client_name = ""

            if get_client is None:
                Clientx.add(client_id, client_login.lower(), client_name, client_rlname="0", client_surname="0", client_number=0) 
            else:
                if client_name != get_client.client_name:
                    Clientx.update(get_client.client_id, client_name=client_name)

                if client_login.lower() != get_client.client_login:
                    Clientx.update(get_client.client_id, client_login=client_login.lower())

        return await handler(event, data)

