---
title: 机器学习
date: 2023-10-09
cover: /img/cover/18.png
categories:
  - ML
tags:
  - ML
  - 机器学习
  - Python
  - sklearn
---



# 机器学习

在很多场景，

## 分类&回归

简单来说，分类解决离散问题；回归解决连续问题。
分类（Binary Classification）：一个例子，对于给定的一个字符串，检测是否为恶意的，那么这种就是分类问题，一般来说二分类问题比较常见。
回归（Regression）：给定一个人的各方面信息，评估他的个人收入，他的收入显然是有大量可能的，因此这是回归问题。

## 分类模型


### 线性回归


## 回归模型


### Logist回归


### 朴素贝叶斯

[了解更多](https://zhuanlan.zhihu.com/p/26262151)

### 决策树


## 机器学习一般步骤：

- 文件读取
- 数据处理
- 特征提取&向量化
- 训练集&测试集划分
- 模型训练
- 模型测试
- 模型保存
- 模型使用

### 1. 文件读取

一般来说，数据集存储在txt或者csv文件中，它包括数据和标签两个部分。
需要注意的是数据集的并没有统一格式，需要根据具体情况便携代码。
首先将其读入程序，以便我们能够处理，可以将其读入列表，字典或者pd对象当中。
下面提供pandas读取csv文件的代码，并将数据集存储到pd对象中：

```python
def read_file(file_path):
    file_pd = pd.read_csv(file_path, usecols=["data","lable"])

    return file_pd

```

- 程序数据处理

```Python
def data_process(normal, malicious):
    all = pd.concat([normal, malicious])
    data = all["data"]
    lable = all["lable"]
    data, lable = shuffle(data, lable, random_state=42)

    return data, lable

data, lable = data_process(normal, malicious)

```

- 特征向量

```Python
def data_tokenizer(data):
    return re.findall(r'\w+', data)


def data_vectorizer(data, lable):
    vectorizer = TfidfVectorizer(stop_words=None, tokenizer=data_tokenizer)
    x = vectorizer.fit_transform(data)
    y = lable

    return x, y, vectorizer

```

- 训练集&测试集

```Python
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

```

- 模型训练

```Python
def model_train(x_train, y_train):
    # 在这里选择适合适的模型
    model = modelname()
    model.fit(x_train, y_train)

    return model

```

- 模型测试

```Python
def model_test(model, x_test, y_test):
    y_predict = model.predict(x_test)
    report = classification_report(y_test, y_predict, labels=["malicious", "normal"], target_names=["恶意URL", "正常URL"],digits=2)

    return report

```

- 优化