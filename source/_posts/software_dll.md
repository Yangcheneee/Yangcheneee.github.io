---
title: 恶意代码
date: 2024-01-17
categories:
  - 恶意代码
tags:
  - 恶意代码
---



# 恶意代码分析概述


## 静态分析方法


### 恶意代码指纹：哈希

- WinMD5

### 反病毒引擎扫描

目前收集到的在线反病毒引擎：
- VirusTotal
- VirScan

### 特征字符串：Strings

- Strings
使用命令`Strings main.exe > main.txt`将可执行文件中的字符重定向到文件main.txt中。

### 去壳与反汇编

压缩和混淆的代码通常至少包括LoadLibrary和GetProcAddress函数，它们用于加载和访问其他函数。
待学习。。。

## 2. 动态分析技术

虚拟机&&虚拟机逃逸

### 进程查看

[Process Explore](https://learn.microsoft.com/zh-cn/sysinternals/downloads/procmon)
[Process Monitor](https://learn.microsoft.com/zh-cn/sysinternals/downloads/process-explorer)

### 注册表相关

[sourceforge](https://sourceforge.net/)
[regshot](https://sourceforge.net/projects/regshot/)

### 网络相关

warshark