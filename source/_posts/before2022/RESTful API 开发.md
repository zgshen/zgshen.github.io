---
title: RESTful API开发的简单应用
categories: 技术
tags: Web技术
date: 2017-09-02
---

在很早之前接触 Spring MVC 的时候，都知道 Spring MVC 支持 RESTful 风格API的开发，但对于 RESTful 只是有个模糊的认识，以至于甚至在开发写出来的接口其实不符合 RESTful 的要求。
##### 定义
REST 的全称是 Resource Representational State Transfer ，资源以某种表现形式进行状态转移
Resource：资源，即数据；
Representational：某种表现形式，比如用JSON，XML，JPEG等；
State Transfer：状态变化。通过HTTP动词实现。
<!--more-->
HTTP动词有如下几个：
- GET    用来获取资源，
- POST  用来新建资源（也可以用于更新资源），
- PUT    用来更新资源，
- DELETE  用来删除资源

在RESTful API中，URL中只使用名词来指定资源，原则上不使用动词，并且一般使用复数，比如 GET 操作 https://v1/users/1 来获取用户id为1的信息资源，禁止使用 http://v1/getUserById 、 http://v1/deleteUser 之类的url。

##### 用处
一种技术的存在肯定是为了解决一些问题而诞生的，REST是一种软件架构模式，通过使用RESTful 风格的 API 用来解决多端（PC、Android、IOS）共用一套统一的 API ，避免重复开发。

##### 在 SpringMVC 中的应用
用 SpringMVC 可以开发 restful 风格的restful api，以 Spring Boot 为基本框架，这里写一个基本的 controller 类
```java
@RestController
@RequestMapping("/users")
public class UserController {
    @Autowired
    UserService userService;

    @RequestMapping(value="{id}", method=RequestMethod.GET)
    public String getUserById(@PathVariable("id") String userId) {
        return ResultUtil.success(userService.getUserById(userId), "操作成功");
    }

    @RequestMapping(value="{id}", method=RequestMethod.PUT)
    public String updateUser(@PathVariable("id") String userId) {
        int num = userService.updateUser(userId);
        if (1==num){
            return ResultUtil.success("操作成功");
        } else return ResultUtil.error("操作失败");
    }

    @RequestMapping(method=RequestMethod.POST)
    public String insertUser(String userCode, String userName) {
        int num = userService.insertUser(userCode, userName);
        if (1==num){
            return ResultUtil.success("操作成功");
        } else return ResultUtil.error("操作失败");
    }

    @RequestMapping(value="{id}", method=RequestMethod.DELETE)
    public String deleteUser(@PathVariable("id") String userId) {
        int num = userService.deleteUser(userId);
        if (1==num){
            return ResultUtil.success("操作成功");
        } else return ResultUtil.error("操作失败");
    }
}

```
ResultUtil 封装返回数据格式，这里只是一个简单的封装
```java
public class ResultUtil {

    private final static String SUCCESS = "success";
    private final static String MSG = "msg";
    private final static String DATA = "data";

    public static String success(String msg){
        Map<String,Object> result = new HashMap<String,Object>();
        result.put(SUCCESS, true);
        result.put(MSG, msg);
        result.put(DATA, new Object());
        return JSON.toJSONString(result);
    }

    public static String success(Object data, String msg){
        Map<String,Object> result = new HashMap<String,Object>();
        result.put(SUCCESS, true);
        result.put(MSG, msg);
        result.put(DATA, data);
        return JSON.toJSONString(result);
    }

    public static String error(String msg){
        Map<String,Object> result = new HashMap<String,Object>();
        result.put(SUCCESS, false);
        result.put(MSG, msg);
        result.put(DATA, new Object());
        return JSON.toJSONString(result);
    }

    public static String error(Object data, String msg){
        Map<String,Object> result = new HashMap<String,Object>();
        result.put(SUCCESS, false);
        result.put(MSG, msg);
        result.put(DATA, data);
        return JSON.toJSONString(result);
    }
}
```

对应的请求url为：
```
查询、更新、删除： /users/1
插入： /users
```
有时需要管理版本号会把版本号写在url，比如 `v1/users/1`、 `v2/users/1` 。至于请求是什么类型的，可以在请求在head中设置，如果是ajax请求则设置比较简单
```javascript
$.ajax({
    url: '/users/1',
    type: 'get',//put、delete
    success: function(data) {
        console.log(data)
    }
});

$.ajax({
    url: '/users',
    type: 'post',
    data: {
        userCode: 'test',
        userName: '测试名字'
    },
    success: function(data) {
        console.log(data)
    }
});
```

RESTful API 的开发涉及许多细节和技术实现，实际开发中的应用会可能会用到一些封装库和框架，这里不做深入了解，只是简单的记录自己的一些基本认识，相关的知识参考了以下的链接。

#####相关参考链接
- [REST的出处论文 - 作者Roy Fielding](http://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)
- [RESTful API 设计指南 - 阮一峰的网络日志](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)
- [怎样用通俗的语言解释REST，以及RESTful？ - 回答作者: 覃超](https://zhihu.com/question/28557115/answer/48094438)

