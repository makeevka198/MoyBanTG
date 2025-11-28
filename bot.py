from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

API_TOKEN = "8581310157:AAE_PWKwEcBbRMFBPggxq-edTE76QAIQs9Y"
WEBHOOK_HOST = "https://ваш-домен.com"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 8080   # <-- ваш порт

CHANNEL_ID = -1002874954438

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=['left_chat_member'])
async def on_user_left(message: types.Message):
    user = message.left_chat_member

    await bot.kick_chat_member(message.chat.id, user.id)

    text = f"@{user.username} покинул и получил бан."
    await bot.send_message(CHANNEL_ID, text)

    await message.delete()


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
