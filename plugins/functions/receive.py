# SCP-079-HIDE - Hide the real sender
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-HIDE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from json import loads

from pyrogram import Client, Message

from .. import glovar
from .etc import bold, code, get_text, thread, user_mention
from .telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


def receive_text_data(message: Message) -> dict:
    # Receive text's data from exchange channel
    data = {}
    try:
        text = get_text(message)
        if text:
            data = loads(text)
    except Exception as e:
        logger.warning(f"Receive data error: {e}")

    return data


def receive_version_reply(client: Client, sender: str, data: dict) -> bool:
    # Receive version reply
    try:
        aid = data["admin_id"]
        mid = data["message_id"]
        version = data["version"]
        text = (f"管理员：{user_mention(aid)}\n\n"
                f"发送者：{code(sender)}\n"
                f"版本：{bold(version)}\n")
        thread(send_message, (client, glovar.test_group_id, text, mid))

        return True
    except Exception as e:
        logger.warning(f"Receive version reply error: {e}", exc_info=True)

    return False
