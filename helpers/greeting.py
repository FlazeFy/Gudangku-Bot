from telegram import Update
from telegram.ext import ContextTypes

async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, Welcome to GudangKu')
    await update.message.reply_text('Type your username : ')
    
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What do you want \n1. Show inventory\n2. Add inventory\n3. Update inventory\n4. Delete inventory\n5. Show report\n6. Show history\n7. Show stats\n8. Change password\n\n 0. Exit bot')