---
title: 网络扫描
date: 2023-09-23
cover: /img/cover/12.jpg
categories:
  - 计算机网络
tags:
  - 计算机网络
  - Python
  - ARP
  - Nmap
  - Scapy
  - TCP
  - ICMP
---



# 网络扫描

通过网络扫描，可以获取网段内存活的主机以及其开放的端口，更加深入的扫描则能够探测主机的操作系统，配置，安装的软件等。

## 主机发现

在网络中发现主机有很多方法，如果在局域网内使用arp协议可以轻易的发现存活的kv主机，如果在不同的网段使用ICMP协议也可以尝试和主机取得联系，TCP和UDP协议同样可以

### ARP协议探测

ARP协议通过向局域网广播的方式将同网段主机IP地址解析为MAC地址。
在一个路由器下的局域网内，如果对某个IP发起ARP请求，如果这个IP通过路由器上网，那么路由器肯定有这个主机的MAC地址，因此广播到路由器时会受到主机的IP地址；如果不存在这个IP，那么将没有MAC地址的回复。根据是否受到MAC地址，就可以判断局域网内的这个主机是否存活。

```python
def arp(ipy):
    dst_ip_list = IPY(ipy)
    alive_ip_list = []

    for dst_ip in dst_ip_list:
        pkt = ARP(pdst=str(dst_ip))
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is not None:
            # ans.summary()
            # ans.show()
            alive_ip_list.append(dst_ip)
            print(dst_ip, 'is up')
        else:
            print(dst_ip, 'is closed')

    return alive_ip_list

```


### ICMP协议探测

ICMP中的request/ping报文可以用于测试网络的可达性和延迟情况，如果主机可达将会返回reply报文，如果不可达会返回具体原因的报文。

```python
def ping(ipy):
    dst_ip_list = IPY(ipy)
    alive_ip_list = []
    for dst_ip in dst_ip_list:
        pkt = IP(dst=str(dst_ip)) / ICMP() / b'hello'
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is not None:
            if ans[ICMP].type == 0:
                if ans[IP].ttl <= 64:
                    print(dst_ip, '(Linux)', 'is up')
                elif ans[IP].ttl <= 128:
                    print(dst_ip, '(Windows)', 'is up')
                else:
                    print(dst_ip, '(Mac/Unix)', 'is up')
                alive_ip_list.append(dst_ip)
            elif ans[ICMP].type == 11:
                print(dst_ip, 'is timeout')
            elif ans[ICMP].type == 3:
                print(dst_ip, 'is unreachable')
            elif ans[ICMP].type == 4:
                print(dst_ip, 'source quench')
            elif ans[ICMP].type == 5:
                print(dst_ip, 'redirect')
            elif ans[ICMP].type == 12:
                print(dst_ip, '参数问题')
            else:
                print(dst_ip, '其他问题：[ICMP].type', ans[ICMP].type)
        else:
            print(dst_ip, 'is probably filtered(no response)')

    return alive_ip_list

```


## 端口扫描

基于TCP协议可以完成多种扫描。

### TCP扫描

通过与端口建立TCP连接判断端口的开放情况。如果端口开放，那么可以通过TCP的三次握手建立连接，然后断开连接即可；如果端口关闭，那么TCP握手无法完成。
这种方法的缺点是会在扫描的主机留下痕迹，因为一旦与主机的某个端口建立TCP连接，操作系统就会记录这条连接。并且，完成三次握手的时间会比较长，当扫描端口数量很多的时候速度会比较慢。
`nmap  -sT [IP]`

### SYN扫描

SYN扫描相比于TCP扫描更加简单，它发送一个SYN报文进行握手，如果端口开放那么会收到一个SYN&ACK报文，这时候回复一个RST报文断开连接即可，并且由于握手没有完成，操作系统不会记录这次扫描；如果端口关闭，那么不会收到SYN&ACK报文。
`nmap  -sS [IP]`

```python
def syn_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i))
        # pkt = IP(dst=str(dst_ip)) / TCP(sport=random.randint(1,65536),dport=int(i))
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is not None:
            # ans.summary()
            # ans.show()
            if ans[TCP].flags == 'SA':
                print(i, 'port is open')
                alive_port_list.append(i)
                rst = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags='R')
                sr1(rst, timeout=1, verbose=False)
            else:
                print(i, 'port is closed')
        else:
            print(i, 'port is filtered')

    return alive_port_list

```

*根据RFC文档，对于错误TCP报文无论是开放端口还是关闭端口都应该回复RST报文，windows按照规则，但是Linux对于开放端口不会回复RST报文。*

### ACK扫描

ACK扫描发送一个ACK报文进行端口探测。对于Windows系统，无论是开放还是关闭的端口都会回复RST报文；但是对于Linux系统，开放的端口将不会回复任何内容，关闭的端口则会回复RST报文。
另外，如果开启防火墙那么无论Windows操作系统还是Linux操作系统都不会对错误报文回复任何内容。
`nmap sA [IP]`

```python
def null_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags=0)
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is None:
            print(i, 'port is open or filtered')
            alive_port_list.append(i)
        else:
            # ans.summary()
            # ans.show()
            print(i, 'port is closed')

    return alive_port_list

```


### FIN扫描

向目标主机的端口发送FIN报文。
`nmap  -sF [IP]`

```python
def fin_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags='F')
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is None:
            print(i, 'port is open or filtered')
            alive_port_list.append(i)
        else:
            # ans.summary()
            # ans.show()
            print(i, 'port is closed')

    return alive_port_list

```


### NULL扫描


```python
def null_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags=0)
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is None:
            print(i, 'port is open or filtered')
            alive_port_list.append(i)
        else:
            # ans.summary()
            # ans.show()
            print(i, 'port is closed')

    return alive_port_list

```


### XMAS扫描


```python
def xmas_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags=1)
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is None:
            print(i, 'port is open or filtered')
            alive_port_list.append(i)
        else:
            # ans.summary()
            # ans.show()
            print(i, 'port is closed')

    return alive_port_list

```


### WINDOWS扫描


```python
def windows_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags='S')
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is not None:
            # ans.summary()
            # ans.show()
            if ans[TCP].window != 0:
                print(i, 'port is open')
                alive_port_list.append(i)
                rst = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags='R')
                sr1(rst, timeout=1, verbose=False)
            else:
                print(i, 'port is closed')
        else:
            print(i, 'port is filtered')

    return alive_port_list

```


## 源代码


```python
from scapy.all import *
from IPy import IP as IPY
from scapy.layers.inet import ICMP, IP, TCP
from scapy.layers.l2 import ARP


def preview(list):
    preview = input("预览（y/n）:")
    if preview == 'y' or 'Y':
        for li in list:
            print(li)


def arp(ipy):
    dst_ip_list = IPY(ipy)
    alive_ip_list = []

    for dst_ip in dst_ip_list:
        pkt = ARP(pdst=str(dst_ip))
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is not None:
            # ans.summary()
            # ans.show()
            alive_ip_list.append(dst_ip)
            print(dst_ip, 'is up')
        else:
            print(dst_ip, 'is closed')

    return alive_ip_list


def ping(ipy):
    dst_ip_list = IPY(ipy)
    alive_ip_list = []
    for dst_ip in dst_ip_list:
        pkt = IP(dst=str(dst_ip)) / ICMP() / b'hello'
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is not None:
            if ans[ICMP].type == 0:
                if ans[IP].ttl <= 64:
                    print(dst_ip, '(Linux)', 'is up')
                elif ans[IP].ttl <= 128:
                    print(dst_ip, '(Windows)', 'is up')
                else:
                    print(dst_ip, '(Mac/Unix)', 'is up')
                alive_ip_list.append(dst_ip)
            elif ans[ICMP].type == 11:
                print(dst_ip, 'is timeout')
            elif ans[ICMP].type == 3:
                print(dst_ip, 'is unreachable')
            elif ans[ICMP].type == 4:
                print(dst_ip, 'source quench')
            elif ans[ICMP].type == 5:
                print(dst_ip, 'redirect')
            elif ans[ICMP].type == 12:
                print(dst_ip, '参数问题')
            else:
                print(dst_ip, '其他问题：[ICMP].type', ans[ICMP].type)
        else:
            print(dst_ip, 'is probably filtered(no response)')

    return alive_ip_list


def syn_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i))
        # pkt = IP(dst=str(dst_ip)) / TCP(sport=random.randint(1,65536),dport=int(i))
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is not None:
            # ans.summary()
            # ans.show()
            if ans[TCP].flags == 'SA':
                print(i, 'port is open')
                alive_port_list.append(i)
                rst = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags='R')
                sr1(rst, timeout=1, verbose=False)
            else:
                print(i, 'port is closed')
        else:
            print(i, 'port is filtered')

    return alive_port_list


def ack_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags='A')
        # pkt.show()
        ans = sr1(pkt, timeout=0.2, verbose=False)
        if ans is None:
            print(i, 'port is filtered')
        else:
            # ans.summary()
            # ans.show()
            print(i, 'port is closed')

    return alive_port_list


def fin_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags='F')
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is None:
            print(i, 'port is open or filtered')
            alive_port_list.append(i)
        else:
            # ans.summary()
            # ans.show()
            print(i, 'port is closed')

    return alive_port_list


def null_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags=0)
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is None:
            print(i, 'port is open or filtered')
            alive_port_list.append(i)
        else:
            # ans.summary()
            # ans.show()
            print(i, 'port is closed')

    return alive_port_list


def xmas_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags=1)
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is None:
            print(i, 'port is open or filtered')
            alive_port_list.append(i)
        else:
            # ans.summary()
            # ans.show()
            print(i, 'port is closed')

    return alive_port_list


def windows_scan(dst_ip, n, m):
    alive_port_list = []
    for i in range(n, m):
        pkt = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags='S')
        # pkt.show()
        ans = sr1(pkt, timeout=1, verbose=False)
        if ans is not None:
            # ans.summary()
            # ans.show()
            if ans[TCP].window != 0:
                print(i, 'port is open')
                alive_port_list.append(i)
                rst = IP(dst=str(dst_ip)) / TCP(dport=int(i), flags='R')
                sr1(rst, timeout=1, verbose=False)
            else:
                print(i, 'port is closed')
        else:
            print(i, 'port is filtered')

    return alive_port_list


if __name__ == '__main__':
    # 主机ip（移动）
    # dst_ip = '10.132.68.173'
    # 网关ip
    # dst_ip = '10.132.168.1'
    # 子网
    # dst_ip = '10.132.168.0/21'
    # Windows虚拟机ip
    # dst_ip = '192.168.59.132'
    # Linux虚拟机ip
    # dst_ip = '192.168.59.131'

    while True:
        print('-------net scanner-------')
        service = input('你选择主机扫描或是端口扫描?（host/port）：')
        if service == 'host':
            way = input('请输入扫描方式（arp/ping）：')
            if way == 'ping':
                dst_ip = input('请输入你要查询的主机或者范围：')
                alive_ip_list = ping(dst_ip)
                preview(alive_ip_list)
            elif way == 'arp':
                dst_ip = input('请输入你要查询的主机或者范围：')
                alive_ip_list = arp(dst_ip)
                preview(alive_ip_list)
        elif service == 'port':
            way = input('请输入扫描方式（syn/windows/ack/fin/null/xmas）：')
            if way == 'syn':
                dst_ip = input('请输入你要查询的主机：')
                alive_port_list = syn_scan(dst_ip, 1, 1024)
                preview(alive_port_list)
            elif way == 'windows':
                dst_ip = input('请输入你要查询的主机：')
                alive_port_list = windows_scan(dst_ip, 1, 1024)
                preview(alive_port_list)
            elif way == 'ack':
                dst_ip = input('请输入你要查询的主机：')
                alive_port_list = ack_scan(dst_ip, 1, 1024)
                preview(alive_port_list)
            elif way == 'fin':
                dst_ip = input('请输入你要查询的主机：')
                alive_port_list = fin_scan(dst_ip, 1, 1024)
                preview(alive_port_list)
            elif way == 'null':
                dst_ip = input('请输入你要查询的主机：')
                alive_port_list = null_scan(dst_ip, 1, 1024)
                preview(alive_port_list)
            elif way == 'xmas':
                dst_ip = input('请输入你要查询的主机：')
                alive_port_list = xmas_scan(dst_ip, 1, 1024)
                preview(alive_port_list)
        else:
            print('i am a teapot')

```
