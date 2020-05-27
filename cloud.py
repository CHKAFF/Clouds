import requests
import sys
import os
import hashlib
from console_write import console_write
from class_help import help_parser
from command_reg import command_reg
from command_list import command_list
from dropbox import dropbox

def main(args):
    command = sys.argv[1:][0]
    result = []
    if command == "list":
        result = command_list(args).result
    elif command == "reg":
        result = command_reg(args).result
    else:
        cloud = dropbox(args)
    if command == "dir":
        result = cloud.dir()
    elif command == "download":
        result = cloud.download()
    elif command == "upload":
        result = cloud.upload()
    return result



if __name__ == '__main__':
    parser = help_parser().parser
    args = parser.parse_args(sys.argv[1:])
    if not args.command:
        sys.exit("Обратитесь за справкой: python cloud.py [-h]")
    console = console_write(main(parser.parse_args(sys.argv[1:]))).write()
