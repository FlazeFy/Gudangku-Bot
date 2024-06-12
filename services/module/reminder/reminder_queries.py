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
        user.c.telegram_user_id,
        user.c.firebase_fcm_token
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

async def get_my_reminder():
    # Query builder
    query = select(
        inventory.c.inventory_name,
        reminder.c.reminder_desc,
        reminder.c.reminder_type,
        reminder.c.reminder_context,
        reminder.c.created_at
    ).join(
        inventory, inventory.c.id == reminder.c.inventory_id
    ).join(
        user, user.c.id == reminder.c.created_by
    ).order_by(
        reminder.c.created_at.desc(),
        inventory.c.inventory_name.asc()
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    res = f"You have {len(data)} reminder in your inventory.\nHere is the list:\n"
    inventory_name_before = ''

    for dt in data:
        if inventory_name_before == '' or inventory_name_before != dt.inventory_name:
            res += f"\n<b>Item: {dt.inventory_name}</b>\n"
            inventory_name_before = dt.inventory_name
        
        res += (
            f"Notes : {dt.reminder_desc}\n"
            f"Setting : {dt.reminder_type} - {dt.reminder_context}\n"
            f"Created at : {dt.created_at}\n"
        )

    return res