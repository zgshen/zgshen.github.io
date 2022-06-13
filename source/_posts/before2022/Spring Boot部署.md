---
title: Spring Boot 打包部署
categories: 技术
tags: web框架
date: 2017-07-15
---
Spring Boot默认集成Web容器，部署也相对简单，如果需要以war包形式部署在外部Web容器上也可以，只需要做一些简单的修改配置。
<!--more-->

## 使用集成的Web容器部署方式
__打包__
maven 工程在 eclipse 中执行 Run as Maven build，输入 clean package 进行打包，这里要注意的是 Spring Boot 打成jar包要可以运行，必须使用Spring Boot提供的一个插件，不然打成的普通的jar是无法运行Spring Boot工程的，一般会提示 jar中没有主清单属性。
在pom.xml加入插件
```xml
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
```
生成的 jar 包使用 `java -jar xx.jar` 命令就可以启动。

## 部署到外部Web容器方式
在 pom.xml 文件将 `<packaging>jar</packaging>` 改为 `<packaging>war</packaging>`
加上build插件，表明此Web工程不需要web.xml文件
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-war-plugin</artifactId>
    <configuration>
        <failOnMissingWebXml>false</failOnMissingWebXml>
    </configuration>
</plugin>
```

排除 Spring Boot Tomcat 组件，scope 属性设为 provided
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-tomcat</artifactId>
    <scope>provided</scope>
</dependency>
```

在 Application 即main方法类同包下创建实现外部 Web 容器启动的启动类
例子
```java
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.support.SpringBootServletInitializer;

public class WxServletInitializer extends SpringBootServletInitializer{
    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder builder) {
        return builder.sources(WxApplication.class);//WxApplication 为原main函数启动类
    }
}
```

打包完毕将war包部署到外部Web容器。
