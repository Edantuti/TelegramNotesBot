from telegram import *
from telegram.ext import *
from os import remove, environ
import time
from drive import upload_notes


bot = Bot(token=environ.get('TOKEN'))

updater = Updater(environ.get('TOKEN'), use_context=True)

dispatcher = updater.dispatcher

list_of_subject={
    "Mathematics": "1xmuRL0aA-Eq5V0ajZKvv-Pmp9IU1l7sq",
    "Chemistry": "1x_vj-5G7DxAHeVlMOoIfNRogK3kom3Fq",
    "Physics": "1xboUnEtB8sZkLU3YzmLPT9thnomKs6bC",
    "IPE": "1-4m4Xp43UwecwvpLJrGLbgZxucX_orJL",
}

folder_id = ""

def error(update, context):
    print(context.error)

def start(update, context):
    update.message.reply_text('Hi!')

def delete_files(name_file):
    remove(name_file)

def button(update: Update, context:CallbackContext):
    global folder_id
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")
    folder_id = list_of_subject[query.data]

#query selector

def folderSelector(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Mathematics", callback_data="Mathematics"),
            InlineKeyboardButton("Physics", callback_data="Physics"),
        ],
        [
            InlineKeyboardButton("Chemistry", callback_data="Chemistry"),
            InlineKeyboardButton("IPE", callback_data="IPE"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose: ", reply_markup=reply_markup)

#upload function

def upload(update:Update, context:CallbackContext):
    global folder_id
    if(folder_id == ""):
        bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="Please select a particular folder and send then photo.",
            parse_mode=ParseMode.HTML
        )
        return None

    try:
        name = update.message.document.file_name
        file = bot.getFile(update.message.document.file_id)
        file.download(name)
        time.sleep(5)
        bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="Done uploading",
            parse_mode=ParseMode.HTML
        )
        upload_notes(name, folder_id)
        delete_files(name)

    except(AttributeError, TypeError):
        name = update.message.photo[2].file_id + ".jpg"
        file = bot.getFile(update.message.photo[2].file_id)
        file.download(name)
        time.sleep(5)
        upload_notes(name, folder_id)
        delete_files(name)
        bot.sendMessage(
            chat_id=update.effective_chat.id,
            text = "Done uploading",
            parse_mode= ParseMode.HTML,
        )

#Handler for variety
dispatcher.add_handler(CommandHandler("start", start)) #To check whether the bot is online
dispatcher.add_handler(CommandHandler("select", folderSelector)) #To Select the folder
dispatcher.add_handler(MessageHandler(Filters.document, upload))#To upload the document
dispatcher.add_handler(MessageHandler(Filters.photo, upload))#to upload the photo
dispatcher.add_handler(CallbackQueryHandler(button))#query selector handler
dispatcher.add_error_handler(error)#error handler

updater.start_polling()
updater.idle()
