---
title: dga域名检测
date: 2023-10-25
cover: /img/4.jpg
categories:
  - ML
tags:
  - ML
  - 深度学习
  - LSTM
  - Keras
---



## DGA域名

通过dga算法生成的域名，需要知道的是dga算法有很多分支。
在字符特征上与普通域名有一些差别，dga域名通常是一些无意义的数字和字母，而正常域名通常带有一些意义比如baidu.com（百度），另外正常域名通常有更多的元音字母，因为这让人更加容易记住和读。
不过，随着dga域名的改进（通过正常域名修改两个字母等），这些差距都可以被缩小，dga域名将会变得越来越像正常域名，这时候依靠于字符特征是难以起效了。
因此，找出dga域名更加深层的特征是必要的，dga域名通常用于黑客和僵尸网络通信，因此这将是未来一个有意义的方向。
下面，我们使用lstm检测dga域名，因为lstm相比于tf-idf和词袋模型更好的捕捉词语间的语序信息。
需要注意的是，我们训练的模型依然依靠的是dga域名的字符信息，因此这个模型具有局限性。

## 源代码


```python
# 数据读取
import pandas as pd
# 数据处理
from sklearn.utils import shuffle
from tensorflow.keras.preprocessing import sequence
import numpy as np
# 划分数据集
from sklearn.model_selection import train_test_split
# 模型构建
from keras.models import Sequential
from keras.layers import Dense, LSTM
# 加载模型
from keras.models import load_model


def read_dga(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()[18:1324316]
    dga_list = [line.split('\t')[1].split('\s')[0] for line in lines]

    return dga_list


# dga_list = read_dga("dga-domain.txt")


def read_umbrella(file_path):
    umbrella_pd = pd.read_csv(file_path, usecols=[1], nrows=1000000, header=None, names=["data"])
    umbrella_list = umbrella_pd["data"].tolist()

    return umbrella_list


# umbrella_list = read_umbrella("umbrella-top-1m.csv")


def data_process(data_list):
    # 将字母转化为Ascall码，并做归一化处理
    X = [[ord(char) - 96 for char in domain] for domain in data_list]
    # 填充数据，使得每个序列长度一致
    X = sequence.pad_sequences(X, maxlen=253)
    return X


# X = data_process(dga_list + umbrella_list)
# y = np.array([1] * len(dga_list) + [0] * len(umbrella_list))
#
# X, y = shuffle(X, y, random_state=42)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


def train_model(X_train, y_train):
    # 模型构建
    model = Sequential()
    # LSTM层，32个神经单元。输入形状：时间步长（特征维度），步长（每次训练使用特征数）
    # X_train.shape输出训练集的样本数和特征维度的列表,input_shape：时间步长，步长
    model.add(LSTM(32, input_shape=(X_train.shape[1], 1)))
    # 输出层
    # sigmod函数解决二分类问题
    model.add(Dense(1, activation='sigmoid'))

    # 编译模型
    # 二分类问题编译，优化
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # 训练模型
    # 模型输入为三维：样本数，时间步长，步长
    model.fit(X_train.reshape(X_train.shape[0], X_train.shape[1], 1), y_train, epochs=10, batch_size=32)

    return model


# model = train_model(X_train[0:8000], y_train[0:8000])


def test_model(model, X_test, y_test):
    # model.summary()
    evaluation = model.evaluate(X_test, y_test, return_dict=True)
    loss = evaluation["loss"]
    accuracy = evaluation["accuracy"]
    print('Test Loss:', loss)
    print('Test Accuracy:', accuracy)
    return evaluation


# evaluation = test_model(model, X_test[0:2000], y_test[0:2000])


def model_save(model):
    save = input("是否保存模型到model.h5（y/n）：")
    if save == "Y" or save == "y":
        model.save("model.h5")
        return True
    else:
        return False


# model_save(model)


model = load_model('model.h5')
while True:
    domain_list = input("输入需要检测的域名：").split('\n')
    X = [[ord(char) - 96 for char in domain] for domain in domain_list]
    X = sequence.pad_sequences(X, maxlen=253)
    # print(X.shape)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    # print(X.shape)
    y = model.predict(X)
    if y > 0.5:
        print(y, "：预测结果为dga域名")
    else:
        print(1-y, "：预测结果为正常的域名")

```
