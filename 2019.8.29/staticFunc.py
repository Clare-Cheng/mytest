import base64
import os
import sys
import shutil
# import logging
from mysqlController import MySQLController
from config import WaitingUploadPath, UploadingPath


def decode_base64(parameter):
    """
    解析base64加密的参数
    :param parameter:这里是get请求带来的参数
    :return: 解析后的路径
    """
    if parameter[-1] == '=':
        if ' ' in parameter:
            result = parameter.replace(' ', '+')
            filepath = base64.b64decode(result)
            return filepath.decode()
        filepath = base64.b64decode(parameter)
        return filepath.decode()
    if parameter.count("=") > 0:
        result = parameter.partition("=")[-1]
        if ' ' in result:
            result = result.replace(' ', '+')
            filepath = base64.b64decode(result)
            return filepath.decode()
        else:
            filepath = base64.b64decode(result)
            return filepath.decode()
    elif ' ' in parameter:
        result = parameter.replace(' ', '+')
        filepath = base64.b64decode(result)
        return filepath.decode()
    else:
        filepath = base64.b64decode(parameter)
        return filepath.decode()


def movefile(oldpath, newpath):
    """
    将文件移动到指定位置
    :param oldpath: 文件现存放路径
    :param newpath: 目标路径
    :return:
    """
    for item in os.listdir(oldpath):
        full_path = os.path.join(oldpath, item)  # 将文件名与文件目录连接起来，形成完整路径
        des_path = os.path.join(newpath, item)  # 目标路径
        if os.path.isfile(full_path):
            shutil.move(full_path, des_path)  # 移动文件到目标路径
        else:
            # 不是文件则为文件夹,尝试删除文件夹
            try:
                os.rmdir(full_path)
            except Exception as ex:
                # logging.error(ex)
                print(ex)


def md5_to_gltfname(data):
    """
    获取md5值来得到原文件名,并将文件名改回原文件名
    :param data:
    :return:
    """
    ms = MySQLController()
    filename = data.split('\\')[-1]
    md5 = filename.split('.')[0]
    result = ms.get_msg_by_md5(md5)
    gltfname = result[0]
    try:
        oldpath = os.path.join(WaitingUploadPath, filename)
        des = os.path.join(WaitingUploadPath, gltfname)
        os.rename(oldpath, des)
    except Exception as ex:
        print(ex)
        # logging.error(ex)
    finally:
        return result


def sort_by_filename():
    """
    待分片后排序上传使用,暂未投用
    :return:
    """
    files = os.listdir(WaitingUploadPath)
    # 以时间戳命名后可以以切片形式取一段来排序
    files.sort(key=lambda x: int(x.split('.')[0]))


def is_gitffile():
    """
    判断要上传的文件是不是gltf文件
    :return: 待上传的gltf文件
    """
    for item in os.listdir(UploadingPath):
        if os.path.isfile(os.path.join(UploadingPath, item)) and item.split('.')[-1] == 'gltf':
            yield item
        else:
            try:
                os.remove(item)
            except Exception as ex:
                print(ex)
                # logging.error(ex)


def percentage(consumed_bytes, total_bytes):
    """
    oss上传的回调函数,用来显示上传进度
    :param consumed_bytes:
    :param total_bytes:
    :return:
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r[已上传]{0}% '.format(rate), end='')
        sys.stdout.flush()
