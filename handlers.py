from pyrogram.types import *
from Msg import get_bans_for_user, start_msg, help_msg
from utils import *
from pyrogram.errors import ChatAdminRequired


def unblock(_, call: CallbackQuery):
    """ unban the user from group by CallbackQuery """
    if is_admin(call.message):
        try:
            call.message.chat.unban_member(int(call.data))
            call.answer(Msg.unblock_success, True)
            call.message.delete()

        except ChatAdminRequired:
            call.answer(Msg.need_permissions, True)

    else:
        call.answer(Msg.only_admins)  # displaying error if the query sent by non-admin


def exit(_, call: CallbackQuery):
    """ deleting the checking message """
    call.message.delete()


@db_session
def private(_, msg: Message):
    """ private check for list of bans in groups """
    match = select(b for b in Ban if b.uid == msg.from_user.id)
    if not match:
        msg.reply(Msg.not_found_bans_for_user)
        return

    txt = Msg.head_msg
    for ban in match:
        txt += "\n"
        dct = dict(chat_title=ban.chat_title, date=ban.date, reason=ban.reason)
        txt += get_bans_for_user(dct)
    msg.reply(txt)


def start(_, msg: Message):
    """ sending start mdg """
    msg.reply(start_msg.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton(Msg.add_to_group, url=f'http://t.me/{Msg.bot_username}?startgroup=true')
    ]]))

def help(_, msg: Message):
    """ sending help msg """
    msg.reply(help_msg)

