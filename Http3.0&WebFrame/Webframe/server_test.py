"""
    快速测试Httpserver的程序
"""
from socket import *
import json

s = socket()
s.bind(('127.0.0.1',8080))
s.listen(5)

while True:
    c,addr = s.accept()
    data = c.recv(1024).decode()
    print(data)
    data = json.dumps({'status':'200','data':'python is good!'})
    c.send(data.encode())
