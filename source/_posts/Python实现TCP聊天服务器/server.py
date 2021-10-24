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