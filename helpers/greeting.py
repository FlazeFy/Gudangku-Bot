from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackContext
import os
import pandas as pd

# Services
from helpers.typography import send_long_message
from helpers.generator import generate_csv_template
from services.module.inventory.inventory_queries import get_all_inventory, get_all_inventory_name, get_detail_inventory
from services.module.history.history_queries import get_all_history
from services.module.report.report_queries import get_all_report
from services.module.stats.stats_queries import get_stats, get_dashboard
from services.module.reminder.reminder_queries import get_my_reminder
from services.module.stats.stats_capture import get_stats_capture
from services.module.image_processing.load import analyze_photo
from services.module.inventory.inventory_commands import post_inventory_query

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
    elif query.data == '3':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        template_inventory_add = generate_csv_template(type='Add Inventory',
            fields_name=['inventory_name', 'inventory_category', 'inventory_desc', 'inventory_merk', 'inventory_room', 'inventory_storage', 
                         'inventory_rack', 'inventory_price', 'inventory_unit', 'inventory_vol', 'inventory_capacity_unit', 
                         'inventory_capacity_vol', 'is_favorite'])
        await query.message.reply_document(document=template_inventory_add, 
            caption=(
                f"Generate CSV form of create inventory...\n\n"
                f"Rules to follow :\n"
                f" - name, category, room, price, unit, volume, is favorite is a mandatory field\n"
                f" - price, volume, and capacity volume must be numeric only and equal or more than 1 for the value\n"
                f" - is favorite must be 0 if the inventory is not favorite and 1 if the inventory is favorited\n"
            ))
        await query.edit_message_text(text="Fill this form below and send back to me when you want to submit it...", reply_markup=reply_markup)
    elif query.data == '4':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Updating inventory...", reply_markup=reply_markup)
    elif query.data == '5':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Deleting inventory...", reply_markup=reply_markup)
    elif query.data == '6':
        res = await get_all_report()
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message_chunks = send_long_message(res)
        for chunk in message_chunks:
            await query.edit_message_text(text=chunk, reply_markup=reply_markup, parse_mode="HTML")        
    elif query.data == '7':
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
    elif query.data == '8':
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
    elif query.data == '9':
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Changing password...", reply_markup=reply_markup)
    elif query.data == '2':
        res = await get_all_inventory_name()
        keyboard = []
        for dt in res:
            keyboard.append([InlineKeyboardButton(dt.inventory_name, callback_data='detail_inventory_'+dt.id)])
            
        keyboard.append([InlineKeyboardButton("Back", callback_data='back')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Showing inventory...", reply_markup=reply_markup)
    elif query.data.startswith('detail_inventory_'):
        inventory_id = query.data.split('_')[2]
        res, img_url, file = await get_detail_inventory(inventory_id)
        if img_url is not None:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=img_url)
        if file is not None:
            await context.bot.send_document(chat_id=query.message.chat_id, filename=file.name, document=file)
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

async def handle_file(update: Update, context: CallbackContext):
    try:
        doc = update.message.document
        file = await doc.get_file()
        file_name = doc.file_name
        file_ext = os.path.splitext(file_name)[1].replace('.','')
        if file_ext == 'csv':
            doc_path = f"received_file_{doc.file_name}"
            await file.download_to_drive(doc_path)
            # A2:N2 => [1:2, 0:14]
            df = pd.read_csv(doc_path)
            # range = df.iloc[1:2, 0:14]
            list_val = df.iloc[0:].values  
            value_data = 'Data 1 :\n'
            for idx, inventories in enumerate(list_val):
                # for dt in inventories:
                #     value_data += f"{dt}\n"
                data = {
                    'inventory_name': inventories[0],
                    'inventory_category': inventories[1],
                    'inventory_desc': inventories[2] if inventories[2].strip() != "" else None,
                    'inventory_merk': inventories[3] if inventories[3].strip() != "" else None,
                    'inventory_room': inventories[4],
                    'inventory_storage': inventories[5] if inventories[5].strip() != "" else None,
                    'inventory_rack': inventories[6] if inventories[6].strip() != "" else None,
                    'inventory_price': inventories[7],
                    'inventory_unit': inventories[8],
                    'inventory_vol': inventories[9],
                    'inventory_capacity_unit': inventories[10] if inventories[10].strip() != "" else None,
                    'inventory_capacity_vol': inventories[11] if inventories[11] != "" else None,
                    'is_favorite': inventories[12],
                    'created_by': '2d98f524-de02-11ed-b5ea-0242ac120002',
                }
                await post_inventory_query(data=data)
                value_data += f"\nData ${idx} :\n"

            await update.message.reply_document(
                document=doc, 
                caption=f"The inventory has been added. Here's the previous CSV with updated columns for success insert:\n\n"
            ) 
        else:
            await update.message.reply_text(text=f"Your file is not compatible for me to handle")
    except Exception as e:
        await update.message.reply_text(f"Failed to analyze the file: {str(e)}")
    finally:
        if os.path.exists(doc_path):
            os.remove(doc_path)
        
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
        [InlineKeyboardButton("2. Detail inventory", callback_data='2')],
        [InlineKeyboardButton("3. Add inventory", callback_data='3')],
        [InlineKeyboardButton("4. Update inventory", callback_data='4')],
        [InlineKeyboardButton("5. Delete inventory", callback_data='5')],
        [InlineKeyboardButton("6. Show report", callback_data='6')],
        [InlineKeyboardButton("7. Show history", callback_data='7')],
        [InlineKeyboardButton("8. Show stats", callback_data='8')],
        [InlineKeyboardButton("9. Change password", callback_data='9')],
        [InlineKeyboardButton("10. Dashboard", callback_data='10')],
        [InlineKeyboardButton("11. My Reminder", callback_data='11')],

        [InlineKeyboardButton("0. Exit bot", callback_data='0')]
    ]
    return InlineKeyboardMarkup(keyboard)
