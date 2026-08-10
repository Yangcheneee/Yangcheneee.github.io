---
title: 微博爬虫实例
date: 2023-09-15
cover: /img/cover/8.jpg
categories:
  - 爬虫
tags:
  - 爬虫
  - Python
  - Web
  - Requests
  - 微博
---


*你需要先了解…*
*关于此文章…*

# 一. 帖子

懒得写，贴个源码。爬不了的话，传入你的cookie

```python
import requests  # 网络请求
import random  # 与time控制网络请求频率
import time  # 与random控制网络请求频率
import json  # 响应的json数据分析
from tqdm import tqdm  # 进度条


# 由此函数完成 请求-响应解析 的过程
# 接收评论json文件的url，解析json文件并返回评论信息字典（max，total_number,max_id，max_id_type，commentlist[]）
def getCommentTnfo(commenturl):
    # 请求评论json文件
    # print(commenturl)
    headers = {
        "cookie": "",
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/116.0.1938.76'
    }
    response = requests.get(commenturl, headers=headers)

    # 解析json文件内容：max_id，max_id_type，commentlist[]
    # max,total_number是第一次请求要获取的信息
    dic = {
        'max': 0,
        'total_number': 0,
        'max_id': 0,
        'max_id_type': 0,
        'comment_list': []
    }
    comment_json = json.loads(response.text)
    if (comment_json["ok"] == 1):
        data = comment_json["data"]
        dic["max"] = data["max"]
        dic["total_number"] = data["total_number"]
        dic["max_id"] = data["max_id"]
        dic["max_id_type"] = data["max_id_type"]
        list = data["data"]
        for li in list:
            user = li["user"]
            name = user["screen_name"]
            gender = user["gender"]
            source = li["source"]
            text = li["text"]
            # print(name + "(" + gender + "|" + source + ")" + ":" + text)
            dic["comment_list"].append(name + "(" + gender + "|" + source + ")" + ":" + text)

        return dic
    # 如果不写else，那么python默认函数返回None
    else:
        return dic

# 此函数调用getCommentList函数,输入不同的max_id
# 输入文章url，返回评论信息
def getcomments():
    blog = input("请输入帖子的url:")
    id = blog.split('/')[-1]
    mid = blog.split('/')[-1]
    max_id_type = 0
    comment_list = []

    print("正在分析中...")
    comment_url = "https://m.weibo.cn/comments/hotflow?id=" + id + "&mid=" + mid + "&max_id_type=" + str(max_id_type)
    dic = getCommentTnfo(comment_url)
    # max，total_number第一次请求时赋值，分析有多少页和多少评论
    max = dic["max"]
    total_number = dic["total_number"]
    max_id = dic["max_id"]
    max_id_type = dic["max_id_type"]
    comment_list = comment_list + dic["comment_list"]
    print("查询到" + str(max) + "页内容，共计" + str(total_number) + "条评论")

    print("正在爬取中...")
    for i in tqdm(range(max-1)):
    # for i in range(max - 1):
        time.sleep(random.uniform(1.0, 3.0))
        comment_url = "https://m.weibo.cn/comments/hotflow?id=" + id + "&mid=" + mid + "&max_id=" + str(max_id) + "&max_id_type=" + str(max_id_type)
        if(dic["max_id"]!=0):
            dic = getCommentTnfo(comment_url)
            max_id = dic["max_id"]
            max_id_type = dic["max_id_type"]
            comment_list = comment_list + dic["comment_list"]

    # 是否预览
    preview = input("共" + str(len(comment_list)) + "条记录，预览（y/n）：")
    if (preview == "y" or preview == "Y"):
        for comment in comment_list:
            print(comment)

    # 是否保存
    save = input("共" + str(len(comment_list)) + "条记录，保存（y/n）：")
    if (save == "y" or save == "Y"):
        print("正在写入中...")
        with open("comment.txt", "w", encoding="utf-8") as f:
            for comment in tqdm(comment_list):
                f.writelines(comment + "\n")


if __name__ == '__main__':
    while (True):
        print("-------微博评论爬虫-------")
        print("             by liangyue")
        getcomments()

```


# 二. 评论


```python
import requests  # 网络请求
import random  # 与time控制网络请求频率
import time  # 与random控制网络请求频率
import json  # 响应的json数据分析
from tqdm import tqdm  # 进度条


def analyse(blogurl):
    # 请求&响应
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/116.0.1938.76'
    }
    response = requests.get(blogurl, headers=headers)

    # 响应解析
    list_dic_blog = []
    response_json = json.loads(response.text)
    if (response_json["ok"] == 1):
        data = response_json["data"]
        cards = data["cards"]
        for card in cards:
            dic_blog = {
                "user_name": "",
                "user_gender": "",
                "user_region": "",
                "blog_text": "",
                "blog_url": ""
            }
            if "mblog" in card:
                myblog = card["mblog"]
                user = myblog["user"]
                dic_blog["user_name"] = user["screen_name"]
                dic_blog["user_gender"] = user["gender"]
                if ("status_province" in myblog):
                    dic_blog["user_region"] = myblog["status_province"]
                mid = myblog["mid"]
                dic_blog["blog_text"] = myblog["text"]
                dic_blog["blog_url"] = "https://m.weibo.cn/detail/" + mid
                list_dic_blog.append(dic_blog)
            if "card_group" in card:
                card_grop = card["card_group"]
                if "mblog" in card_grop[0]:
                    myblog = (card_grop[0])["mblog"]
                    user = myblog["user"]
                    dic_blog["user_name"] = user["screen_name"]
                    dic_blog["user_gender"] = user["gender"]
                    if ("status_province" in myblog):
                        dic_blog["user_region"] = myblog["status_province"]
                    mid = myblog["mid"]
                    dic_blog["blog_text"] = myblog["text"]
                    dic_blog["blog_url"] = "https://m.weibo.cn/detail/" + mid
                list_dic_blog.append(dic_blog)
        return list_dic_blog
    else:
        return list_dic_blog

def getblog():
    keyword = input("请输入关键字：")
    page = input("请输入爬取页码（1-100）：")
    page = int(page)
    if (page < 1 or page > 100):
        exit(418)

    print("正在爬取中...")
    list_dic_blog = []
    for i in tqdm(range(page)):
        if (page == 0):
            blogurl = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D" + keyword + "&page_type=searchall"
            list_dic_blog = list_dic_blog + analyse(blogurl)
        else:
            time.sleep(random.uniform(1, 2))
            blogurl = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D" + keyword + "&page_type=searchall" + "&page=" + str(
                i)
            list_dic_blog = list_dic_blog + analyse(blogurl)

    # 是否预览？
    preview = input("共" + str(len(list_dic_blog)) + "条记录，你是否希望预览（y/n）：")
    if (preview == "y" or preview == "Y"):
        for dic_blog in list_dic_blog:
            print(dic_blog)

    # 是否保存？
    save = input("共" + str(len(list_dic_blog)) + "条记录，保存到blog.txt（y/n）：")
    if (save == "y" or save == "Y"):
        with open("blog.txt", "w", encoding='Utf-8') as f:
            for dic_blog in tqdm(list_dic_blog):
                f.writelines(str(dic_blog) + "\n")

if __name__ == '__main__':
    print("-------微博帖子-------")
    print("           By liangyue")
    while(True):
        getblog()

```
