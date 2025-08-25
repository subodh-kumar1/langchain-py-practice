import errno
import os
import stat
import shutil


####################################################################################################
# Method to check if the passed dir is empty or not
####################################################################################################
def is_directory_empty(directory):
    try:
        return not any(os.scandir(directory))
    except FileNotFoundError:
        return True


####################################################################################################
# Method to delete all the content from the passed dir
####################################################################################################
def delete_directory_contents(directory):
    try:
        shutil.rmtree(directory, ignore_errors=False, onerror=handle_access)
    except FileNotFoundError:
        print("file not found")
    except Exception as ex:
        print(ex)


####################################################################################################
# Method for handling the access related issues while deleting the content of dir
####################################################################################################
def handle_access(func, path, exc):
    exc_value = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and exc_value.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise
