from services.module.inventory.inventory_model import inventory
from helpers.converter import convert_price_number
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
            res += f"\n<b>Category: {dt.inventory_category}</b>\n"
            inventory_category_before = dt.inventory_category
        
        res += f"{i}. {dt.inventory_name}\n"
        i += 1

    return res

async def get_all_inventory_name():
    # Query builder
    query = select(
        inventory.c.id, 
        inventory.c.inventory_name, 
    ).where(
        inventory.c.created_by == "2d98f524-de02-11ed-b5ea-0242ac120002",
    ).order_by(
        desc(inventory.c.inventory_name)
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    return data

async def get_detail_inventory(id):
    # Query builder
    query = select(
        inventory.c.inventory_name,
        inventory.c.inventory_category,
        inventory.c.inventory_desc,
        inventory.c.inventory_merk,
        inventory.c.inventory_room,
        inventory.c.inventory_storage,
        inventory.c.inventory_rack,
        inventory.c.inventory_price,
        inventory.c.inventory_image,
        inventory.c.inventory_unit,
        inventory.c.inventory_vol,
        inventory.c.inventory_capacity_unit,
        inventory.c.inventory_capacity_vol,
        inventory.c.is_favorite,
        inventory.c.is_reminder,
        inventory.c.created_at,
        inventory.c.updated_at, 
    ).where(
        and_(
            inventory.c.created_by == "2d98f524-de02-11ed-b5ea-0242ac120002",
            inventory.c.id == id
        )
    )

    # Exec
    result = con.execute(query)
    data = result.first()

    capacity = f"{data.inventory_capacity_vol or '-'} {data.inventory_capacity_unit or '-'}"
    if data.inventory_capacity_unit == 'percentage' :
        capacity = f"{data.inventory_capacity_vol or '-'}%"

    res = (
        f"<b>{data.inventory_name}</b>\n"
        f"Category : {data.inventory_category}\n"
        f"Description : {data.inventory_desc or '-'}\n"
        f"Merk : {data.inventory_merk or '-'}\n"
        f"Room : {data.inventory_room}\n"
        f"Storage : {data.inventory_storage or '-'}\n"
        f"Rack : {data.inventory_rack or '-'}\n"
        f"Price : Rp. {convert_price_number(data.inventory_price)},00\n"
        f"Dimension : {data.inventory_vol or '-'} {data.inventory_unit}\n"
        f"Capacity : {capacity} \n\n"
        f"{'' if data.is_favorite != 1 else 'This item is favorited'}\n"
        f"{'' if data.is_reminder != 1 else 'This item have reminder'}\n"
        f"Props\n"
        f"Created At : {data.created_at}\n"
        f"Updated At : {data.updated_at or '-'}\n"
    )

    return res, data.inventory_image