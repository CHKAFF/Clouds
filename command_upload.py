from hashlist import hashlist
from command_list import command_list
from command_dir import command_dir
import requests
import os
class command_upload(object):

    def __init__(self, args, access_token):
        self.args = args
        self.cloud = args.cloud
        self.result = ["Upload"]
        self.access_token = access_token
        if self.access_token is None:
            self.result.append(False)
        else:
            self.upload(args.path, args.file_names)
            self.result.append(True)
        
    def upload(self, path, file_paths):
        for p in file_paths:
            i = p.rfind('\\')
            try:
                files = os.listdir(p)
                for j in range(len(files)):
                    files[j] = p+"\\"+files[j]
                self.upload("/"+p[i+1:]+"/", files)
                continue
            except:
                try:
                    with open(p, "rb") as g:
                        pass
                except:
                    self.result.append([p, "Файла или Дирректории не существует", False])
                    continue
            name = p[i+1:]
            fg = False
            flag = "true"
            if path == "/" or path == "\\":
                path = ""
            d = command_dir(self.args, self.access_token, path).result[:-1]
            for dr in d:
                if name in dr:
                    answer = input(p + '- уже был загружен на облако. Хотите '
                                       'загрузить его повторно[Y/N]')
                    if answer == "Y" or answer == "y":
                        answer = input('Перезапистать его - Y, Создать копию '
                                       '- N: ')
                        if answer == "Y" or answer == "y":
                            flag = "false"
                        else:
                            flag = "true"
                    else:
                        self.result.append([p, "Отмена", False])
                        fg = True
                        break
            if fg:
                continue
            try:
                fls = requests.post('https://content.dropboxapi.com/2/files/upload',
                                headers={"Authorization": "Bearer " + self.access_token,
                                "Dropbox-API-Arg": "{\"path\": \""+path+name+"\",\"mode\": \"add\",\"autorename\": true,\"mute\": false,\"strict_conflict\": "+flag+"}",
                                "Content-Type": "application/octet-stream"},
                                data=p)
                self.result.append([p, True])
            except:
                self.result.append([p, False, "Ошибка при загрузке"])