from aiogram import types, Dispatcher
from utils.balance import get_balance
from utils.delivery import deliver_account, save_pending_account

async def start(msg: types.Message):
    menu = "👋 স্বাগতম!\n\nআপনার অপশন:\n/buy - অ্যাকাউন্ট কিনুন\n/sell_account - অ্যাকাউন্ট বিক্রি করুন\n/balance - ব্যালেন্স দেখুন"
    await msg.reply(menu)

async def buy(msg: types.Message):
    user_id = str(msg.from_user.id)
    balance = get_balance(user_id)
    if balance < 5:
        await msg.reply("❌ পর্যাপ্ত ব্যালেন্স নেই।")
        return
    filepath = deliver_account()
    if filepath:
        await msg.bot.send_document(msg.chat.id, open(filepath, 'rb'))
        await msg.reply("✅ আপনার অ্যাকাউন্ট পাঠানো হয়েছে।")
    else:
        await msg.reply("❌ কোন অ্যাকাউন্ট উপলব্ধ নেই!")

async def balance(msg: types.Message):
    user_id = str(msg.from_user.id)
    balance = get_balance(user_id)
    await msg.reply(f"💰 আপনার ব্যালেন্স: {balance}৳")

async def sell_account(msg: types.Message):
    user_id = str(msg.from_user.id)
    content = msg.text.replace("/sell_account", "").strip()
    if not content:
        await msg.reply("⚠️ অ্যাকাউন্ট তথ্য দিন! উদাহরণ:\n/sell_account\nUsername: @user123\nPassword: pass123")
        return
    acc_id = save_pending_account(user_id, content)
    await msg.reply(f"✅ আপনার অ্যাকাউন্ট গ্রহণ করা হয়েছে। রিভিউ ID: {acc_id}")

def register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(buy, commands=['buy'])
    dp.register_message_handler(balance, commands=['balance'])
    dp.register_message_handler(sell_account, commands=['sell_account'])