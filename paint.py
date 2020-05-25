class console_write(object):

    def __init__(self, parameter_list):
        self.parameter_list = parameter_list

    def write(self):
        command = self.parameter_list[0]
        if command == "Reg":
            self.command_reg(self.parameter_list[1])
        elif command == "Dir":
            self.command_dir(self.parameter_list[-1])
        print("---------------------")

    def command_dir(self, answer):
        print("Dropbox:")
        print("---------------------")
        if answer:
            pass
        else:
            print("Ошибка:")
            print("    Недействительный access_token")

    def command_list(self):
        pass

    def command_reg(self, answer):
        print("Reg:")
        print("---------------------")
        if answer:
            print("Успешно!")
        else:
            print("Пользователь с таким ником уже существует")

    