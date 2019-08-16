"""
http server v2.1
env: python 3.6
IO多路复用 , http训练
"""

from socket import *
from select import select

# 具体功能服务
class HTTPServer:
    def __init__(self,host='0.0.0.0',port=80,dir=None):
        self.host = host
        self.port = port
        self.dir = dir
        self.address = (host,port)
        # select 的监控列表
        self.rlist = []
        self.wlist = []
        self.xlist = []
        # 直接创建出套接字
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,
                               SO_REUSEADDR,1)
    # 绑定
    def bind(self):
        self.sockfd.bind(self.address)

    # 启动入口
    def serve_forever(self):
        self.sockfd.listen(3)
        print("Listen the port %d"%self.port)
        # 搭建IO多路服用监控各种IO请求
        self.rlist.append(self.sockfd)
        while True:
            rs,wx,xs = select(self.rlist,
                              self.wlist,
                              self.xlist)
            for r in rs:
                # 浏览器连接进来
                if r is self.sockfd:
                    c,addr = r.accept()
                    self.rlist.append(c)
                else:
                    # 处理客户端请求
                    self.handle(r)

    # 处理客户端请求
    def handle(self,connfd):
        # 接收http请求
        request = connfd.recv(4096)

        # 客户端断开
        if not request:
            self.rlist.remove(connfd)
            connfd.close()
            return

        # 提起请求内容 (将字节串按行切割)
        request_line = request.splitlines()[0]
        info = request_line.decode().split(' ')[1]
        print('请求内容:',info)

        # 根据请求内容进行数据整理
        # 分为两类: 1. 请求网页,2. 其他
        if info == '/' or info[-5:] == '.html':
            self.get_html(connfd,info)
        else:
            self.get_data(connfd, info)

    # 处理网页
    def get_html(self,connfd,info):
        if info == '/':
            # 请求主页
            filename = self.dir + '/index.html'
        else:
            filename = self.dir + info
        try:
            fd = open(filename)
        except Exception:
            # 网页不存在
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += '\r\n'
            response += "<h1>Sorry....</h1>"
        else:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += '\r\n'
            response += fd.read()
        finally:
            # 讲内容发送给浏览器
            connfd.send(response.encode())

    # 处理其他
    def get_data(self,connfd,info):
        f = open(self.dir+"/timg.jpg",'rb')
        data = f.read()
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:image/jpeg\r\n"
        response += '\r\n'
        response = response.encode() + data
        connfd.send(response)

# 用户应该怎么用HTTPServer
if __name__ == '__main__':
    """
    通过HTTPServer快速启动服务,用于展示自己的网页
    """
    # 需要用户自己决定的内容
    HOST = '0.0.0.0'
    PORT = 8000
    DIR = "./static" # 网页存储位置

    httpd = HTTPServer(HOST,PORT,DIR)
    httpd.serve_forever() # 服务启动入口




