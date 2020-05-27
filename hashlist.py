import os
import hashlib

class hashlist(object):

    def __init__(self, cloud):
        self.name_hashlist = cloud + "hashlist.txt"

    def get_changes_list(self, path, new_hashlist):
        with open(path + '/' + self.name_hashlist, 'r') as f:
            hashlist = f.read().splitlines()
            changes = [x for x in new_hashlist if x not in hashlist]
        return changes


    def get_new_hashlist(self, files, path):
        new_hashlist = []
        self.set_line_new_hashlist(path, new_hashlist, files, "")
        return new_hashlist


    def set_line_new_hashlist(self, path, new_hashlist, files, prepath):
        for fl in files:
            try:
                with open(path + "/" + fl, 'rb') as f:
                    new_hashlist.append(prepath + fl + ":" + self.get_hash_md5(f))
            except:
                new_path = path + "/" + fl
                self.set_line_new_hashlist(new_path, new_hashlist, os.listdir(new_path), prepath + fl + "/")


    def set_hashlist(self, files, path):
        with open(path + '/' + self.name_hashlist, 'w') as h:
            self.set_new_line_in_hashlist(path, h, files, "")


    def set_new_line_in_hashlist(self, path, hashlist, files, prepath):
        for fl in files:
            try:
                with open(path + "/" + fl, 'rb') as f:
                    hashlist.write(prepath + fl + ":" + get_hash_md5(f) + "\n")
            except:
                new_path = path + "/" + fl
                self.set_new_line_in_hashlist(new_path, hashlist, os.listdir(new_path), prepath + fl + "/")
    

    def get_hash_md5(self, f):
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()