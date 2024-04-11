from services.module.inventory.inventory_model import inventory
from configs.configs import con
from sqlalchemy import select, desc, and_

async def get_all_inventory():
    # Query builder
    query = select(
        inventory.c.inventory_name, 
        inventory.c.inventory_category
    ).where(
        and_(
            inventory.c.created_by == "2d98f524-de02-11ed-b5ea-0242ac120002",
            inventory.c.deleted_at.is_(None) 
        )
    ).order_by(
        desc(inventory.c.inventory_category),
        desc(inventory.c.is_favorite),
        desc(inventory.c.created_at)
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    res = f"You have {len(data)} items in your inventory.\nHere is the list:\n"
    inventory_category_before = ''
    i = 1

    for dt in data:
        if inventory_category_before == '' or inventory_category_before != dt.inventory_category:
            res += f"\nCategory: {dt.inventory_category}\n"
            inventory_category_before = dt.inventory_category
        
        res += f"{i}. {dt.inventory_name}\n"
        i += 1

    return res