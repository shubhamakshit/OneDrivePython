from datetime import datetime


class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        if not self.log_file:
            raise ValueError('log_file must be provided')

        # check if the file exists, if not create it
        with open(self.log_file, 'a') as f:
            pass

    def time_stamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def log(self, message):
        with open(self.log_file, 'a') as f:
            f.write(f'{self.time_stamp()} - {message}\n')