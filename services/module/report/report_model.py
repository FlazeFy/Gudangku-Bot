from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,DateTime

report=Table(
    'report',meta,
    Column('id',String(36),primary_key=True),
    Column('report_title',String(36)),
    Column('report_desc',String(255),nullable=True),
    Column('report_category',String(36)),

    Column('is_reminder',Integer),
    Column('remind_at',DateTime,nullable=True),
    Column('created_at',DateTime),
    Column('created_by',String(36)),
    Column('updated_at',DateTime,nullable=True),
    Column('deleted_at',DateTime,nullable=True)
)

report_item=Table(
    'report_item',meta,
    Column('id',String(36),primary_key=True),
    Column('inventory_id',String(36)),
    Column('report_id',String(36)),
    Column('item_name',String(75)),
    Column('item_desc',String(144)),
    Column('item_qty',Integer),
    Column('item_price',Integer),

    Column('created_at',DateTime),
    Column('created_by',String(36)),
)