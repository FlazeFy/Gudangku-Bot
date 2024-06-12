from linebot import LineBotApi
import re
from linebot.models import TextSendMessage
import json
from typing import Final

with open('configs/line.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN: Final = config['TOKEN']

line_bot_api = LineBotApi(TOKEN)

def send_line_message(user_id, message):
    try:
        clean = re.compile('<.*?>')
        response = line_bot_api.push_message(user_id, TextSendMessage(text=re.sub(clean,'',message)))
        print(response)
        return True
    except Exception as e:
        print(e)
        return False
