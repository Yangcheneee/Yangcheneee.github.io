---
title: XSS注入检测
date: 2023-10-09
categories:
  - ML
tags:
  - ML
  - AI
  - 人工智能
  - 机器学习
  - Python
  - sklearn
  - XSS
---



# 源代码

*pd对象和python字典类似，行为属性，列为列表*

### pd.read_csv()函数：

- 参数header：pandas是否选择csv文件第一行作为列名
- 参数usecols：pandas读取csv文件列

### pd.to_csv()函数：

- 参数header：pandas是否将属性名写入csv文件
- 参数columns：pandas写入csv文件的属性（影响写入的顺序）
- 参数index：pandas是否写入序号

```python
# 数据提取&处理
import pandas as pd
from sklearn.utils import shuffle
# 特征提取
import re
from sklearn.feature_extraction.text import TfidfVectorizer
# 训练集和测试集划分
from sklearn.model_selection import train_test_split
# 逻辑回归算法训练模型
from sklearn.linear_model import LogisticRegression
# 模型评估报告打印
from sklearn.metrics import classification_report
# 模型保存
import pickle


def read_csv(file_path, lable):
    data = pd.read_csv(file_path, header=None, names=["str"], usecols=[0])
    data["lable"] = lable

    return data


# normal = read_csv("dmzo_nomal.csv", "normal")
# xss = read_csv("xssed.csv", "xss")


def data_process(normal, xss):
    all = pd.concat([normal, xss])
    data = all["str"]
    lable = all["lable"]
    data, lable = shuffle(data, lable, random_state=42)

    return data, lable


# data ,lable = data_process(normal, xss)


def data_tokenizer(data):
    return re.findall(r'\w+', data)


def data_vectorizer(data,lable):
    vectorizer = TfidfVectorizer(tokenizer=data_tokenizer)
    x = vectorizer.fit_transform(data)
    y = lable

    return x, y, vectorizer


# x, y ,vectorizer = data_vectorizer(data, lable)
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)


def model_train(x_train, y_train):
    model = LogisticRegression()
    model.fit(x_train, y_train)

    return model


# model = model_train(x_train, y_train)


def model_evaluate(x_test,y_test):
    y_predict = model.predict(x_test)
    report = classification_report(y_test, y_predict, labels=["xss", "normal"], target_names=["xss字符串", "正常字符串"],digits=2)

    return report


# report = model_evaluate(x_test, y_test)
# print(report)


def model_save(model, vectorizer):
    save = input("是否保存训练的模型（y/n）：")
    if save == "y" or "Y":
        print(save)
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)
        with open('vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)
        print("保存成功！")
        return True
    else:
        return False


# model_save(model, vectorizer)

if __name__ == "__main__":
    print("-------XSS检测-------")
    while True:
        with open("model.pkl", 'rb') as f:
            model = pickle.load(f)
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        str_list = input("输入需要检测的字符串:").split("\n")
        x = vectorizer.transform(str_list)
        y_predict = model.predict(x)
        print("检测结果为：",y_predict)

```
