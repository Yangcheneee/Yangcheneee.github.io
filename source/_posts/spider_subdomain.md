---
title: 子域名爬虫
date: 2023-09-14
categories:
  - 爬虫
tags:
  - 爬虫
  - 子域名
---



# 子域名爬虫


## 百度

百度子域名搜索语法：`domain:xxx.com`
百度将子域名存在于 *div* 标签的 *mu* 属性中，你可以通过 *class=”result c-container xpath-log new-pmd”* 找到这个 *div* 标签。

```python
# 定义一个采用baidu搜索的方法
def baidu_search():
    print("Powered by baidu...")
    domain = input("input the domain you want to query:")
    page = int(input("The more page,the more subdomain(not sure):"))
    if page < 1 or page > 100:
        exit(418)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
        # 'cookie': ''
    }

    print("url requesting...")
    resp_list = []
    for i in tqdm(range(page)):
        time.sleep(random.uniform(0.3, 2.0))
        if i == 0:
            url = "https://www.baidu.com/s?wd=domain%3A" + domain
            resp = requests.get(url, headers=headers)
            resp_list.append(resp)
        else:
            url = "https://www.baidu.com/s?wd=domain%3A" + domain + "&pn=" + str(i*10)
            resp = requests.get(url, headers=headers)
            resp_list.append(resp)

    print("response analying...")
    time.sleep(1)
    subdomain_list = []  # 定义一个空列表用于存储收集到的子域名
    for resp in tqdm(resp_list):
        # 锁定含有子域名的标签
        # 创建一个BeautifulSoup对象，第一个参数是网页源码，第二个参数是Beautiful Soup 使用的 HTML 解析器，
        soup = BeautifulSoup(resp.content, 'html.parser')
        tag_div = soup.find_all("div", class_='result c-container xpath-log new-pmd')
        for i in tag_div:
            link = i.get('mu')  # 获取标签内mu属性值，即子域名
            # urlparse是一个解析url的工具，scheme获取url的协议名，netloc获取url的网络位置
            subdomain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
            # 如果解析后的domain存在于Subdomain中则跳过，否则将domain存入子域名表中
            if (subdomain in subdomain_list) | (domain not in subdomain):
                pass
            else:
                subdomain_list.append(subdomain)

    # preview？
    print(str(len(subdomain_list))+" records total")
    preview = input("preview or not(y/n):")
    if preview == "y" or preview == "Y":
        for subdomain in subdomain_list:
            print(subdomain)

    # isSave?
    save = input("save or not(y/n):")
    if save == "y" or save == "Y":
        print("file writing...")
        with open('subdomain.txt', 'w') as f:
            # for subdomain in subdomain_list:
            for subdomain in tqdm(subdomain_list):
                f.writelines(subdomain + "\n")

```


## 必应

必应子域名搜索语法：`domain：xxx.com`
必应的子域名位于 **h2** 标签下的 **a** 标签的 **href** 属性，很多链接都会放在a标签的href属性中。
另外在 *div* 标签的 *cite* 标签也可以找到，通过属性 *class=”b_attribution”* 可以找到这个 *div* 标签。

# 定义一个采用bing搜索的方法


```python
# 定义一个采用bing搜索的方法
def bing_search():
    print("Powered by bing...")
    domain = input("input the domain you want to query:")
    page = int(input("The more page,the more subdomain(not sure):"))
    if page < 1 or page > 100:
        exit(418)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
        # 'cookie':''
    }

    resp_list = []
    print("requesting...")
    for i in tqdm(range(0, page)):
        time.sleep(random.uniform(0.3, 2.0))
        if i == 0:
            url = "https://cn.bing.com/search?q=domain%3a" + domain
            resp = requests.get(url=url, headers=headers)
            resp_list.append(resp)
        else:
            url = "https://cn.bing.com/search?q=domain%3a" + domain + "first=" + str(i*10)
            resp = requests.get(url=url, headers=headers)
            resp_list.append(resp)

    subdomain_list = []
    print("response analying...")
    time.sleep(1)
    for resp in tqdm(resp_list):
        # 创建一个BeautifulSoup对象，第一个参数是网页源码，第二个参数是Beautiful Soup 使用的 HTML 解析器，
        soup = BeautifulSoup(resp.content, 'html.parser')
        # 锁定含有子域名的标签
        tag_cite = soup.find_all("cite")
        for i in tag_cite:
            link = i.text
            # urlparse是一个解析url的工具，scheme获取url的协议名，netloc获取url的网络位置
            subdomain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
            # 如果解析后的domain存在于Subdomain中则跳过，否则将domain存入子域名表中
            if subdomain in subdomain_list:
                pass
            else:
                subdomain_list.append(subdomain)

    # preview？
    print(str(len(subdomain_list))+" records total")
    preview = input("preview or not(y/n):")
    if preview == "y" or preview == "Y":
        for subdomain in subdomain_list:
            print(subdomain)

    # save?
    save = input("save or not(y/n):")
    if save == "y" or save == "Y":
        print("file writing...")
        with open('subdomain.txt', 'w') as f:
            for subdomain in tqdm(subdomain_list):
                f.writelines(subdomain + "\n")

```


## 源代码


```python
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tqdm import tqdm


# 定义一个采用baidu搜索的方法
def baidu_search():
    print("Powered by baidu...")
    domain = input("input the domain you want to query:")
    page = int(input("The more page,the more subdomain(not sure):"))
    if page < 1 or page > 100:
        exit(418)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
        # 'cookie': ''
    }

    print("url requesting...")
    resp_list = []
    for i in tqdm(range(page)):
        time.sleep(random.uniform(0.3, 2.0))
        if i == 0:
            url = "https://www.baidu.com/s?wd=domain%3A" + domain
            resp = requests.get(url, headers=headers)
            resp_list.append(resp)
        else:
            url = "https://www.baidu.com/s?wd=domain%3A" + domain + "&pn=" + str(i*10)
            resp = requests.get(url, headers=headers)
            resp_list.append(resp)

    print("response analying...")
    time.sleep(1)
    subdomain_list = []  # 定义一个空列表用于存储收集到的子域名
    for resp in tqdm(resp_list):
        # 锁定含有子域名的标签
        # 创建一个BeautifulSoup对象，第一个参数是网页源码，第二个参数是Beautiful Soup 使用的 HTML 解析器，
        soup = BeautifulSoup(resp.content, 'html.parser')
        tag_div = soup.find_all("div", class_='result c-container xpath-log new-pmd')
        for i in tag_div:
            link = i.get('mu')  # 获取标签内mu属性值，即子域名
            # urlparse是一个解析url的工具，scheme获取url的协议名，netloc获取url的网络位置
            subdomain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
            # 如果解析后的domain存在于Subdomain中则跳过，否则将domain存入子域名表中
            if (subdomain in subdomain_list) | (domain not in subdomain):
                pass
            else:
                subdomain_list.append(subdomain)

    # preview？
    print(str(len(subdomain_list))+" records total")
    preview = input("preview or not(y/n):")
    if preview == "y" or preview == "Y":
        for subdomain in subdomain_list:
            print(subdomain)

    # isSave?
    save = input("save or not(y/n):")
    if save == "y" or save == "Y":
        print("file writing...")
        with open('subdomain.txt', 'w') as f:
            # for subdomain in subdomain_list:
            for subdomain in tqdm(subdomain_list):
                f.writelines(subdomain + "\n")


# 定义一个采用bing搜索的方法
def bing_search():
    print("Powered by bing...")
    domain = input("input the domain you want to query:")
    page = int(input("The more page,the more subdomain(not sure):"))
    if page < 1 or page > 100:
        exit(418)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
        # 'cookie':''
    }

    resp_list = []
    print("requesting...")
    for i in tqdm(range(0, page)):
        time.sleep(random.uniform(0.3, 2.0))
        if i == 0:
            url = "https://cn.bing.com/search?q=domain%3a" + domain
            resp = requests.get(url=url, headers=headers)
            resp_list.append(resp)
        else:
            url = "https://cn.bing.com/search?q=domain%3a" + domain + "first=" + str(i*10)
            resp = requests.get(url=url, headers=headers)
            resp_list.append(resp)

    subdomain_list = []
    print("response analying...")
    time.sleep(1)
    for resp in tqdm(resp_list):
        # 创建一个BeautifulSoup对象，第一个参数是网页源码，第二个参数是Beautiful Soup 使用的 HTML 解析器，
        soup = BeautifulSoup(resp.content, 'html.parser')
        # 锁定含有子域名的标签
        tag_cite = soup.find_all("cite")
        for i in tag_cite:
            link = i.text
            # urlparse是一个解析url的工具，scheme获取url的协议名，netloc获取url的网络位置
            subdomain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
            # 如果解析后的domain存在于Subdomain中则跳过，否则将domain存入子域名表中
            if subdomain in subdomain_list:
                pass
            else:
                subdomain_list.append(subdomain)

    # preview？
    print(str(len(subdomain_list))+" records total")
    preview = input("preview or not(y/n):")
    if preview == "y" or preview == "Y":
        for subdomain in subdomain_list:
            print(subdomain)

    # save?
    save = input("save or not(y/n):")
    if save == "y" or save == "Y":
        print("file writing...")
        with open('subdomain.txt', 'w') as f:
            for subdomain in tqdm(subdomain_list):
                f.writelines(subdomain + "\n")


if __name__ == '__main__':
    print("Subdomain Getter...")
    while True:
        engine = input("select a engine(baidu/bing):")
        if engine == "baidu":
            baidu_search()
        elif engine == "bing":
            bing_search()
        else:
            exit(418)

```
