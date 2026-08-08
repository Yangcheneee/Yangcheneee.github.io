---
title: 论文：Techniques for data hiding
date: 2024-01-10
categories:
  - 信息隐藏
tags:
  - 信息隐藏
---



# 论文概述

Techniques for data hiding

## Patchwork算法


## 理论基础

在图像中随机选取A和B两个点，假设a为A点的亮度，b为B点的亮度，那么：![alt text](/image.png)经过多次重复这个操作，S的期望值应该为0。
具体计算：略。。

## 算法实现

1. 使用伪随机生成器生成秘钥（ai，bi）。
2. 将a的亮度提高，b的亮度降低（1/256-5/256d）。
3. 重复上面步骤n次。（通常来说是10000次）。