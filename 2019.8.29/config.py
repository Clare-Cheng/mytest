"""
配置文件
author:chengyao
"""
# mysql相关信息
UHOST = "localhost"
USER = "root"
PSW = "123456"
DB = "test"
TABLENAME = "downloadfile"  # 表名
# 通讯ruby的接口
# RUBY_URL = "http://192.168.1.151:3005/"
RUBY_URL = "http://httpbin.org/"
# 通讯web服务器的接口
# WEB_URL = "http://192.168.1.131:3006/"
WEB_URL = "http://httpbin.org/"
# WEB_URL = "http://httpbin.org/"
# skp文件下载保存路径
DownloadPath = r"D:\01\downloadfile"
# 待解析skp文件路径
DesPath = r"D:\01\skpfile"
# 上传中的路径
UploadingPath = r'D:\01\inupload'
# 待上传路径也是ruby解析后保存gltf的路径
WaitingUploadPath = r'D:\01\gltffile'
# HTTPServer运行IP和端口
HOST = '0.0.0.0'
PORT = 5000
PORT2 = 5001
# PORT2 = 5001
route1 = '/'
# OSS相关信息
OBJNAME = "gltffile"  # 上传的具体文件夹
BUCKETNAME = "skp-parsing"
ENDPOINT = "http://oss-cn-beijing.aliyuncs.com"
ACCESSKEYID = "LTAIP8LFFJ7TVLOV"
KEY = "K8G5E0IxkJxrXIKKEcso8gIUEpRYaV"
# 上传/下载失败后的延时时间
TIME = 30
