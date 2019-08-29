******************此脚本的配置文档***********************
*e.g 本程序与web/ruby的通讯方式均为http的get请求
*e.g 所有可能常改动的参数已写入到config.py中

# Python下载程序运行端口(download_run.py)
    0.0.0.0:5000(本机为 192.168.1.151:5000)
# Python上传程序运行端口(upload_run.py)
    0.0.0.0:5001(本机为 192.168.1.151:5001)
# web端通讯Python(本机)的接口
    "http://192.168.1.151:5000/?url=<XXX>"
# ruby端通讯Python(本机)的接口
    "http://192.168.1.151:5001/1?gltf=<XXX>"
# Python(本机)通讯ruby端的接口
    "http://192.168.1.151:3005/"
# Python(本机)通讯web端的接口
    "http://192.168.1.131:3006/?mess=<XXX>&data=<XXX>"

# SKP文件下载路径
    "D:\01\downloadfile"
# 待解析的SKP文件路径
    "D:\01\skpfile"
# 正在解析的SKP文件路径
    "D:\01\parsingfile"
# 解析完成的SKP文件路径
    "D:\01\isparsedfile"
# 解析出的gltf文件保存路径
    "D:\01\gltffile"
# 正在上传中的gltf文件路径
    "D:\01\inupload"

# MySQL数据库相关信息
  字符集
    utf8
  数据库名称
    test
  数据表名称
    downloadfile
  数据表字段
    id      int 主键自增
    skpname        varchar(200)  //用于存放下载的skp文件名
    gltfname        varchar(200)  //用于存放上传的gltf文件名
    url     varchar(200)  //用于存放下载的链接
    uploadpath     varchar(200)  //用于存放上传后的文件地址
    md5     varchar(200)  //用于存放文件的md5值
    m_active        int default 0 //用于判断md5值有没有生效
    downloading     int default 0 //用于判断文件是不是正在下载
    downloaded     int default 0 //用于判断文件是不是已经下载完成
    is_active     int default 1 //用于判断数据是否被逻辑删除
