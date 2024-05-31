from services.module.history.history_model import history
from configs.configs import con
from sqlalchemy import select, desc, and_

async def get_all_history():
    # Query builder
    query = select(
        history.c.history_context, 
        history.c.history_type, 
        history.c.created_at, 
    ).where(
        history.c.created_by == "2d98f524-de02-11ed-b5ea-0242ac120002"
    ).order_by(
        desc(history.c.created_at)
    )

    # Exec
    result = con.execute(query)
    data = result.fetchall()

    res = f"Here is the history:\n"
    day_before = ''

    for dt in data:    
        if day_before == '' or day_before != dt.created_at.strftime('%d %b %Y'):
            day_before = dt.created_at.strftime('%d %b %Y')
            res += f"\n<b>"+day_before+"</b>\n"
            date = dt.created_at.strftime('%H:%M')
        else: 
            date = dt.created_at.strftime('%H:%M')
                
        res += f"- {dt.history_type} from item called {dt.history_context} at {date}\n"

    return res