from configs.configs import con
from sqlalchemy import text

async def get_total_item_by_context(tableName, targetColumn):
    # Query builder
    sql_query = f"""
        SELECT {targetColumn} AS context, COUNT(1) AS total 
        FROM {tableName}
        GROUP BY {targetColumn}
        ORDER BY total
    """
    compiled_sql = text(sql_query)

    # Exec
    result = con.execute(compiled_sql)
    data = result.fetchall()

    return data