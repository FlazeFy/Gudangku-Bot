from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# Services
from services.module.inventory.inventory_queries import get_all_inventory
from services.module.history.history_queries import get_all_history

async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Type your username : ')
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Handle different button presses here
    if query.data == '1':
        res = await get_all_inventory()
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing inventory...\n{res}", reply_markup=reply_markup)
    elif query.data == '2':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Adding inventory...", reply_markup=reply_markup)
    elif query.data == '3':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Updating inventory...", reply_markup=reply_markup)
    elif query.data == '4':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Deleting inventory...", reply_markup=reply_markup)
    elif query.data == '5':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Showing report...", reply_markup=reply_markup)
    elif query.data == '6':
        res = await get_all_history()
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing history...\n{res}", reply_markup=reply_markup)
    elif query.data == '7':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Showing stats...", reply_markup=reply_markup)
    elif query.data == '8':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Changing password...", reply_markup=reply_markup)
    elif query.data == '9':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing inventory...\n{res}", reply_markup=reply_markup)
    elif query.data == '0':
        await query.edit_message_text(text="Exiting bot...")
    elif query.data == 'back':
        await query.edit_message_text(text='What do you want:', reply_markup= main_menu_keyboard())

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = main_menu_keyboard()
    await update.message.reply_text('What do you want:', reply_markup=reply_markup)

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("1. Show inventory", callback_data='1')],
        [InlineKeyboardButton("2. Add inventory", callback_data='2')],
        [InlineKeyboardButton("3. Update inventory", callback_data='3')],
        [InlineKeyboardButton("4. Delete inventory", callback_data='4')],
        [InlineKeyboardButton("5. Show report", callback_data='5')],
        [InlineKeyboardButton("6. Show history", callback_data='6')],
        [InlineKeyboardButton("7. Show stats", callback_data='7')],
        [InlineKeyboardButton("8. Change password", callback_data='8')],

        [InlineKeyboardButton("9. Detail inventory", callback_data='9')],

        [InlineKeyboardButton("0. Exit bot", callback_data='0')]
    ]
    return InlineKeyboardMarkup(keyboard)
