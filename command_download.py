import requests
import os
import shutil

class command_download(object):

    def __init__(self, args, access_token):
        self.result = ["Download"]
        self.access_token = access_token
        if self.access_token is None:
            self.result.append(False)
        else:
            self.download(args.file_names, args.path)
            self.result.append(True)

    
    def download(self, file_names, path):
        for f in file_names:
            try:
                files_in_directory = os.listdir(path)
            except:
                self.result.append([f, False, "Сбой. Неправильо указан путь для загрузки"])
                continue
            try:
                if f in files_in_directory:
                    answer = input("\n" + f + " - Этот файл уже заходится в этой директории, хотите перезаписать его?[Y/N]")
                    if answer == "y" or "Y":
                        os.remove(path + "/" + f)
                    else:
                        continue
            except:
                shutil.rmtree(path + "/" + f)
            if '.' not in f:
                files = []
                fls = requests.post('https://api.dropboxapi.com/2/files/list_folder',
                                headers={"Authorization": "Bearer " + self.access_token, "Content-Type": "application/json"},
                                data="{\"path\": \"" "/"+ f + "/" + "\",\"recursive\": false,\"include_media_info\": false,"
                                                                "\"include_deleted\": false,"
                                                                "\"include_has_explicit_shared_members\": false,"
                                                                "\"include_mounted_folders\": true,"
                                                                "\"include_non_downloadable_files\": true}").json()
                for e in fls['entries']:
                    files.append(f+ "/" + e['name'])
                os.mkdir(path+"/"+f)
                self.result.append([f,False, "Folder"])
                self.download(files,path)
                continue
            r = requests.get('https://content.dropboxapi.com/2/files/download',
                                headers={"Authorization": "Bearer " + self.access_token, "Dropbox-API-Arg": "{\"path\": \"/" + f + "\"}"})
            if "error" in r.text:
                self.result.append([f, False, "Сбой. Неправильный путь к файлу или его имя"])
                continue
            try:
                with open(path + '/' + f, "wb") as code:
                    code.write(r.content)
                self.result.append([f, True])
            except:
                self.result.append([f, False, "Сбой. Неправильо указан путь для загрузки"])
