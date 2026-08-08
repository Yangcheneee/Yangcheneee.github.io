---
title: 爬虫（一）：请求&响应
date: 2023-09-07
categories:
  - 爬虫
tags:
  - 爬虫
  - Python
  - Web
  - Requests
---


*你需要先了解…*
*关于此文章…*

# 一. Requests-概述

Request是Python的第三方库，用于网络请求并接收返回的数据，你需要在Python的虚拟环境中安装使用。
- Request帮助你发送网络请求，同时你可以自定义Request携带的参数。
- 另外，Request模块接收响应请求的数据，并把Response作为函数的返回。
- 如果你想实现一个爬虫，对返回的网页文件进行Xpath/正则表达式解析，并将你需要的内容存储即可。

# 二. Request基础


## 1. 下载&安装


```cmd
pip/pip3 install requests

```


## 2. Request库


### 关于request

request支持各种HTTP方法，同时你可以指定请求所携带的内容。
- 获取响应文件

```Python
response = request.get(url)

```

- 带上请求头headers

```Python
response = request.get(url, headers = headers)

```

- 伪装浏览器代理，避免反爬虫*如果你向https://www.douban.com/发送请求，响应码为418，

```Python
headers = {
    'user-agent':
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/116.0.1938.69'
    }

```


### 关于response

你可以定义参数response（或者其他名字）接收request的返回。
- 返回响应状态码

```Python
status_code = response.status_code

```

- 返回网页HTML文件

```Python
content = response.content

```


### 了解更多

- 菜鸟教程

# 三. 代码实例


```python
    import requests

    url = 'https://www.baidu.com'
    response = requests.get(url)

    if(response.status_code == 200):
        print(response.content)
    else:
        print(response.status_code)

```


# 四. 问题？


## 1. response.text/response.content返回中文？

你可以使用 *response.content.decode(‘utf-8’)* 使得content正常的显示中文内容。
另外， *response.text* 使用推测的解码格式（ISO-8859-1），相当于 *response.content.decode(response.encoding)* 。

## 2. 418 | I’m a teapot？

大概：服务器表示我是一个茶壶，需要咖啡的话别找我。
当然，具体意思需要结合实际场景。
如果某些网站反爬虫，那么如果你不表示你的代理是浏览器的话，你也会收到418。
解决方案也很简单，使用 *headers{‘user-agent’:’xxx’}* 来声称你使用浏览器代理访问网站。