from firebase_admin import credentials, storage, initialize_app
import os

async def upload_photo(path:str):
    bucket = storage.bucket()
    blob = bucket.blob(f'analyze/{os.path.basename(path)}')
    blob.upload_from_filename(path)
    photo_url = blob.public_url

    return photo_url