from hashlist import hashlist
from command_list import command_list
class command_upload(object):

    def __init__(self, args, access_token):
        self.cloud = args.cloud
        self.result = ["Upload"]
        self.access_token = access_token
        if self.access_token is None:
            self.result.append(False)
        else:
            self.upload(args.file_names, args.file_names)
            self.result.append(True)
        
    def upload(file_names, file_paths):
        for path in file_paths:
            h = hashlist(self.cloud)
        #папка или не папка выбрать путь
        #command_list
            result = command_list(args).result
            if result[-1]:
                pass
            elif result[-2] == 1:
                answer = input(path + ' - уже были загружена на облако. Хотите загрузить его повторно[Y/N]')
            else:
                pass
                    #Начать сессию
                    #Закачивать файлы
                    #Закрыть сессию
    #Начать сессию
    #Закачивать файлы
    #Закрыть сессию