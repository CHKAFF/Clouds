import argparse



class help_parser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers(dest="command")

        reg_parser = subparsers.add_parser("reg",
                                           help="Позволяет запомнить токен и использовать его дальше при помощи "
                                                "указанного имени")
        reg_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
        reg_parser.add_argument('username', action='store', help="User name")
        reg_parser.add_argument('token', action='store', help="access token for cloud")

        list_parser = subparsers.add_parser("list",
                                            help="Возвращает список файлов, которые изменились после последней загрузки в "
                                                 "облако")
        list_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
        list_parser.add_argument('paths', help="Paths to catalog or file", nargs='+')

        dir_parser = subparsers.add_parser("dir", help="Возвращает файлы, расположенные в облаке")
        dir_parser.add_argument('cloud', action='store', help="Сloud name", choices=['dropbox'])
        dir_parser.add_argument('username_or_access_token', action='store')
        