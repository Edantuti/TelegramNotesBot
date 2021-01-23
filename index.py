from telegram import *
from telegram.ext import *
from os import remove, path, environ
bot = Bot(environ.get("TOKEN"))

updater = Updater(environ.get("TOKEN"), use_context=True)
name = ""

dispatcher: Dispatcher = updater.dispatcher
print("hello")
def receive(update:Update,context: CallbackContext):
    global name
    print('Hello')
    print(update.message.document.file_id)
    print(update.message.document.file_name)
    file = bot.getFile(update.message.document.file_id)
    import time
    time.sleep(5)
    name = update.message.document.file_name
    print(name)
    file.download(name)
    print(name)
    time.sleep(10)
    print(name)
    upload_notes(name)
    move_files()
    bot.send_message(
      chat_id = update.effective_chat.id,
      text = "Done uploading",
      parse_mode = ParseMode.HTML
    )

def move_files():
    global name
    if path.exists(name):
      remove(name)

dispatcher.add_handler(MessageHandler(Filters.document, receive))
updater.start_polling()

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

auth = GoogleAuth()

auth.LoadCredentialsFile("creds.txt")
if auth.credentials is None:
    auth.GetFlow()
    auth.flow.params.update({'access_type': 'offline'})
    auth.flow.params.update({'approval_prompt': 'force'})
    auth.CommandLineAuth()
elif auth.access_token_expired:
    auth.Refresh()
else:
    auth.Authorize()

auth.SaveCredentialsFile('creds.txt')

drive = GoogleDrive(auth)
def upload_notes(name_file):
    file = drive.CreateFile({'parents':[{'id': "1xWGrreIOa69FpCXl0Z4fTIJzJ3dheik-"}]})
    file.SetContentFile(name_file)
    file.Upload()
