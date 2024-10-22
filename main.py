import json
from typing import Final
from telegram.ext import Application, CommandHandler,  CallbackQueryHandler, MessageHandler, filters

# Cron job
from services.jobs.schedule import console_reminder

# Helpers
from helpers.greeting import start_command, button, handle_photo, handle_file

with open('configs/telegram.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN: Final = config['TOKEN']

if __name__ == '__main__':
    print('Bot is running')
    # asyncio.run(console_reminder())
    app = Application.builder().token(TOKEN).build()

    # Command
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print('Polling...')
    app.run_polling(poll_interval=1)
