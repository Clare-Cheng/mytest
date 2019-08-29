import requests
import hashlib
import os
import time
import sys
# import logging
from config import DownloadPath, TIME, DesPath
from mysqlController import MySQLController
from request import connector_finished_download, connector_start_parsing, connector_return_uploadpath, \
    connector_in_downloading, connector_download_failed, connector_start_timer
from staticFunc import movefile


class Dwonloader:
    def __init__(self, url, skpname, gltfname):
        self.url = url
        self.skpname = skpname
        self.gltfname = gltfname
        self.id = -1
        self.md5 = ""
        self.mysql = MySQLController()
        self.count = 0  # 用于记录下载失败的次数

    def check_download_queue(self):
        """
        检查下载列队,查看该下载链接的文件是否正在下载
        :return:
        """
        results = self.mysql.check_downloading_from_sql(self.url)
        if results:
            for item in results:
                if 1 in item:
                    return False
            else:
                return True
        else:
            return True

    def downloadfile(self):
        """
        下载程序,利用requests,这里带了进度条
        :return:
        """
        size = 0
        chunk_size = 4096
        try:
            skp = requests.get(self.url, stream=True, timeout=5)
            total_size = int(skp.headers['content-length'])
            print("文件大小:%0.2f MB" % (total_size / 1024 / 1024))
            with open(os.path.join(DownloadPath, self.skpname), 'wb') as f:
                for data in skp.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    size += len(data)
                    rate = int((float(size) / float(total_size)) * 100)
                    print('\r[已下载]{0}% '.format(rate), end='')
                    sys.stdout.flush()
        except Exception as ex:
            print(ex)  # 下载失败
            # logging.error(ex)
            self.download_failed()
            self.mysql.update_downloadfield_to_sql2(self.id)
        else:
            self.count = 0  # 下载成功,计次归0
            self.mysql.update_downloaded_to_sql(self.id)
            connector_finished_download(self.skpname)

    def download_failed(self):
        """
        下载失败后的处理操作
        :return: 递归,尝试重新下载
        """
        while self.count < 3:
            self.count += 1
            time.sleep(TIME)
            print("这是第{}次重试".format(self.count))
            return self.downloadfile()
        else:
            connector_download_failed(self.skpname)
            self.count = 0

    def get_md5_and_rename(self):
        """
        读取已下载文件MD5值 并用MD5值给文件重命名
        :return:
        """
        filepath = os.path.join(DownloadPath, self.skpname)
        filetype = filepath.split('.')[-1]  # 获取文件后缀
        filename = filepath.split('\\')[-1]  # 获取文件前缀
        path = filepath.split(filename)[0]  # 获取文件路径
        try:
            with open(filepath, 'rb')as f:
                md5obj = hashlib.md5()
                md5obj.update(f.read())
                md5 = md5obj.hexdigest()  # 获取MD5值
        except Exception as ex:
            print(ex)
            # logging.error(ex)
        else:
            # 获取MD5成功
            new_filename = md5 + '.' + filetype  # 新文件名
            des = os.path.join(path, new_filename)  # 目标路径
            try:
                os.rename(filepath, des)
            except Exception as ex:
                print(ex)
                # logging.error(ex)
                # 改名失败 删除重名文件
                os.remove(filepath)
        finally:
            return md5

    def run(self):
        self.id = self.mysql.insert_data_to_sql(self.skpname, self.gltfname, self.url)
        self.mysql.update_downloading_to_sql(self.id)
        connector_in_downloading(self.skpname)
        self.downloadfile()
        self.md5 = self.get_md5_and_rename()
        result = self.mysql.check_md5_from_sql(self.md5)
        if result is None:
            self.mysql.update_md5_to_sql(self.md5, self.id)
            movefile(DownloadPath, DesPath)
            time.sleep(5)
            connector_start_parsing()
            connector_start_timer(self.skpname, self.id)
        else:
            try:
                os.remove(os.path.join(DownloadPath, '{}.skp'.format(self.md5)))
            except Exception as ex:
                print(ex)
                # logging.error(ex)
            self.mysql.logically_deleted_from_sql(self.id)
            uploadpath = result[0]  # 获取路径 返回给web端
            connector_return_uploadpath(uploadpath)
