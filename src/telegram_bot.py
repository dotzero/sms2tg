from datetime import datetime

import telegram
from pytz import timezone
from telegram.helpers import escape_markdown

from src.conf import REPORT_TIMEZONE, TG_CHAT_ID, TG_TOKEN

bot = telegram.Bot(TG_TOKEN)


async def send_message(text: str):
    await bot.send_message(chat_id=TG_CHAT_ID, text=text)


async def send_sms_message(sender: str, time: datetime, text: str):
    timezone_time = time.astimezone(timezone(REPORT_TIMEZONE))
    text_block = (
        "SMS от `"
        + escape_markdown(sender, version=2)
        + timezone_time.strftime("` \(*%d %B в %H:%M*\):\n\n")
    )
    lines = escape_markdown(text, version=2).split("\n")
    text_block = text_block + "\n".join("> " + line for line in lines)
    await bot.send_message(chat_id=TG_CHAT_ID, text=text_block, parse_mode="MarkdownV2")
