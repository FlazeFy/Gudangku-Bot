from firebase_admin import storage
import os
from datetime import datetime, timedelta

async def upload_photo(path:str):
    bucket = storage.bucket()
    blob = bucket.blob(f'analyze/{os.path.basename(path)}')
    blob.upload_from_filename(path)
    expiration_date = datetime.utcnow() + timedelta(days=365)
    photo_url = blob.generate_signed_url(expiration=expiration_date)

    return photo_url