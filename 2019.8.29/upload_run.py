"""
由flask框架搭建的服务端,用来监听上传请求,异步上传文件,提高响应速度.
监听地址:0.0.0.0:5001/
author:chengyao
"""
# import logging
import os
import time
from flask import Flask, request
from config import HOST, PORT2, route1, WaitingUploadPath
from uploader import Uploader
from request import connector_reday_for_upload, connector_parse_slowly
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from staticFunc import decode_base64, md5_to_gltfname
from mysqlController import MySQLController

# logging.basicConfig(level=logging.ERROR,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='/01/upload.log',
#                     filemode='w')

executor = ThreadPoolExecutor(1)
executor2 = ProcessPoolExecutor(1)
app = Flask(__name__)
count = 0


@app.route(route1, methods=['GET', 'POST'])
def start_uploader():
    """
    上传中台,接收ruby端的请求来启动上传程序
    :return:
    """
    if request.method == 'GET':
        print("接收到了上传请求")
        result = request.args.get('gltf', 0)
        if result:
            data = decode_base64(result)
            print(data)
            try:
                result = md5_to_gltfname(data)
                executor2.submit(uploadfile, data=data, result=result)
            except Exception as ex:
                print(ex)
                path = data.replace('parsingfile', 'gltffile')
                os.remove(path)
    else:
        print("接到了启动定时器")
        skpname = request.form.get('skpname')
        data_id = request.form.get('id')
        executor.submit(timer, skpname, data_id)
        return request.host_url
    return 'ok'


def uploadfile(data, result):
    """
    异步执行的上传程序
    :param data: get请求带来得参数
    :param result: 根据参数从数据库查找出的数据(md5和url)
    :return:
    """
    if result:
        connector_reday_for_upload(result)
        upload = Uploader(result)
        upload.run()
    else:
        filename = data.split('\\')[-1]
        path = os.path.join(WaitingUploadPath, filename)
        try:
            os.remove(path)
            print("已删除测试文件%s" % filename)
        except Exception as ex:
            print(ex)


def timer(skpname, data_id):
    """
    定时器,用来检查一定时间内文件是否解析完成,未完成返回web端状态.
    :param skpname:
    :param data_id:
    :return:
    """
    ms = MySQLController()
    global count
    res = ms.check_parsed(data_id)
    if res[0] is not None:
        count = 0
        print('定时器结束')
        return
    else:
        time.sleep(10)
        count += 1
        if count > 60:
            connector_parse_slowly(skpname)
            count = 0
        return timer(skpname, data_id)


if __name__ == '__main__':
    app.run(HOST, PORT2, debug=True)
