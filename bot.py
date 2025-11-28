from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
import asyncio

TOKEN = "8581310157:AAE_PWKwEcBbRMFBPggxq-edTE76QAIQs9Y"
CHANNEL_ID = -1002874954438  # ID канала для уведомлений

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я бот для контроля покинувших группу пользователей.")

# Обработчик выхода пользователя
@dp.message(F.left_chat_member)
async def on_user_left(message: Message):
    user = message.left_chat_member

    # 1. Баним в группе
    try:
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=user.id
        )
        print(f"User {user.id} был забанен в группе")
    except Exception as e:
        print("Ошибка бана в группе:", e)

    # 2. Отправляем уведомление в канал
    try:
        await bot.send_message(
            CHANNEL_ID,
            f"Пользователь @{user.username} (ID: {user.id}) покинул группу и был забанен."
        )
    except Exception as e:
        print("Ошибка отправки в канал:", e)

    # 3. Баним в канале (опционально)
    try:
        await bot.ban_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user.id
        )
        print(f"User {user.id} заблокирован в канале")
    except Exception as e:
        print("Ошибка бана в канале:", e)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())