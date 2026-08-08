---
title: 博客（一）：从零开始搭建你的个人博客
date: 2023-08-20
categories:
  - 博客
tags:
  - 博客
  - nodejs
  - npm
  - git
  - github
  - hexo
  - butterfly
---


*此文章将会指引你搭建hexo框架的博客，并将其部署到Git Hub上。*

# 一. 环境搭建


## 1. 安装Nodejs（npm）

下载链接：[Nodejs官方网站](https://nodejs.org/en)
这里直接选择官方推荐的稳定版本：Recommend For Most Users。
![Alt text](/img/blog_hexo/image.png)
安装过程一路回车就好，默认选项不需要任何额外的操作。
安装完成以后，打开cmd。输入命令：*node -v*，若返回nodejs版本信息则安装成功。
nodejs内置npm。输入命令*npm -v*，返回npm版本信息则安装成功。
![Alt text](/img/blog_hexo/image-1.png)

## 2. 安装Git

[Git下载网址](https://git-scm.com/download/win)
下载标注的版本。
![Alt text](/img/blog_hexo/image-2.png)
安装一路回车就好。

# 二. 本地部署你的博客


## 1. 安装Hexo，新建hexo框架项目

打开cmd输入命令：*npm install -g hexo-cli*，等待安装完成即可。
安装完成以后输入命令：*hexo -v*查看版本，返回结果则安装成功。
选择一个用于放置博客文件的文件夹，在此目录下使用命令：*hexo init myblog*，新建你的博客项目。你可以看到在你的文件夹下多了一个myblog的项目。
输入命令：*cd myblog*进入myblog项目，安装npm：*npm install*即可。

## 2. 在本地启动你的项目

在你的项目根目录下输入命令：*hexo g*生成博客网站的文件。
然后输入命令：*hexo server*启动你的博客。
接下来，你可以输入网址：[http://localhost/4000](http://localhost/4000) 以访问你的个人博客。
像这样：
![Alt text](/img/blog_hexo/image-5.png)
当然，如果你想停止你的博客服务，输入命令：*Ctrl C*即可。

# 四. GiHub搭建博客

如果你没有GitHub账号，请前往官网注册：[GitHub官网](https://github.com/) 

## 1. 新建Pages类型仓库

![Alt text](/img/blog_hexo/image-3.png)
**你的仓库名（Repository name）必须是：xxx.github.io（xxx是你GitHub的用户名）**
下面的选项选择Public。
![Alt text](/img/blog_hexo/image-4.png)

## 2. 安装hexo上传插件

输入命令：*npm install hexo-deployer-git –save*
这个插件使用git上传hexo生成的网页文件。

## 3. 修改hexo配置文件指定仓库路径

你可以在目录blog\hexo下找到 **_config.yml** 文件，修改以下配置。
如果你需要在文档快速定位以下内容，使用 **Ctrl+F** 查找 **Deployment** ，你可以定位文档中所有出现Deployment的地方。

```
# Deployment
## Docs: https://hexo.io/docs/one-command-deployment
deploy:
type: 'git'
repo: https://github.com/Yangcheneee/Yangcheneee.github.io.git
branch: main

```

*这里将yangcheneee修改为你的GitHub用户名即可*

## 4. 部署博客到对应仓库

输入命令：*hexo clean*清除之前生成的博客文件
输入命令：*hexo generate*（*hexo g*）生成博客的静态网页文件
输入命令：*hexo deploy*（*hexo d*）将生成的博客文件推送到github仓库
将博客文件上传到GitHub仓库时，需要进行身份验证，在这个过程中保持登录GitHub，根据提示完成验证即可。
接下来访问网站：[http://xxx.github.io](http://xxx.github.io/) （xxx为你的用户名）即可。