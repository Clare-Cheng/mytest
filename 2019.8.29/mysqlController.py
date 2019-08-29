"""
用于和mysql数据库交互
author:chengyao
"""
import pymysql
# import logging
from config import UHOST, USER, PSW, DB, TABLENAME


class MySQLController:
    def __init__(self):
        self.tablename = TABLENAME
        try:
            self.conn = pymysql.connect(
                host=UHOST,
                user=USER,
                passwd=PSW,
                db=DB,
            )
            self.cursor = self.conn.cursor()
        except Exception as ex:
            print(ex)
            # logging.error(ex)

    def check_downloading_from_sql(self, url):
        """
            检查文件是否在下载状态
        :param url: 文件的下载地址
        :return:
        """
        sql = """ select downloading from %s where url='%s';""" % (self.tablename, url)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as ex:
            print(ex)
            # logging.error(ex)

    def check_md5_from_sql(self, md5):
        """
            通过和数据库内MD5比对,判断是否为同一文件
        :param md5: 文件MD5值
        :return: 文件上传的目标路径
        """
        sql = """ select uploadpath from %s where md5='%s'and m_active=1;""" % (TABLENAME, md5)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result
        except Exception as ex:
            print(ex)
            # logging.error(ex)

    def get_msg_by_md5(self, md5):
        """
        根据md5获得gltfname和url
        :param md5:
        :return:
        """
        sql = """ select gltfname,url from %s where md5='%s';""" % (self.tablename, md5)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            print(result)
            return result
        except Exception as ex:
            print(ex)
            # logging.error(ex)

    def check_parsed(self, data_id):
        """
        检查文件是否已解析完成
        :param data_id:
        :return: 
        """
        sql = """select uploadpath from %s where id='%s';""" % (self.tablename, data_id)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            print(result)
            return result
        except Exception as ex:
            print(ex)
            # logging.error(ex)

    def insert_data_to_sql(self, skpname, gltfname, download_url):
        """
            接到请求,解析数据后插入数据库
        :param skpname:
        :param gltfname:
        :param download_url:
        :return: 该条数据的ID
        """
        sql = """INSERT INTO %s(skpname,gltfname,url)VALUES ('%s','%s','%s')""" % (
            self.tablename, skpname, gltfname, download_url)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            data_id = self.cursor.lastrowid  # 获取插入数据的ID
            return data_id
        except Exception as ex:
            print(ex)
            # logging.error(ex)
            self.conn.rollback()  # 如果发生错误则回滚

    def update_downloading_to_sql(self, data_id):
        """
        下载前将正在下载修改为1(True)
        :param data_id: 数据ID
        :return:
        """
        sql = "UPDATE %s SET downloading = 1 WHERE id = '%s'" % (self.tablename, data_id)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            print(ex)
            # logging.error(ex)
            self.conn.rollback()  # 如果发生错误则回滚

    def update_downloadfield_to_sql2(self, data_id):
        """
        下载失败后,将downloading改回0
        :param data_id: 数据ID
        :return:
        """
        sql = "UPDATE %s SET downloading =0 WHERE id = '%s'" % (self.tablename, data_id)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            print(ex)
            # logging.error(ex)
            self.conn.rollback()  # 如果发生错误则回滚

    def update_md5_to_sql(self, md5, data_id):
        """
        将文件md5值添加进数据库
        :param md5: 文件的md5值
        :param data_id: 当前数据的id
        :return:
        """
        sql = "UPDATE %s SET md5 ='%s' WHERE id = '%s'" % (self.tablename, md5, data_id)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            print(ex)
            # logging.error(ex)
            self.conn.rollback()  # 如果发生错误则回滚

    def update_downloaded_to_sql(self, data_id):
        """
        下载成功后,将downloaded修改为1,downloading改回0
        :param data_id: 数据ID
        :return:
        """
        sql = "UPDATE %s SET downloaded = 1 ,downloading =0 WHERE id = '%s'" % (self.tablename, data_id)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            print(ex)
            # logging.error(ex)
            self.conn.rollback()  # 如果发生错误则回滚

    def logically_deleted_from_sql(self, data_id):
        """
        当文件md5值相同时 逻辑删除已经插入修改的数据.
        :param data_id:
        :return:
        """
        sql = "UPDATE %s SET is_active = 0 WHERE id = '%s'" % (self.tablename, data_id)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            print(ex)
            # logging.error(ex)
            self.conn.rollback()  # 如果发生错误则回滚

    def update_filepath_to_sql(self, path, url):
        """
        上传成功后激活md5,记录上传路径
        :param path:上传路径
        :param url:key,下载路径
        :return:
        """
        sql = "UPDATE %s SET m_active=1,uploadpath='%s' WHERE url = '%s'" % (self.tablename, path, url)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return path
        except Exception as ex:
            print(ex)
            # logging.error(ex)
            self.conn.rollback()  # 如果发生错误则回滚

    def delete_from_sql(self, filename):
        """
            上传失败,从数据库删除此条数据
        :param filename:
        :return:
        """
        sql = "delete from %s  WHERE gltfname = '%s'" % (self.tablename, filename)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            print(ex)
            # logging.error(ex)
            self.conn.rollback()  # 如果发生错误则回滚
