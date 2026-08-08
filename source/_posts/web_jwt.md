---
title: Web开发（五）-JWT
date: 2023-09-10
categories:
  - Web开发
tags:
  - Web开发
  - web
  - web开发
  - java
  - springboot
  - jwt
---


*这篇文章将会向你介绍JWT的理论基础和程序实现*

# 一. JWT-理论


## JWT基础

*如果你没有任何基础，请耐心看完这一部分*
想象一下你登录某个网站的场景。你从登录页面输入账号密码进入到该网站，同时该网站返回你的个人信息，包括你的昵称，头像，个性签名，显示到网页上。更重要的是，登录网站意味着你的身份得到服务器的验证，你获得了访问你的个人信息的权限。
服务器通过账号密码识别我们的身份吗？是，但不完全是。首先，你需要明白我们浏览器所依靠的http协议是无状态的。这就好像你和一个记忆力差劲的人交流，每一轮对话之后，他都会忘记你的名字。所以，你在每次和他说话之前，都需要重申你的身份。服务器就像这么一个人，尽管你对它说尽千言万语，而服务器只会在众多用户中迷失你的名字。
那么，这是否意味着我们必须在每一个请求之前都输入我们的账号密码来告知服务器我们的合法身份呢？答案是否定的，有更简单的解决方案。JWT（JSON WEB TOKEN）就是一种实现方式。
在输入账号密码之后，服务器会返回一个token给我们。以后在每次请求，我们带上token，服务器便会在用户中认出你。但是，如果你企图修改token，服务器能轻易检查出。这一部分是通过签名实现，当服务器用秘钥对token签名后，任何对token的更改都需要这个秘钥。

## JWT

JWT由三个部分组成：header，payload，signature。header标识类型和签名算法。payload一般会存放标识你的一些信息账号id，用户名等。signnature是服务器的签名，防止你篡改上一部分的信息冒充他人。

### header：


```
{
    'typ': 'JWT',
    'alg': 'HS256'
}

```

*类型是JWT；签名算法是HS256*

### 一般header会进行base64编码：


```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9

```


### payload：


```
{
    "sub": "1234567890",
    "name": "John Doe",
    "admin": true
}

```

*iss: jwt签发者；sub: jwt所面向的用户；aud: 接收jwt的一方；exp: jwt的过期时间，这个过期时间必须要大于签发时间；nbf: 定义在什么时间之前，该jwt都是不可用的.；iat: jwt的签发时间；jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。*

### 一般会对payload进行base64编码：


```
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9

```


## signature：

signature对上面两部分的base64编码使用key进行签名

```
HMACSHA256（base64(header) . base64(payload) , key）

```

一般像这样：      eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ

## JWT

将这三部分合并，中间用“.”分隔，得到一个完整的JWT

```
  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ

```


# 二. JWT-实现


## 0. 添加依赖


```
    <!--JWT-->
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt</artifactId>
        <version>0.9.1</version>
    </dependency>

```


## 1. 生成token


```
//token有效时间
private static long expire = 604800;
//校验token有效性秘钥
private static String key = "aaaabbbbccccddddaaaabbbbccccdddd";
//token生成
public static String generateToken(String username){
Date now = new Date();
Date expiration = new Date(now.getTime()+1000*expire);
return Jwts.builder()
//          .setHeaderParams()
            .setSubject(username)
            .setIssuedAt(now)
            .setExpiration(expiration)
            .signWith(SignatureAlgorithm.HS512,key)
            .compact();
}

```


## 2. token校验


```
//token校验
public static Claims getClaimsByToken(String token){
    return Jwts.parser()
            .setSigningKey(key)
            .parseClaimsJws(token)
            .getBody();
}

```


## 3. 一个简单的例子

你可以将上面两个函数封装在JwtUtils的类中，在Controller中调用token相关的函数在网络请求中使用token。

```
String token = generateToken(name);

```

登录之后将token返回到客户端。

```
getClaimsByToken(token).getSubject().equals(name)

```

校验客户端的token后，允许其访问对应接口。