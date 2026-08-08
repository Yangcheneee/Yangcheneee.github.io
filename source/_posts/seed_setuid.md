---
title: SEED：Environment Variable and Set-UID Program Lab
date: 2023-10-28
categories:
  - SEED
tags:
  - SEED
  - Environment Variable and Set-UID Program Lab
---



# Environment Variable and Set-UID Program Lab


## 1. Task1 Get Familiar with the Shellcode


### 修改shellcode_32.py文件，使其能够删除文件。

 ![Alt text](/img/os_stackoverflow/image.png)

### 测试

在该目录下创建文件task1，通过ls命令发现task1文件创建成功。 ![Alt text](/img/os_stackoverflow/image-1.png)可以看到执行a32.out文件后，通过ls命令发现task1文件被删除。 ![Alt text](/img/os_stackoverflow/image-2.png)

## 2. Task2 Level-1 Attack


### attack-code传入hello，获取server的堆栈信息。

 ![Alt text](/img/os_stackoverflow/image-3.png)Buf基地址为：0xffffd598Ebp地址为：0xffffd608

### 编写exploit.py文件。

在32位环境下，ret地址为ebp地址+4（单位为字节），已知buf基地址，则偏移量为ebp地址+4-buf基地址。ret的值存储指令地址，要执行shellcode，因此要将ret指向shellcode地址。而shellcode使用了Nop填充，所以ret指向ret+4即可空转跳转到shellcode。![Alt text](/img/os_stackoverflow/image-4.png)

### 生成badfile，获取服务器权限

 ![Alt text](/img/os_stackoverflow/image-5.png)3. Task3 Level-2 Attack

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