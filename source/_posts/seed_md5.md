---
title: SEED：MD5 Collision Attack Lab
date: 2023-09-30
categories:
  - SEED
tags:
  - SEED
  - MD5 Collision Attack Lab
---


*你可以到SEED官网获取实验资料：MD5 Collision Attack Lab*

# MD5碰撞概述


### 哈希函数

[哈希究竟代表什么？哈希表和哈希函数的核心原理](https://www.bilibili.com/video/BV1SZ4y1z7wT/)
归纳起来，哈希函数应该有以下几个特点：
- 单向
- 压缩
- 弱抗碰撞性：给出一个输入，无法找到一个不同的输入使得它们输出相同。
- 强抗碰撞性：无法找到两个不同的输入有相同的输出。

### MD5碰撞

由于哈希函数压缩的特性，因此必然产生碰撞。但是一个好的哈希函数应该让寻找碰撞的计算代价尽可能的大，让它在计算上满足抗碰撞性。
然而，MD5不是这样一个合格的哈希函数。对于MD5哈希函数，使用特定程序能够轻易的找出两个不同输入。

### 哈希函数 && 安全

哈希函数广泛用于数据完整性校验。
在网络中，在一条消息后面附上其哈希输出，那么接收消息后检查消息的哈希输出是否一致就可以判断消息是否被更改。
在计算机系统中，可以为文件附上哈希，那么当这个文件被恶意篡改就能够及时发现。
另外，由于单向的特性，哈希函数也能用于信息保密。
在账号口令系统中，通常使用哈希加盐的方式存储口令，这样可以避免泄露用户的真实口令。

# 一、	作业题目

本次实验主要是加深大家对MD5碰撞及其原理的理解，使用SEED实验环境中的工具及编程语言，完成以下任务：
*1.	使用md5collgen生成两个MD5值相同的文件，并利用bless十六进制编辑器查看输出的两个文件，描述你观察到的情况；*
*2.	参考Lab3_task2.c的代码，生成两个MD5值相同但输出不同的两个可执行文件。*
*3.	参考Lab3_task3.c的代码，生成两个MD5值相同但代码行为不相同的可执行文件。*
*4.	回答问题：通过上面的实验，请解释为什么可以做到不同行为的两个可执行文件具有相同的MD5值？*

# 二、	实验步骤及结果


## 1.	md5collgen生成碰撞文件


### 新建前缀文件prefix.txt

 ![Alt text](/img/cipher_md5/image.png)###	用md5collgen生成碰撞文件out1.bin和out2.bin./md5collgen -p prefix.txt -o out1.bin out2.bin ![Alt text](/img/cipher_md5/image-1.png)###	使用bless比较两个文件内容两个文件小部分内容不同。 ![Alt text](/img/cipher_md5/image-2.png) ![Alt text](/img/cipher_md5/image-3.png)###	比价两个文件md5值md5sum xxx检查文件md5值，发现这两个不同内容的文件有相同的md5值。（md5算法将文件压缩到128位） ![Alt text](/img/cipher_md5/image-4.png)###	分析首先，out1.bin和out2.bin文件前面部分都是prefix.txt文件内容，但进行了补全，补全的部分是前64字节。
其次，out1,bin和out2.bin文件后半部分都是128字节，且这部分包含了这两个文件的差异，并且两个文件的差异比较小。

## 2.	Lab3_task2.c文件碰撞


### 新建文件task2.c

 ![Alt text](/img/cipher_md5/image-5.png) ![Alt text](/img/cipher_md5/image-6.png)###	编译文件gcc task.c -o task###	寻找替换程序字符串部分因为md5collgen的prefix部分需要是64字节的倍数，否则补全可能会造成task程序无法运行。因此在task程序找到字符串部分中64字节倍数作为前缀。 ![Alt text](/img/cipher_md5/image-7.png)（0x3040 => 12352；12352/64 = 193）###	剪切出前缀文件，并生成替换文件从12352字节开始剪切，注意的是生成文件会额外占据128字节，因此要将中间的128字节去掉。 ![Alt text](/img/cipher_md5/image-8.png)生成替换文件task_out1.bin和task_out2.bin文件 ![Alt text](/img/cipher_md5/image-9.png)###	拼接生成的文件和后缀，并执行这两个文件。可以发现这两个文件输出是不一样的，原因就是md5collgen生成的两个文件128字节不同导致输出字符发生改变。 ![Alt text](/img/cipher_md5/image-10.png)###	分析查看两个文件md5值，发现一样，但是输出不一样（也就是程序中的字符串不一样）。原理就是md5collgen生成的文件改变了字符串，但是没有让md5值发生改变。 ![Alt text](/img/cipher_md5/image-11.png)

## 3.	Lab3_task3.c文件碰撞


### 分析

题目分析：代码判断两个变量是否相等导致不同的输出路径；构造两个程序相同md5值有不同输出路径。
思路：源程序A构造两个相同变量x，y；程序B利用md5构造两个相同变量，输出路径为：==；程序C利用md5collgen构造两个不同变量保持和程序A相同的md5值，输出路径为：!=，###	编写程序task3_a.c上面未显示的部分定义了两个相同的字符串x和y，都是200个0x41（“A”）。 ![Alt text](/img/cipher_md5/image-12.png)###	这里task3_a程序与之前程序类似，我们定位到字符串内容依旧可以选取0x3040进行截取（对应下一个字符串0x3120）。截取的程序头部为task3_pre。 ![Alt text](/img/cipher_md5/image-13.png)
利用截取的头部tsak3_pre生成程序头task3_b，task3_c ![Alt text](/img/cipher_md5/image-14.png)###	拼接字符串x得到程序task3_b，task3_c ![Alt text](/img/cipher_md5/image-15.png)###	在bless调整字符串y得到task3_b，task3_cTask3_b的x，y字符串相同 ![Alt text](/img/cipher_md5/image-16.png) ![Alt text](/img/cipher_md5/image-17.png)task3_c的x，y字符串不同，y字符串来自task3_b ![Alt text](/img/cipher_md5/image-18.png)###	运行两个文件检查两个程序md5值 ![Alt text](/img/cipher_md5/image-19.png)
可以发现这两个程序走向了两个不同的方向。因为程序B字符串x，y都是md5collgen生成的同一个，然而程序C的x，y字符串则是md5collgen生成的两个不同的。但是它们的md5值相等。 ![Alt text](/img/cipher_md5/image-20.png)

## 4.	相同md5值，不同行为的程序？

从本质上来说，md5值是有限的（2的128次方个），然而程序是无穷的，因此两个不同行为程序完全可能有相同的md5值，碰撞不可避免。
就这道题分析：使用md5collgen可以生成两个相同md5值但是不同的文件。利用这个特性去替换程序中的字符串，使得一个程序是同一个md5collgen生成值替换，所以两个字符串一样，判断为same；另一个程序使用不同md5collgen生成值，两个字符串不一致，判断为diff，然而同为一个前缀生成，两个md5collgen生成值md5相等，两个程序的md5值也相等。