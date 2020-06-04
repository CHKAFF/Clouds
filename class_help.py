import argparse

class help_parser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(dest="command")

        reg_parser = subparsers.add_parser("reg",
                                           help="Позволяет запомнить токен и "
                                                "использовать его дальше при "
                                                "помощи "
                                                "указанного имени")
        reg_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
        reg_parser.add_argument('username', action='store', help="Имя пользователя которое будет использоваться при работе в приложении")

        list_parser = subparsers.add_parser("list",
                                            help="Возвращает список файлов, "
                                                 "которые изменились после "
                                                 "последней загрузки в "
                                                 "облако")
        list_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
        list_parser.add_argument('path', help="Path to catalog or file")

        dir_parser = subparsers.add_parser("dir", help="Возвращает файлы, "
                                                       "расположенные в "
                                                       "облаке")
        dir_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
        dir_parser.add_argument('username', action='store', help="Имя "
                                                                 "пользователя указаное при Reg")

        download_parser = subparsers.add_parser("download", help="Позволяет "
                                                                 "скачать "
                                                                 "файлы или "
                                                                 "папки из "
                                                                 "облака")
        download_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
        download_parser.add_argument('username', action='store', help="Имя "
                                                                      "пользователя указаное при Reg")
        download_parser.add_argument('path', action='store', help="Путь на "
                                                                  "диске, "
                                                                  "куда вы "
                                                                  "хотите "
                                                                  "загрузить "
                                                                  "файлы")
        download_parser.add_argument('file_names', help="Название файлов "
                                                        "которые вы хотите "
                                                        "загрузить(Если файл "
                                                        "находится в папке, "
                                                        "то укажите путь. "
                                                        "Пример: "
                                                        "папка/имя_файла)",
                                     nargs='+')

        upload_parser = subparsers.add_parser("upload", help="Позволяет "
                                                             "загрузить файл"
                                                             " или папки на "
                                                             "облако")
        upload_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
        upload_parser.add_argument('username', action='store', help="Имя "
                                                                    "пользователя указаное при Reg")
        upload_parser.add_argument('path', action='store', help="Путь на "
                                                                "облаке куда "
                                                                "нужно "
                                                                "загрузить "
                                                                "загрузить "
                                                                "файлы(Если "
                                                                "вы хотите "
                                                                "загрузить в "
                                                                "корень, "
                                                                "то напишите "
                                                                "'/')")
        upload_parser.add_argument('file_names', help="Пути к файлам на диске, которые вы хотите загрузить", nargs='+')