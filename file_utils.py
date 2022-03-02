# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : file_utils.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/10/30 19:26
--------------------------------------
"""
from time import time
from os import makedirs, listdir, remove
from os.path import isdir, splitext, exists, join as path_join, getctime, getsize
from shutil import copy, move, rmtree
from zipfile import ZipFile


class FileUtils:
    """一些文件处理相关的功能"""

    @classmethod
    def paths_join(cls, a: str, *paths: str):
        """路径拼接"""
        return path_join(a, *paths)

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
    def unzip(cls, zip_path: str, dst_dir: str = './'):
        """解压单个zip压缩文件到 dst目录"""
        with ZipFile(zip_path, 'r') as f:
            files = f.namelist()
            file_length = len(files)

            for no, i in enumerate(files, 1):
                f.extract(i, dst_dir)
                cls.__progress_bar(no, file_length, zip_path)

    @classmethod
    def unzips(cls, src: str, dst: str):
        """解压src目录下的zip文件，到dst目录"""
        zip_files = cls.list_paths(src, suffix='zip')
        if zip_files:
            for z_file in zip_files:
                cls.unzip(z_file, dst)

    @staticmethod
    def __progress_bar(portion, total, file_name):
        from sys import stdout
        from math import ceil
        """
        total 总数据大小，portion 已经传送的数据大小
        :param portion: 已经接收的数据量
        :param total:   总数据量
        :return:        接收数据完成，返回True
        """
        # file_name 用于进度条显示文件名，
        # 之前用zip_path全路径，太长
        file_name = file_name.split('/')[-1] or file_name
        part = total / 50  # 1%数据的大小
        count = ceil(portion / part)
        stdout.write('\r')
        stdout.write(
            ('[%-50s]%.2f%% | %d/%d | %s' % (
                ('=' * count),
                portion / total * 100,
                portion,
                total,
                file_name)
             )
        )
        stdout.flush()

        if portion >= total:
            stdout.write('\n')
            return True

    @classmethod
    def list_paths(cls, dir_path: str, depth: int = 0, suffix=None, key_str: str = None):
        """
        1) Generator。
        2) 遍历 dir_path 目录下的文件的路径。
        3) 注意：这里的路径使用'/'。
        :param dir_path:    str     要遍历的目录路径
        :param depth:       int     扫描的深度 0:当前目录，1：当前目录的下一级目录
        :param suffix:      str     返回的路径中包含特定后缀，如 ".py" 或者 "py"，默认None，没有后缀限制
        :param key_str:     str     返回的路径中包含特定的关键词
        """

        # 设定当前目录的表示值
        current_dir_level = 0

        if suffix:
            if not suffix.startswith('.'):
                suffix = '.' + suffix

        for _path in listdir(dir_path):
            tmp_path = path_join(dir_path, _path)

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

    @staticmethod
    def clean_expiry_files_dirs(dir_path, expiry_days: int or float):

        """
            根据创建时间，清理 dir_path下超期的文件和文件夹。expiry_days默认为None，不清理
        """
        if expiry_days < 0:
            return

        current_date_seconds = time()
        expiry_seconds = expiry_days * 24 * 60 ** 2

        for i in listdir(dir_path):
            path_ = path_join(dir_path, i)
            create_date_seconds = getctime(path_)

            if current_date_seconds - create_date_seconds > expiry_seconds:
                rmtree(path_)
                print(f"path: {path_}, deleted.")

    @staticmethod
    def get_file_size(file_path: str) -> float:
        """获取文件大小，单位：MB"""

        return round(getsize(file_path) / 1024 ** 2, 2)


def demo():
    test_path = './'
    depth = 0  # 当前目录
    suffix = "zip"  # 搜索后缀为"zip"的文件
    key_str = '_'
    res = FileUtils.list_paths(test_path, depth=depth, suffix=suffix, key_str=key_str)
    for i in res:
        print(i)


if __name__ == "__main__":
    demo()
