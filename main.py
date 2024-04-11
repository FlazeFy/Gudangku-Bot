import json
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Helpers
from helpers.greeting import start_command
from helpers.handlers import handle_message

with open('configs/telegram.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN: Final = config['TOKEN']

if __name__ == '__main__':
    print('Bot is running')
    app = Application.builder().token(TOKEN).build()

    # Command
    app.add_handler(CommandHandler('start', start_command))
    
    # app.add_handler(CommandHandler('help', help_command))
    # app.add_handler(CommandHandler('custom', custom_command))

    # Response
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)