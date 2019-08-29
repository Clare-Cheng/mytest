"""
由flask框架搭建的服务端,用来监听下载请求,异步下载文件,提高响应速度.
监听地址:0.0.0.0:5000/
author:chengyao
"""
# import logging
from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor
from config import route1, HOST, PORT
from request import connector_in_downloading, connector_reday_for_download
from staticFunc import decode_base64
from downloader import Dwonloader

# logging.basicConfig(level=logging.ERROR,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='/01/download.log',
#                     filemode='w')
executor = ThreadPoolExecutor(1)
app = Flask(__name__)
myset = set()


@app.route(route1, methods=['GET', 'POST'])
def start_downloader():
    """
    下载中台,接收WEB端的请求来启动下载程序
    :return:
    """
    if not request.method == "POST":
        # 获取参数里的下载链接
        url = request.args.get('url', 0)  # 利用默认值剔除不带约定参数的get请求
        if url:
            url = decode_base64(url)
            s = len(myset)
            myset.add(url)
            e = len(myset)
            if e > s:
                connector_reday_for_download(url)
                executor.submit(downloadfile)
                return 'ok', 200
            else:
                # 请求完全相同,暂不做处理
                return 'error', 666
        else:
            # 没有拿到正确参数 暂不做处理
            return 'verror', 404
    else:
        # POST请求暂不做处理
        pass


def downloadfile():
    """
    异步执行的下载程序
    :return:
    """
    for item in myset:
        skpname = item.split('/')[-1]
        gltfname = skpname.split('.')[0] + '.gltf'
        downloader = Dwonloader(item, skpname, gltfname)  # 创建下载器实体类
        if downloader.check_download_queue():  # 如果没有同名文件在下载
            # 调用下载器
            downloader.run()
            myset.discard(item)
            return
        else:
            connector_in_downloading(skpname)


if __name__ == '__main__':
    myset.clear()
    app.run(HOST, PORT, debug=True)
