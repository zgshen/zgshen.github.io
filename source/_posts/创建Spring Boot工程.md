---
title: 创建一个Spring Boot工程
categories: 技术
tags: web框架
date: 2017-05-10
---
> 在搭建传统的SpringMVC项目或其他Spring项目的的时候，我们通常都需要写一堆与Spring整合的xml配置文件，过程繁琐复杂不说，而且容易出错。为了简化开发，Spring Boot应运而生。
Spring Boot可以创建独立运行的基于Spring的应用，并且大多数时候只需编写少量的配置。能独立运行的原因是Spring Boot项目本身嵌入了Tomcat等其他web容器插件，详细介绍看官网http://projects.spring.io/spring-boot/。

### 创建一个Spring Boot 项目
1、pom.xml配置
(1)基本配置
这里使用Maven构建工程，根据官网的推荐，项目可继承于`spring-boot-starter-parent` 来管理工程。<!--more-->
```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>1.5.2.RELEASE</version>
</parent>
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```
(2)如果不使用官方依赖
实际开发中我们可能想自己创建父工程来管理依赖，例如我们创建聚合工程时有自己的parent工程，那么我们在自己的父工程定义版本号，根据需要引入对应的包。
```xml
<!-- 版本号 -->
<properties>
	<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
	<spring.version>1.5.2.RELEASE</spring.version>
</properties>

<dependencyManagement>
   <dependencies>	
   		<dependency>
	  	  <groupId>org.springframework.boot</groupId>
		  <artifactId>spring-boot-starter-web</artifactId>
		  <version>${spring.version}</version>
	    </dependency>
    </dependencies>
<dependencyManagement>
```

2、编写应用入口类
```java
package com.fyft.test;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 *<p>Title: TestApplication.java</p>
 *<p>Description: TODO</p>
 *<p>CreateDate: 2017年5月10日</p>
 *@author shen
 *@version v1.0
 */
@SpringBootApplication
public class TestApplication {
	
	public static void main(String[] args) {
		SpringApplication.run(TestApplication.class, args);
	}
	
}

```
直接执行此主函数项目就启动了，默认的端口是8080，如果需要改变端口可以在此类实现`EmbeddedServletContainerCustomizer` 接口，这个接口包含内置Servlet容器的一些配置，例如设置访问端口为8003
```java
@SpringBootApplication
public class TestApplication implements EmbeddedServletContainerCustomizer{
	
	public static void main(String[] args) {
		SpringApplication.run(TestApplication.class, args);
	}

	@Override
	public void customize(ConfigurableEmbeddedServletContainer config) {
		config.setPort(8003);
	}
	
}
```

### 创建Controller类
要让Controller被扫描到，必须放在主入口类 `TestApplication ` 的同级目录或下级目录，这样才能被扫描到，注解才会生效。
其他的带注解类都是一样的逻辑， Spring Boot 默认扫描入口启动类所在包之下的目录。

### 打包部署启动
Spring Boot工程直接打成jar包就行了，如果工程是要跑在外部web容器的，也可以打成war包发布，这需要修改一些配置，这里先不做介绍。
在eclipse上直接用maven打包就行，输入 `clean package` 命令，勾上`Skip Tests` 忽略测试就行。

在dos下cd到jar包目录下执行 `java -jar xx.jar`  启动工程，出现一个错误
![这里写图片描述](/img/ba/8iwM9Tr.png)

原因是 maven 自身打包生成的目录结构和文件和 Spring Boot 需要的有所不同，需要在pom.xml加上一段配置，使用 `spring-boot-maven-plugin` 来打包
```xml
<build>
	 <plugins>
		<plugin>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-maven-plugin</artifactId>
            <executions>
                <execution>
                    <goals>
                        <goal>repackage</goal>
                    </goals>
                </execution>
            </executions>
		</plugin> 
	 </plugins>
</build>
```
若上面的dos正cd到target目录下，须退出此目录，在打包编译时会删除一次target目录，若不退出将会包无法删除此目录，因为你正打开它。
再次执行`java -jar` 命令启动成功

![这里写图片描述](/img/ba/GQsVBkE.png)


 