import requests
import sys
import os
import hashlib
import argparse
from paint import paint
from class_help import help_parser

def main(args):
    command = sys.argv[1:][0]
    if command == "list":
        command_list(args)
    elif command == "dir":
        command_dir(args)
    elif command == "reg":
        command_reg(args)
    print("---------------------")


def command_reg(args):
    print("Reg:")
    print("---------------------")
    if check_username(args.cloud + ":" + args.username) is not None:
        print("Пользователь с таким ником уже существует")
        return
    with open("usertokenlist.txt", "a") as f:
        f.write('\n' + args.cloud + ":" + args.username + ":" + args.token)
        print("Успешно!")


def check_username(logname):
    with open("usertokenlist.txt", "r") as f:
        for line in f:
            if logname in line:
                return line.split(':')[2]
    return None


def command_dir(args):
    if args.cloud == 'dropbox':
        print("Dropbox:")
        print("---------------------")
        token = check_username(args.cloud + ":" + args.username_or_access_token)
        if token is None:
            token = args.username_or_access_token
        print_contain_dropbox(token, 0, "")


def print_contain_dropbox(access_token, indentation, path):
    try:
        files = requests.post('https://api.dropboxapi.com/2/files/list_folder',
                              headers={"Authorization": "Bearer " + access_token, "Content-Type": "application/json"},
                              data="{\"path\": \"" + path + "\",\"recursive\": false,\"include_media_info\": false,"
                                                            "\"include_deleted\": false,"
                                                            "\"include_has_explicit_shared_members\": false,"
                                                            "\"include_mounted_folders\": true,"
                                                            "\"include_non_downloadable_files\": true}").json()
        for f in files['entries']:
            if f['.tag'] == 'folder':
                print(" " * indentation + 'FOLDER: ' + f['name'])
                print_contain_dropbox(access_token, indentation + 4, path + "/" + f['name'])
            else:
                print(" " * indentation + f['name'])
    except:
        print("Ошибка:")
        print("    Недействительный access_token")
        return


def command_list(args):
    name_hashlist = args.cloud + "hashlist.txt"
    for path in args.paths:
        print("---------------------")
        print("Каталог: " + path)
        print("---------------------")
        try:
            files = os.listdir(path)
        except:
            print("Данного каталога не существуе")
            continue
        if name_hashlist not in files:
            set_hashlist([], path, name_hashlist)
            new_hashlist = []
            set_line_new_hashlist(path, new_hashlist, files, "")
            for f in new_hashlist:
                print(f.split(':')[0])
        else:
            files.remove(name_hashlist)
            new_hashlist = get_new_hashlist(files, path)
            changes = get_changes_list(path, new_hashlist, name_hashlist)
            if len(changes) == 0:
                print("В каталоге нет изменений.")
            else:
                for change in changes:
                    print(change.split(':')[0])


def get_changes_list(path, new_hashlist, name_hashlist):
    f = open(path + '/' + name_hashlist, 'r')
    hashlist = f.read().splitlines()
    changes = [x for x in new_hashlist if x not in hashlist]
    f.close()
    return changes


def get_new_hashlist(files, path):
    new_hashlist = []
    set_line_new_hashlist(path, new_hashlist, files, "")
    return new_hashlist


def set_line_new_hashlist(path, new_hashlist, files, prepath):
    for fl in files:
        try:
            with open(path + "/" + fl, 'rb') as f:
                new_hashlist.append(prepath + fl + ":" + get_hash_md5(f))
        except:
            new_path = path + "/" + fl
            set_line_new_hashlist(new_path, new_hashlist, os.listdir(new_path), prepath + fl + "/")


def set_hashlist(files, path, name_hashlist):
    hashlist = open(path + '/' + name_hashlist, 'w')
    set_new_line_in_hashlist(path, hashlist, files, "")
    hashlist.close()


def set_new_line_in_hashlist(path, hashlist, files, prepath):
    for fl in files:
        try:
            with open(path + "/" + fl, 'rb') as f:
                hashlist.write(prepath + fl + ":" + get_hash_md5(f) + "\n")
        except:
            new_path = path + "/" + fl
            set_new_line_in_hashlist(new_path, hashlist, os.listdir(new_path), prepath + fl + "/")


def get_hash_md5(f):
    m = hashlib.md5()
    while True:
        data = f.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

if __name__ == '__main__':
    args = help_parser().parser.parse_args(sys.argv[1:])
    if not args.command:
        sys.exit("Обратитесь за справкой: python program.py [-h]")
    main(parser.parse_args(sys.argv[1:]))
