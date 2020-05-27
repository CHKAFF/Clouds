import requests
import sys
import os
import hashlib
from console_write import console_write
from class_help import help_parser
from command_dir import command_dir
from command_reg import command_reg
from command_list import command_list
from command_download import command_download
from command_upload import command_upload

def main(args):
    command = sys.argv[1:][0]
    result = []
    if command == "list":
        command_list(args)
    elif command == "dir":
        result = command_dir(args).result
    elif command == "reg":
        result = command_reg(args).result
    elif command == "download":
        result = command_download(args).result
    elif command == "upload":
        result = command_upload(args).result 
    return result



if __name__ == '__main__':
    parser = help_parser().parser
    args = parser.parse_args(sys.argv[1:])
    if not args.command:
        sys.exit("Обратитесь за справкой: python cloud.py [-h]")
    console = console_write(main(parser.parse_args(sys.argv[1:]))).write()
