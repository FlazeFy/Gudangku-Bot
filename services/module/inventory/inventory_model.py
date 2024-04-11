from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,DateTime

inventory=Table(
    'inventory',meta,
    Column('id',String(36),primary_key=True),
    Column('inventory_name',String(75)),
    Column('inventory_category',String(75)),
    Column('inventory_desc',String(255), nullable=True),
    Column('inventory_merk',String(75),nullable=True),
    Column('inventory_room',String(36)),
    Column('inventory_storage',String(36), nullable=True),
    Column('inventory_rack',String(36), nullable=True),
    Column('inventory_price',Integer),
    Column('inventory_image',String(500), nullable=True),
    Column('inventory_unit',String(36)),
    Column('inventory_vol',Integer, nullable=True),
    Column('inventory_capacity_unit',String(36), nullable=True),
    Column('inventory_capacity_vol',Integer, nullable=True),

    Column('is_favorite',Integer),
    Column('is_reminder',Integer),
    Column('created_at',DateTime),
    Column('created_by',String(36)),
    Column('updated_at',DateTime,nullable=True),
    Column('deleted_at',DateTime,nullable=True)
)