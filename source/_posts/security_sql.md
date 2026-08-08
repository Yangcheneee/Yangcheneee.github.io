---
title: Web安全：sqlmap使用
date: 2024-01-13
categories:
  - Web安全
tags:
  - Web安全
  - SQL注入
  - sqlmap
---



# sqlmap

介绍：[sqlmap](https://sqlmap.org/)
根据官方的说法：sqlmap是一个开源的渗透测试工具，它可以自动化的检测和利用SQL注入漏洞以及接管数据库服务器。

## sqlmap下载&&安装

sqlmap是一个python项目，下载即可，没有安装过程。
下载：[sqlmap](https://sqlmap.org/)

## sqlmap使用教程

切换到sqlmap下载目录进行cmd，使用python运行sqlmap.py。
*如果想在任意目录使用sqlmap.py，添加环境变量？*

### –help

使用`python sqlmap.py --help`进行测试。
![Alt text](/image-1.png)
sqlmap支持非常多的选项.
- Target选项：
- Request选项：

### 使用sqlmap实现漏洞利用

1. 首先寻找注入点