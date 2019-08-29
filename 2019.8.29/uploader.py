# import logging
import os
import oss2
import time
from config import WaitingUploadPath, UploadingPath, OBJNAME, ACCESSKEYID, KEY, ENDPOINT, BUCKETNAME, TIME
from request import connector_finished_uploading, connector_upload_failed
from mysqlController import MySQLController
from staticFunc import movefile, percentage, is_gitffile


class Uploader:
    def __init__(self, result_tuple):
        self.url = result_tuple[1]
        self.filename = ""
        self.filepath = ""
        self.mysql = MySQLController()
        self.count = 0

    def upload(self):
        """
        阿里云OSS官方上传程序,详参官网
        https://help.aliyun.com/document_detail/88426.html?spm=a2c4g.11186623.6.884.551c7815YamMpC
        :return:
        """
        auth = oss2.Auth(ACCESSKEYID, KEY)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKETNAME)
        objname = '{}/{}'.format(OBJNAME, self.filename)  # 上传到OSS的哪个项目目录
        try:
            with open(self.filepath, 'rb') as fileobj:
                bucket.put_object(objname, fileobj, progress_callback=percentage)
            # 上传成功删除本地文件
            os.remove(self.filepath)
            path = self.url.split('/skpfile')[0]
            uploadpath = path + '/{}'.format(objname)
            self.mysql.update_filepath_to_sql(uploadpath, self.url)
            connector_finished_uploading(self.filename, uploadpath)
        except Exception as ex:
            print(ex)
            # logging.error(ex)
            # 上传失败
            self.upload_failed()
        else:
            # 上传成功计次清0
            self.count = 0

    def upload_failed(self):
        """
        上传失败后的逻辑处理
        :return:
        """
        while self.count < 3:
            self.count += 1
            connector_upload_failed(self.filename, self.count)
            time.sleep(TIME)
            print("这是第{}次重试".format(self.count))
            return self.upload()
        else:
            self.count = 0
            self.mysql.delete_from_sql(self.filename)

    def run(self):
        # 接到请求
        movefile(WaitingUploadPath, UploadingPath)
        items = is_gitffile()
        for item in items:
            self.filepath = os.path.join(UploadingPath, item)
            self.filename = item
            self.upload()
