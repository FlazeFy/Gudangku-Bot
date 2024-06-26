from datetime import datetime
from services.mailer.mail import send_email
from services.mailer.fcm_notif import send_fcm_notif
from services.module.reminder.reminder_queries import get_all_reminder
from services.mailer.line import send_line_message
from telegram.error import TelegramError
from telegram import Bot
import json
from typing import Final

with open('configs/telegram.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN: Final = config['TOKEN']

async def task_reminder_inventory():
    bot = Bot(token=TOKEN)

    res = await get_all_reminder()

    for dt in res:
        email = dt.email
        telegram_user_id = dt.telegram_user_id
        firebase_fcm_token = dt.firebase_fcm_token
        line_user_id = dt.line_user_id
        created_at_formatted = dt.created_at.strftime('%d-%b-%Y %H:%M')

        message_body = (f"Hello {dt.username},\n"
        f"You have a reminder from item <b>{dt.inventory_name}</b> about {dt.reminder_desc}.\n"
        f"This reminder was created at {created_at_formatted}.")

        # Send email
        await send_email(
            subject="Inventory Reminder",
            body=message_body,
            to_email=email
        )

        # Send Telegram message
        if telegram_user_id != None:
            try:
                await bot.send_message(
                    chat_id=telegram_user_id,
                    text=message_body,
                    parse_mode='HTML',
                )
            except TelegramError as e:
                print(f"Failed to send message to {dt.username} ({telegram_user_id}): {e}")

        # Send Notification to GudangKu Mobile Apps
        if firebase_fcm_token != None:
            try: 
                send_fcm_notif(firebase_fcm_token, title="Inventory Reminder", body=message_body)
            except TelegramError as e:
                print(f"Failed to send message to {dt.username} ({firebase_fcm_token}): {e}")

        # Send Line message
        if line_user_id != None:
            try: 
                send_line_message(user_id=line_user_id, message=message_body)
            except TelegramError as e:
                print(f"Failed to send message to {dt.username} ({line_user_id}): {e}")