---
title: CPP
date: 2024-01-26 00:00:00
categories:
  - cpp
tags:
  - cpp
---

2024-1-26开始学习cpp…

<!--more-->

# 1-26

*参考视频：[最好的C++教程](https://www.bilibili.com/video/BV1VJ411M7WR)*

# P1: Welcome to CPP

CPP

- 编译型语言
- 更高的效率
- 对硬件的直接控制
- 跨平台

# P2: How to Setup CPP on Windows

### IDE: Visual Studio

集成开发环境IDE

### Hello cpp

```cpp
# include <iostream>

int main()
{
    std::cout << "hello cpp" << std::endl;
    std::cin.get();
}
```

# P3: How CPP Works

### #include

任何以"#"开头的都是预处理指令。

include指的是包含一个文件

另外std表示标准

std::cout << << std::endl输出到控制台，endl表示换行

<<就像printf一样，std::cout.print().print(std::endl)

std::cin.get()等待输入回车。

int main：函数输入输出，输入值和返回值，如果没有指定返回值那么将返回0.

### 预处理

include 相当于把文件复制粘贴到代码中。

### 可执行程序

### 编译

### 链接

# P8: Variables in CPP

程序：数据操作

数据类型的差距只是大小，另外就是格式化输出的时候会有差距。

# P16: Pointers

指针只是一个地址，一个整数

### 0 NULL nullptr

### * &

### new

```cpp
int main()
{
    char* buffer = new char[8];
    memset(buffer, 0, 8);
    delete[] buffer;
    std::cin.get();
}
```

# P18: Classes in CPP

### OOP

C++

c

java

c#

面向对象

面向过程

### Classes

类是一种将数据和函数组织在一起的方式,本质上是一种自制类型。

```cpp
class Player
{
public:
    int x, y;
    int speed;

    void Move(int xa, int ya)
    {
        x += xa * speed;
        y += yx * speed;
    }   
};

int main()
{
    Player player;
    player.x = 5;
}
```

# P25: Constructors in CPP

构造函数是一种特殊的方法，它会在类每次实例化的时候运行

```cpp
#include <iostream>

class Entity
{
public:
    float x, y;

    Entity()
    {
        x = 0.0f;
        y = 0.0f;
    }

    void Print()
    {
    std::cout << x << ", " << y << std::endl;
    }
};

int main()
{
    Entity e;
    std::cout << e.x << std::endl;
    e.Print();

    std::cin.get();
}
```

# P27: 继承

继承允许创建相关联的类的层次结构。

```cpp
#include <iostream>

class Entity
{
public:
    float X, Y;

    void Move(float xa, float ya)
    {
        X += xa;
        Y += ya;
    }
};

class Player : public Entity
{
public:
    const char* Name;

    void PrintName()
    {
        std::cout << Name << std::endl;
    }
};

int main()
{
    std::cout << sizeof(Entity) << std::endl;
    std::cout << sizeof(Player) << std::endl;

    std::cin.get();
}
```
