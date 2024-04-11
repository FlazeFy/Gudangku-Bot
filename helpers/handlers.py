import json
from typing import Final
from telegram import Update
from telegram.ext import ContextTypes

# Services
from services.module.inventory.inventory_queries import get_all_inventory
from services.module.history.history_queries import get_all_history

with open('configs/telegram.json', 'r') as config_file:
    config = json.load(config_file)
    
BOT_USERNAME: Final = config['BOT_USERNAME']

async def handle_menu_res(text: str) -> str:
    val: str = text.lower()

    if '1' in val:
        data = await get_all_inventory()
        return data

    if '6' in val:
        data = await get_all_history()
        return data
    
    if '0' in val:
        return 'Are you sure want to exit this chat?'
    
    return 'Your message is not identified'

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    val: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{val}"')

    if message_type == 'group':
        if BOT_USERNAME in val:
            new_val: str = val.replace(BOT_USERNAME,'').strip()
            res: str = await handle_menu_res(new_val)
        else:
            return
    else:
        res: str = await handle_menu_res(val)

    print('Bot: ', res)
    await update.message.reply_text(res)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')