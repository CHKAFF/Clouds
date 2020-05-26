import requests
import webbrowser
class command_reg(object):

    def __init__(self, args):
        if self.check_username(args.cloud + ":" + args.username) is not None:
            self.result = ["Reg", False]
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
            self.result = ["Reg", True]

    def check_username(self, logname):
        with open("usertokenlist.txt", "r") as f:
            for line in f:
                if logname in line:
                    return line.split(':')[2]
        return None