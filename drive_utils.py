from logger import Logger
log = Logger('log.txt')
class OneDrive:

    @staticmethod
    def getFiles_Only(response_json):
        files = []
        for item in (response_json['value'] if 'value' in response_json else response_json):
            if 'file' in item:
                files.append(item)

        print(files)
        return files

    @staticmethod
    def getFolders_Only(response_json):
        folders = []
        response_json = response_json['value'] if 'value' in response_json else response_json
        for item in response_json:
            if 'folder' in item:
                folders.append(item)

        return folders