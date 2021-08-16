import shutil
import datetime

def Directory_zip(dirpath):
    shutil.make_archive('archive_'+ datetime, 'zip', dirpath )

if __name__ == "__main__":
    Directory_zip('C:\\bin')
