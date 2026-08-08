---
title: 爬虫（三）：结果保存
date: 2023-09-09
categories:
  - 爬虫
tags:
  - 爬虫
  - Python
  - Web
  - txt
---


*一般来说会把爬取的结果存储到列表或者字典中，然后将结果写入文件中*

# 一. TXT

代码比较简单,看一下应该就懂了…
对于列表

```Python
    # 是否保存
    save = input("共" + str(len(comment_list)) + "条记录，保存到commen.txt（y/n）：")
    if (save == "y" or save == "Y"):
        print("正在写入中...")
        with open("comment.txt", "w", encoding="utf-8") as f:
            for comment in tqdm(comment_list):
                f.writelines(comment + "\n")

```

对于字典

```Python
    # 是否保存？
    save = input("共" + str(len(list_dic_blog)) + "条记录，保存到blog.txt（y/n）：")
    if (save == "y" or save == "Y"):
        with open("blog.txt", "w", encoding='Utf-8') as f:
            for dic_blog in tqdm(list_dic_blog):
                f.writelines(str(dic_blog) + "\n")

```


# 二. JSON


```Python
    json_str = json.dumps(the_dict,indent=4,ensure_ascii=False)
    with open(file_name, 'w') as json_file:
        json_file.write(json_str)

```


# 三. Excel


```python
# -*- coding: utf-8 -*-
import xlsxwriter as xw
 
 
def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['序号', '酒店', '价格']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        insertData = [data[j]["id"], data[j]["name"], data[j]["price"]]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    workbook.close()  # 关闭表
 
 
# "-------------数据用例-------------"
testData = [
    {"id": 1, "name": "立智", "price": 100},
    {"id": 2, "name": "维纳", "price": 200},
    {"id": 3, "name": "如家", "price": 300},
]
fileName = '测试.xlsx'
xw_toExcel(testData, fileName)

```
