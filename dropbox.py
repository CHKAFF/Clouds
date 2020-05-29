from command_dir import command_dir
from command_reg import command_reg
from command_list import command_list
from command_download import command_download
from command_upload import command_upload
import re

class dropbox(object):
    
    def __init__(self, args):
        self.access_token = self.check_username(args.cloud + ":" + args.username)
        self.args = args

    def check_username(self, logname):
        with open("usertokenlist.txt", "r") as f:
            for line in f:
                if re.search(logname+":", line) != None:
                    return line.split(':')[2]
        return None
    
    def dir(self):
        return command_dir(self.args, self.access_token, "").result

    def download(self):
        return command_download(self.args, self.access_token).result

    def upload(self):
        return command_upload(self.args, self.access_token).result
