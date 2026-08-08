---
title: Web开发：MySQL
date: 2023-11-09
categories:
  - Web开发
tags:
  - Web开发
  - MySQL
---



# 一. MySQL概述


## MySQL启动&终止


### 启动服务

`net start mysql`

### 终止服务

`net stop mysql`

### 登录：

*如果找不到环境变量（路径），则在SQL文件的bin目录下*
*启动不成功也可能是mysql服务没开*
`mysql -u root -p`

## MySQL操作语言


### 数据库：

`show databases`
`use xxx`
`show tables`

### 查：

`select * from table`

### 增：

`insert into table values(int,"str")`

### 删：

`delete from table where id=int`

### 改：

`update table set col="xxx" where id=int`