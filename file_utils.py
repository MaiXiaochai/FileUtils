# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : file_utils.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/10/30 19:26
--------------------------------------
"""

from os import makedirs, listdir, remove
from os.path import isdir, splitext, exists, join
from shutil import copy, move


class FileUtils:
    """一些文件处理相关的功能"""

    @classmethod
    def paths_join(cls, a: str, *paths: str):
        """路径拼接"""
        return cls.trans_path(join(a, *paths))

    @staticmethod
    def exists(path: str) -> bool:
        """判断路径是否存在"""
        return exists(path)

    @staticmethod
    def make_dirs(dir_path: str):
        """递归创建目录"""
        makedirs(dir_path)

    @classmethod
    def copy_files(cls, src_dir: str, dst_dir: str, depth=0, suffix=None, key_str: str = None):
        """
        复制指定目录 src_dir下的文件到 dst_dir目录
            depth：  src_dir递归查找深度，0: 当前目录，1:子目录，...
            suffix: 搜索指定后缀的文件,None,表示所有文件
            key_str: 搜索路径中含特定字符的路径，None,表示没有特定字符
        """
        for file in cls.list_paths(src_dir, depth=depth, suffix=suffix, key_str=key_str):
            # 复制文件到目录
            copy(file, dst_dir)

    @classmethod
    def move_files(cls, src_dir: str, dst_dir: str, depth=0, suffix=None):
        """
        移动指定目录 src_dir下的文件到 dst_dir目录
            depth：  src_dir递归查找深度，0: 当前目录，1:子目录，...
                    注意：所有文件都在 dst_dir下同一级
            suffix: 搜索指定后缀的文件,None,表示所有文件
        """
        for file in cls.list_paths(src_dir, depth, suffix):
            # 复制文件到目录
            move(file, dst_dir)

    @classmethod
    def remove_files(cls, src_dir: str, depth=0, suffix=None):
        """
        删除指定目录 src_dir下的所有文件
            depth：  src_dir递归查找深度，0: 当前目录，1:子目录，...
                    注意：所有文件都在 dst_dir下同一级
            suffix: 搜索指定后缀的文件,None,表示所有文件
        """
        for file in cls.list_paths(src_dir, depth, suffix):
            # 复制文件到目录
            remove(file)

    @classmethod
    def trans_path(cls, dir_path: str) -> str:
        """路径转换, '\\'=>'/'"""
        slash = '/'
        if '\\' in dir_path:
            dir_path = dir_path.replace('\\', slash)

        if not ('.' in dir_path or dir_path.endswith(slash)):
            dir_path = dir_path + slash

        return dir_path

    @classmethod
    def list_paths(cls, dir_path, depth=0, suffix=None, key_str=None):
        """
        1) Generator。
        2) 遍历 dir_path 目录下文件的路径。
        3) 注意：这里的路径使用'/'。
        :param dir_path:    str     要遍历的目录路径
        :param depth:       int     扫描的深度 0:当前目录，1：当前目录的下一级目录
        :param suffix:      str     文件后缀，如 ".py" 或者 "py"
        :param key_str:     str     路径中含的特定字符，None,表示没有特定字符限制
        """

        # 设定当前目录的表示值
        current_dir_level = 0

        dir_path = dir_path if dir_path.endswith("/") else dir_path + "/"

        if suffix:
            if not suffix.startswith('.'):
                suffix = '.' + suffix

        for _path in listdir(dir_path):
            tmp_path = dir_path + _path

            if isdir(tmp_path):
                if current_dir_level < depth:
                    yield from cls.list_paths(tmp_path, depth - 1, suffix, key_str)

            else:
                found = []
                if suffix:
                    if splitext(tmp_path)[-1] == suffix:
                        found.append(True)
                    else:
                        found.append(False)

                if key_str:
                    if key_str in tmp_path:
                        found.append(True)
                    else:
                        found.append(False)

                if all(found):
                    yield tmp_path


def demo():
    from datetime import datetime, timedelta
    test_path = './'
    depth = 0  # 当前目录
    suffix = "zip"  # 搜索后缀为"py"的文件
    key_str = '_'
    res = FileUtils.list_paths(test_path, depth=depth, suffix=suffix, key_str=key_str)
    for i in res:
        print(i)


if __name__ == "__main__":
    demo()
