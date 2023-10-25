import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import Txt, Config
from helper.database import db
from helper.utils import is_subscribed, force_sub


# 🌐 Global Buttons to be Modified
btn1 = InlineKeyboardButton('✅ Approval Message On',
                            callback_data='approvalmsg_on')
btn2 = InlineKeyboardButton(
    '❌ Approval Message Off', callback_data='approvalmsg_off')
btn4 = InlineKeyboardButton('✅ Leaving Message On',
                            callback_data='leavingmsg_on')
btn3 = InlineKeyboardButton('❌ Leaving Message Off',
                            callback_data='leavingmsg_off')


# Force Sub Handler
@Client.on_message(filters.private)
async def _(bot: Client, cmd):
    if not await is_subscribed(bot, cmd):
        return await force_sub(bot, cmd)

    await cmd.continue_propagation()


@Client.on_message(filters.private & filters.command('start'))
async def Start_message(bot: Client, msg: Message):

    user = msg.from_user
    await db.add_user(bot, user)
    await msg.reply_text(text=Txt.START_MSG.format(msg.from_user.mention), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Developer', url='https://t.me/Snowball_Official')]]))


@Client.on_message(filters.private & filters.command(['setting', 'config']) & filters.user(Config.OWNER))
async def Settings(bot: Client, msg: Message):

    SnowDev = await msg.reply_text('Please Wait ⏳')
    bool_approve = await db.get_bool_approve_msg(msg.from_user.id)
    bool_leave = await db.get_bool_leave_msg(msg.from_user.id)

    if bool_approve and bool_leave:
        await SnowDev.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn1], [btn4]]))

    elif bool_approve:
        await SnowDev.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn1], [btn3]]))

    elif bool_leave:
        await SnowDev.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn2], [btn4]]))

    else:
        await SnowDev.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn2], [btn3]]))


@Client.on_callback_query()
async def query(bot: Client, query: CallbackQuery):

    data = query.data

    if data.startswith('approvalmsg'):

        condition = data.split('_')[1]
        bool_leave = await db.get_bool_leave_msg(query.message.chat.id)
        if condition == 'on':
            if bool_leave:
                await db.set_bool_approve_msg(query.message.chat.id, False)
                await query.message.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn2], [btn4]]))
            else:
                await db.set_bool_approve_msg(query.message.chat.id, False)
                await query.message.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn2], [btn3]]))

        elif condition == 'off':
            if bool_leave:
                await db.set_bool_approve_msg(query.message.chat.id, True)
                await query.message.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn1], [btn4]]))
            else:
                await db.set_bool_approve_msg(query.message.chat.id, True)
                await query.message.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn1], [btn3]]))

    elif data.startswith('leavingmsg'):
        condition = data.split('_')[1]
        bool_approve = await db.get_bool_approve_msg(query.message.chat.id)
        if condition == 'on':
            if bool_approve:
                await db.set_bool_leave_msg(query.message.chat.id, False)
                await query.message.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn1], [btn3]]))
            else:
                await db.set_bool_leave_msg(query.message.chat.id, False)
                await query.message.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn2], [btn3]]))

        elif condition == 'off':
            if bool_approve:
                await db.set_bool_leave_msg(query.message.chat.id, True)
                await query.message.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn1], [btn4]]))
            else:
                await db.set_bool_leave_msg(query.message.chat.id, True)
                await query.message.edit(text="**Your Approval and Leaving Message Settings ⚙️**", reply_markup=InlineKeyboardMarkup([[btn2], [btn4]]))


@Client.on_message(filters.private & filters.command('set_approvemsg') & filters.user(Config.OWNER))
async def set_ApproveMsg(bot: Client, msg: Message):

    if msg.reply_to_message:
        ms = await msg.reply_text("Please Wait...")
        await db.set_approve_msg(msg.from_user.id, msg.reply_to_message.text)
        await ms.edit("**Successfully Added ✅**")
        await asyncio.sleep(3)
        await ms.delete()

    else:
        await msg.reply_text("Reply To a Message\nSupport Only Text & All HTML format !\n\nEg. `Hi {mention} You Request Accepted for {title}`")


@Client.on_message(filters.private & filters.command('set_leavemsg') & filters.user(Config.OWNER))
async def set_ApproveMsg(bot: Client, msg: Message):

    if msg.reply_to_message:
        ms = await msg.reply_text("Please Wait...")
        await db.set_leave_msg(msg.from_user.id, msg.reply_to_message.text)
        await ms.edit("**Successfully Added ✅**")
        await asyncio.sleep(3)
        await ms.delete()

    else:
        await msg.reply_text("Reply To a Message\nSupport Only Text & All HTML format !\n\nEg. `Hi {mention} You Left Group/Channel form {title}`")
