from PIL import Image
import os
from datetime import datetime

async def analyze_image_properties(path: str):
    file_info = os.stat(path)

    with Image.open(path) as img:
        width, height = img.size
        file_type = img.format

    created_at = datetime.fromtimestamp(file_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    updated_at = datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    
    properties = {
        'file_path': path,
        'file_size': file_info.st_size,
        'creation_date': created_at,
        'modification_date': updated_at if created_at != updated_at else None,
        'file_type': file_type,
        'dimensions': f"{width}x{height}"
    }

    return properties