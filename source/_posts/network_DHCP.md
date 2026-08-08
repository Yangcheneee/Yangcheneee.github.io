---
title: DHCP安全性分析
date: 2023-09-25
categories:
  - 计算机网络
tags:
  - 计算机网络
  - internet
  - Protocol
  - DHCP
---



# 一. DHCP协议概述


## 1. 上网配置信息

计算机在连入WIFI后，需要获取网络配置信息才能正常上网，这些信息包括以下：
- 主机IP地址
- 子网掩码
- 网关IP地址
- DNS服务器IP地址

## 2. DHCP报文

当你连入WIFI之前，使用Warshark对进行抓包，可以捕获到到以下DHCP报文：
- DISCOVER
- OFFER
- REQUEST
- ACK
如果你已经接入WIFI，你可以在终端输入命令 *ipconfig release* 释放你已经获取的网络配置信息。重新接入WIFI。
如果你只是单纯断开WIFI，那么原来的网络配置信息并不会清空。相比正常的DHCP交互缺少 *DISCOVER* 和 *OFFER* 报文。

# 二. DHCP饿死攻击


## 1. 概述

DHCP服务器根据DHCP报文中提供的MAC地址分发IP地址。
因此，使用主机伪造DHCP报文中的MAC地址，耗尽DHCP能够分配的IP地址，那么正常连接网络的主机将不能够接入网络，攻击完成。

## 2. 试试？


### 环境

Windows7（虚拟机）；Ubuntu20.04（虚拟机）

### 下载Yersinia

*sudo apt install yersinia*
![Alt text](/img/network_dhcp/image-6.png)

### 打开Yersinia图形界面

*yersinia -G*
作者还挺幽默哈
![Alt text](/img/network_dhcp/image-5.png)

### 发起攻击

![Alt text](/img/network_dhcp/image-9.png)

### 攻击情况

warshark抓包分析yersinia发包速度很快，电脑受不了没做太多测试。
![Alt text](/img/network_dhcp/image-8.png)

# 三. 冒充DHCP服务器


## 1. 概述

当你向你的主机安装一个DHCP Server程序后，你的计算机也成为了一台DHCP服务器，但是你可以配置错误的网络配置信息，这可以使得接入网络的计算机无法获取正确的网络配置从而无法上网。

## 2. 试试？


### 实验环境

*Ubuntu20.04（虚拟机）：*
![Alt text](/img/network_dhcp/image.png)
*Windows7（虚拟机）：*
![Alt text](/img/network_dhcp/image-2.png)

### 在Ubuntu中安装dhcp服务器：


```
sudo apt-get install isc-dhcp-server

```


### 配置dhcp服务器相关信息：

*vim /etc/default/isc-dhcp-server*

```
# Defaults for isc-dhcp-server (sourced by /etc/init.d/isc-dhcp-server)

# Path to dhcpd's config file (default: /etc/dhcp/dhcpd.conf).
#DHCPDv4_CONF=/etc/dhcp/dhcpd.conf
#DHCPDv6_CONF=/etc/dhcp/dhcpd6.conf

# Path to dhcpd's PID file (default: /var/run/dhcpd.pid).
#DHCPDv4_PID=/var/run/dhcpd.pid
#DHCPDv6_PID=/var/run/dhcpd6.pid

# Additional options to start dhcpd with.
#	Don't use options -cf or -pf here; use DHCPD_CONF/ DHCPD_PID instead
#OPTIONS=""

# On what interfaces should the DHCP server (dhcpd) serve DHCP requests?
#	Separate multiple interfaces with spaces, e.g. "eth0 eth1".
INTERFACESv4="ens33"
INTERFACESv6=""

```

*vim /etc/dhcp/dhcpd.conf*

```
# dhcpd.conf
#
# Sample configuration file for ISC dhcpd
#
# Attention: If /etc/ltsp/dhcpd.conf exists, that will be used as
# configuration file instead of this file.
#

# option definitions common to all supported networks...
option domain-name "example.org";
option domain-name-servers 8.8.8.8;


# option domain-name-servers ns1.example.org, ns2.example.org;

default-lease-time 600;
max-lease-time 7200;

# The ddns-updates-style parameter controls whether or not the server will
# attempt to do a DNS update when a lease is confirmed. We default to the
# behavior of the version 2 packages ('none', since DHCP v2 didn't
# have support for DDNS.)
ddns-update-style none;

# If this DHCP server is the official DHCP server for the local
# network, the authoritative directive should be uncommented.
authoritative;

# Use this to send dhcp log messages to a different log file (you also
# have to hack syslog.conf to complete the redirection).
# log-facility local7;

# No service will be given on this subnet, but declaring it helps the 
# DHCP server to understand the network topology.

#subnet 10.152.187.0 netmask 255.255.255.0 {
#}

# This is a very basic subnet declaration.

subnet 192.168.59.0 netmask 255.255.255.0 {
   range 192.168.59.50 192.168.59.200;
   option routers 192.168.59.2;
   option subnet-mask 255.255.255.0;
   option broadcast-address 192.168.59.255;
}

# This declaration allows BOOTP clients to get dynamic addresses,
# which we don't really recommend.

#subnet 10.254.239.32 netmask 255.255.255.224 {
#  range dynamic-bootp 10.254.239.40 10.254.239.60;
#  option broadcast-address 10.254.239.31;
#  option routers rtr-239-32-1.example.org;
#}

# A slightly different configuration for an internal subnet.
#subnet 10.5.5.0 netmask 255.255.255.224 {
#  range 10.5.5.26 10.5.5.30;
#  option domain-name-servers ns1.internal.example.org;
#  option domain-name "internal.example.org";
#  option subnet-mask 255.255.255.224;
#  option routers 10.5.5.1;
#  option broadcast-address 10.5.5.31;
#  default-lease-time 600;
#  max-lease-time 7200;
#}

# Hosts which require special configuration options can be listed in
# host statements.   If no address is specified, the address will be
# allocated dynamically (if possible), but the host-specific information
# will still come from the host declaration.

#host passacaglia {
#  hardware ethernet 0:0:c0:5d:bd:95;
#  filename "vmunix.passacaglia";
#  server-name "toccata.example.com";
#}

# Fixed IP addresses can also be specified for hosts.   These addresses
# should not also be listed as being available for dynamic assignment.
# Hosts for which fixed IP addresses have been specified can boot using
# BOOTP or DHCP.   Hosts for which no fixed address is specified can only
# be booted with DHCP, unless there is an address range on the subnet
# to which a BOOTP client is connected which has the dynamic-bootp flag
# set.
#host fantasia {
#  hardware ethernet 08:00:07:26:c0:a5;
#  fixed-address fantasia.example.com;
#}

# You can declare a class of clients and then do address allocation
# based on that.   The example below shows a case where all clients
# in a certain class get addresses on the 10.17.224/24 subnet, and all
# other clients get addresses on the 10.0.29/24 subnet.

#class "foo" {
#  match if substring (option vendor-class-identifier, 0, 4) = "SUNW";
#}

#shared-network 224-29 {
#  subnet 10.17.224.0 netmask 255.255.255.0 {
#    option routers rtr-224.example.org;
#  }
#  subnet 10.0.29.0 netmask 255.255.255.0 {
#    option routers rtr-29.example.org;
#  }
#  pool {
#    allow members of "foo";
#    range 10.17.224.10 10.17.224.250;
#  }
#  pool {
#    deny members of "foo";
#    range 10.0.29.10 10.0.29.230;
#  }
#}

```


### 启动DHCP服务器

*启动DHCP服务器：sudo systemctl start isc-dhcp-server.service*
*查看DHCP服务器运行状态：sudo systemctl status isc-dhcp-server.service*
*关闭DHCP服务器：sudo systemctl stop isc-dhcp-server.service*
![Alt text](/img/network_dhcp/image-1.png)

### Windows7获取Ubuntu20.04的DHCP服务器网络配置

如果你已经连接网络，使用 *ipconfig /release* 释放获取的网络配置
然后，使用 *ipconfig /renew* 重新连接DHCP服务器获取网络配置
![Alt text](/img/network_dhcp/image-3.png)
可以看见Windows7网络配置发生了改变
![Alt text](/img/network_dhcp/image-4.png)

# 四. DHCP中间人攻击

这部分原理与ARP中间人攻击一致…
中间人攻击基本都是用ARP实现吗？…