---
title: Web开发（四）-MyBatis
date: 2023-09-09
cover: /img/cover/4.jpg
categories:
  - Web开发
tags:
  - Web开发
  - web
  - web开发
  - java
  - springboot
  - mybatis
  - mysql
---



# 一. MyBatis-理论

这一部分我也不是很了解，简单的写点理解。

## 1. MyBatis基础

MyBatis将数据库语句映射到java函数，将一个函数同SQL语句绑定后，当你调用这个函数，对应的SQL语句将会执行，并且返回参数到函数的返回值。
同时，MyBatis将数据库的表和java的对象做了很好的连接。在MyBatis的作用下，映射SQL查询语句的函数可以返回java对象。

# 二. MyBatis实现


## 1. 依赖和配置


### 依赖

你可以直接使用MyBatis-plus版本，它支持MyBatis

```
    <!--mybatis-plus-->
    <dependency>
        <groupId>com.baomidou</groupId>
        <artifactId>mybatis-plus-boot-starter</artifactId>
        <version>3.4.2</version>
    </dependency>
    <!--Mysql jdbc驱动-->
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>5.1.47</version>
    </dependency>
    <!--druid 连接池-->
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>druid</artifactId>
        <version>1.1.20</version>
    </dependency>

```


### 配置


```
spring.datasource.type=com.alibaba.druid.pool.DruidDataSource
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/mybatis?useUnicode=true&characterEncoding=UTF-8&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=root

```


## 2. 新建实体类

这是一个简单的User类，定义了id，name，password三个属性，以及set，get，toString三个方法。

```
public class User {
    private int id;
    private String name;

    private String password;

    public int getId() {
        return id;
    }

    public String getName(){
        return name;
    }
    public String getPassword(){
        return password;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void setId(int id) {
        this.id = id;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", password='" + password + '\'' +
                '}';
    }
}

```


## 新建Mapper接口

在下面代码中，你可以阅读注释，你很容易明白这些@注解的作用。

```
@Mapper
public interface UserMapper
{

    //返回查询对象的集合
    @Select("select * from user")
    public List<User> findAll();

    //返回查询对象
    @Select("select * from user where id = #{id}")
    public User findById(int id);

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
    @Update("update user set name = #{newName},password= #{newPassword} where id = #{id}")
    public int update(int id,String newName,String newPassword);

}

```


## 3. 编写Controller方法

通过Mapper类你可以将数据库表的数据轻松的赋给java对象或者对数据库进行操作。
下面是一个用户登录的例子

```
@RestController
public class UserController {

    @Autowired
    private UserMapper userMapper;

    //登录
    @PostMapping("/")
    public String login(@RequestParam String name,@RequestParam String password){
        //权限标识
        int verify = 0;

        //检查账号，密码
        List<User> list = userMapper.findAll();
        for(int i=0; i<list.size(); i++){
            User useri = list.get(i);
            if(useri.getName().equals(name) && useri.getPassword().equals(password)){
                verify = 1;
                break;
            }
        }


        //权限判断
        if(verify==1){
            return "login";
        }else{
            return "error";
        }
    }

    //返回用户个人信息
    @GetMapping("/user")
    public String info(@RequestParam int id,@RequestParam String name,@RequestParam String token) {
        if(getClaimsByToken(token).getSubject().equals(name)){
        User user = userMapper.findById(id);
        return user.toString();
        }else{
            return "error";
        }
    }

    //用户注册
    @PostMapping("/user")
    public String register(@RequestParam String name,@RequestParam String password){
        int id = 0;
        userMapper.insert(id,name,password);
        return "register";
    }

    //用户注销
    @DeleteMapping("/user")
    public String delete(@RequestParam int id){
        userMapper.delete(id);
        return "delete";
    }

    //修改个人信息
    @PutMapping("/user")
    public String update(@RequestParam int id,@RequestParam String newName,@RequestParam String newPassword) {
        userMapper.update(id,newName,newPassword);
        return "update";
    }

}

```
