---
title: Spring Boot 普通类调用Bean对象的一种方式
categories: 技术
tags: Spring
date: 2017-06-08
---
有时我们有一些特殊的需要，可能要在一个不被Spring管理的普通类中去调用Spring管理的bean对象的一些方法，比如一般SpringMVC工程在controller中通过 
```java
@Autowired
private TestService testService;
```
注入TestService 接口就可以调用此接口实现类的实现的方法。<!--more-->
但在一般类中显然不可以这么做，注入的 TestService  将会报空指针异常，你无法拿到这个bean，在一般的ssm工程中我们可以通过xml配置把普通类设置成一个bean对象，那么 TestService 就有效了， 或者使用 `ApplicationContext` 直接读取xml配置中的bean也可以拿到 TestService。`

Spring Boot 已经摒弃了各种繁琐的xml配置，当然就不再使用xml配置的方式，之前在网上看到一种很简便的方式，但现在又找不到链接了，这里做下记录。

在普通类中定义 `ApplicationContext` 静态变量和set方法
```java
	private static ApplicationContext applicationContext;//启动类set入，调用下面set方法
	
	public static void setApplicationContext(ApplicationContext context) {
		applicationContext = context;
	}
```

在启动类中，启动时事实已经生成 ConfigurableApplicationContext 对象， ConfigurableApplicationContext 是 ApplicationContext 接口的实现，这里直接传到普通类的 setApplicationContext 方法就行了
```java
@SpringBootApplication
@ServletComponentScan
public class WxApplication implements EmbeddedServletContainerCustomizer{
	
	public static void main(String[] args) {
		ConfigurableApplicationContext applicationContext = SpringApplication.run(WxApplication.class, args);
		TestClass.setApplicationContext(applicationContext);
	}
}
```

由于是静态变量，类加载时 applicationContext 已经存在，就可获取到 TestService 了，唯一不好就是静态变量在服务器启动后将一直存在
```java
public class TestClass {
	
	private static ApplicationContext applicationContext;//启动类set入，调用下面set方法
	
	public static void setApplicationContext(ApplicationContext context) {
		// TODO Auto-generated method stub
		applicationContext = context;
	}
	
	public void getBeanTest(){
		TestService testService  = (TestService)applicationContext.getBean(TestService.class);
	}
}
```

__补充__：
在普通 Spring 工程在启动的时候都会通过 `org.springframework.web.context.ContextLoaderListener` 监听器从加载系统资源并管理bean， Spring 提供的 `WebApplicationContextUtils` 工具类能在请求时获取到运行时工程的bean，如果看源码就可以知道监听器执行时与 `WebApplicationContextUtils` 类的关联

```java
//封装一下，类的class和请求request为必要参数
public static <T> T getBean(Class<? extends Object> cla,HttpServletRequest request){
        if(request == null){
            return null;
        }
        return (T)WebApplicationContextUtils.getRequiredWebApplicationContext(request.getServletContext()).getBean(cla);//getBean参数可为bean类的.class或直接是bean的Id
    }

//这样获取bean
TestService testService= (TestService)getBean(TestService.class, request);
```