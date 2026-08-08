---
title: Web开发（三）-TomCat
date: 2023-09-08
categories:
  - Web开发
tags:
  - Web开发
  - web
  - web开发
  - java
  - springboot
  - tomcat
---



# 一. TomCat-理论


## 1. Tomcat基础

TomCat是一个Web服务器，它默认活跃在电脑的8080端口，接收HTTP请求。
同时，TomCat提供规范的HTTP接口，它接收规范的HTTP请求，对于Response，你也不需要自己编写，因为TomCat帮助你返回标准的Response。
下面是具体实现：
- 当你访问此localhost:8080时，浏览器或者其他代理发送的HTTP请求将会被TomCat截获，
- 如果你在SpringBoot框架中使用TomCat，你可以获取HTTP请求，对数据做处理。
- 最后，你希望对这个请求作出响应，TomCat帮助你构建标准的HTTP响应。

# 二. TomCat-实现


## 1. 依赖和配置

当你新建一个SpringBoot项目时，该项目集成了TomCat。
因此，你不必要花时间去配置TomCat。

## 2. Controller类

一般来说，我们把对请求的处理封装在Controller类中。

### @RestController

你可以在使用这个注解标注为Controller类，在这个类中你可以定义函数处理HTTP请求。
@RestController = @Controller + @ResponseBody
@Controller：将当前修饰的类注入SpringBoot IOC容器，使得从该类所在的项目跑起来的过程中，这个类就被实例化。当然也有语义化的作用，即代表该类是充当Controller的作用
@ResponseBody：它的作用简短截说就是指该类中所有的API接口返回的数据，甭管你对应的方法返回Map或是其他Object，它会以Json字符串的形式返回给客户端，本人尝试了一下，如果返回的是String类型，则仍然是String。

### @RequestMapping

你可以使用这个注解标注函数接收的HTTP请求类型和路径，这样函数对应一个接口。
@RequestMapping有两个参数，你可以指定HTTp方法，以及接收的参数。
更简单的方法是使用@GetMapping/PostMapping/DeleteMapping/PutMapping这样你只需要指定接收路径。

### @RequestParam

指定函数必须从HTTP请求中接收的参数，否则报错。

## 3. 代码实例


```
@RestController
public class UserController {

    @GetMapping("/index")
    public String getIndex(@RequestParam String name){
        return "Hello "+name;
    }

}

```

当你访问[http://localhost:8080/index?name=tomcat](http://localhost:8080/index?name=tomcat)时，你传入name参数值为tomcat。Controller接收后，在响应中返回hello tomcat。