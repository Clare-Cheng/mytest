"""
用于通讯的函数
author:chengyao
"""
import requests
from config import RUBY_URL, WEB_URL
# import logging
import time


def connector_start_parsing():
    """
    下载完成发送一个请求给ruby程序
    :return:
    """
    url = RUBY_URL
    headers = {'Connection': 'close', }
    try:
        requests.get(url, headers=headers, timeout=5)
    except Exception as ex:
        print(ex)
        # logging.error(ex)


def connector_finished_download(data):
    """
    下载完成后返回前端一个状态
    :param data:
    :return:
    """
    url = WEB_URL + "?mess=下载成功,正在解析&data={}".format(data)
    try:
        requests.get(url)
        # res = requests.get(url)
        # print("下载完成:", res.status_code)
    except Exception as ex:
        print(ex)
        # logging.error(ex)


def connector_reday_for_upload(data):
    """
    反馈web端文件解析完成准备上传
    :param data: gltf文件名
    :return:
    """
    data = data[0]
    url = WEB_URL + "?mess=解析完成,正在上传&data={}".format(data)
    try:
        requests.get(url)
        # res = requests.get(url)
        # print("准备上传:", res.status_code)
    except Exception as ex:
        print(ex)
        # logging.error(ex)


def connector_finished_uploading(data, path):
    """
    上传成功返回一个状态
    :param data:
    :param path:
    :return:
    """
    url = WEB_URL + "?mess={}上传成功,路径为&data={}".format(data, path)
    try:
        requests.get(url)
        # res = requests.get(url)
        # print("上传完成:", res.status_code)
    except Exception as ex:
        print(ex)
        # logging.error(ex)


def connector_return_uploadpath(filepath):
    """
    md5相同时返回数据库路径
    :param filepath:
    :return:
    """
    url = WEB_URL + "?mess=该文件已解析过,文件存放在&data={}".format(filepath)
    try:
        requests.get(url)
        # res = requests.get(url)
        # print("已解析过:", res.status_code)
    except Exception as ex:
        print(ex)
        # logging.error(ex)


def connector_in_downloading(filename):
    url = WEB_URL + "?mess=文件正在下载中,请稍等...&data={}".format(filename)
    try:
        requests.get(url)
        # res = requests.get(url)
        # print("正在下载:", res.status_code)
    except Exception as ex:
        print(ex)
        # logging.error(ex)


def connector_download_failed(filename):
    url = WEB_URL + "?mess=文件下载失败&data={}".format(filename)
    try:
        requests.get(url)
        # res = requests.get(url)
        # print("下载失败执行重试:", res.status_code)
    except Exception as ex:
        print(ex)
        # logging.error(ex)


def connector_upload_failed(filename, count):
    url = WEB_URL + "?mess={}文件上传失败&data=正在执行第{}次重试...".format(filename, count)
    try:
        requests.get(url)
        # res = requests.get(url)
        # print("上传失败执行重试:", res.status_code)
    except Exception as ex:
        print(ex)
        # logging.error(ex)
        time.sleep(10)
        return connector_upload_failed(filename, count)


def connector_reday_for_download(data):
    """
    将已解析好的文件状态返还给web端
    :param data: base64解析出的数据
    :return:
    """
    # data = data.split('\\')[-1]
    url = WEB_URL + "?mess=准备开始下载&data={}".format(data)
    try:
        requests.get(url)
        # res = requests.get(url)
        # print("准备下载:", res.status_code)
    except Exception as ex:
        print(ex)
        # logging.error(ex)


def connector_parse_slowly(data):
    url = WEB_URL + "?mess=文件过大,解析缓慢,请耐心等待...&data={}".format(data)
    try:
        requests.get(url)
        # res = requests.get(url)
        # print("下载缓慢:", res.status_code)
    except Exception as ex:
        print(ex)
        # logging.error(ex)


def connector_start_timer(skpname, data_id):
    msg = {'skpname': skpname, 'id': data_id}
    url = "http://192.168.1.151:5001/"
    try:
        requests.post(url, data=msg, timeout=5)
    except Exception as ex:
        print(ex)
