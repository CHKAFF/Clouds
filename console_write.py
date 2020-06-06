class console_write:

    def __init__(self, parameter_list):
        self.parameter_list = parameter_list

    def write(self):
        if self.parameter_list == []:
            return
        commands = {
            "Reg": self.command_reg,
            "Dir": self.command_dir,
            "List": self.command_list,
            "Download": self.command_download,
            "Upload": self.command_upload}
        commands[self.parameter_list[0]]()
        print("---------------------")

    def command_upload(self):
        print("---------------------")
        print("Upload(Dropbox)")
        print("---------------------")
        if self.parameter_list[-1]:
            for f in self.parameter_list[1:-1]:
                if f[1]:
                    print(f[0] + " | Успешно!")
                else:
                    print(f[0] + " | " + f[-1])
        else:
            print("Сбой. Пользователя с такким именем не существет.")

    def command_download(self):
        print("---------------------")
        print("Download(Dropbox)")
        print("---------------------")
        if self.parameter_list[-1]:
            for f in self.parameter_list[1:-1]:
                if f[1]:
                    print(f[0] + " | Успешно!")
                else:
                    print(f[0] + " | " + f[2])
        else:
            print("Сбой. Пользователя с такким именем не существет.")


    def command_dir(self):
        print("Dropbox:")
        print("---------------------")
        if self.parameter_list[-1]:
            for e in self.parameter_list[1:-1]:
                print(e)
        else:
            print("Ошибка:")
            print('''    Пользователя с такким именем не существет.
            Попробуйте зараегистрировться ещё раз(Справка: python cloud.py reg -h)''')

    def command_list(self):
        print("---------------------")
        print("Каталог: " + self.parameter_list[1])
        print("---------------------")
        if self.parameter_list[-1]:
            for p in self.parameter_list[2:-1]:
                print(p)
        else:
            if self.parameter_list[-2] == 1:
                print("В каталоге нет изменений")
            else:
                print("Данного каталога не существует")

    def command_reg(self):
        print("---------------------")
        print("Reg:")
        print("---------------------")
        if self.parameter_list[-1]:
            print("Успешно!")
        else:
            print("Пользователь с таким ником уже существует")

    