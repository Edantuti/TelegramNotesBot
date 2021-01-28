from telegram import *
from telegram.ext import *
from os import remove, environ
import emoji
import time
from drive import *
from json import load

bot = Bot("1510119990:AAHtBtwdj2yozGsTuMTRvQZszrmQecBxdzA")

updater = Updater("1510119990:AAHtBtwdj2yozGsTuMTRvQZszrmQecBxdzA", use_context=True)

dispatcher = updater.dispatcher

file_json = load(open('file.json'))
option_id = ""

folder_id = ""

folder_list = file_json['flist']

end = emoji.emojize(':no_entry:')
thumbs_emoji = emoji.emojize(':thumbs_up:')

FIRST, SECOND = range(2)


def start(update, context):
    update.message.reply_text('Hi!')


def delete_files(name_file):
    remove(name_file)


def error(update, context):
    print(context.error)


def update_json(update, context):
    global option_id, file_json
    option_id = ""
    reset()
    create_json()
    file_json = load(open('file.json'))
    update.message.reply_text("Done!")

def folder_selector(update, context):

    keyboard = [[InlineKeyboardButton(i, callback_data=i)] for i in folder_list]
    keyboard[len(keyboard)-1].append(InlineKeyboardButton(end, callback_data="exit"))
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose the Folder: ", reply_markup=reply_markup)
    return FIRST


def folder(update, context):
    global option_id, end, folder_id
    query = update.callback_query
    query.answer()
    if query.data == 'exit':
        option_id = file_json['fid']
        query.edit_message_text(text=f"Thank you for selecting the option. {thumbs_emoji}")
        return ConversationHandler.END
    elif file_json[query.data]['title']:
        folder_id = file_json[query.data]['fid']
        keyboard = [
            [InlineKeyboardButton(file_json[query.data]['title'][i], callback_data=file_json[query.data]['id'][i])] for
            i in range(len(file_json[query.data]['title']))]
        keyboard[len(keyboard)-1].append(InlineKeyboardButton(end, callback_data="exit"))
    else:
        query.edit_message_text(text=f"Thank you for selecting the option. {thumbs_emoji}")
        option_id = file_json[query.data]['fid']
        return ConversationHandler.END
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=f"The option you selected: {query.data}", reply_markup=reply_markup)
    return SECOND


def id_selector(update, context):
    global option_id, folder_id
    query = update.callback_query
    query.answer()
    if query.data == 'exit':
        option_id = folder_id
        query.edit_message_text(text=f"Thank you for selecting the option. {thumbs_emoji}")
        return ConversationHandler.END
    option_id = query.data
    query.edit_message_text(text=f"Thank you for selecting the option. {thumbs_emoji}")
    return ConversationHandler.END


def upload(update: Update, context: CallbackContext):
    global option_id
    if option_id == "":
        bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="Please select a particular folder and then send the photo. ",
            parse_mode=ParseMode.HTML
        )
        return None

    try:
        name = update.message.document.file_name
        file = bot.getFile(update.message.document.file_id)
        file.download(name)
        time.sleep(5)
        upload_notes(name, option_id)
        delete_files(name)
        bot.sendMessage(
            chat_id=update.effective_chat.id,
            text="Done uploading",
            parse_mode=ParseMode.HTML
        )

    except(AttributeError, TypeError):
        try:
            name = update.message.photo[2].file_id + ".jpg"
            file = bot.getFile(update.message.photo[2].file_id)
            file.download(name)
            time.sleep(5)
            upload_notes(name, option_id)
            delete_files(name)
            bot.sendMessage(
                chat_id=update.effective_chat.id,
                text="Done uploading",
                parse_mode=ParseMode.HTML,
            )
        except(IndexError):
            name = update.message.photo[0].file_id + ".jpg"
            file = bot.getFile(update.message.photo[0].file_id)
            file.download(name)
            time.sleep(5)
            upload_notes(name, option_id)
            delete_files(name)
            bot.sendMessage(
                chat_id=update.effective_chat.id,
                text="Done uploading",
                parse_mode=ParseMode.HTML,
            )


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('upload', folder_selector)],
    states={
        FIRST: [
            CallbackQueryHandler(folder),
        ],
        SECOND: [
            CallbackQueryHandler(id_selector)
        ]
    },
    fallbacks=[CommandHandler('upload', folder_selector)],
    per_message=False
)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('update', update_json))
dispatcher.add_handler(MessageHandler(Filters.document, upload))
dispatcher.add_handler(MessageHandler(Filters.photo, upload))
dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
