import os
from apicompropy.settings import MEDIA_ROOT


def delete_files(filenames, obj=None, dir_name=None, abspath=False):
    if abspath:
        subpath = MEDIA_ROOT
    else:
        subpath = os.path.join(MEDIA_ROOT, obj, dir_name)
    for filename in filenames:
        path = os.path.join(subpath, filename)
        if os.path.exists(path):
            os.remove(path)


def remove_dir(obj, dir_name):
    path = os.path.join(MEDIA_ROOT, obj, dir_name)
    if os.path.exists(path):
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
        os.rmdir(path)


