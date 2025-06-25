from aiogram import types, Dispatcher
from config import ADMIN_ID
from utils.delivery import list_pending_accounts, approve_account, reject_account
import json

async def add_balance(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        _, user_id, amount = msg.text.split()
        with open('database/users.json', 'r+') as f:
            users = json.load(f)
            users[user_id] = users.get(user_id, 0) + int(amount)
            f.seek(0)
            json.dump(users, f)
            f.truncate()
        await msg.reply(f"{user_id} এর ব্যালেন্স এখন {users[user_id]}৳")
    except:
        await msg.reply("ব্যবহার: /add_balance USER_ID AMOUNT")

async def pending(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    entries = list_pending_accounts()
    if not entries:
        await msg.reply("📭 কোন pending অ্যাকাউন্ট নেই।")
    else:
        text = "\n".join([f"ID: {k}\n{v['data']}\n" for k, v in entries.items()])
        await msg.reply(text)

async def approve(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        _, acc_id = msg.text.split()
        approve_account(acc_id)
        await msg.reply(f"✅ ID {acc_id} অ্যাকাউন্ট অ্যাপ্রুভ হয়েছে।")
    except:
        await msg.reply("ব্যবহার: /approve ID")

async def reject(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        _, acc_id = msg.text.split()
        reject_account(acc_id)
        await msg.reply(f"❌ ID {acc_id} বাতিল করা হয়েছে।")
    except:
        await msg.reply("ব্যবহার: /reject ID")

def register(dp: Dispatcher):
    dp.register_message_handler(add_balance, commands=['add_balance'])
    dp.register_message_handler(pending, commands=['pending'])
    dp.register_message_handler(approve, commands=['approve'])
    dp.register_message_handler(reject, commands=['reject'])