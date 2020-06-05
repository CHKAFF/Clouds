import requests
import os
import re
import webbrowser


class dropbox:

    def __init__(self, args):
        longname = args.cloud + ":" + args.username
        self.access_token = self.check_username(longname)
        self.args = args

    def check_username(self, logname):
        with open("usertokenlist.txt", "r") as f:
            for line in f:
                if re.search(logname + ":", line) is not None:
                    return line.split(':')[2]
        return None

    def dir(self):
        self.result = ["Dir"]
        if self.args.cloud == 'dropbox':
            if self.access_token is None:
                self.result.append(False)
                return
            self.contain_dropbox(0, "")
            if len(self.result) != 2:
                self.result.append(True)
        return self.result

    def contain_dropbox(self, indentation, path):
        try:
            files = requests.post(
                'https://api.dropboxapi.com/2/files/list_folder',
                headers={"Authorization": "Bearer " + self.access_token,
                         "Content-Type": "application/json"},
                data="{\"path\": \"" + path + "\",\"recursive\": false,"
                                              "\"include_media_info\": false, "
                                              "\"include_deleted\": false,"
                                              "\"include_has_explicit_shared_members\": false, "
                                              "\"include_mounted_folders\": true,"
                                              "\"include_non_downloadable_files\": true}").json()
            for f in files['entries']:
                if f['.tag'] == 'folder':
                    self.result.append(
                        " " * indentation + 'FOLDER: ' + f['name'])
                    self.contain_dropbox(indentation + 4,
                                         path + "/" + f['name'])
                else:
                    self.result.append(" " * indentation + f['name'])
        except:
            self.result.append(False)

    def download(self):
        self.result = ["Download"]
        if self.access_token is None:
            self.result.append(False)
        else:
            self.load(self.args.file_names, self.args.path)
            self.result.append(True)
        return self.result

    def dload(self, file_names, path):
        for f in file_names:
            if os.path.isdir(path):
                files_in_directory = os.listdir(path)
            else:
                self.result.append(
                    [f, False, "Сбой. Неправильо указан путь для загрузки"])
                continue
            if f in files_in_directory:
                answer = input(
                    "\n" + f + "- Этот файл уже заходится в этой директории, "
                               "хотите перезаписать его?[Y/N]")
                if answer in ['y', 'Y']:
                    if os.path.isdir(path + "/" + f):
                        shutil.rmtree(path + "/" + f)
                    else:
                        os.remove(path + "/" + f)
                else:
                    self.result.append([f, False, "Загрузка отменена"])
                    continue
            if '.' not in f:
                files = []
                fls = requests.post(
                    'https://api.dropboxapi.com/2/files/list_folder',
                    headers={"Authorization": "Bearer " + self.access_token,
                             "Content-Type": "application/json"},
                    data="{\"path\": \"" "/" + f + "/" + "\",\"recursive\": false,\"include_media_info\": false,"
                                                         "\"include_deleted\": false,"
                                                         "\"include_has_explicit_shared_members\": false,"
                                                         "\"include_mounted_folders\": true,"
                                                         "\"include_non_downloadable_files\": true}").json()
                if 'error' in fls.keys():
                    self.result.append([f, False,
                        "Сбой. Неправильный путь к файлу или его имя"])
                    continue
                for e in fls['entries']:
                    files.append(f + "/" + e['name'])
                os.mkdir(path + "/" + f)
                self.result.append([f, False, "Folder"])
                self.load(files, path)
                continue
            r = requests.get(
                'https://content.dropboxapi.com/2/files/download',
                headers={
                        "Authorization": "Bearer " + self.access_token,
                        "Dropbox-API-Arg": "{\"path\": \"/" + f + "\"}"})
            if "error" in r.text:
                self.result.append(
                    [f, False, "Сбой. Неправильный путь к файлу или его имя"])
                continue
            try:
                with open(path + '/' + f, "wb") as code:
                    code.write(r.content)
                self.result.append([f, True])
            except Exception:
                self.result.append(
                    [f, False, "Сбой. Неправильо указан путь для загрузки"])

    def upload(self):
        self.result = ["Upload"]
        if self.access_token is None:
            self.result.append(False)
        else:
            self.uload(self.args.path, self.args.file_names)
            self.result.append(True)
        return self.result

    def uload(self, path, file_paths):
        for p in file_paths:
            if p.rfind('\\') < p.rfind('/'):
                i = p.rfind('/')
            else:
                i = p.rfind('\\')
            if os.path.isdir(p):
                files = os.listdir(p)
                for j in range(len(files)):
                    files[j] = p + "\\" + files[j]
                self.uload("/" + p[i + 1:] + "/", files)
                continue
            if not os.path.isfile(p):
                self.result.append(
                    [p, "Файла или Дирректории не существует", False])
                continue
            name = p[i + 1:]
            fg = False
            flag = "false"
            if path in ['/', '\\']:
                path = ""
            d = dropbox(self.args).dir()[:-1]
            for dr in d:
                if name == dr:
                    answer = input(
                        p + '- уже был загружен на облако. Хотите загрузить '
                            'его повторно[Y/N]')
                    if answer in ['y', 'Y']:
                        answer = input(
                            'Перезапистать его - Y, Создать копию - N: ')
                        if answer not in ['y', 'Y']:
                            flag = 'true'
                    else:
                        self.result.append([p, "Отмена", False])
                        fg = True
                        break
            if fg:
                continue
            try:
                fls = requests.post(
                    'https://content.dropboxapi.com/2/files/upload',
                    headers={
                        "Authorization": "Bearer " + self.access_token,
                        "Dropbox-API-Arg": "{\"path\": \"/" + name + "\",\"mode\": \"add\",\"autorename\": true,\"mute\": false,\"strict_conflict\": " + flag + "}",
                        "Content-Type": "application/octet-stream"},
                    data=p)
                self.result.append([p, True])
            except:
                self.result.append([p, False, "Ошибка при загрузке"])
