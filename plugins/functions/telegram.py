# SCP-079-HIDE - Hide the real sender
# Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>
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
from typing import Iterable, List, Optional, Union

from pyrogram import Client, InlineKeyboardMarkup, Message
from pyrogram.errors import ChatAdminRequired, ButtonDataInvalid, ButtonUrlInvalid, ChannelInvalid, ChannelPrivate
from pyrogram.errors import FloodWait, MessageDeleteForbidden, PeerIdInvalid

from .etc import delay, wait_flood
from .decorators import retry

# Enable logging
logger = logging.getLogger(__name__)


def delete_messages(client: Client, cid: int, mids: Iterable[int]) -> Optional[bool]:
    # Delete some messages
    result = None

    try:
        mids = list(mids)

        if len(mids) <= 100:
            return delete_messages_100(client, cid, mids)

        mids_list = [mids[i:i + 100] for i in range(0, len(mids), 100)]
        result = bool([delete_messages_100(client, cid, mids) for mids in mids_list])
    except Exception as e:
        logger.warning(f"Delete messages in {cid} error: {e}", exc_info=True)

    return result


@retry
def delete_messages_100(client: Client, cid: int, mids: Iterable[int]) -> Optional[bool]:
    # Delete some messages
    result = None

    try:
        mids = list(mids)
        result = client.delete_messages(chat_id=cid, message_ids=mids)
    except FloodWait as e:
        raise e
    except MessageDeleteForbidden:
        return False
    except Exception as e:
        logger.warning(f"Delete messages in {cid} error: {e}", exc_info=True)

    return result


def download_media(client: Client, file_id: str, file_ref: str, file_path: str) -> Optional[str]:
    # Download a media file
    result = None
    try:
        flood_wait = True
        while flood_wait:
            flood_wait = False
            try:
                result = client.download_media(message=file_id, file_ref=file_ref, file_name=file_path)
            except FloodWait as e:
                flood_wait = True
                wait_flood(e)
    except Exception as e:
        logger.warning(f"Download media {file_id} to {file_path} error: {e}", exc_info=True)

    return result


def forward_messages(client: Client, cid: int, fid: int, mids: Iterable,
                     as_copy: bool = False) -> Union[List[Message], bool]:
    # Forward messages to a chat
    result = []
    try:
        flood_wait = True
        while flood_wait:
            flood_wait = False
            try:
                result = client.forward_messages(
                    chat_id=cid,
                    from_chat_id=fid,
                    message_ids=mids,
                    disable_notification=True,
                    as_copy=as_copy
                )
            except FloodWait as e:
                flood_wait = True
                wait_flood(e)
            except (PeerIdInvalid, ChannelInvalid, ChannelPrivate):
                return False
    except Exception as e:
        logger.warning(f"Forward messages {mids} from {fid} to {cid} error: {e}", exc_info=True)

    return result


def send_document(client: Client, cid: int, document: str, file_ref: str = None, caption: str = "", mid: int = None,
                  markup: InlineKeyboardMarkup = None) -> Union[bool, Message, None]:
    # Send a document to a chat
    result = None
    try:
        flood_wait = True
        while flood_wait:
            flood_wait = False
            try:
                result = client.send_document(
                    chat_id=cid,
                    document=document,
                    file_ref=file_ref,
                    caption=caption,
                    parse_mode="html",
                    reply_to_message_id=mid,
                    reply_markup=markup
                )
            except FloodWait as e:
                flood_wait = True
                wait_flood(e)
            except ButtonDataInvalid:
                logger.warning(f"Send document {document} to {cid} - invalid markup: {markup}")
            except (ChatAdminRequired, PeerIdInvalid, ChannelInvalid, ChannelPrivate):
                return False
    except Exception as e:
        logger.warning(f"Send document {document} to {cid} error: {e}", exec_info=True)

    return result


def send_message(client: Client, cid: int, text: str, mid: int = None,
                 markup: InlineKeyboardMarkup = None) -> Union[bool, Message, None]:
    # Send a message to a chat
    result = None
    try:
        if not text.strip():
            return None

        flood_wait = True
        while flood_wait:
            flood_wait = False
            try:
                result = client.send_message(
                    chat_id=cid,
                    text=text,
                    parse_mode="html",
                    disable_web_page_preview=True,
                    reply_to_message_id=mid,
                    reply_markup=markup
                )
            except FloodWait as e:
                flood_wait = True
                wait_flood(e)
            except ButtonDataInvalid:
                logger.warning(f"Send message to {cid} - invalid markup: {markup}")
            except (ChatAdminRequired, PeerIdInvalid, ChannelInvalid, ChannelPrivate):
                return False
    except Exception as e:
        logger.warning(f"Send message to {cid} error: {e}", exc_info=True)

    return result


@retry
def send_report_message(secs: int, client: Client, cid: int, text: str, mid: int = None,
                        markup: InlineKeyboardMarkup = None) -> Optional[bool]:
    # Send a message that will be auto deleted to a chat
    result = None

    try:
        if not text.strip():
            return None

        result = client.send_message(
            chat_id=cid,
            text=text,
            parse_mode="html",
            disable_web_page_preview=True,
            reply_to_message_id=mid,
            reply_markup=markup
        )

        if not result:
            return None

        mid = result.message_id
        mids = [mid]
        result = delay(secs, delete_messages, [client, cid, mids])
    except FloodWait as e:
        raise e
    except (ButtonDataInvalid, ButtonUrlInvalid):
        logger.warning(f"Send report message to {cid} - invalid markup: {markup}")
    except (ChannelInvalid, ChannelPrivate, ChatAdminRequired, PeerIdInvalid):
        return None
    except Exception as e:
        logger.warning(f"Send report message to {cid} error: {e}", exc_info=True)

    return result
