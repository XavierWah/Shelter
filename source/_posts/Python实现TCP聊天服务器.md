---
title: Python实现TCP聊天服务器
toc: true
date: 2021-08-02 22:16:05
categories: Coding
tags: 
    - Python
    - Socket
---

# 引子

刚刚琢磨了一下`socket`，随手摸了一个TCP聊天出来。

<!-- more -->

# 通信原理

服务端开放端口用于通信。  
当有客户端加入时，向其他客户端广播用户加入消息。  
当客户端发送信息时，接受并广播给其它客户端。  
当有客户端退出时，向其他客户端广播用户退出消息。

# 服务端

[<i class="fas fa-download"></i>](server.py) `下载 server.py` 下方的代码。

``` python Python 3
import socket
import threading

# 初始化服务器
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 32768))
server.listen()
clients = []
nicknames = []

# 广播消息
def broadcast(message):
    for client in clients:
        client.send(message)

# 处理消息
def handle(client):
    while True:
        try:
            # 广播消息
            message = client.recv(1024)
            broadcast(message)
        except:
            # 处理用户退出请求
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} 退出了聊天'.format(nickname).encode('utf-8'))
            nicknames.remove(nickname)
            break

# 监听消息
def receive():
    while True:
        # 接受连接并请求昵称
        client, address = server.accept()
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # 通知用户进入服务器
        print("{} ({}:{}) 加入了聊天".format(nickname, *address))
        broadcast("{} 加入了聊天".format(nickname).encode('utf-8'))
        client.send('已连接至聊天服务器'.encode('utf-8'))

        # 创建线程处理信息
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
```

# 客户端

[<i class="fas fa-download"></i>](client.py) `下载 client.py` 下方的代码。

``` python Python 3
import socket
import threading

# 输入昵称
nickname = input("请输入昵称: ")

# 连接至服务器
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))

# 多线程用于收发信息
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=wr
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 32768))

# 监听服务器并回应昵称请求
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # 出错时关闭与服务器连接
            print("意外的错误出现")
            client.close()
            break

# 向服务器发送信息
def write():ite)
write_thread.start()
```
