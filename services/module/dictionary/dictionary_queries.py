
from sqlalchemy import select
from services.module.dictionary.dictionary_model import dictionary

async def get_all_dct(session):
    query_dct = select(
        dictionary.c.dictionary_type,
        dictionary.c.dictionary_name
    ).order_by(dictionary.c.dictionary_type.asc())
    result_dct = session.execute(query_dct)
    dcts = result_dct.fetchall()

    return dcts