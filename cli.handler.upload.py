from uploader import FileUploader

ENV_FILE = '.env'


def read_env():
    import os
    if not os.path.exists(ENV_FILE):
        print('Please create a .env file with the access token')
        exit(1)

    env_data = {}
    with open(ENV_FILE, 'r') as f:
        data = f.read()
        for line in data.split('\n'):
            if line:
                key, value = line.split('=')
                key = key.strip()
                value = value.strip()
                env_data[key] = value
    return env_data


def check_path(path):
    import os
    path = os.path.expandvars(path.strip())
    if not os.path.exists(path):
        print('The file does not exist')
        exit(1)
    return path


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Upload a file to the server')
    parser.add_argument('--file', '-f', nargs='?', type=str, help='The file to upload')
    parser.add_argument('--ac_token', '--ac', nargs='?', type=str, help='The access token', default='')

    args = parser.parse_args()
    if not args.ac_token:
        if 'access_token' not in read_env():
            print('Please provide an access token')
            exit(1)

    access_token = args.ac_token if args.ac_token else read_env()['access_token']

    upload_file_path = check_path(input('Enter the path to upload the file to: ')) if not args.file else args.file

    uploader = FileUploader(upload_file_path, access_token)
    print('Uploading file...')
    uploader.upload_chunks()


if __name__ == '__main__':
    main()
