from services.module.stats.template import get_total_item_by_context, get_custom_aggregate
from helpers.converter import convert_price_number

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

