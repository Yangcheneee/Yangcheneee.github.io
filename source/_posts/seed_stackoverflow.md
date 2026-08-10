---
title: SEED：Buffer Overflow Attack Lab (Server Version)
date: 2023-10-14
cover: /img/5.jpg
categories:
  - SEED
tags:
  - SEED
  - Buffer Overflow Attack Lab (Server Version)
---


*你可以到SEED官网获取实验资料：Buffer-Overflow Attack Lab (Server Version)*
*网络攻防技术——缓冲区溢出攻击（基于服务器）*

# 一 缓存区溢出攻击概述


## C语言和堆栈


### 局部变量

函数中定义的变量

### 堆

内存大，链表，碎片化

### 栈（堆栈）

内存小，编译器决定1-8MB，后进先出LIFO，快

### 局部变量和堆栈

[c语言进阶：堆栈原理揭秘](https://zhuanlan.zhihu.com/p/142964520)
C语言有很多不同类别的数据，他们有不同的生命周期，这不是C语言本身决定的，而是操作系统存放这些数据的位置决定了他们的生命周期。
运行一个程序，操作系统会将数据其映射到内存中，不同的数据将会映射到不同的内存中栈/堆/代码区等。

### 函数调用和堆栈


### 缓冲区溢出原理

[一文理解缓冲区溢出](https://zhuanlan.zhihu.com/p/186812518)
缓冲区溢出被定义为程序试图将数据写入缓冲区边界之外的情况。恶意用户可以利用此漏洞更改程序的流控制，从而导致恶意代码的执行。

### 栈溢出详解

缓冲区溢出在栈溢出上应用很多，因为当程序调用函数时，会将返回地址ret暂时存在栈区上。如果构造一次恶意溢出使用恶意抵制覆盖返回地址ret的值，那么将可以控制程序流甚至执行以进程权限执行任意程序。如果这个进程是根权限，那么shellcode也将获取到根权限。

### shellcode和栈溢出

可以这样理解，攻击方式就像武器库，而攻击载荷就像弹药库。
栈溢出就像攻击者的导弹，瞄准程序的弱点，但是实际造成攻击还需要弹药，也就是shellcode，shellcode决定对目标主机造成什么攻击。

# 二 实验环境

在这个实验中，有四个不同的服务器，不同服务器上以根权限运行着不同难度的缓冲区溢出漏洞的程序，对应关系如下：
- level-1：10.9.0.5:9090运行32位缓冲区溢出漏洞程序
- level-2：10.9.0.6:9090运行32位缓冲区溢出漏洞程序
- level-3：10.9.0.7:9090运行64位缓冲区溢出漏洞程序
- level-4：10.9.0.8:9090运行64位缓冲区溢出漏洞程序
- level-5：10.9.0.9:9090运行32位缓冲区溢出漏洞程序
任务是开发一种利用该漏洞的方案，并最终获得这些服务器上的根权限。除了攻击之外，还将尝试几种对抗缓冲区溢出攻击的对策。

### 关闭地址随机化

在开始这个实验之前，需要确保地址随机化对策被关闭;否则，进攻会很困难。可以使用以下命令：`sudo /sbin/sysctl -w kernel.randomize_va_space=0`

### 漏洞程序：stack.c


```c
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
/* Changing this size will change the layout of the stack.
* Instructors can change this value each year, so students
* won’t be able to use the solutions from the past.
#ifndef BUF_SIZE
#define BUF_SIZE 100
#endif
int bof(char *str)
{
char buffer[BUF_SIZE];
/* The following statement has a buffer overflow problem */
strcpy(buffer, str); ✰
return 1;
}
int main(int argc, char **argv)
{
char str[517];
int length = fread(str, sizeof(char), 517, stdin);
bof(str);
fprintf(stdout, "==== Returned Properly ====\n");
return 1;
}

```

上述程序有缓冲区溢出漏洞。它从标准输入中读取数据，然后将数据传递给函数bof()中的另一个缓冲区。原始输入的最大长度为517字节，但bof()中的缓冲区只有BUF SIZE字节长，小于517字节。因为strcpy()不检查边界，所以会发生缓冲区溢出。

### 服务器程序：server.c

在server-code文件夹中，可以找到一个名为server.c的程序。这是服务器的主要入口点。它监听端口9090。当它接收到TCP连接时，它调用堆栈程序，并将TCP连接设置为堆栈程序的标准输入。这样，当stack从stdin读取数据时，它实际上是从TCP连接中读取的，也就是说，这些数据是由TCP客户端用户提供的。由于程序stack.c将在具有root权限的服务器上运行，如果用户可以利用这个缓冲区溢出漏洞，他们就可以在服务器上获得根shell。学生不需要阅读server.c的源代码。

### 容器启动

了解完实验的整个流程和配置信息，通过下面命令操作容器，开始实验。
进入Labsetup目录，使用命令`dcbuild` `dcup` `dcdown`。 

### 熟悉Shellcode

缓冲区溢出攻击的最终目的是将恶意代码注入到目标程序中，这样代码就可以使用目标程序的特权来执行。Shellcode被广泛用于大多数代码注入攻击。让我们在这个任务中熟悉它。
Shellcode通常用于代码注入攻击。它基本上是一段启动shell的代码，通常用汇编语言编写。在这个实验中，我们只提供一个通用shellcode的二进制版本，而不解释它是如何工作的，因为它很重要。如果您对shellcode的工作原理感兴趣，并且想从头开始编写一个shellcode，您可以从一个名为shellcode lab的独立SEED实验室中学习。我们的通用shellcode如下所示(我们只列出32位版本):

```python
shellcode = (
"\xeb\x29\x5b\x31\xc0\x88\x43\x09\x88\x43\x0c\x88\x43\x47\x89\x5b"
"\x48\x8d\x4b\x0a\x89\x4b\x4c\x8d\x4b\x0d\x89\x4b\x50\x89\x43\x54"
"\x8d\x4b\x48\x31\xd2\x31\xc0\xb0\x0b\xcd\x80\xe8\xd2\xff\xff\xff"
"/bin/bash*"                                                 
"-c*"                                                        
"/bin/ls -l; echo Hello; /bin/tail -n 2 /etc/passwd        *"
# The * in this line serves as the position marker         *
"AAAA" # Placeholder for argv[0] --> "/bin/bash"
"BBBB" # Placeholder for argv[1] --> "-c"
"CCCC" # Placeholder for argv[2] --> the command string
"DDDD" # Placeholder for argv[3] --> NULL
).encode(’latin-1’)

```

您可以在shellcode文件夹中找到通用的shellcode。在里面，您将看到两个Python程序，shellcode 32.py和shellcode 64.py。它们分别适用于32位和64位的shellcode。这两个Python程序将分别将二进制shellcode写入codefile 32和codefile 64。然后可以使用call shellcode来执行其中的shellcode。

```shell
// Generate the shellcode binary
$ ./shellcode_32.py ¨ generate codefile_32
$ ./shellcode_64.py ¨ generate codefile_64
// Compile call_shellcode.c
$ make
¨ generate a32.out and a64.out
// Test the shellcode
$ a32.out
¨ execute the shellcode in codefile_32
$ a64.out
¨ execute the shellcode in codefile_64

```


#### 任务：修改shellcode_32.py文件，使其能够删除文件。

 ![Alt text](/img/os_stackoverflow/image.png)

#### 测试

在该目录下创建文件task1，通过ls命令发现task1文件创建成功。 ![Alt text](/img/os_stackoverflow/image-1.png)可以看到执行a32.out文件后，通过ls命令发现task1文件被删除。 ![Alt text](/img/os_stackoverflow/image-2.png)

### 注意

实验开发者在程序中添加了一点随机性，让不同学生可能看到不同的缓冲区地址和帧地址，为了让不同学生作业有些区别。但是这些值在容器启动后保持不变，因此只要不关闭容器每次实验结果仍然是相同的。

# 三 实验任务


## Task 1: Level-1 Attack

运行level-1漏洞程序的容器是10.9.0.5，端口是9090，漏洞程序是32位。

### 获取server的堆栈信息

先向服务器发送一条正常消息获取堆栈信息。
![Alt text](/img/os_stackoverflow/image-3.png)
Buf基地址为：0xffffd598
Ebp地址为：0xffffd608

### 编写exploit.py文件

在32位环境下，ret地址为ebp地址+4（单位为字节），已知buf基地址，则偏移量为ebp地址+4-buf基地址。
ret的值存储指令地址，要执行shellcode，因此要将ret指向shellcode地址。而shellcode使用了Nop填充，所以ret指向ret+4即可空转跳转到shellcode。![Alt text](/img/os_stackoverflow/image-4.png)

### 生成badfile，获取服务器权限

 ![Alt text](/img/os_stackoverflow/image-5.png)

## Task 3: Level-2 Attack


### attack-code传入hello，获取server堆栈信息。

 ![Alt text](/img/os_stackoverflow/image-6.png)Buf基地址：0xffffd548Ebp地址：由于buf大小在100-300字节，因此ebp地址在buf基地址+100到buf基地址+300之间。

### 编写exploit.py文件。

Ret地址等于ebp地址+4，因此ret地址可能在buf基地址+104到buf基地址+304之间，所以offset的值可能在104到304之间。将这段content都填入ret指向地址即可。Ret的值需要指向shellcode，而buf大小不确定，因此ret指向地址必须大于buf最大值+8，以执行ret上方的shellcode，避免从下面空转到ret陷入循环。 ![Alt text](/img/os_stackoverflow/image-7.png)

### 生成badfile，获取服务器权限。


## 4. Task4 Level-3 Attack


### attack-code传入hello获取server堆栈信息。

 ![Alt text](/img/os_stackoverflow/image-8.png)Rbp指针：0x00007fffffffe540Buf基地址：0x00007fffffffe470

### 编写exploit.py文件。

首先插入64位的shellcode，并把执行命令改为反弹shell。start的值设置为0，此时shellcode在content头部，位置为content[0,len(shellcode)]。Ret地址为rbp地址+8（64位环境），offset的值为ret地址-buf基地址。ret的值指向shellcode地址，此时shellcode代码在content头部，即buf基地址0x470。 ![Alt text](/img/os_stackoverflow/image-9.png)

### 生成badfile，获取服务器权限

 ![Alt text](/img/os_stackoverflow/image-10.png)

## 5. Task5 Level-4 Attack


### attack-code传入hello，获取server堆栈信息。

 ![Alt text](/img/os_stackoverflow/image-11.png)Rbp指针：0x00007fffffffe540Buf基地址：0x00007fffffffe470

### 编写exploit.py文件

相比于上一个task，这个task实行shellcode依靠于Return-to-libc，因此需要改变ret指向地址。        经过尝试以后，ret为rbp+1400的时候能够实现反弹shell。![Alt text](/img/os_stackoverflow/image-12.png) 

### 生成badfile，获取服务器权限。

 ![Alt text](/img/os_stackoverflow/image-13.png)

## 6. Task6 Level-5 Attack


### 打开地址随机化。

 ![Alt text](/img/os_stackoverflow/image-14.png)

### attack-code传入hello，获取server堆栈信息。

可以发现随着地址随机化的打开，server堆栈地址发生改变。 ![Alt text](/img/os_stackoverflow/image-15.png) ![Alt text](/img/os_stackoverflow/image-16.png)

### 编写exploit.py文件。

 ![Alt text](/img/os_stackoverflow/image-17.png)

### 生成badfile，运行脚本brute-force.sh不断向server传入badfile。

当server程序满足badfile的堆栈条件时，脚本停止，成功获取服务器权限。 ![Alt text](/img/os_stackoverflow/image-18.png) ![Alt text](/img/os_stackoverflow/image-19.png) ![Alt text](/img/os_stackoverflow/image-20.png)

## 7.	Task7 Level-6 Attack


### 在server-code目录下：

去除-fon-stack-protector选项（即打开栈保护机制）编译stack.c，将badfile输入。Server成功检测到stack smashing（堆栈溢出漏洞） ![Alt text](/img/os_stackoverflow/image-21.png)

### 在shellcode目录下：

去除-z execstack（这个选项会认为栈空间的指令可以被执行，因此我们才能之前的实验运行栈溢出的shellcode和空转指令）编译call_shellcode.c编译并运行。![Alt text](/img/os_stackoverflow/image-22.png)