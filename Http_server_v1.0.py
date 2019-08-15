'''
    该程序用来演示HTTP服务器的功能，在浏览器上访问成功时
    返回index.html的网页

    Author by:Lofues
'''
from socket import *


def handle_client(connfd):
    '''对客户端发送的请求报文按行打印并返回一个网页'''
    request = connfd.recv(4096)
    # print(request)

    # 用splitlines对request按行分割
    for line in request.splitlines():
        print(line.decode())

    # 若打开网页失败
    try:
        f = open('index.html')
    except IOError:
        responce = 'HTTP/1.1 404 not found\r\n'
        responce += '\r\n'
        responce += '====Sorry not found===='
    else:
        responce = 'HTTP/1.1 200 OK\r\n'
        responce += '\r\n'
        responce += f.read()
    finally:
        connfd.send(responce.encode())


# 创建套接字
def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(('0.0.0.0', 8888))
    sockfd.listen(3)
    print('Listen to the port 8888')
    while True:
        connfd, addr = sockfd.accept()
        # 处理请求
        handle_client(connfd)

        connfd.close()


if __name__ == '__main__':
    main()
