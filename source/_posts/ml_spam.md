---
title: 垃圾邮件检测
date: 2023-10-06
cover: /img/cover/19.png
categories:
  - ML
tags:
  - ML
  - AI
  - 人工智能
  - 机器学习
  - Python
  - sklearn
  - spam
  - jieba
---



## 1. 数据集


### tre06c

tre06c/data：邮件数据，包括真实世界的正常邮件和垃圾邮件
tre06c/full：标签

## 2. 数据提取&处理

*jieba官方文档*
*列表推导式（expression for li in list if condition）*

### 读取邮件数据

递归读取目录trec06c/data的文件，获取邮件数据并进行分词处理，返回处理后的邮件列表。

```python
# 读取邮件数据
def read_file(file_path):
    # print(file_path)
    email_list = []
    files = os.listdir(file_path)
    for file in files:
        if os.path.isdir(file_path + '/' + file):
            email_list = email_list + read_file(file_path + '/' + file)
        else:
            with open(file_path + '/' + file, 'r', encoding='gbk', errors='ignore') as f:
                email = f.read()

            # 替换非汉字字符
            email = re.sub(r"[^\u4e00-\u9fff]", " ", email)
            # 替换连续的空格
            email = re.sub(r"\s{2,}", " ", email)
            # 去除首尾的空格
            email = email.strip()
            # 结巴分词
            email = [word for word in jieba.lcut(email) if word.strip() != ' ']
            email = ' '.join(email)

            email_list.append(email)

    return email_list


# email = read_file("trec06c/data")

```


### 读取标签数据

读取文件trec06c/full/index，获取邮件标签列表。

```python
# 读取标签数据
def read_lable(file_path):
    lable = []
    with open(file_path, "r") as f:
        for l in f.readlines():
            if "s" in l:
                lable.append("spam")
            else:
                lable.append("ham")

    return lable


# lable = read_lable("trec06c/full/index")

```


### 打乱数据顺序


```python
def data_process(email, lable):
    email, lable = shuffle(email, lable, random_state=42)

    return email, lable


# email, lable = data_process(email, lable)

```


## 3. 词云

随便写写，感觉词云有一些bug，同一个词重复出现

```python
# 词云
def word_cloud(text):
    wc = WordCloud(
        background_color = "white",
        max_words = 200,
        # 可以使用其他字体
        # 但是如果无法正常显示，需要更换字体
        font_path = "C:\Windows\Fonts\SIMYOU.ttf",
        min_font_size = 15,
        max_font_size = 50,
        width = 600
    )
    wordcloud = wc.generate(text)
    wordcloud.to_file('jieba.jpg')
with open('./jieba.txt', 'r', encoding='utf-8') as f:
    txt = f.readlines()
showWordCloud(' '.join(txt))

```

全部邮件词云：
![Alt text](/img/ai_spamdetection/email.jpg)

```python
spam_list = []
ham_list = []
with open("./full.txt", "r", encoding='utf-8') as f:
    tag_list = f.readlines()
    with open("./jb.txt", "r", encoding="utf-8") as g:
        email_list = g.readlines()
        i = 0
        for tag in tag_list:
            if tag[0] == '1':
                spam = email_list[i]
                spam_list.append(spam)
            elif tag[0] == '0':

                ham = email_list[i]
                ham_list.append(ham)
            i = i + 1

```

垃圾邮件词云：
![Alt text](/img/ai_spamdetection/ham.jpg)
正常邮件词云：
![Alt text](/img/ai_spamdetection/spam.jpg)

## 4. 特征提取


```python
def data_vectorizer(email,lable):
    # 邮件样本已经分好了词，词之间用空格隔开，所以 tokenizer=tokenizer_space
    vectoring = TfidfVectorizer(input='content', analyzer='word')
    x = vectoring.fit_transform(email)
    y = lable

    return x, y, vectoring


# x, y, vectorizer = data_vectorizer(email, lable)

```


## 5. 换分数据集


```python
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

```


## 6. 模型训练


```python
def model_train(x_train, y_train):
    model = svm.LinearSVC()
    model.fit(x_train, y_train)

    return model


# model = model_train(x_train, y_train)

```


## 7. 模型测试


```python
def model_test(x_test, y_test):
    y_pred = model.predict(x_test)
    report = classification_report(y_test, y_pred, digits=2)

    return report


# report = model_test(model)

```


## 8. 模型保存


```python
def model_save(model,vectorizer,report):
    save = input("是否保存训练的模型（y/n）：")
    if save == "y" or "Y":
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


# model_save(model, vectorizer, report)

```


## 9. 模型使用


```python
if __name__ == "__main__":
    print("-------垃圾邮件检测-------")
    while True:
        with open("model.pkl", 'rb') as f:
            model = pickle.load(f)
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        file_path = input("输入需要检测的邮件文件的路径:")
        with open(file_path, "r", encoding="gbk", errors="ignore") as f:
            email = f.read()
        email_list = [email]
        print(email)
        x = vectorizer.transform(email_list)
        y_predict = model.predict(x)
        print("检测结果为：", y_predict[0])

```


## 源代码&数据集

注释的代码用于生成模型。
如果已经生成了模型，main函数用于调用模型检测邮件。

```python
# 数据提取
import os
# 数据处理
from sklearn.utils import shuffle
import re
import jieba
# 提取特征
from sklearn.feature_extraction.text import TfidfVectorizer
# 划分训练集，测试集
from sklearn.model_selection import train_test_split
# 训练模型
from sklearn import svm
# 模型评估报告
from sklearn import metrics
# 模型保存
import pickle


# # 递归读取文件夹内所有文件
# def list_file(file_path):
#     file_list = []
#     files = os.listdir(file_path)
#     for file in files:
#         if os.path.isdir(file_path + '/' + file):
#             file_list = file_list + list_file(file_path + '/' + file)
#         else:
#             file_list.append(file_path + '/' + file)
#
#     return file_list


# # 读取邮件数据
# def read_email(file_list):
#     email = []
#     for file in file_list:
#         with open(file, "r", encoding='gbk', errors='ignore') as f:
#             email = email + f.readlines()
#
#     return email


# 读取邮件数据
def read_file(file_path):
    # print(file_path)
    email_list = []
    files = os.listdir(file_path)
    for file in files:
        if os.path.isdir(file_path + '/' + file):
            email_list = email_list + read_file(file_path + '/' + file)
        else:
            with open(file_path + '/' + file, 'r', encoding='gbk', errors='ignore') as f:
                email = f.read()

            # 替换连续的空格
            email = re.sub(r"[^\u4e00-\u9fff]", " ", email)
            # 替换非汉字字符
            email = re.sub(r"\s{2,}", " ", email)
            # 去除首尾的空格
            email = email.strip()
            # 结巴分词
            email = [word for word in jieba.lcut(email) if word.strip() != ' ']
            email = ' '.join(email)

            email_list.append(email)

    return email_list


# email = read_file("trec06c/data")


# 读取标签数据
def read_lable(file_path):
    lable = []
    with open(file_path, "r") as f:
        for l in f.readlines():
            if "s" in l:
                lable.append("spam")
            else:
                lable.append("ham")

    return lable


# lable = read_lable("trec06c/full/index")


# 数据处理
def data_process(email, lable):
    email, lable = shuffle(email, lable, random_state=42)

    return email, lable


# email, lable = data_process(email, lable)


# 特征提取
def data_vectorizer(email,lable):
    # 邮件样本已经分好了词，词之间用空格隔开，所以 tokenizer=tokenizer_space
    vectoring = TfidfVectorizer(input='content', analyzer='word')
    x = vectoring.fit_transform(email)
    y = lable

    return x, y, vectoring


# x, y, vectorizer = data_vectorizer(email, lable)


# 划分训练集和测试集
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)


def model_train(x_train, y_train):
    model = svm.LinearSVC()
    model.fit(x_train, y_train)

    return model


# model = model_train(x_train, y_train)


def model_test(x_test, y_test):
    y_pred = model.predict(x_test)
    print("模型评估报告：\n", metrics.classification_report(y_test, y_pred, digits=2))


# model_test(model)


def model_save(model, vectorizer):
    save = input("是否保存训练的模型（y/n）：")
    if save == "y" or "Y":
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
    print("-------垃圾邮件检测-------")
    while True:
        with open("model.pkl", 'rb') as f:
            model = pickle.load(f)
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        file_path = input("输入需要检测的邮件文件的路径:")
        with open(file_path, "r", encoding="gbk", errors="ignore") as f:
            email = f.read()
        email_list = [email]
        print(email)
        x = vectorizer.transform(email_list)
        y_predict = model.predict(x)
        print("检测结果为：", y_predict[0])

```
