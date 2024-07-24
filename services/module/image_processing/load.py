from services.module.image_processing.color import analyze_color
from services.module.image_processing.storage import upload_photo
from services.module.image_processing.props import analyze_image_properties
from firebase_admin import db
import os

async def analyze_photo(url:str):
    res_color = await analyze_color(url=url)
    upload_url = await upload_photo(path=url)
    res_props = await analyze_image_properties(path=url)

    # Store to realtime db
    ref = db.reference('analyze')
    analyze_ref = ref.push({
        'color_analysis': res_color,
        'photo_url': upload_url,
        'props':res_props
    })
    id = analyze_ref.key

    props_str = (
        f"- File Size: {res_props['file_size']} bytes\n"
        f"- Creation Date: {res_props['creation_date']}\n"
        f"- Modification Date: {res_props['modification_date']}\n"
        f"- File Type: {res_props['file_type']}\n"
        f"- Dimensions: {res_props['dimensions']}"
    )

    res = (
        f"ID: {id}\n\n"
        f"Color Analysis: {res_color}\n\n"
        f"Download Link: {upload_url}\n\n"
        f"Image Properties:\n{props_str}"
    )
    os.remove(url)

    return res