---
title: SEED：Shellcode Development Lab
date: 2023-10-21
categories:
  - SEED
tags:
  - SEED
  - Shellcode Development Lab
---



# 一. Shellcode概述

shellcode广泛用于许多涉及代码注入的攻击中。编写shellcode是相当有挑战性的。虽然我们可以很容易地从互联网上找到现有的shellcode，但是能够从头开始编写我们自己的shellcode总是令人兴奋的。shellcode中涉及到几种有趣的技术。本实验室的目的是帮助学生理解这些技术，以便他们能够编写自己的shellcode。
编写shellcode有几个挑战，一个是确保二进制文件中没有0x00，另一个是找出命令中使用的数据的地址。第一个挑战不是很难解决，有几种方法可以解决它。第二个挑战的解决方案导致了编写外壳代码的两种典型方法。在一种方法中，数据在执行期间被推入堆栈，因此可以从堆栈指针获得它们的地址。在第二种方法中，数据存储在代码区域中，就在调用指令之后，因此在调用调用函数时，其地址被推入堆栈（作为返回地址）。两种解决方案都非常优雅，我们希望学生能够学习这两种技术。 

# 二. 实验


## 1. Task1 Writing Shellcode


### 1.1. Task1.a The Entire Process


### Compiling to object code

使用汇编软件nasm将mysh.s（汇编程序）汇编为mysh.o（目标文件）： ![Alt text](/img/os_shellcode/image-1.png)

### Linking to generate final binary

使用链接程序ld链接mysh.o（目标文件）为mysh（ELF可执行文件）： ![Alt text](/img/os_shellcode/image-2.png)使用命令”echo $$”获取shellcode进程PID： ![Alt text](/img/os_shellcode/image-3.png)

### Getting the machine code

使用objdump命令反汇编mysh.o文件，并使用intel格式显示汇编代码，左边一列为机器码，右边一列为汇编代码：![Alt text](/img/os_shellcode/image-4.png)
使用xxd命令获取目标文件数据内容。这里-p代表16进制显示，-c 20代表一行显示20字节数据（这里截取了前三行内容）： ![Alt text](/img/os_shellcode/image-5.png)可以发现的是xxd命令显示了目标文件全部的16进制数据，然而objdump命令反汇编内容只是目标文件的机器代码部分，这是因为目标文件协议包括其他字段内容： ![Alt text](/img/os_shellcode/image-6.png)

### Using the shellcode in attacking code

打开文件convert.py，将上面16进制数据中的机器码部分复制到代码中的ori_sh变量中（这个程序将这个字符串转化为shellcode）： ![Alt text](/img/os_shellcode/image-7.png)运行convert.py将字符串转化为shellcode： ![Alt text](/img/os_shellcode/image-8.png)

### 1.2. Task1.b Eliminating Zero from the Code

字符串复制是注入恶意代码的一个常用手段，然而字符串复制例如函数strcpy通常会从零截断。因此，为了保证shellcode不被截断，更加范用，要对一般的shellcode做去零的处理。去零方式：自异或；使用短位寄存器；移位

### 找出mysh.s中的去零操作

汇编指令xor eax eax将eax置零，之后push eax相当于push 0，但是不会像push 0一样将shellcode引入0。 ![Alt text](/img/os_shellcode/image-9.png)同理，在下面eax的值没有发生改变，push eax相当于push 0： ![Alt text](/img/os_shellcode/image-10.png)指令xor edx,edx将edx置零： ![Alt text](/img/os_shellcode/image-11.png)由于al寄存器占eax寄存器的低8位，因此将0xb存入寄存器al，相当于将0x000b存入寄存器eax，push eax则避免了eax高位为零的情况： ![Alt text](/img/os_shellcode/image-12.png)

### Task：编写shellcode执行程序/bin/bash，不能有多余的“/”

这里使用al寄存器存储“h”，push eax相当于push 0x000h。 ![Alt text](/img/os_shellcode/image-13.png)对编译后的shellcode进行查看，没有字节为0，即没有出现0x00： ![Alt text](/img/os_shellcode/image-14.png)

### 1.3. Task1.c Providing Arguments for System Calls

对于执行程序/bin/sh的shellcode，这里给出了参数argv数组需要填写的值：/bin/sh；-c；ls -la；0。也就是说我们需要将这些参数构造在堆栈上，然后执行系统调用即可。首先使用eax寄存器将字符串压入栈中，中间使用0分隔；然后使用寄存器寄存器将argv数组的值压入栈中；最后将ecx指向argv即可。 ![Alt text](/img/os_shellcode/image-15.png) ![Alt text](/img/os_shellcode/image-16.png)编译链接以后成功执行/bin/sh -c ls -la： ![Alt text](/img/os_shellcode/image-17.png)

### 1.4 Task1.d Providing Environment Variables for execve()

对比上一个任务，这个任务压入四个环境变量aaa,bbb,cccc,0并将edx指向env数组即可。然后argv的参数少了几个。
 ![Alt text](/img/os_shellcode/image-18.png) ![Alt text](/img/os_shellcode/image-19.png) ![Alt text](/img/os_shellcode/image-20.png)![Alt text](/img/os_shellcode/image-21.png)

## 2. Task2 Using Code Segment


### 解释mysh2.s为什么能够成功执行程序/bin/sh：

 ![Alt text](/img/os_shellcode/image-22.png)程序mysh2.s通过构造db字符串实现shellcode注入。首先构造db字符串占位；其次替换掉字符串中的零，写入参数地址；最后将ecx指向参数地址，执行系统调用。

### 使用mysh2.s中的方法执行程序/usr/bin/env

重新编写mysh2.s： ![Alt text](/img/os_shellcode/image-23.png) ![Alt text](/img/os_shellcode/image-24.png)编译并链接汇编程序mysh2.s，需要注意的是这里链接时需要加入“–omagic”指示代码区可修改，否则会出现segment fault ![Alt text](/img/os_shellcode/image-25.png)

## 3. Task3 Writing 64-bit Shellcode

对于64位系统架构：寄存器存储8字节数据；系统调用的参数使用寄存器rdx，rsi，rdi。

### 编写程序mysh_64.s，执行程序/bin/bash（即在64位环境下完成Task1.b中的Task）

思路和mysh.s的编写一致，只有寄存器使用变化。使用rax寄存器将“/bin/bash”入栈，使用寄存器rdi作为argv直指向字符串，rsi寄存器指向argv即可。 ![Alt text](/img/os_shellcode/image-26.png)