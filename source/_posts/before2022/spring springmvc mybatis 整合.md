---
title: spring springmvc mybatis 整合
categories: 技术
tags: Spring
date: 2016-04-10
---
最近鼓捣ssm框架的东西，写篇博文记录。
环境 apache-tomcat-8.0.33、jdk1.8.0_05  maven Dynamic Web Module 2.5
1、各个xml配置文件的配置
(1)pom.xml 配置清单文件
连接池用的阿里巴巴Druid，数据库mysql，指定jdk编译版本1.8<!--more-->

```

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>cn.shen</groupId>
  <artifactId>ssmdemo</artifactId>
  <packaging>war</packaging>
  <version>0.0.1-SNAPSHOT</version>
  <name>ssmdemo Maven Webapp</name>
  <url>http://maven.apache.org</url>
  
  <dependencies>
		<!-- 添加spring依赖，对应版本号jar包 -->
		
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-webmvc</artifactId>
			<version>4.1.7.RELEASE</version>
		</dependency>
	 
		<!-- 添加tomcat下servlet-api依赖,对应版本 -->
		<dependency>
			<groupId>javax.servlet</groupId>
			<artifactId>javax.servlet-api</artifactId>
			<version>3.1.0</version>
			<scope>provided</scope>
		</dependency>

		<dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<version>4.12</version>
		</dependency>

		
		<!-- 添加jtl支持 -->
		<dependency>
			<groupId>javax.servlet</groupId>
			<artifactId>jstl</artifactId>
			<version>1.2</version>
		</dependency>
	  
	  	<!-- 添加Spring支持 -->
		<dependency>
	  		<groupId>org.springframework</groupId>
	  		<artifactId>spring-core</artifactId>
	  		<version>4.1.7.RELEASE</version>
	  	</dependency>
	  	<dependency>
	  		<groupId>org.springframework</groupId>
	  		<artifactId>spring-beans</artifactId>
	  		<version>4.1.7.RELEASE</version>
	  	</dependency>
	  	<dependency>
	         <groupId>org.springframework</groupId>
	         <artifactId>spring-tx</artifactId>
	         <version>4.1.7.RELEASE</version>
	        </dependency>
	  	<dependency>
	  		<groupId>org.springframework</groupId>
	  		<artifactId>spring-context</artifactId>
	  		<version>4.1.7.RELEASE</version>
	  	</dependency>
	  	<dependency>
	  		<groupId>org.springframework</groupId>
	  		<artifactId>spring-context-support</artifactId>
	  		<version>4.1.7.RELEASE</version>
	  	</dependency>
	  	
	  	<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-web</artifactId>
			<version>4.1.7.RELEASE</version>
		</dependency>
		
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-webmvc</artifactId>
			<version>4.1.7.RELEASE</version>
		</dependency>
		
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-aop</artifactId>
			<version>4.1.7.RELEASE</version>
		</dependency>
		
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-aspects</artifactId>
			<version>4.1.7.RELEASE</version>
		</dependency>
		
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-jdbc</artifactId>
			<version>4.1.7.RELEASE</version>
		</dependency>
	  
		  <dependency>
			<groupId>org.mybatis</groupId>
			<artifactId>mybatis-spring</artifactId>
			<version>1.2.3</version>
		</dependency>
		
		<!-- 添加日志支持 -->
	  	<dependency>
			<groupId>log4j</groupId>
			<artifactId>log4j</artifactId>
			<version>1.2.17</version>
		</dependency>
		
		<dependency>
			<groupId>org.slf4j</groupId>
			<artifactId>slf4j-log4j12</artifactId>
			<version>1.7.12</version>
		</dependency>
		
		<!-- 添加mybatis支持 -->
		 <dependency>
			<groupId>org.mybatis</groupId>
			<artifactId>mybatis</artifactId>
			<version>3.3.0</version>
		</dependency>
		
		<!-- jdbc驱动包  -->
		<dependency>
			<groupId>mysql</groupId>
			<artifactId>mysql-connector-java</artifactId>
			<version>5.1.37</version>
		</dependency>
		
		<dependency>
			<groupId>commons-fileupload</groupId>
			<artifactId>commons-fileupload</artifactId>
			<version>1.3.1</version>
		</dependency>
		
		<!-- 添加连接池druid支持 -->
		<dependency>
			<groupId>com.alibaba</groupId>
			<artifactId>druid</artifactId>
			<version>1.0.16</version>
		</dependency>
		
	</dependencies>
  
  <build>
    <finalName>ssmdemo</finalName>
    <!-- 指定jdk编译器版本 -->
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-compiler-plugin</artifactId>
				<version>3.1</version>
				<configuration>
					<source>1.8</source>
					<target>1.8</target>
				</configuration>
			</plugin>
		</plugins>
  </build>
</project>

```
(2)web.xml配置

```

<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance
 http://www.springmodules.org/schema/cache/springmodules-cache.xsd
 http://www.springmodules.org/schema/cache/springmodules-ehcache.xsd "
	xmlns="http://java.sun.com/xml/ns/javaee" 
	xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd" 
	id="WebApp_ID" version="2.5">
  <display-name>Archetype Created Web Application</display-name>
  
   <!-- Spring配置文件 -->
   <!--  -->
	<context-param>
		<param-name>contextConfigLocation</param-name>
		<param-value>classpath:applicationContext.xml</param-value>
	</context-param>
   
   <!-- 解决工程编码过滤器 -->
	<filter>
		<filter-name>encodingFilter</filter-name>
		<filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
		<init-param>
			<param-name>encoding</param-name>
			<param-value>UTF-8</param-value>
		</init-param>
		<init-param>
			<param-name>forceEncoding</param-name>
			<param-value>true</param-value>
		</init-param>
	</filter>
	<filter-mapping>
		<filter-name>encodingFilter</filter-name>
		<url-pattern>/*</url-pattern>
	</filter-mapping>
   
    <!-- Spring监听器 -->
	<listener>
		<listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
	</listener>
	
   <!-- 添加对springmvc的支持 -->
	<servlet>
		<servlet-name>springMVC</servlet-name>
		<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
		<init-param>
			<param-name>contextConfigLocation</param-name>
			<param-value>classpath:spring-mvc.xml</param-value>
		</init-param>
		<load-on-startup>1</load-on-startup>
		<async-supported>true</async-supported>
	</servlet>
	<servlet-mapping>
        <servlet-name>springMVC</servlet-name>
        <url-pattern>*.do</url-pattern>
    </servlet-mapping>
	<servlet-mapping>
		<servlet-name>springMVC</servlet-name>
		<url-pattern>*.html</url-pattern>
	</servlet-mapping>
</web-app>
```
(3)mybatis配置

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN" "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
	<!-- 别名 -->
	<typeAliases>
		<package name="cn.web.open.model"/>
	</typeAliases>
</configuration>
```
(4)springmvc配置

```

<?xml version="1.0" encoding="UTF-8"?>    
<beans xmlns="http://www.springframework.org/schema/beans"    
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"   
    xmlns:p="http://www.springframework.org/schema/p"  
    xmlns:aop="http://www.springframework.org/schema/aop"   
    xmlns:context="http://www.springframework.org/schema/context"  
    xmlns:jee="http://www.springframework.org/schema/jee"  
    xmlns:tx="http://www.springframework.org/schema/tx"  
    xmlns:mvc="http://www.springframework.org/schema/mvc"
    xsi:schemaLocation="    
        http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.0.xsd  
        http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-4.0.xsd  
        http://www.springframework.org/schema/mvc   http://www.springframework.org/schema/mvc/spring-mvc.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.0.xsd  
        http://www.springframework.org/schema/jee http://www.springframework.org/schema/jee/spring-jee-4.0.xsd  
        http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.0.xsd">    

	
	<!-- 使用注解的包，包括子集 -->
	<context:component-scan base-package="cn.web.open.controller" />
	<!-- 开启注解 -->
	<mvc:annotation-driven/>
	
	<mvc:resources mapping="/static/**" location="/static/"/>

	<!-- 视图解析器 -->
	<bean id="viewResolver"
		class="org.springframework.web.servlet.view.InternalResourceViewResolver">
		<property name="prefix" value="/" />	
		<property name="suffix" value=".jsp"></property>
	</bean>
	
	<!-- 文件上传解析器 id 必须为multipartResolver -->
	<bean id="multipartResolver"
        class="org.springframework.web.multipart.commons.CommonsMultipartResolver">
		<property name="defaultEncoding" value="UTF-8"/>  
	    <property name="maxUploadSize" value="10000000"/>
	</bean>

</beans>  

```
(5)数据源及整合配置applicationContext.xml

```
<?xml version="1.0" encoding="UTF-8"?>    
<beans xmlns="http://www.springframework.org/schema/beans"    
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"   
    xmlns:p="http://www.springframework.org/schema/p"  
    xmlns:aop="http://www.springframework.org/schema/aop"   
    xmlns:context="http://www.springframework.org/schema/context"  
    xmlns:jee="http://www.springframework.org/schema/jee"  
    xmlns:tx="http://www.springframework.org/schema/tx"  
    xsi:schemaLocation="    
        http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.0.xsd  
        http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-4.0.xsd  
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.0.xsd  
        http://www.springframework.org/schema/jee http://www.springframework.org/schema/jee/spring-jee-4.0.xsd  
        http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.0.xsd">    
        
	
	
	<!-- 配置数据源 ,连接池用的阿里druid-->
	<bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">
		<property name="driverClassName" value="com.mysql.jdbc.Driver"/>
		<!-- 
		<property name="url" value="jdbc:mysql://IP+数据库"/>
		<property name="username" value="用户名"/>
		<property name="password" value="密码"/>
		 -->
		 <property name="url" value="jdbc:mysql://121.42.57.186:3306/blog"/>
		<property name="username" value="root"/>
		<property name="password" value="shen200800"/>
		
	</bean>

	<!-- 配置mybatis的sqlSessionFactory -->
	<bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
		<property name="dataSource" ref="dataSource" />
		<!-- 自动扫描mappers.xml文件 -->
		<property name="mapperLocations" value="classpath:mappers/*.xml"></property>
		<!-- mybatis配置文件 -->
		<property name="configLocation" value="classpath:mybatis-config.xml"></property>
	</bean>

	<!-- DAO接口所在包名，Spring会自动查找其下的类 -->
	<bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
		<property name="basePackage" value="cn.web.open.dao" />
		<property name="sqlSessionFactoryBeanName" value="sqlSessionFactory"></property>
	</bean>

	<!-- (事务管理)transaction manager, use JtaTransactionManager for global tx -->
	<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
		<property name="dataSource" ref="dataSource" />
	</bean>
	<!-- 5. 使用声明式事务 transaction-manager：引用上面定义的事务管理器-->
	<tx:annotation-driven transaction-manager="txManager" />
	
	
  <!-- 配置事务通知属性 -->  
    <tx:advice id="txAdvice" transaction-manager="transactionManager">  
        <!-- 定义事务传播属性 -->  
        <tx:attributes>  
            <tx:method name="insert*" propagation="REQUIRED" />  
            <tx:method name="update*" propagation="REQUIRED" />  
            <tx:method name="edit*" propagation="REQUIRED" />  
            <tx:method name="save*" propagation="REQUIRED" />  
            <tx:method name="add*" propagation="REQUIRED" />  
            <tx:method name="new*" propagation="REQUIRED" />  
            <tx:method name="set*" propagation="REQUIRED" />  
            <tx:method name="remove*" propagation="REQUIRED" />  
            <tx:method name="delete*" propagation="REQUIRED" />  
            <tx:method name="change*" propagation="REQUIRED" />  
            <tx:method name="check*" propagation="REQUIRED" />  
            <tx:method name="get*" propagation="REQUIRED" read-only="true" />  
            <tx:method name="find*" propagation="REQUIRED" read-only="true" />  
            <tx:method name="load*" propagation="REQUIRED" read-only="true" />  
            <tx:method name="*" propagation="REQUIRED" read-only="true" />  
        </tx:attributes>  
    </tx:advice>  
	
  
    <!-- 配置事务切面 -->  
    <aop:config>  
        <aop:pointcut id="serviceOperation"  
            expression="execution(* cn.web.open.service.*.*(..))" />  
        <aop:advisor advice-ref="txAdvice" pointcut-ref="serviceOperation" />  
    </aop:config>  
    
   <!-- 自动扫描 -->
	<context:component-scan base-package="cn.web.open.service" />
</beans>

```
2、工程结构
(1)分层结构
![这里写图片描述](http://img.blog.csdn.net/20160409215530663)

(2)实体类

```
package cn.web.open.model;

import java.util.Date;

public class User {
	private String userCode;
	private String userName;
	private String userPwd;
	private String email;
	private String address;
	private Date userBorn;
	
	public String getUserCode() {
		return userCode;
	}
	public void setUserCode(String userCode) {
		this.userCode = userCode;
	}
	public String getUserName() {
		return userName;
	}
	public void setUserName(String userName) {
		this.userName = userName;
	}
	public String getUserPwd() {
		return userPwd;
	}
	public void setUserPwd(String userPwd) {
		this.userPwd = userPwd;
	}
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	public String getAddress() {
		return address;
	}
	public void setAddress(String address) {
		this.address = address;
	}
	public Date getUserBorn() {
		return userBorn;
	}
	public void setUserBorn(Date userBorn) {
		this.userBorn = userBorn;
	}
	
}
```

dao接口

```
package cn.web.open.dao;
import cn.web.open.model.User;

public interface UserDao {
	User findById(String code,String pwd);
}
```
service接口

```
package cn.web.open.service;
import cn.web.open.model.User;

public interface UserService {
	
	User findById(String code,String pwd);
}
```

service实现类,@Resource注入dao

```
package cn.web.open.service.impl;

import javax.annotation.Resource;
import org.springframework.stereotype.Service;
import cn.web.open.dao.UserDao;
import cn.web.open.model.User;
import cn.web.open.service.UserService;

@Service("userService")
public class UserServiceImpl implements UserService{
	@Resource
	private UserDao userDao;

	public User findById(String code,String pwd) {
		User user = userDao.findById(code,pwd);
		return user;
	}

}
```

控制器controller

```
package cn.web.open.controller;


import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import cn.web.open.model.User;
import cn.web.open.service.UserService;

@Controller
//@RequestMapping("/user")
public class UserController {
	
	@Resource
	private UserService userService;
	
	@RequestMapping("/login")
	public String login(HttpServletRequest request, Model model) {
		String code = request.getParameter("usercode");
		String pwd = request.getParameter("password");
		User user_login = userService.findById(code,pwd);
		System.out.println("--->"+user_login);
		
		if (null == user_login) {
			System.out.println("Error login!");
			return "redirect:index.jsp?oper=error";
		} else {
			model.addAttribute("user", user_login);
			return "pages/success";
		}
	}
}
```

sql语句文件mappers/userMapper.xml

```
<pre name="code" class="html"><pre name="code" class="html"><?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="cn.web.open.dao.UserDao">
	<resultMap type="User" id="UserResult">
		<result column="USER_CODE" property="userCode" />
		<result column="USER_NAME" property="userName" />
		<result column="USER_PWD" property="userPwd" />
	</resultMap>
	<!-- 查询条件:账号密码用户类型. 0第一个参数,1第二个参数,对应dao接口参数 -->
	<select id="findById" parameterType="String" resultMap="UserResult">
		SELECT USER_CODE,USER_NAME,USER_PWD FROM BLOG_USER WHERE USER_CODE=#{0} AND USER_PWD=#{1} AND USER_TYPE=2
	</select>

	<!-- 
	<select id="getAllUsers" resultMap="userResult">
		SELECT USER_CODE,USER_NAME,USER_PWD,CREATE_DATE
		FROM BLOG_USER
	</select>
	 -->
</mapper>
```
(3)前台的一些测试页面
![这里写图片描述](http://img.blog.csdn.net/20160409221836381)
WEB_INF下文件不能通过URL直接访问,登录页面网上拿了别人做了一个页面，挺有趣的，访问工程地址,端口你自己配的,输入管理员类型的账号测试
![这里写图片描述](http://img.blog.csdn.net/20160409222553125)
刚开始对于各种注解的使用不甚了解鼓捣了许久,用maven管理项目构建时也碰到许多小问题，着实查了许多资料,下过别人的demo参考，总算是把ssm这一套搭起来了，如果发现有问题，请留言指教。demo下载http://download.csdn.net/detail/u012809062/9486330