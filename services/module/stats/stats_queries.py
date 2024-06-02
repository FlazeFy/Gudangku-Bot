from services.module.stats.template import get_total_item_by_context, get_custom_aggregate
from services.module.inventory.inventory_model import inventory
from helpers.converter import convert_price_number
from configs.configs import con
from sqlalchemy import text
from sqlalchemy import select, desc, and_

async def get_stats():
    dt_total_inventory_by_category = await get_total_item_by_context(tableName="inventory", targetColumn="inventory_category")
    dt_total_inventory_by_room = await get_total_item_by_context(tableName="inventory", targetColumn="inventory_room")
    dt_total_inventory_by_favorite = await get_total_item_by_context(tableName="inventory", targetColumn="is_favorite")
    dt_price_inventory_by_category = await get_custom_aggregate(tableName="inventory", targetColumn="inventory_category", extra="SUM(inventory_price) as total")
    dt_price_inventory_by_room = await get_custom_aggregate(tableName="inventory", targetColumn="inventory_room", extra="SUM(inventory_price) as total")
    dt_price_inventory_by_favorite = await get_custom_aggregate(tableName="inventory", targetColumn="is_favorite", extra="SUM(inventory_price) as total")

    res = f"<b>Total Inventory By Category:</b>\n"
    for dt in dt_total_inventory_by_category:
        res += (
            f"- {dt.context} : {dt.total}\n"
        )

    res += f"\n<b>Total Inventory By Room:</b>\n"
    for dt in dt_total_inventory_by_room:
        res += (
            f"- {dt.context} : {dt.total}\n"
        )

    res += f"\n<b>Total Inventory By Is Favorite:</b>\n"
    for dt in dt_total_inventory_by_favorite:
        if dt.context == 0:
            res += f"- Normal Item : {dt.total}\n"
        else:
            res += f"- Favorite : {dt.total}\n"

    res += f"\n<b>Total Price Inventory By Category:</b>\n"
    for dt in dt_price_inventory_by_category:
        res += (
            f"- {dt.context} : Rp. {convert_price_number(dt.total)},00\n"
        )

    res += f"\n<b>Total Price Inventory By Room:</b>\n"
    for dt in dt_price_inventory_by_room:
        res += (
            f"- {dt.context} : Rp. {convert_price_number(dt.total)},00\n"
        )

    res += f"\n<b>Total Price Inventory By Is Favorite:</b>\n"
    for dt in dt_price_inventory_by_favorite:
        if dt.context == 0:
            res += f"- Normal Item : Rp. {convert_price_number(dt.total)},00\n"
        else:
            res += f"- Favorite : Rp. {convert_price_number(dt.total)},00\n"
    return res

async def get_dashboard():
    userId = "2d98f524-de02-11ed-b5ea-0242ac120002"

    # Query builder
    sql_total_item = f"""
        SELECT COUNT(1) AS total
        FROM inventory
        WHERE created_by = '{userId}'
    """
    compiled_sql_total_item = text(sql_total_item)

    sql_total_favorite = f"""
        SELECT COUNT(1) AS total
        FROM inventory
        WHERE created_by = '{userId}'
        AND is_favorite = 1
    """
    compiled_sql_total_favorite = text(sql_total_favorite)

    sql_total_low= f"""
        SELECT COUNT(1) AS total
        FROM inventory
        WHERE created_by = '{userId}'
        AND inventory_capacity_unit = 'percentage'
        AND inventory_capacity_vol <= 30
    """
    compiled_sql_total_low = text(sql_total_low)

    query_last_added = select(
        inventory.c.inventory_name
    ).where(
        and_(
            inventory.c.created_by == userId,
            inventory.c.deleted_at.is_(None) 
        )
    ).order_by(
        desc(inventory.c.created_at)
    )

    query_highest_price = select(
        inventory.c.inventory_name
    ).where(
        and_(
            inventory.c.created_by == userId,
            inventory.c.deleted_at.is_(None) 
        )
    ).order_by(
        desc(inventory.c.inventory_price)
    )

    # Exec
    result_total_item = con.execute(compiled_sql_total_item)
    data_total_item = result_total_item.first()

    result_total_favorite = con.execute(compiled_sql_total_favorite)
    data_total_favorite = result_total_favorite.first()

    result_total_low = con.execute(compiled_sql_total_low)
    data_total_low = result_total_low.first()

    result_last_added = con.execute(query_last_added)
    data_last_added = result_last_added.first()

    dt_total_inventory_by_category = await get_total_item_by_context(tableName="inventory", targetColumn="inventory_category")
    most_category = f"({dt_total_inventory_by_category[0].total}) {dt_total_inventory_by_category[0].context}"

    result_highest_price = con.execute( query_highest_price)
    data_highest_price = result_highest_price.first()
    
    res = (
        f"<b>Total Item: {data_total_item.total}</b>\n"
        f"<b>Total Favorite : {data_total_favorite.total}</b>\n"
        f"<b>Total Low Capacity : {data_total_low.total}</b>\n"
        f"<b>Last Added : {data_last_added.inventory_name}</b>\n"
        f"<b>Most Category : {most_category}</b>\n"
        f"<b>The Highest Price : {data_highest_price.inventory_name}</b>\n"
    )



    return res

