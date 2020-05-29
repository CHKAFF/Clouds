import os
import hashlib
from hashlist import hashlist
class command_list(object):

    def __init__(self, args, path):
        self.result = ['List', path]
        h = hashlist(args.cloud)
        try:
            files = os.listdir(path)
        except:
            self.result.append(0)
            self.result.append(False)
            return
        if h.name_hashlist not in files:
            h.set_hashlist([], path)
            new_hashlist = []
            h.set_line_new_hashlist(path, new_hashlist, files, "")
            for f in new_hashlist:
                self.result.append(f.split(':')[0])
        else:
            files.remove(h.name_hashlist)
            new_hashlist = h.get_new_hashlist(files, path)
            changes = h.get_changes_list(path, new_hashlist)
            if len(changes) == 0:
                self.result.append(1)
                self.result.append(False)
                return
            else:
                for change in changes:
                    self.result.append(change.split(':')[0])
        self.result.append(True)