from configs.configs import con
from sqlalchemy import text

async def get_total_item_by_context(tableName, targetColumn):
    userId = "2d98f524-de02-11ed-b5ea-0242ac120002"

    # Query builder
    sql_query = f"""
        SELECT {targetColumn} AS context, COUNT(1) AS total 
        FROM {tableName}
        WHERE created_by = '{userId}'
        GROUP BY {targetColumn}
        ORDER BY total DESC
    """
    compiled_sql = text(sql_query)

    # Exec
    result = con.execute(compiled_sql)
    data = result.fetchall()

    return data

async def get_custom_aggregate(tableName, targetColumn, extra):
    userId = "2d98f524-de02-11ed-b5ea-0242ac120002"

    # Query builder
    sql_query = f"""
        SELECT {targetColumn} AS context, {extra}
        FROM {tableName}
        WHERE created_by = '{userId}'
        GROUP BY 1
        ORDER BY 2 DESC
    """
    compiled_sql = text(sql_query)

    # Exec
    result = con.execute(compiled_sql)
    data = result.fetchall()

    return data