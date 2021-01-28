from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from json import dump
collector = {
    "name": "Aakash notes",
    "fid": "1xWGrreIOa69FpCXl0Z4fTIJzJ3dheik-",
    "flist": [],
    "Mathematics": {
        "fid": ""
    },
    "Chemistry": {
        "fid": ""
    },
    "Physics": {
        "fid": ""
    },
    "IPE": {
        "fid": ""
    },
    "Timetable": {
        "fid": ""
    },
    "Screenshots to be sorted": {
        "fid": ""
    }
}
list_folder = []
temp = []
list_subjects = []
folder_temp_list = []

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

def ListFolder(parent):
    filelist = []
    file_list = drive.ListFile({
        'q':
        "'%s' in parents and trashed=false" % parent
    }).GetList()
    for f in file_list:
        if f['mimeType'] == 'application/vnd.google-apps.folder':  # if folder
            filelist.append({
                "id": f['id'],
                "title": f['title'],
            })
    return filelist

def reset():
    for file in ListFolder(collector["fid"]):
        list_folder.append(file['title'])
        temp.append({
            "id": file['id'],
            "title": file['title'],
        })

def create_json():
    global tmp, folder_temp_list
    for i in temp:
        for y in collector:
            if y == i['title']:
                folder_temp_list.append(i['title'])

    if not collector['flist']:
        for item in folder_temp_list:
            collector['flist'].append(item)
    if collector['flist'] != folder_temp_list:
        collector['flist'] = folder_temp_list

    for i in temp:
        for j in collector:
            if i['title'] == j:
                collector[j]['fid'] = i['id']
                list_subjects.append(i['title'])

    for i in list_subjects:
        tmp = []
        for j in ListFolder(collector[i]['fid']):
            tmp.append(j)
        collector[i]['title'] = []
        collector[i]['id'] = []
        for k in tmp:
            collector[i]['title'].append(k['title'])
            collector[i]['id'].append(k['id'])

    with open('file.json', 'w') as write_file:
        dump(collector, write_file)
    print('done')


def upload_notes(name_file, id):
    file = drive.CreateFile({'parents': [{'id': id}]})
    file.SetContentFile(name_file)
    file.Upload()

