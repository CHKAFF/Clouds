import requests
import sys
import os
import hashlib
import argparse
from paint import console_write
from class_help import help_parser
from command_dir import command_dir
from command_reg import command_reg
from enum import Enum

def main(args):
    command = sys.argv[1:][0]
    result = []
    if command == "list":
        command_list(args)
    elif command == "dir":
        result = command_dir(args).result
    elif command == "reg":
        result = command_reg(args).result
    return result

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
    parser = help_parser().parser
    args = parser.parse_args(sys.argv[1:])
    if not args.command:
        sys.exit("Обратитесь за справкой: python program.py [-h]")
    console = console_write(main(parser.parse_args(sys.argv[1:])))
    console.write()
