"""
    Http server V3.0
        1.将请求发送给WebFrame
        2.从WebFrame接收反馈数据
        3.将数据组织为Response格式发送给客户端

    Author by: Lofues
"""

from socket import *
import sys
from threading import Thread
import  json,re
from config import * # 导入配置文件内容

# 负责和webframe交互,socket客户端
def connect_frame(env):
    s = socket()
    try:
        s.connect((frame_ip,frame_port))
    except Exception as e:
        print(e)
        return
    else:
        # 将env转换为json发送
        data = json_dumps(env)
        s.send(data.encode())

        # 接收webframe反馈的数据 10M
        data = s.recv(1024 * 1024 * 10).decode()

        return json.loads(data)


def json_dumps(data):
    return json.dumps(data)


# HttpServer功能
class HTTPServer():
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.create_socket()
        self.bind()


    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,
                               SO_REUSEADDR,
                               DEBUG)

    # 绑定地址
    def bind(self):
        self.address = (self.host,self.port)
        self.sockfd.bind(self.address)

    # 启动服务
    def server_forever(self):
        self.sockfd.listen(5)
        print('Start the http server:%d'%self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            client = Thread(target = self.handle,
                            args = (connfd,))
            client.setDaemon(True) # 守护线程
            client.start() # 线程启动


    # 具体处理客户端请求
    def handle(self,connfd):
        request = connfd.recv(4096).decode()
        # print(request)

        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'
        try:
            # 可能请求为空
            env = re.match(pattern,request).groupdict() # 得到子组名称和对应内容
        except:
            connfd.close()
            return
            print(env)
        else:
            # 得到WebFrame的返回数据
            data = connect_frame(env)

            if data:
                # 发送给客户端
                self.response(connfd,data)

    def response(self,connfd,data):
        # data-->{'status':'200','data':'xxx'}
        if data['status'] == '200':
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += 'Content-Type:text/html\r\n'
            responseHeaders += '\r\n'
            responseBody = data['data']

        elif data['status'] == '404':
            responseHeaders = "HTTP/1.1 404 Not Found\r\n"
            responseHeaders += 'Content-Type:text/html\r\n'
            responseHeaders += '\r\n'
            responseBody = data['data']

        elif data['status'] == '302':
            pass

        # 将数据发送给浏览器
        data = responseHeaders + responseBody
        connfd.send(data.encode())


if __name__ == '__main__':
    httpd = HTTPServer()
    httpd.server_forever() # 启动服务