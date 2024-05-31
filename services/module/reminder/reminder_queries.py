from services.module.reminder.reminder_model import reminder
from services.module.inventory.inventory_model import inventory
from services.module.user.user_model import user
from configs.configs import con
from sqlalchemy import select, func

async def get_all_reminder():
    # Query builder
    query = select(
        inventory.c.inventory_name,
        reminder.c.reminder_desc,
        reminder.c.reminder_type,
        reminder.c.reminder_context,
        reminder.c.created_at,
        user.c.email,
        user.c.username,
        user.c.telegram_user_id
    ).join(
        inventory, inventory.c.id == reminder.c.inventory_id
    ).join(
        user, user.c.id == reminder.c.created_by
    ).order_by(
        reminder.c.created_at.desc()
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    return data