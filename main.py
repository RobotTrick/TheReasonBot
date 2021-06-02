from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Msg import return_reason
from handlers import unblock, private, exit, start, help
from utils import *

app = Client("the_reason")

app.add_handler(CallbackQueryHandler(unblock, ~filters.regex("exit")))  # check msg in group
app.add_handler(CallbackQueryHandler(exit, filters.regex("exit")))  # delete check msg
app.add_handler(MessageHandler(private, filters.private & filters.command("my_bans")))  # check msg in private
app.add_handler(MessageHandler(start, filters.command("start")))  # start msg
app.add_handler(MessageHandler(help, filters.command("help")))  # help msg


@app.on_message(filters.group & filters.command(["ban", "ban@" + Msg.bot_username]))
def ban(app: Client, msg: Message):
    """ ban user with a reason """

    if len(msg.command) < 2:
        msg.reply(Msg.need_reason)
        return

    if not is_admin(msg):
        try:
            msg.delete()
        except ChatAdminRequired:
            pass
        return

    if msg.reply_to_message and len(msg.entities) == 1:
        user = msg.reply_to_message.from_user
    elif len(msg.entities) >= 2:
        if msg.entities[1].type == "mention":
            user = app.get_users(msg.text[msg.entities[1].offset:msg.entities[1].offset + msg.entities[1].length])
        elif msg.entities[1].type == "text_mention":
            user = msg.entities[1].user

    kick_msg = None
    try:
        kick_msg = msg.chat.kick_member(user.id)
    except ChatAdminRequired:
        msg.reply(Msg.need_permissions)

    id_baned = save_ban(msg, app)  # save details to db
    msg.reply(Msg.ban_success.format(id_baned), reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton(Msg.exit_btn, "exit")]]))

    if isinstance(kick_msg, Message):
        try:
            kick_msg.delete()
        except ChatAdminRequired:
            msg.reply(Msg.need_permissions)


@app.on_message(filters.group & filters.command(["check", "check@" + Msg.bot_username]
                                                ) & ~filters.reply)
def check(_, msg: Message):
    """ check the reason of user-baned with id provided """
    if not is_admin(msg):
        msg.reply(Msg.only_admins)
        return

    if len(msg.command) < 2:
        msg.reply(Msg.need_id)
        return

    reason = get_reason(int(msg.command[1]), msg.chat.id)
    if not reason:
        msg.reply(Msg.not_found)
        return

    msg.reply(return_reason(reason), reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(Msg.unblock_btn, str(msg.command[1]))],
        [InlineKeyboardButton(Msg.exit_btn, "exit")]
    ]))


@app.on_message(filters.group & filters.command(["check", "check@" + Msg.bot_username]
                                                ) & filters.reply)
def reply(_, msg: Message):
    """ check the reason of user-baned with reply to forward msg """
    if not is_admin(msg):
        msg.reply(Msg.only_admins)
        return

    if msg.reply_to_message.forward_sender_name and not msg.reply_to_message.forward_sender_name.startswith(
            msg.reply_to_message.from_user.first_name):  # check if the user didn't hide forward msgs
        msg.reply(Msg.hide_sender)
        return

    reason = get_reason(msg.reply_to_message.from_user.id, msg.chat.id)
    if not reason:
        msg.reply(Msg.not_found)
        return

    msg.reply(return_reason(reason), reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton(Msg.unblock_btn, str(msg.command[1]))
    ]]))


app.run()
