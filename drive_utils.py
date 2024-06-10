class OneDrive:

    @staticmethod
    def getFiles_Only(response_json):
        files = []
        for item in response_json['value']:
            if 'file' in item:
                files.append(item)
        return files

    @staticmethod
    def getFolders_Only(response_json):
        folders = []
        for item in response_json['value']:
            if 'folder' in item:
                folders.append(item)
        return folders