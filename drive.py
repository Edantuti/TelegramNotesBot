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

def upload_notes(name_file, id):
    file = drive.CreateFile({'parents': [{'id': id}]})
    file.SetContentFile(name_file)
    file.Upload()

