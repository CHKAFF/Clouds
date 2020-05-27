import requests
class command_dir(object):

    def __init__(self, args, token):
        self.result = ["Dir"]
        if args.cloud == 'dropbox':
            if token is None:
                self.result.append(False)
                return
            self.contain_dropbox(token, 0, "")
            if len(self.result) != 2:
                self.result.append(True)

    def contain_dropbox(self, access_token, indentation, path):
        try:
            files = requests.post('https://api.dropboxapi.com/2/files/list_folder',
                                headers={"Authorization": "Bearer " + access_token, "Content-Type": "application/json"},
                                data="{\"path\": \"" + path + "\",\"recursive\": false,\"include_media_info\": false,"
                                                                "\"include_deleted\": false,"
                                                                "\"include_has_explicit_shared_members\": false,"
                                                                "\"include_mounted_folders\": true,"
                                                                "\"include_non_downloadable_files\": true}").json()
            for f in files['entries']:
                if f['.tag'] == 'folder':
                    self.result.append(" " * indentation + 'FOLDER: ' + f['name'])
                    self.contain_dropbox(access_token, indentation + 4, path + "/" + f['name'])
                else:
                    self.result.append(" " * indentation + f['name'])
        except:
            self.result.append(False)