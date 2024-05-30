from datetime import datetime
from services.mailer.mail import send_email
from services.module.reminder.reminder_queries import get_all_reminder

async def task_reminder_inventory():
    res = await get_all_reminder()

    for dt in res:
        email = dt.email
        created_at_formatted = dt.created_at.strftime('%d-%b-%Y %H:%M')

        await send_email(
            subject="Inventory Reminder",
            body=f"""
            Hello {dt.username},<br><br>
            You have a reminder from item <b>{dt.inventory_name}</b> about {dt.reminder_desc}.<br><br>
            This reminder was created at {created_at_formatted}.
            """,
            to_email=email
        )