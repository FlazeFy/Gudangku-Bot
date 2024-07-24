import easyocr
import cv2

async def analyze_text_easyocr(path:str):
    reader = easyocr.Reader(['en'])
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = reader.readtext(gray)
    res = ''
    
    for (bbox, text, accuracy) in data:
        res += f"- {text}\n<i>Accuracy : {round(accuracy, 2)}</i>\n"

    return res