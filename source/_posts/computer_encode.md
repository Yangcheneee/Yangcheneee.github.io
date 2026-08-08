---
title: 计算机编码
date: 2024-06-26
categories:
  - 计算机基础
tags:
  - 计算机基础
  - 计算机
---



# 编码

现代计算机使用二进制编码的方式表示事物，在几千年前也有相似的东西：八卦。
《周易·系辞上》：“易有太极，是生两仪，两仪生四象，四象生八卦”，阴阳变换就像二进制的0、1变换，八卦和二进制有着相同的思想内核。计算机内使用二进制表示字符，八卦则用来表示不同的事物。
八卦：
![alt text](/img/computer_encode/image-1.png)
ASCLL码：
![alt text](/img/computer_encode/image-2.png)
这就是编码，就像一张对应关系的表，将二进制和字符或者其他东西对应起来。

### ASCLL

ASCII（American Standard Code for Information Interchange），即美国信息交换标准代码。
ASCLL使用7位二进制编码了26个拉丁字母、符号、数字、控制字符等128个字符。其中ASCLL码前32个字符是控制符，表示开始、换行、回车、结束等。但是ASCLL码在存储时使用8位二进制，最高位用于奇偶校验。
ASCLL扩展编码在兼容ASCLL码的基础上，使用8位二进制编码了256个字符。
![alt text](/img/computer_encode/image-5.png)

### GB2312

ASCLL码的局限性在于不是所有国家使用英文字符作为文字，并且无论是7位的ASCLL码还是8位的扩展ASCLL码能表达的字符十分有限。
因此各个国家都开创了适配自己的编码，GB2312就是其中一个例子。
GB2312使用两个大于127的字节表示汉字，这样ASCLL码依然占一个字节，汉字占据两个字节。GB2312在编码汉字的同时，既兼容了ASCLL码又在一定程度上节省了空间。
GB2312虽然包含了大部分中文字符，但是没有编码冷门生僻字和繁体字等等。于是在兼容GB2312的基础上扩展之后的编码方案被称为GBK标准。但是还有少数民族同胞的字符没有考虑在内，这样GBK扩展成为GB18030。这样，适配于中国的字符编码就完善了。

### Unicode&&USC

由于几乎每个不兼容ASCLL的国家都创建了一套适配自己的编码，这造成了混乱。计算机想要识别一串文字，必须首先知道它采用的编码，否则你就要尝试所有编码方式，直到得到正确结果。
ISO（国际标谁化组织）决定解决这个问题。他们采用的方法很简单：弃用所有的地区性编码方案，重新设计一个包括了地球上所有文化的字母和符号的编码：“Universal Multiple-Octet Coded Character Set”，简称 UCS。
统一码联盟，也开发了Unicode标准（The Unicode Standard），后面双方开始合并工作成果，并为创立一个单一编码表而协同工作。
![alt text](/img/computer_encode/image-4.png)

### UTF-8

Unicode的实现方式不同于编码方式。一个字符的Unicode编码是确定的。但是在实际传输和存储过程中，由于不同系统平台的设计不一定一致，以及出于节省空间的目的，对Unicode编码的实现方式有所不同。Unicode的实现方式称Unicod转换格式（Unicode Transformation Format，简称为UTF）。其中UTF-8使用最为广泛。
UTF-8（8-bit Unicode Transformation Format）是一种针对Unicode的可变长度符编码，也是一种前缀码。它可以用一至四个字节对Unicode字符集中的所有有效编码点进行编码。
![alt text](/img/computer_encode/image-3.png)
当文件受损，后续的字节都是以10开头，这样即使从某个中间字节开始读，计算机也能跳过。