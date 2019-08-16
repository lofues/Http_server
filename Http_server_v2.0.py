#!/usr/bin/python3
# -*- coding = utf-8 -*-

'''
http server v2.0
1.多线程并发
2.可以请求简单数据
3.能进行简单请求解析
4.结构使用类进行封装
'''

from socket import *
from threading import Thread
import sys
import traceback


# httpserver类，封装具体的服务器功能
class HTTPServer(object):
    def __init__(self, server_addr, static_dir):
        # 增添服务器对象属性
        self.server_address = server_addr
        self.static_dir = static_dir
        self.ip = server_addr[0]
        self.port = server_addr[1]
        # 创建套接字
        self.create_socket()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(self.server_address)

    # 设置监听，等待客户端连接
    def server_forever(self):
        self.sockfd.listen(5)
        print('listen the port {}'.format(self.port))

        while True:
            try:
                connfd, addr = self.sockfd.accept()
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('服务器退出')
            except Exception as e:
                traceback.print_exc()
                continue

            # 创建新的线程处理请求
            client_thread = Thread \
                (target=self.handleRequest, args=(connfd,))
            client_thread.setDaemon(True)  # 在start之前使用，将子线程设置为守护线程
            client_thread.start()

    # 客户端请求函数
    def handleRequest(self, connfd):

        # 接受客户端请求
        request = connfd.recv(4096)

        # 解析请求内容
        requestHeaders = request.splitlines()
        print(connfd.getpeername(), ':{}'.format(requestHeaders[0]))

        # 获得具体请求内容
        getRequest = requestHeaders[0].decode().split(' ')[1]

        if getRequest == '/' or getRequest[-5:] == '.html':
            self.get_html(connfd, getRequest)
        else:
            self.get_data(connfd, getRequest)

        connfd.close()

    # 获取静态html的方法
    def get_html(self, connfd, getRequest):
        if getRequest == '/':
            filename = '/index.html'
        else:
            filename = getRequest

        try:
            fr = open(self.static_dir + filename, 'r')
        except Exception as e:
            responseHeaders = 'HTTP/1.1 404 NOT FOUND\r\n'
            responseHeaders += '\r\n'
            responseBody = 'Sorry,not found the page'
            print(e)
        else:
            responseHeaders = 'HTTP/1.1 404 NOT FOUND\r\n'
            responseHeaders += '\r\n'
            # print('{} get the page:{}'.format(connfd.getpeername(),filename[1:]))
            responseBody = fr.read()
        finally:
            response = responseHeaders + responseBody
            connfd.send(response.encode())

    # 发送其他种类的数据
    def get_data(self, connfd, getRequest):
        # 设置请求内容格式为/time 或者/python
        urls = ['/time', '/python']

        if getRequest in urls:
            responseHeaders = 'HTTP/1.1 404 NOT FOUND\r\n'
            responseHeaders += '\r\n'
            if getRequest == '/time':
                import time
                responseBody = time.ctime()
            elif getRequest == '/python':
                responseBody = '人生苦短我用大蛇'
        else:
            responseHeaders = 'HTTP/1.1 404 NOT FOUND\r\n'
            responseHeaders += '\r\n'
            responseBody = 'Sorry,not found the page'

        response = responseHeaders + responseBody
        connfd.send(response.encode())


if __name__ == '__main__':
    # 服务器IP
    server_addr = ('0.0.0.0', 8888)
    # 我的静态页面存储目录
    static_dir = './html'

    # 生成对象
    https = HTTPServer(server_addr, static_dir)

    # 启动服务器
    https.server_forever()
