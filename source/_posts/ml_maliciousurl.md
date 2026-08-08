---
title: 恶意URL检测
date: 2023-10-10
categories:
  - ML
tags:
  - ML
  - AI
  - 人工智能
  - 机器学习
  - Python
  - sklearn
  - url
---



# 源代码


```python
# 数据提取&处理（csv）
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


def read_dmoz0409(file_path, lable):
    normal_pd = pd.read_csv(file_path, header=None, names=["url"], usecols=[1], nrows=14989)
    normal_pd["lable"] = lable
    # print(normal_pd)

    return normal_pd


def read_phishing_verified_online(file_path, lable):
    malicious_pd = pd.read_csv(file_path, usecols=[1], nrows=14989)
    malicious_pd["lable"] = lable
    # print(malicious_pd)

    return malicious_pd


def data_process(normal, malicious):
    all = pd.concat([normal, malicious])
    data = all["url"]
    lable = all["lable"]
    data, lable = shuffle(data, lable, random_state=42)


    return data, lable


def data_tokenizer(data):
    return re.findall(r'\w+', data)


def data_vectorizer(data, lable):
    vectorizer = TfidfVectorizer(tokenizer=data_tokenizer)
    x = vectorizer.fit_transform(data)
    y = lable

    return x, y, vectorizer


def model_train(x_train, y_train):
    model = LogisticRegression()
    model.fit(x_train, y_train)

    return model


def model_test(model, x_test, y_test):
    # accuracy = model.score(x_test, y_test)
    # print("模型准确率:", accuracy)
    y_predict = model.predict(x_test)
    report = classification_report(y_test, y_predict, labels=["malicious", "normal"], target_names=["恶意URL", "正常URL"],digits=2)

    return report


def model_save(model, vectorizer, report):
    save = input("是否保存训练的模型（y/n）：")
    if save == "y" or save == "Y":
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)
        with open('vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)
        with open('report.txt', 'w') as f:
            f.write(report)
        print("保存成功！")
        return True
    else:
        return False


def new_model():
    # 数据提取
    print("数据提取...")
    normal = read_dmoz0409("dmoz0409.csv", "normal")
    malicious = read_phishing_verified_online("phishing_verified_online.csv", "malicious")

    # 数据处理（合并，打乱数据集）
    print("数据处理...")
    data, lable = data_process(normal, malicious)

    # 特征提取
    print("向量化...")
    x, y, vectorizer = data_vectorizer(data, lable)
    # print(vectorizer.vocabulary_)
    # print(x.toarray)

    # 数据集划分
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

    # 模型训练
    print("模型训练...")
    model = model_train(x_train, y_train)

    # 模型评估
    report = model_test(model, x_test, y_test)
    print("模型评估报告：" + "\n", report)

    # 模型保存?
    model_save(model, vectorizer, report)


def use_model():
    while True:
        url_list = input("输入需要测试的url：").split("\n")
        with open("vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)
        x = vectorizer.transform(url_list)
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
        y_predict = model.predict(x)
        for i in range(len(url_list)):
            print(url_list[i], y_predict[i])

if __name__ == "__main__":
    choice = input("训练新的模型或是使用已经训练的模型（train/use）：")
    if choice == "train":
        new_model()
    elif choice=="use":
        print("-------恶意URL检测-------")
        use_model()
    else:
        print("无效的输入！")

```
