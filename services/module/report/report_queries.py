from services.module.report.report_model import report, report_item
from services.module.inventory.inventory_model import inventory
from configs.configs import con
from sqlalchemy import select, func

async def get_all_report():
    # Query builder
    query = select(
        report.c.report_title,
        report.c.report_desc,
        report.c.report_category,
        report.c.is_reminder,
        report.c.remind_at,
        report.c.created_at,
        func.count(1).label('total_variety'),
        func.sum(report_item.c.item_qty).label('total_item'),
        func.group_concat(inventory.c.inventory_name, ',').label('report_items'),
        func.sum(report_item.c.item_price * report_item.c.item_qty).label('item_price')
    ).join(
        report_item, report.c.id == report_item.c.report_id, isouter=True
    ).join(
        inventory, inventory.c.id == report_item.c.inventory_id,isouter=True
    ).where(
        inventory.c.created_by == "2d98f524-de02-11ed-b5ea-0242ac120002",
    ).filter(
        report.c.created_by == "2d98f524-de02-11ed-b5ea-0242ac120002",
        report.c.deleted_at.is_(None)
    ).group_by(
        report.c.id
    ).order_by(
        report.c.created_at.desc()
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    res = f"You have {len(data)} report. Here is the list:\n\n"

    for dt in data:
        res += (
            f"<b>{dt.report_title}</b> ~ {dt.report_category}\n"
            f"{dt.report_desc or '<i>- No description provided -</i>'}\n\n"
            f"Items ({dt.total_item})\n"
        )
        if dt.report_items:
            report_items = dt.report_items.split(',')
            for item in report_items:
                if item != "":
                    res += f"- {item}\n"
        else:
            res += "- No items -\n"
        
        res += (
            f"{'Remind At : '+dt.remind_at if dt.remind_at else ''}\n"
            f"Created At : {dt.created_at}\n"
            f"= = = = = = = = = = = = = = = = = = =\n\n"
        )

    return res