from services.module.image_processing.color import analyze_color

async def analyze_photo(url:str):
    res_color = await analyze_color(url=url)
    res = f"{res_color}"

    return res