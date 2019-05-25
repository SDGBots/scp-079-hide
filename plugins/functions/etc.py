# SCP-079-HIDE - Hide the real watcher
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
from json import dumps, loads
from random import uniform
from threading import Thread
from time import sleep
from typing import Callable, List

from pyrogram import Message
from pyrogram.errors import FloodWait

# Enable logging
logger = logging.getLogger(__name__)


def bold(text) -> str:
    # Get a bold text
    text = str(text)
    if text.strip():
        return f"**{text}**"

    return ""


def code(text) -> str:
    # Get a code text
    text = str(text)
    if text.strip():
        return f"`{text}`"

    return ""


def code_block(text) -> str:
    # Get a code block text
    text = str(text)
    if text.strip():
        return f"```{text}```"

    return ""


def format_data(sender: str, receivers: List[str], action: str, action_type: str, data=None) -> str:
    # See https://scp-079.org/exchange/
    data = {
        "from": sender,
        "to": receivers,
        "action": action,
        "type": action_type,
        "data": data
    }

    return code_block(dumps(data, indent=4))


def get_text(message: Message) -> str:
    # Get message's text
    text = ""
    try:
        if message.text or message.caption:
            if message.text:
                text += message.text
            else:
                text += message.caption
    except Exception as e:
        logger.warning(f"Get text error: {e}", exc_info=True)

    return text


def receive_data(message: Message) -> dict:
    # Receive data from exchange channel
    data = {}
    try:
        text = get_text(message)
        if text:
            data = loads(text)
    except Exception as e:
        logger.warning(f"Receive data error: {e}")

    return data


def thread(target: Callable, args: tuple) -> bool:
    # Call a function using thread
    t = Thread(target=target, args=args)
    t.daemon = True
    t.start()

    return True


def user_mention(uid: int) -> str:
    # Get a mention text
    return f"[{uid}](tg://user?id={uid})"


def wait_flood(e: FloodWait) -> bool:
    # Wait flood secs
    try:
        sleep(e.x + uniform(0.5, 1.0))
        return True
    except Exception as e:
        logger.warning(f"Wait flood error: {e}", exc_info=True)

    return False
