import requests
import argparse
import sys
import os
import hashlib
from console_write import console_write
from dropbox import dropbox


def main(args):
    command = sys.argv[1:][0]
    result = []
    if command == "list":
        result = command_list(args)
    elif command == "reg":
        result = reg(args)
    else:
        cloud = dropbox(args)
        commands = {"dir": cloud.dir, "download": cloud.download, "upload": cloud.upload}
        result = commands[command]()
    return result


def command_list(self, args):
    path = args.path
    result = ['List', path]
    h = hashlist(args.cloud)
    if not os.path.isdir(path):
        result.append(0)
        result.append(False)
        return result
    files = os.listdir(path)
            
    if h.name_hashlist not in files:
        h.set_hashlist([], path)
        new_hashlist = []
        h.set_line_new_hashlist(path, new_hashlist, files, "")
        for f in new_hashlist:
            result.append(f.split(':')[0])
    else:
        files.remove(h.name_hashlist)
        new_hashlist = h.get_new_hashlist(files, path)
        changes = h.get_changes_list(path, new_hashlist)
        if not changes:
            result.append(1)
            result.append(False)
            return result
        else:
            for change in changes:
                result.append(change.split(':')[0])
    result.append(True)
    return result


def reg(args):
    if check_username(args.cloud + ":" + args.username) is not None:
        result = ["Reg", False]
    else:
        webbrowser.open("https://www.dropbox.com/oauth2/authorize?client_id=pkrfs6p9e5s3u84&response_type=code")
        authorization_code = input("Введите код полученый при авторизации: ")
        r = requests.post("https://api.dropboxapi.com/oauth2/token", data={
                "code": authorization_code,
                "grant_type": "authorization_code",
                "client_id": "pkrfs6p9e5s3u84",
                "client_secret": "ai2b1ab0e87nak6"
                }).json()
        with open("usertokenlist.txt", "a") as f:
                f.write('\n' + args.cloud + ":" + args.username + ":" + r['access_token'])
        result = ["Reg", True]
    return result

def check_username(self, logname):
    with open("usertokenlist.txt", "r") as f:
        for line in f:
            if logname in line:
                return line.split(':')[2]
    return None


def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    reg_parser = subparsers.add_parser(
        "reg", 
        help="Позволяет запомнить токен и использовать его дальше при помощи указанного имени")
    reg_parser.add_argument(
        'cloud', action='store', 
        help="Сloud name", choices=['dropbox'])
    reg_parser.add_argument(
        'username', action='store', 
        help="Имя пользователя которое будет использоваться при работе в приложении")

    list_parser = subparsers.add_parser(
        "list", 
        help="Возвращает список файлов, которые изменились после последней загрузки в облако")
    list_parser.add_argument(
        'cloud', action='store', 
        help="Сloud name", choices=['dropbox'])

    list_parser.add_argument('path', help="Path to catalog or file")

    dir_parser = subparsers.add_parser("dir", help="Возвращает файлы, расположенные в облаке")
    dir_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
    dir_parser.add_argument('username', action='store', help="Имя пользователя указаное при Reg")

    download_parser = subparsers.add_parser("download", help="Позволяет скачать файлы или папки из облака")
    download_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
    download_parser.add_argument('username', action='store', help="Имя пользователя указаное при Reg")
    download_parser.add_argument('path', action='store', help="Путь на диске, куда вы хотите загрузить файлы")
    download_parser.add_argument(
        'file_names', 
        help="Название файлов которые вы хотите загрузить(Если файл находится в папке, то укажите путь. Пример: папка/имя_файла)", 
        nargs='+')

    upload_parser = subparsers.add_parser("upload", help="Позволяет загрузить файл или папки на облако")
    upload_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
    upload_parser.add_argument('username', action='store', help="Имя пользователя указаное при Reg")
    upload_parser.add_argument(
        'path', 
        action='store', 
        help="Путь на облаке куда нужно загрузить загрузить файлы(Если вы хотите загрузить в корень, то напишите '/')")
    upload_parser.add_argument('file_names', help="Пути к файлам на диске, которые вы хотите загрузить", nargs='+')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if not args.command:
        sys.exit("Обратитесь за справкой: python cloud.py [-h]")
    output_date = main(args)
    console = console_write(output_date).write()
