from PIL import Image
import numpy as np

def rgb_to_hex(r, g, b):
    return f"#{(1 << 24) + (r << 16) + (g << 8) + b:06X}"

def get_closest_color_name(r, g, b):
    color_names = {
        "black": [0, 0, 0],
        "white": [255, 255, 255],
        "red": [255, 0, 0],
        "lime": [0, 255, 0],
        "blue": [0, 0, 255],
        "yellow": [255, 255, 0],
        "cyan": [0, 255, 255],
        "magenta": [255, 0, 255],
        "silver": [192, 192, 192],
        "gray": [128, 128, 128],
        "maroon": [128, 0, 0],
        "olive": [128, 128, 0],
        "green": [0, 128, 0],
        "purple": [128, 0, 128],
        "teal": [0, 128, 128],
        "navy": [0, 0, 128]
    }
    
    def euclidean_distance(c1, c2):
        return np.sqrt(np.sum((np.array(c1) - np.array(c2))**2))

    closest_color = None
    closest_distance = float('inf')

    for name, color in color_names.items():
        distance = euclidean_distance([r, g, b], color)
        if distance < closest_distance:
            closest_color = name
            closest_distance = distance

    return closest_color

async def analyze_color(url:str):
    image = Image.open(url)
    image = image.convert('RGB')
    image = np.array(image)

    average_color = image.mean(axis=(0, 1))
    r, g, b = average_color.astype(int)

    hex_color = rgb_to_hex(r, g, b)

    closest_color_name = get_closest_color_name(r, g, b)

    res = f"Color Analyze :\n- RGB : {(r, g, b)}\n- Hex : {hex_color}\n- Name : {closest_color_name}"

    return res
