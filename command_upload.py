from hashlist import hashlist
class command_upload(object):

    def __init__(self, args):
        self.cloud = args.cloud
        self.result = ["Upload"]
        self.access_token = self.check_username(args.cloud + ":" + args.username)
        if self.access_token is None:
            self.result.append(False)
        else:
            self.upload(args.file_names, args.path)
            self.result.append(True)
        
    def upload(file_names, path):
        hashlist = hashlist(self.cloud)
    #Начать сессию
    #Закачивать файлы
    #Закрыть сессию


    def check_username(self, logname):
        with open("usertokenlist.txt", "r") as f:
            for line in f:
                if logname in line:
                    return line.split(':')[2]
        return None