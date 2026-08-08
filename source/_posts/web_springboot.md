---
title: Web开发（二）-SpringBoot
date: 2023-09-07
categories:
  - Web开发
tags:
  - Web开发
  - web
  - web开发
  - java
  - springboot
---


*你需要先了解…*
*有关此文章…*

# 一. 新建SpringBoot项目


## 1. IDEA新建SpringBoot项目

(参考文章)[[https://blog.csdn.net/qq_43006591/article/details/106137465]](https://blog.csdn.net/qq_43006591/article/details/106137465])

# 二. SpringBoot框架解析


## 1. .idea


## 2. .mvn


## 3. src


### /main

- /resource/static存放CSS，JS以及图片等
- /resource/templates存放Web页面
- application.properties/application.yml用于存放程序的各种依赖模块的配置信息，比如 服务端口，数据库连接配置等
- /main/java/com.example.xxx存放java源码
- /main/java/Application.javaSpringBoot 程序执行的入口，执行该程序中的 main 方法，启动当前SpringBoot项目。

### /test

与mian目录结构类似，没有resource目录。
存放测试代码。

## 4. target

如果你想测试某个单元，在这里启动它。

## 5. gitignore

使用版本控制工具 git 的时候，设置一些忽略提交的内容

## 6. xxx.iml

intellij idea的工程配置文件，里面是当前project的一些配置信息

## 7. HELP.md

项目的帮助文档，相当于记事本

## 8. mvnw

主要是用于当用户使用maven的命令时，发现本地的maven版本与.mvn文件夹下的maven-wrapper.properties文件中的maven版本不一致，就会下载maven-wrapper.properties文件中的maven版本，然后来执行maven命令，用于Linux环境

## 9. mvnw.cmd

同上，用于Windows环境

## 10. pom.xml

maven依赖的配置

# 三. 了解更多

(SpringBoot官网)[[https://spring.io/projects/spring-boot]](https://spring.io/projects/spring-boot])