import schedule
from services.jobs.task.reminder import task_reminder_inventory
import asyncio

async def console_reminder():
    await task_reminder_inventory()

    schedule.every().day.at("18:20").do(task_reminder_inventory)

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)