# -*-coding:utf-8-*-

import os, inspect, hashlib
from random import Random


def random_str(char=''):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    random = Random()
    for i in range(6):
        str += chars[random.randint(0, len(chars) - 1)]
    return char+str


def path(file_path, **kwargs):
    """
    :param file_path: 默认为根目录所指向的路径，否则为'current_path'上层目录值的相对路径
    :param kwargs: key值'current_path'为调用函数.py文件的绝对路径
    :return:
    """
    if 'current_path' in kwargs.keys():
        folder_path = os.path.abspath(os.path.dirname(kwargs['current_path']))  # 获取调用方.py文件名目录
        file_path = os.path.join(folder_path, file_path)
        return file_path
    else:
        file_obj = inspect.getfile(inspect.currentframe())  # 获取当前.py的路径
        folder_path = os.path.abspath(os.path.dirname(file_obj))
        file_path = os.path.join(folder_path, '../', file_path)
        return file_path


# 获取文件名称
def get_filename(file_path):
    """
    :param file_path: 以根目录开始的相对路径
    :return:
    """
    file_name = os.path.split(file_path)[1]
    return file_name


# 获取文件大小
def get_filesize(file_path):
    """
    :param file_path: 以根目录开始的相对路径
    :return:
    """
    file_size = os.stat(file_path).st_size
    return file_size


def file_identifier(file_path):
    file_data = open(file_path, 'rb').read(6291456)
    identifier = hashlib.md5(file_data).hexdigest()
    return identifier