class command_reg(object):

    def __init__(self, args):
        if self.check_username(args.cloud + ":" + args.username) is not None:
            self.result = ["Reg", False]
        else:
            with open("usertokenlist.txt", "a") as f:
                f.write('\n' + args.cloud + ":" + args.username + ":" + args.token)
            self.result = ["Reg", True]

    def check_username(self, logname):
        with open("usertokenlist.txt", "r") as f:
            for line in f:
                if logname in line:
                    return line.split(':')[2]
        return None