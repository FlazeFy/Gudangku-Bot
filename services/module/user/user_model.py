from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,DateTime

user=Table(
    'users',meta,
    Column('id',String(36),primary_key=True),
    Column('username',String(36)),
    Column('password',String(500)),
    Column('email',String(144)),
    Column('telegram_user_id',String(144),nullable=True),
    Column('firebase_fcm_token',String(255),nullable=True),
    Column('line_user_id',String(255),nullable=True),
    Column('phone',String(18)),

    Column('created_at',DateTime),
    Column('updated_at',DateTime,nullable=True),
)