from services.module.history.history_model import history
from configs.configs import con
from sqlalchemy import select, desc
import csv
import io 
from datetime import datetime

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

    if len(data) <= 30:
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

        return res, 'text'
    else:
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow([
            "Type", 
            "Context",
            "Created At"
        ])

        for dt in data:
            writer.writerow([
                dt.history_type, 
                dt.history_context,
                dt.created_at
            ])

        output.seek(0)
        res = output.getvalue()
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_bytes = io.BytesIO(res.encode('utf-8'))
        file_bytes.name = f"History_{now_str}.csv"

        return file_bytes, 'file'

