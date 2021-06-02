from datetime import datetime
from typing import Union
from pony.orm import *
from pyrogram.types import Message, User
from pyrogram import Client

from Msg import Msg

db = Database()


class Ban(db.Entity):
    uid = Required(int)
    reason = Required(str)
    chat_id = Required(str)
    chat_title = Optional(str)
    admin_id = Required(int)
    admin_name = Required(str)
    date = Required(str)


db.bind(provider='sqlite', filename='the_reason.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


@db_session
def get_reason(uid: int, chat: int) -> Union[bool, dict]:
    """ return details of ban as a dict """
    try:
        user = Ban.get(uid=uid, chat_id=str(chat))
    except MultipleObjectsFoundError:
        user = select(u for u in Ban if u.uid == uid and u.chat_id == str(chat))[:][-1]

    if not user:
        return False

    data = dict(user_id=user.uid,
                reason=user.reason,
                chat=user.chat_id,
                chat_title=user.chat_title,
                admin_id=user.admin_id,
                admin_name=user.admin_name,
                date=user.date)
    return data


def save_ban(msg: Message, app: Client) -> Union[bool, int]:
    """ enter ban details to database """
    user = ""
    reason = ""
    ents = msg.entities

    if msg.reply_to_message and len(ents) == 1:
        user = msg.reply_to_message.from_user
        reason = " ".join(msg.command[1:])

    elif len(ents) >= 2:

        for ent in ents:
            if ent.type == "mention":
                user = app.get_users(msg.text[ent.offset:ent.offset + ent.length])
                reason = msg.text[ent.offset + ent.length:]
                break
            elif ent.type == "text_mention":
                user = ent.user
                reason = msg.text[ent.offset + ent.length:]
                break
    else:
        return False

    if isinstance(user, User) and reason:

        with db_session:
            ban = Ban(uid=user.id,
                      reason=reason,
                      chat_id=str(msg.chat.id),
                      chat_title=msg.chat.title,
                      admin_id=msg.from_user.id,
                      admin_name=msg.from_user.first_name,
                      date=datetime.utcfromtimestamp(msg.date).strftime('%Y-%m-%d %H:%M:%S'))
            commit()
            return ban.uid

    elif not reason:
        msg.reply(Msg.need_reason)


def is_admin(msg: Message):
    if not msg.from_user or msg.chat.get_member(
            msg.from_user.id).status in ("creator", "administrator"):
        return True
