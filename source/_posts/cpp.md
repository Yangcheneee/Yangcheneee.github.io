---
title: CPP
date: 2024-01-25
categories:
  - cpp
tags:
  - cpp
---


*2024-1-26开始学习cpp…*

# 1-26

*参考视频：最好的C++教程*

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

任何以“#”开头的都是预处理指令。
include指的是包含一个文件另外std表示标准
std::cout << << std::endl输出到控制台，endl表示换行
<<就像printf一样，std::cout.print().print(std::endl)
std::cin.get()等待输入回车。
int main：函数输入输出，输入值和返回值，如果没有指定返回值那么将返回0.

### 预处理

include 相当于把文件复制粘贴到代码中。

### 可执行程序


### 编译


### 链接


# P4


# P5


# P8: Variables in CPP

程序：数据操作
数据类型的差距只是大小，另外就是格式化输出的时候会有差距。  

# P9: Functions in CPP


# P10: CPP Header Files


# P11: How to DEBUG CPP in Visual Studio


# P12: CONDITIONS and BRANCHES in CPP


# P13: BEST Visual Studio Setup for CPP Projects


### filters

VS的虚拟文件目录

### show all files

项目实际文件目录

### setup projects structures

![Alt text](/image.png)

# P14: Loops in CPP


### for

一般使用i表示迭代，i也许代表迭代器iterator

```CPP
for (int i = 0; i < 5; i++)
{
    Log("Hello World!");
}   

```

数组遍历

### while

游戏循环

### do while


# P15: Control Flow in CPP


### continue

直接进入下一次循环

### break

结束循环

### return

结束函数

# P16: Pointers

指针只是一个地址，一个整数

### 0 NULL nullptr


### * &


### new


```CPP
int main()
{
    char* buffer = new char[8];
    memset(buffer, 0, 8);
    delete[] buffer;
    std::cin.get();

}

```


### pointers to pointers

指针也是一个变量，它也有内存地址
指向指针的指针

```cpp
char** buffer = &buffer;

```


# P17 References in CPP

reference只是指针的扩展，一种语法糖

### 传值


### 传址


### 

引用必须初始化，并且没办法更改引用对象
但是可以用指针实现。。。

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
想象游戏中的一个玩家角色，需要X和Y的坐标表示位置，可能还需要其他属性比如移动速度，以及可能需要3D模型在屏幕上显示玩家，所有的数据都需要存储到某些地方。

```cpp
int main()
{
    int PlayerX, PlayerY;
    int PlayerSpeed = 2;

    std::cin.get();

    return 0;
}

```

但是需要创建第二个玩家，第三个玩家的时候需要不断地重复这段代码，这样的源代码是难以维护的，因此考虑使用类进行简化。
就像函数一样，为了简化代码。

### 实例化和对象


```cpp
class Player
{
    int x, y;
    int speed;
};

int main()
{
    Player player;
    player.x = 5;

}

```

编译错误：player中的对象无法访问类中的私有成员。

### 访问控制

当创建一个类是，你可以指定类中属性的可见性，默认情况下，类中的所有成员都是私有的。这意味着，类内部的函数才能访问这些变量。
如果我们需要在main函数中访问类中的变量，需要指定这些变量为公共的public，公有的代表我们可以被允许在类外访问这些变量。

```cpp
class Player
{
public:
    int x, y;
    int speed;
};

int main()
{
    Player player;
    player.x = 5;
}

```

现在可以在外部访问类中的变量了，main函数的变量访问也将成功。

### 方法：Method：类的函数


```cpp
class Player
{
public:
    int x, y;
    int speed;  
};

    void Move(Player& player, int xa, int ya)
    {
        player.x += xa * player.speed;
        player.y += yx * player.speed;
    } 

int main()
{

    
    Player player;
    player.x = 5;
}

```

将上面的函数移动到类中就变成了方法，需要注意的是：当在类中是不再需要传递类中变量的参数而是直接使用。 

```cpp
class Player
{
public:
    int x, y;
    int speed;

    void Move(int xa, int ya)
    {
        x += xa * speed;
        y += yx * .speed;
    }   
};

int main()
{

    
    Player player;
    player.x = 5;
}

```

类可以让代码变得更加简洁，当处理大量代码，这将会是一个巨大的优势。
也许你可以将变量再次改为私有，通过在外部调用函数函数能够访问私有变量吗？

# P19: Classes vs Structs in CPP

类和结构体的区别：非常小的区别，类的变量默认是私有的，结构体则是公有的。
在CPP中结构体存在的唯一原因是cpp需要维持它和c之间的兼容性，因为C中没有类。
那C中的结构体和CPP中的结构体的区别？
C中的结构体可以定义函数吗？可以规定变量的私有或者公有的属性吗？
如果你需要进行兼容。只需要这样既可以

```cpp
#define struct class

```

什么时候使用类，什么时候使用结构体？
我想这个问题没有一个确切的答案，因为每个人对于类和结构的定义不同，类是什么，结构体是什么，这是个人的编程风格。
如果讨论一些plain old data pod的时候，使用struct也许比较好.
一个很好的例子是数学中的向量类：

```cpp
struct Vec2
{
    float x, y;

};

```

这并不是说不在结构体中使用方法，它不想player类一样复杂，需要很多操作。Vec只需要简单的对两个数进行操作，没有啥变化。
继承：继承增加了另外一层复杂性，结构体应该尽量简单。
另外如果结构体B继承了类A，编译器会发出警告，但是不影响运行。
也许你可以在变量是公有的时候使用结构，因为这样可以帮助你省略public？
如果只是代替一个结构中的数据，使用结构体；如果实现有很多功能的类，像游戏世界的玩家，或者其他可以继承的东西，使用类。
额，很多行内的人这样区分；但是技术上这两者处理可见性以外没有什么区别。

### C中的结构体

在结构体中使用指向函数的指针，从而实现类似于面向对象编程中的成员函数的功能。这种技术通常被称为函数指针，通过这种方式，你可以将函数与结构体关联起来，实现一些面向对象编程的特性。这在C语言中常用于实现简单的面向对象的思想。

```cpp
#include <stdio.h>

// 定义一个结构体
struct Person {
    char name[50];
    int age;

    // 声明一个指向函数的指针
    void (*displayInfo)(struct Person*);
};

// 定义一个函数，用于显示人员信息
void display(struct Person* person) {
    printf("Name: %s, Age: %d\n", person->name, person->age);
}

int main() {
    // 创建一个结构体变量
    struct Person person1 = {"Alice", 25};

    // 将函数指针指向 display 函数
    person1.displayInfo = &display;

    // 通过函数指针调用 display 函数
    person1.displayInfo(&person1);

    return 0;
}

```


# P20: How to Write a CPP Class

下面将通过一个简单的日志类实现，演示类的基本用法。 

### 什么是日志类？

日志类是管理日志消息的一种方式，将程序的消息打印到控制台/不同颜色的控制台/输出到文件或者网络。日志消息可以用于调试，在游戏和应用开发中起到帮助。

### 实现日志类

下面实现错误，警告，消息三个级别的日志类。

```cpp
# include <iostream>

class Log
{
public:
    const int LogLevelError = 0;
    const int LogLevelWarning = 1;
    const int LogLevelInfo = 2;
private:
    int m_LogLevel = LogLevelInfo;
public:
    void SetLevel(int level)
    {
        m_LogLevel = level;
    }

    void Error(const char* message)
    {
        if (m_LogLevel >= LogLevelError)
            std::cout << "[Error]: " << message << std::endl;
    }

    void Warn(const char* message)
    {
        if (m_LogLevel >= LogLevelWarning)
            std::cout << "[Warning]: " << message << std::endl;
    }

    void Info(const char* message)
    {
        if (m_LogLevel >= LogLevelInfo)
            std::cout << "[Info]: " << message << std::endl;
    }
};

int main()
{
    Log log;
    log.SetLevel(log.LogLevelWarning);
    log.Warn("Hello");
    log.Error("Hello");
    log.Info("Hello");
    std::cin.get();
}

```

这只是一个简单的demo，并不意味着一个Log类需要这么写，会在后面介绍生产级别的代码。

# P21: Static in CPP

static分为两种，一种是类外，一种是类中。
在link阶段是局部的，也就是只对它的编译单元obj起作用
类中的static变量表示所有类的实例共享，相当于函数多次对一个变量进行操作

### 举个例子


```cpp
// Main.cpp

#include <iostream>

int s_variable = 10;

int main()
{
    std::cout << s_variable << std::endl;

    std::cin.get();
}

```


```cpp
// Static.cpp

static int s_Variable = 5;

```

编译运行之后，结果是main函数输出结果是10，这说明编译单元static.cpp并没有影响到编译单元main.cpp中的变量。
如果将编译单元Static.cpp中的static去掉，那么链接器将会报错，

```cpp
// Static.cpp

int s_Variable = 5;

```

外部连接，将static中的变量导入

```cpp
// Main.cpp

#include <iostream>

extern int s_Variable;

int main()
{
    std::cout << s_Variable << std::endl;

    std::cin.get();
}

```


```cpp
// Static.cpp

int s_Variable = 5;

```

额，后面函数也是一样。

### Static and Private

全局变量可能会造成奇怪的bug，因为其他编译单元可能总是记挂着它，因此可能需要使用static替代。

### 全局变量，静态全局和局部变量

全局变量：整个程序静态全局变量：文件静态局部变量：文件局部

# P22: Static for Classes and Structs in CPP

P21讨论了在类外的static关键字的含义，现在将讨论在类中的static的含义。
在几乎所有面向对象的编程语言中，class内部的static意味着在这个类的所有实例中，只存在一个变量的实例。如果创建一个Entity的类，并不断实例化，然而static的变量只有一个。如果一个实例化对象更改了这个变量，那么所有的实例化对象的这个变量都将会更改，就像全局变量一样。

### 例子

如果类中没有static关键字，那么实例化两个对象，两个对象的x，y是不一样的值，一个属于e，一个属于e1.

```cpp
#include <iostream>

struct Entity
{
    int x, y;
    
    void Print()
    {
        std::cout << x << ", " << y << std::endl; 
    }
};

int main()
{
    Entity e;
    e.x = 2;
    e.y = 3;

    Entity e1 = { 5, 8 };

    e.Print();
    e1.Print();

    std::cin.get();
}

```

将x和y修改为static变量，实际上这样x，y已经不在属于类成员，因此在注释的地方初始化会报错，换个写法可以。但是严格来说，这样也是不对的。毕竟x，y实际上就是一个全局变量。
运行程序，结果显示了两次5，8，这意味着实际上两个实例化对象共享同一个x，y。有点像全局变量。

```cpp
#include <iostream>

struct Entity
{
    static int x, y;
    
    void Print()
    {
        std::cout << x << ", " << y << std::endl; 
    }
};
 
int Entity::x;
int Entity::y;

int main()
{
    Entity e;
    e.x = 2;
    e.y = 3;

    // Entity e1 = { 5, 8 };
    Entity e1;
    e1.x = 5;
    e1.y = 8;

    e.Print();
    e1.Print();

    std::cin.get();
}

```

尽管你可以使用全局变量；或者使用一个静态全局变量，它可以在一个编译单元进行链接，而不会在整个项目中都是全局可见的。也许创建一个静态全局变量和类中的静态变量似乎一样，为什么还要在类内部使用static呢？
如果你有一些东西，比如一条需要在所有实例中共享的消息，，那么将这条消息放在类内部是有意义的，因为它是和类相关的。

### 静态方法无法访问非静态变量

就像这样，静态方法是无法访问非静态变量的。

```cpp
#include <iostream>

struct Entity
{
    int x, y;
    
    static void Print()
    {
        std::cout << x << ", " << y << std::endl; 
    }
};

int main()
{
    Entity e;
    e.x = 2;
    e.y = 3;

    Entity e1;
    e1.x = 5;
    e1.y = 8;

    Entity::Print();
    Entity::Print();

    std::cin.get();
}

```

额，在类中的静态方法属于类本身，而非对象。非静态变量是属于对象的，那么静态变量并不知道调用那么对象的参数。
在类中实现一个方法，其实就是在类外的一个static方法然后传入对象参数。就像这样子：

```cpp
#include <iostream>

struct Entity
{
    int x, y;

    
};

static void Print(Entity e)
{
    std::cout << e.x << ", " << e.y << std::endl;
}

int main()
{
    Entity e;
    e.x = 2;
    e.y = 3;

    Entity e1;
    e1.x = 5;
    e1.y = 8;

    Print(e);
    Print(e1);

    std::cin.get();
}

```


# P23: Local Static in CPP

额，各种地方定义的static变量其实生命周期都是一样的，关键在于它们作用域范围不一样。

```cpp
#include <iostream>

void Function()
{
    // int i = 0;
    static int i = 0;
    i++;
    std::cout << i << std::endl;
}

int main()
{
    Function();
    Function();
    Function();

    std::cin.get();
}

```

如果i不是一个static变量，那么将输出三次“1”，因为每一次进入函数都会初始化一个变量i为0，这样每次程序运行的结果都将一致。那么如果添加static，它就像一个全局变量，只会被初始化一次，并且保持被修改的状态。
就像这样，只不过它的作用域在函数内，不想全局变量一样可以被随意访问。

```cpp
#include <iostream>

int i;

void Function()
{
    i++;
    std::cout << i << std::endl;
}

int main()
{
    Function();
    // 唯一的区别就是你可以在函数以外的地方更改i的值
    i++;
    Function();
    Function();

    std::cin.get();
}

```

local static可以保留全局变量生命周期又可以限制访问范围。

# P24: Enums in CPP

枚举

```cpp
#include <iostream>

enum Example : unsigned char
{
    A = 5, B, C
};

int a = 0;
int b = 1;
int c = 2;


int main()
{
    int Value = B;
    if (Value == B)
    {
        // Do something here
     }

    std::cin.get();
}

```


# P25: Constructors in CPP

构造函数是一种特殊的方法，它会在类每次实例化的时候运行

### 举个例子


```cpp
#include <iostream>

class Entity
{
public:
    float x, y;

    void Print()
    {
    std::cout << x << ", " << y << std::endl;
    }
};

int main()
{
    Entity e;
    // std::cout << e.x << std::endl;
    e.Print();

    std::cin.get();
}

```

看起来似乎打印了一些随机的浮点数值，这是因为实例化Entity类的时候，只分配了内存，但是还没有对内存进行初始化，这样它就会显示内存原来的值。
需要做的是可能需要将初始化内存并把它设置为0.

### Init函数


```cpp
#include <iostream>

class Entity
{
public:
    float x, y;

    void Init()
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
    // e.Init();
    std::cout << e.x << std::endl;
    e.Print();

    std::cin.get();
}

```

虽然Init函数能够帮助我们初始化类的变量，但是每次实例化一个对象都需要显示调用Init函数。构造函数能在每次实例化的时候自动调用，简化了这一过程。

### 初始化：构造函数

java中可以自动化初始化基本数据类型，但是cpp不会。
如果写构造函数，那么它就是一个空的构造函数。

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
    // e.Init();
    std::cout << e.x << std::endl;
    e.Print();

    std::cin.get();
}

```


### 函数重载

有相同函数名，但是参数不一样的函数版本。

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

    Entity(float x1, float y1)
    {
        x = x1;
        y = y1;
    }

    void Print()
    {
    std::cout << x << ", " << y << std::endl;
    }
};

int main()
{
    // Entity e;
    Entity e(10.0f, 5.0f);
    std::cout << e.x << std::endl;
    e.Print();

    std::cin.get();
}

```

构造函数只会在实例化的时候运行，因此，如果使用静态方法，那么构造函数不会执行。

# P26: 析构函数

构造函数是当实例化一个对象时运行，析构函数是当对象销毁时运行。
析构函数是你卸载变量等东西并清理使用的内存。析构函数同时适用于栈和堆分配的对象。
当new一个对象，如果调用delete析构函数会被调用。
如果只是栈上的一个变量，当生命周期结束，析构函数也会被调用。

```cpp
#include <iostream>

class Entity
{
public:
    float x, y;

    Entity()
    {
        std::cout << "Created Entity!" << std::endl;
        x = 0.0f;
        y = 0.0f;
    }

    ~Entity()
    {
        std::cout << "Destroryed Entity!" << std::endl;
    }

    void Print()
    {
    std::cout << x << ", " << y << std::endl;
    }
};

void Function()
{
    Entity e;
    e.Print();
}

int main()
{
    Function();

    std::cin.get();
}

```


# P27: 继承

面向对象是一个巨大的编程范式，类和继承是它的两个基本特性，也是可以利用的最强大的特性。
继承允许创建相关联的类的层次结构。换句话说，它允许我们包含公共功能的基类，他允许在基类（父类）的基础之上创建子类。
如果没有继承的思想，那么代码将会得到相当的重复

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

class Player
{
public:
    const char* Name;
    float X, Y;

    void Move(float xa, float ya)
    {
        X += xa;
        Y += ya;
    }

    void PrintName()
    {
        std::cout << Name << std::endl;
    }
};

int main()
{
    std::cin.get();
}

```

如果使用继承，那么将会得到简洁的版本。代码在X86 和X64下有不同的运行结果。

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


# P28：虚函数

虚函数允许在子类中重写方法，例如一个子类重写父类中的方法。

# P29: 接口 纯虚函数

纯虚函数允许在基类中定义一个没有实现的函数，然后强制子类去实现该函数。

```cpp
#include <iostream>
#include <string>

class Entity
{
public:
    virtual std::string GetName() = 0;
};

class Player : public Entity
{
private:
    std::string m_Name;

public:
    Player(const std::string& name)
        : m_Name(name){}

    std::string GetName() override { return m_Name;  }
};

void PrintName(Entity* entity)
{
    std::cout << entity->GetName() << std::endl;

}

int main()
{
    // Entity* e = new	Entity();
    Entity* e = new Player("123");
    PrintName(e);

    Player* p = new	Player("Cherno");
    PrintName(p);

}

```


# P30: 可见性

可见性是一个属于面向对象的编程理念，它指类的某些成员或方法实际上有很多可见性。
可见性对实际的程序运行方式没有影响。对程序性能或类似的东西也没有影响。它只是语言中存在的东西，帮助你写更好的组织代码。

### private，protected，public

class默认私有，struct默认公有。

```cpp
#include <iostream>
#include <string>

class Entity
{
private:
    int X, Y;
public:
    Entity()
    {
        X = 0;
        Y = 0;
    }
};

class Player : public Entity
{
public:
    Player()
    {
        X = 2;
    }
};

int main()
{
    Entity e;
    e.X = 2;

    std::cin.get();
}

```


# P31: 数组

指针基本上是数组的工作方式。
数组基本上是元素的集合，按特定顺序排列的一堆东西。它方便批量化处理大量数据。

### 数组越界


```cpp
#include <iostream>

int main()
{
    int example[5];
    example[0] = 2;
    example[4] = 4;
    
    // Debug模式会报错，但是Release模式就会发生内存违规访问。
    example[-1] = 5;
    example[5] = 2;

    std::cout << example[0] << std::endl;
    std::cout << example << std::endl;

    std::cin.get();
}

```


### 数组赋值


```cpp
#include <iostream>

int main()
{
    int example[5];
    //example[0] = 2;
    //example[1] = 2;
    //example[2] = 2;
    //example[3] = 2;
    //example[4] = 4;
    
    for (int i = 0; i < 5; i++)
        example[i] = 2;

    std::cout << example[0] << std::endl;
    std::cout << example << std::endl;

    std::cin.get();
}

```


### 数组和指针


```cpp
#include <iostream>

int main()
{
    int example[5];
    
    example[2] = 5;
    std::cout << example[2] << std::endl;

    int* ptr = example;
    *(ptr + 2) = 6;
    //*((int*)ptr +2) = 6;
    //*(int*)((char*)ptr +8) = 6;
    std::cout << example[2] << std::endl;

    std::cin.get();
}

```


### 栈和堆上创建数组

如果你在函数中创建一个数组，需要返回它那么需要使用new关键字或者传入数组的地址。
在堆上创建数组，你可以控制它的生命周期，创建或者销毁。

```cpp
#include <iostream>

class Entity
{
public:
    //int* example = new int[5];
    int example[5];

    Entity()
    {
        for (int i = 0; i < 5; i++)
            example[i] = 2;
    }
};

int main()
{
    Entity e;

    std::cin.get();
}

```


### 安全数组std::array


```cpp
#include <iostream>
#include <array>

class Entity
{
public:
    // 原始数组
    //int example[5];
    std::array<int, 5> example;


    Entity()
    {
        for (int i = 0; i < example.size(); i++)
            example[i] = 2;
    }
};

int main()
{
    Entity e;

    std::cin.get();
}

```


# P32：字符串

字符串就是字符数组
额，烫烫烫是数组守卫，栈守卫。就是那些预分配的位置cc

```cpp
#include <iostream>

int main()
{
    // 不能更改字符
    const char* name = "liang";
    std::cout << name << std::endl;

    // char name2[5] = { 'l', 'i', 'a', 'n', 'g' };
    char name2[6] = { 'l', 'i', 'a', 'n', 'g', '\0'};
    std::cout << name2 << std::endl;

    std::cin.get(); 
}

```


### std::string

string是cpp的类，有一些可使用的方法。
它接收一个const char*的参数

```cpp
#include <iostream>
#include <string>

int main()
{
    //这里接收char*参数，所以不能把指针加在一起
    std::string name = "liang";// + " hello";

    // name是有方法的因此可以使用+
    name += " hello";

    std::cout << name << std::endl;

    std::cin.get(); 
}

```

加一个引用可以避免字符串的复制，因为这很花费时间。

```cpp
#include <iostream>
#include <string>

//承诺不会修改
void PrintString(const std::string& string)
{
    std::cout << string << std::endl;
}

int main()
{
    //这里接收char*参数，所以不能把指针加在一起
    std::string name = "liang";// + " hello";

    // name是有方法的因此可以使用+
    name += " hello";

    std::cout << name << std::endl;

    std::cin.get(); 
}

```


# P33：字符串字面量


```cpp
#include <iostream>
#include <string>

int main()
{
    //const char* name = u8"L\0ang";
    const char* name = "Lang";
    const wchar_t* name2 = L"Lang";

    const char16_t* name3 = u"Lang";
    const char32_t* name4 = U"Lang";

    std::cout << strlen(name) << std::endl;


    std::cin.get();
}

```


# P34：Const

const伪关键字，因为他在代码方面做不了什么。
有点像类的可见性，只是一个机制，让代码更加干净。

```cpp
#include <iostream>
#include <string>

int main()
{
    const int MAX_AGE = 90;
    int a = 5;
    //const int a = 5;
    a = 2;

    std::cin.get();
}

```

const int*和int const*实际是完全一样的，只是你看见不同的编程风格，重要的是这是一个承诺不会改变指向的指针。

```cpp
#include <iostream>
#include <string>

int main()
{
    const int MAX_AGE = 90;
    const int* a = new int;
    //int const* a = new int;
    int* a = new int;

    *a = 2;
    a = (int*)&MAX_AGE;
    std::cout << a << std::endl;

    std::cin.get();
}

```

但是如果int* const和int const*那么将会有很大的区别。

```cpp
#include <iostream>
#include <string>

int main()
{
    const int MAX_AGE = 90;
    // const int* const a = new int;
    int* const a = new int;
    //int const* a = new int;

    *a = 2;
    a = (int*)&MAX_AGE;
    std::cout << a << std::endl;

    std::cin.get();
}

```

如果你个方法标记为const，那么它承诺不会修改函数中的变量，因此只能调用const方法。所以优势后Getter会有const和非const的两个版本。
另外被mutable标记的变量可以被const方法修改。

```cpp
#include <iostream>
#include <string>

class Entity
{
private:
    int m_X, m_Y;
    mutable int var;
public:
    int GetX() const
    {
        //m_X = 2;
        var = 2;
        return m_X;
    }

    void SetX(int x)
    {
        m_X = x;
    }

};

void PrintEntity(const Entity& e)
{
    std::cout << e.GetX() << std::endl;
}

int main()
{
    Entity e;

    std::cin.get();
}

```


# P35：Mutable

mutable主要有两个应用，和const，lambda
主要的应用类的const

```cpp
#include <iostream>
#include <string>

class Entity
{
private:
    std::string m_Name;
    mutable int m_DebugCount = 0;
public:
    const std::string& GetName() const 
    {
        m_DebugCount++;
        return m_Name;
    }


};


int main()
{
    const Entity e;
    e.GetName();

    std::cin.get();
}

```

lambda等于“=”的时候是传值，额使用mutable让代码可以干净一点，但实际上lambda中的x不是和外面的x一样的。

```cpp
#include <iostream>
#include <string>

class Entity
{
private:
    std::string m_Name;
    mutable int m_DebugCount = 0;
public:
    const std::string& GetName() const 
    {
        m_DebugCount++;
        return m_Name;
    }


};


int main()
{
    const Entity e;
    e.GetName();

    int x = 8;
    auto f = [=]() mutable
    {
        // y = x;
        // y++;
        x++;
        std::cout << x << std::endl;
    };

    f();
    // x = 8;


    std::cin.get();
}

```


# P36：初始化列表

相当于一种语法糖，帮助按照定义变量的顺序在构造函数初始化对象。

# P37：三元操作符

三元操作符实际上是if语句的语法糖。
三元运算符可以在定义的时候初始化更快。if也可以做，但是没那么干净，另外三元运算符可以嵌套，但是代码可读性会很差。

```cpp
#include <iostream>
#include <string>

static int s_Level = 1;
static int s_Speed = 2;

int main()
{
    if (s_Level > 5)
        s_Speed = 10;
    else
        s_Speed = 5;
    
    s_Speed = s_Level > 5 ? 10 : 5;

    std::string rank = s_Level > 10 ? "Master" : "Beginner";
    std::string otherRank;
    if (s_Level > 10)
        otherRank = "Master";
    else
        otherRank = "Beginner";

    std::cin.get();
}

```


# P38：创建并初始化CPP对象

基本上创建一个类需要对其进行实例化（除非完全是一个静态类）
即使创建一个空的类，也会至少在内存中占用一个字节。
内存区域：堆，栈，代码区（一些机器码）

### 栈

生命周期结束，就是代码不在需要引用这个对象，那么将会被销毁。在一个函数里面就是调用的函数被返回，函数里面的栈对象就被销毁了。
堆手动创建，手动销毁。

```cpp
#include <iostream>
#include <string>

// define
using String = std::string;

class Entity
{
private:
    String m_Name;
public:
    Entity() : m_Name("Unknown"){}
    Entity(const String& name) : m_Name(name){}
    const String& GetName() const { return m_Name; }

};

int main()
{
    //Entity entity;
    Entity entity = Entity("Lang");
    std::cout << entity.GetName() << std::endl;

    std::cin.get();
}

```

可以任何时候这样实例化一个对象，但是如果需要在函数的生命周期以外使用对象，那么这样是不行的。
就像这样

```cpp
#include <iostream>
#include <string>

// define
using String = std::string;

class Entity
{
private:
    String m_Name;
public:
    Entity() : m_Name("Unknown"){}
    Entity(const String& name) : m_Name(name){}
    const String& GetName() const { return m_Name; }

};

void Function()
{
    int a = 2;
    Entity entity = Entity("Lang");

}

int main()
{
    Entity* e;
    {
        Entity entity("Lang");
        e = &entity;
        std::cout << entity.GetName() << std::endl;
    }

    std::cin.get();
}

```

另外如果对象太多或者韩勇非常多的内存，由于栈只有MB级别的大小，因此也会考虑使用堆。
另外，在堆上创建对象将会更加耗时，并且要手动销毁对象。然后使用new关键字返回的是一个对象指针，你要用“->”去调用方法，而不是“.”，因为需要指向。

```cpp
#include <iostream>
#include <string>

// define
using String = std::string;

class Entity
{
private:
    String m_Name;
public:
    Entity() : m_Name("Unknown"){}
    Entity(const String& name) : m_Name(name){}
    const String& GetName() const { return m_Name; }

};

int main()
{
    Entity* e;
    {
        Entity* entity = new Entity("Lang");
        e = entity;
        std::cout << entity->GetName() << std::endl;
        // delete entity;
    }
    delete e;
    std::cin.get();
}

```
