import shutil
import datetime
import zipfile

def Directory_zip(dirpath):
    shutil.make_archive('archive_'+ datetime, 'zip', dirpath )

#read zip files
def read_zip(filename):
    with zipfile.ZipFile(filename,'r') as archive:
        print(archive.namelist())

if __name__ == "__main__":
    Directory_zip('C:\\bin')
    #read_zip('archive_<>.zip')
