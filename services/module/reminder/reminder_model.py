from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,DateTime

reminder=Table(
    'reminder',meta,
    Column('id',String(36),primary_key=True),
    Column('inventory_id',String(36)),
    Column('reminder_desc',String(255)),
    Column('reminder_type',String(36)),
    Column('reminder_context',String(36)),
    
    Column('created_at',DateTime),
    Column('created_by',String(36))
)