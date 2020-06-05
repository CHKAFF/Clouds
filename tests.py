import unittest
import cloud
import os
import dropbox

class args(onject):
    def __init__(self, username, path, file_names):
        self.cloud = "dropbox"
        self.username = username
        self.path = path
        self.file_names = file_names

class MyTestCase(unittest.TestCase):
    def test_first(self):
        actual = True
        expected = True
        self.assertEqual(expected, actual)

    def test_dir_with_not_correct_username(self):
        cloud = dropbox(args("d", "d", ["fdfd"]))
        result = cloud.dir()
        self.assertEqual(result[-1], False)

    def test_download_with_not_correct_username(self):
        cloud = dropbox(args("d", "d", ["fdfd"]))
        result = cloud.download()
        self.assertEqual(result[-1], False)

    def test_upload_with_not_correct_username(self):
        cloud = dropbox(args("d", "d", ["fdfd"]))
        result = cloud.upload()
        self.assertEqual(result[-1], False)
    
    def test_download_with_not_correct_path(self):
        result = command_download(args("rex", "d", ["fdfd"])).result
        self.assertEqual(result[-2], False)
        self.assertEqual(result[-1], "Сбой. Неправильо указан путь для загрузки")
    
    def test_download_with_not_correct_path_on_cloud(self):
        result = command_download(args("rex", "C:\Users", ["fdfd"])).result
        self.assertEqual(result[-2], False)
        self.assertEqual(result[-1], "Сбой. Неправильный путь к файлу или его имя")

    def test_upload_with_not_correct_path(self):
        result = command_download(args("rex", "d", ["fdfd"])).result
        self.assertEqual(result[-2], "Файла или Дирректории не существует")
        self.assertEqual(result[-1], False)

    def test_list_with_not_correct_path(self):
        result = command_list(args("rex", "d", ["fdfd"])).result
        self.assertEqual(result[-2], 0)
        self.assertEqual(result[-1], False)

if __name__ == '__main__':
    unittest.main()
