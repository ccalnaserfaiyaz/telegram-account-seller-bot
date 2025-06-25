from aiogram import Bot, Dispatcher, types, executor
from config import BOT_TOKEN
from handlers import user, admin

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

user.register(dp)
admin.register(dp)

if __name__ == "__main__":
    executor.start_polling(dp)