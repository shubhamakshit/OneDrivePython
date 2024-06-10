import os

class FileUploader:
    def __init__(self, file_path, access_token, chunk_size=10000000):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.access_token = access_token
        self.chunk_size = chunk_size
        self.size = os.stat(file_path).st_size

    def read_file_data(self):
        with open(self.file_path, "rb") as file:
            return file.read()

    def create_upload_session(self):
        from main import createUploadSession
        response = createUploadSession(self.access_token, self.file_name)
        return response['uploadUrl']

    def upload_chunks(self):
        from main import uploadBytesToUploadSession

        data = self.read_file_data()
        url = self.create_upload_session()
        length = self.size

        count = 1
        while True:
            start = self.chunk_size * (count - 1)
            end = self.chunk_size * count

            print(f"Start: {start} End: {end}")
            if end > length:
                end = length

            response_json = uploadBytesToUploadSession(self.access_token, url, start, data[start:end], length)
            print(response_json)
            if end == length:
                break

            count += 1


