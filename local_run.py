import asyncio
import logging
import sys
import os

# Add api directory to sys.path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from api.index import dp, bot

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot polling boshlandi... To'xtatish uchun Ctrl+C bosing.")
    # Local holatda polling ishlatamiz
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
