from configs.configs import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import String

dictionary=Table(
    'dictionary',meta,
    Column('dictionary_type',String(36)),
    Column('dictionary_name',String(75))
)