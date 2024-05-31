from services.module.stats.template import get_total_item_by_context

async def get_stats():
    dt_total_inventory_by_category = await get_total_item_by_context(tableName="inventory", targetColumn="inventory_category")
    dt_total_inventory_by_room = await get_total_item_by_context(tableName="inventory", targetColumn="inventory_room")
    dt_total_inventory_by_favorite = await get_total_item_by_context(tableName="inventory", targetColumn="is_favorite")

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
    return res

