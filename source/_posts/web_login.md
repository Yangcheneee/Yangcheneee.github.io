---
title: Web 登录实现&身份认证
date: 2023-10-15
categories:
  - Web开发
tags:
  - Web开发
  - web开发
  - java
  - springboot
  - vue
---



## 开发工具&环境


### 前端

vue集成html，css，javascript

### 后端

SpringBoot集成mybatis，java，tomcat

### 数据库

Mysql以及图形化界面SQLyogEnt

### 具体过程

数据库数据-java对象/Dao(mapper)—> 程序数据 (controller)—> 后端数据 —tomcat—> 前端数据 -vue-> html数据

# 数据结构&接口文档


## 数据结构


### 数据库

user表id，username，password；将id设置为主键

### Java类

新建User类：int id，String username，String password

## 接口文档


### 1. 用户注册：

POST localhost/auth/register
username: “xxx”
hash_password: “xxx” 

### 2. 用户登录：

POST localhost/auth/login
username: “xxx”
password: “xxx”
return token

### 2. 拉取用户信息：

GET localhost/user
token: “xxx”
return：id,username,password

### 3. 修改用户信息：

PUT localhost/user
token: “xxx”
username: “xxx”
hash_password: “xxx”

# 后端实现


## 数据库实现

user表id，username，password；将id设置为主键

## 连接数据库


### application.properties文件：


```java
spring.datasource.type=com.alibaba.druid.pool.DruidDataSource

# ????
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
# ?????
spring.datasource.url=jdbc:mysql://localhost:3306/mybatis?useUnicode=true&characterEncoding=UTF-8&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=root

```


## Dao层实现


```java
package com.example.bbb.entity;

public class User {
    private int id;
    private String username;
    private String password;
    public int getId() {
        return id;
    }
    public String getUsername(){
        return username;
    }
    public String getPassword(){
        return password;
    }

    public void setUsername(String username) {
        this.username = username;
    }
    public void setPassword(String password) {
        this.password = password;
    }
    public void setId(int id) {
        this.id = id;
    }

    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", password='" + password + '\'' +
                '}';
    }

}

```


## Mapper层实现


```java
package com.example.bbb.mapper;

import java.util.List;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.bbb.entity.User;
import org.apache.ibatis.annotations.*;
@Mapper
public interface UserMapper
{
    @Select("select id from user where username = #{username}")
    public int getId(String username);

    //返回查询对象的集合
    @Select("select * from user")
    public List<User> findAll();

    //返回查询对象
    @Select("select * from user where id = #{id}")
    public User getInfo(int id);
    @Select("select username from user")
    public List<String> getAllUsername();

    @Select("select * from user where username = #{username}")
    public User findByUsername(String username);

    //将数据库insert语句映射到java程序的insert方法
    //返回值为插入语句影响的记录数目
    @Insert("insert into user values (#{id},#{name},#{password})")
    public int insert(int id, String name,String password);

    //将数据库delete语句映射到java程序的delete方法
    //返回值为删除语句影响的记录数目
    @Delete("delete  from user where id = #{id}")
    public int delete(int id);

    //将数据库update语句映射到java程序的update方法
    //返回值为更新语句影响的记录数目
    @Update("update user set username = #{newName},password= #{newPassword} where id = #{id}")
    public int update(int id,String newName,String newPassword);

    @Select("select username from user where username != #{username}")
    public List<String> otherUserName(String username);

}

```


## Controller层实现


```java
package com.example.bbb.controller;

import com.example.bbb.entity.User;
import com.example.bbb.mapper.UserMapper;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

import com.fasterxml.jackson.databind.ObjectMapper;

import static com.example.bbb.utils.JwtUtils.*;

@RestController
@CrossOrigin
public class UserController {
    @Autowired
    private UserMapper userMapper;
    //登录
    @PostMapping("/auth/login")
    public String login(@RequestParam("username") String username,@RequestParam("password") String password){
        //权限标识
        int verify = 0;
        //检查账号，密码
        List<User> list = userMapper.findAll();
        for(int i=0; i<list.size(); i++){
            User useri = list.get(i);
            if(useri.getUsername().equals(username) && useri.getPassword().equals(password)){
                verify = 1;
                break;
            }
        }
        //权限判断
        if(verify==1){
            String token = generateToken(username);
            int id = userMapper.getId(username);
            System.out.println("用户"+id+"登录成功！");
            return token;
        }else{
            System.out.println("用户"+username+"登录失败！！");
            return "error";
        }
    }

    //返回用户个人信息
    @GetMapping("/user")
    public String info(@RequestParam String token) throws JsonProcessingException {
        if(verifyToken(token)) {
            String username = getUsernameFromToken(token);
            int id = userMapper.getId(username);
            User user = userMapper.getInfo(id);
            ObjectMapper objectMapper = new ObjectMapper();
            String userJson = objectMapper.writeValueAsString(user);
            System.out.println("用户"+id+"查看个人信息！");
            return userJson;
        } else{
            System.out.println("错误的token！！！");
            return "error";
        }
    }

    //用户注册
    @PostMapping("/auth/register")
    public String register(@RequestParam("username") String newusername,@RequestParam String password){
        int id = 0;
        List<String> usernameList = userMapper.getAllUsername();
        for(int i=0; i<usernameList.size(); i++){
            String username = usernameList.get(i);
            if(username.equals(newusername)){
                System.out.println("注册存在的用户名！");
                return("error");
            }
        }
        userMapper.insert(id,newusername,password);
        int newid = userMapper.getId(newusername);
        System.out.println("用户"+newid+"注册成功！！");
        return "用户名："+newusername + '\n' +"密码（hash）："+password;
    }

//    //用户注销
//    @DeleteMapping("/user")
//    public String delete(@RequestParam int id){
//        userMapper.delete(id);
//        return "delete";
//    }

    //修改个人信息
    @PutMapping("/user")
    public String update(@RequestParam String token,@RequestParam String newUsername,@RequestParam String newPassword) {
        if(verifyToken(token)) {
            String username = getUsernameFromToken(token);
            int id = userMapper.getId(username);
            List<String> list = userMapper.otherUserName(username);
            for (int i = 0; i < list.size(); i++) {
                String usernamei = list.get(i);
                if (usernamei.equals(newUsername)) {
                    System.out.println("用户" + id + "使用重复的用户名！");
                    return "error";
                }
            }
            userMapper.update(id, newUsername, newPassword);
            System.out.println("用户" + id + "更新用户名" + username + "为" + newUsername);
            return "ok";
        } else{
            System.out.println("错误的token！！！");
            return "error";
        }
    }
}

```


## JWT实现


```java
package com.example.bbb.utils;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import java.util.Date;

public class JwtUtils {
    //token有效时间
    private static long expire = 604800;
    //token秘钥
    private static String key = "aaaabbbbccccddddaaaabbbbccccdddd";
    //生成token
    public static String generateToken(String username){
        Date now = new Date();
        Date expiration = new Date(now.getTime()+1000*expire);
        return Jwts.builder()
                .setSubject(username)
                .setIssuedAt(now)
                .setExpiration(expiration)
                .signWith(SignatureAlgorithm.HS512,key)
                .compact();
    }
    // 校验token合法性
    public static boolean verifyToken(String token) {
        try {
            Jwts.parser().setSigningKey(key).parseClaimsJws(token);
            return true;
        } catch (Exception e) {
            // 处理异常
            System.out.println("错误的token");
        }
        return false;
    }
    //提取token中的username
    public static String getUsernameFromToken(String token){
        Claims claims = Jwts.parser()
                .setSigningKey(key)
                .parseClaimsJws(token)
                .getBody();

        return claims.getSubject();
    }
}

```
