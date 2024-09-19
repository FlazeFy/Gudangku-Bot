from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackContext
import os

# Services
from helpers.typography import send_long_message
from services.module.inventory.inventory_queries import get_all_inventory, get_all_inventory_name, get_detail_inventory
from services.module.history.history_queries import get_all_history
from services.module.report.report_queries import get_all_report
from services.module.stats.stats_queries import get_stats, get_dashboard
from services.module.reminder.reminder_queries import get_my_reminder
from services.module.stats.stats_capture import get_stats_capture
from services.module.image_processing.load import analyze_photo

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
        message_chunks = send_long_message(res)
        for chunk in message_chunks:
            await query.edit_message_text(text=chunk, reply_markup=reply_markup, parse_mode="HTML")
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
        res = await get_all_report()
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_chunks = send_long_message(res)
        for chunk in message_chunks:
            await query.edit_message_text(text=chunk, reply_markup=reply_markup, parse_mode="HTML")        
    elif query.data == '6':
        res, type = await get_all_history()
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if type == 'file':
            await query.message.reply_document(document=res, caption="Generate CSV file of history...\n\n", reply_markup=reply_markup)
        elif type == 'text':
            message_chunks = send_long_message(res)
            for chunk in message_chunks:
                await query.edit_message_text(text=chunk, reply_markup=reply_markup, parse_mode="HTML")        
        else:
            await query.edit_message_text(text=f"Error processing the response", reply_markup=reply_markup, parse_mode='HTML')     
    elif query.data == '7':
        res = await get_stats()
        res_capture = await get_stats_capture()
        if res_capture:
            for dt in res_capture:
                with open(dt, 'rb') as photo:
                    await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo)
                os.remove(dt)
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing stats...\n\n{res}", reply_markup=reply_markup, parse_mode="HTML")
    elif query.data == '8':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Changing password...", reply_markup=reply_markup)
    elif query.data == '9':
        res = await get_all_inventory_name()
        keyboard = []
        for dt in res:
            keyboard.append([InlineKeyboardButton(dt.inventory_name, callback_data='detail_inventory_'+dt.id)])
            
        keyboard.append([InlineKeyboardButton("Back", callback_data='back')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing inventory...", reply_markup=reply_markup)
    elif query.data.startswith('detail_inventory_'):
        inventory_id = query.data.split('_')[2]
        res, img_url = await get_detail_inventory(inventory_id)
        if img_url is not None:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=img_url)
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Inventory opened...\n\n{res}", reply_markup=reply_markup, parse_mode="HTML")
    elif query.data == '10':
        res = await get_dashboard()
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing dashboard...\n\n{res}", reply_markup=reply_markup, parse_mode="HTML")
    elif query.data == '11':
        res = await get_my_reminder()
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_chunks = send_long_message(res)
        for chunk in message_chunks:
            await query.edit_message_text(text=chunk, reply_markup=reply_markup, parse_mode="HTML")
    elif query.data == '0':
        await query.edit_message_text(text="Exiting bot...")
    elif query.data == 'back':
        await query.edit_message_text(text='What do you want:', reply_markup= main_menu_keyboard())

async def handle_photo(update: Update, context: CallbackContext):
    try:
        photo = update.message.photo[-1] 
        file = await photo.get_file()
        photo_path = f"received_photo_{update.message.message_id}.jpg"
        await file.download_to_drive(photo_path)
        res = await analyze_photo(photo_path)
        
        await update.message.reply_text(f"Photo successfully analyze...\n\n{res}", parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"Failed to analyze the photo: {str(e)}")
    finally:
        if os.path.exists(photo_path):
            os.remove(photo_path)

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
        [InlineKeyboardButton("10. Dashboard", callback_data='10')],
        [InlineKeyboardButton("11. My Reminder", callback_data='11')],

        [InlineKeyboardButton("0. Exit bot", callback_data='0')]
    ]
    return InlineKeyboardMarkup(keyboard)
