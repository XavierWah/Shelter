import socket
import threading

# 输入昵称
nickname = input("请输入昵称: ")

# 连接至服务器
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
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))

# 多线程用于收发信息
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()