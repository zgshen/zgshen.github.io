---
title: SSM框架，基于JavaConfig配置方式，不用xml配置文件
categories: 技术
tags: web框架
date: 2017-06-14
---
在使用Spring开发时，我们经常会看到各种各样xml配置，过于繁多的xml配置显得复杂烦人。在Spring3之后，Spring支持使用JavaConfig来代替xml配置，这种方式也得到越来越多人的推荐，甚至在Spring Boot的项目中，基本上已经见不到xml的影子了。这里将使用JavaConfig方式对SSM框架进行整合。
<!--more-->
一、maven 的pom.xml配置
各种jar包的配置如下
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.open.ssm</groupId>
  <artifactId>ssm-demo</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <packaging>war</packaging>
  
  	
  	<!-- 版本 -->
	<properties>
		<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
		<junit.version>4.12</junit.version>
		<spring.version>4.3.0.RELEASE</spring.version>
		<jackson.version>2.5.0</jackson.version>
		<mysql-connector-java.version>5.1.37</mysql-connector-java.version>
		<fastjson.version>1.2.3</fastjson.version>
		<slf4j.version>1.7.12</slf4j.version>
		<commons-io.version>2.4</commons-io.version>
		<commons-fileupload.version>1.3.2</commons-fileupload.version>
		<commons-collections.version>3.2.2</commons-collections.version>
		<commons-lang3.version>3.3.2</commons-lang3.version>
		<commons-codec.version>1.10</commons-codec.version>
		<javax.servlet-api.version>3.1.0</javax.servlet-api.version>
		<druid.version>1.0.16</druid.version>
		<mybatis.version>3.4.0</mybatis.version>
		<mybatis-spring.version>1.3.0</mybatis-spring.version>
	</properties>
	
	<!-- 依赖管理 -->
    <dependencies>
   	
	   	<!-- 单元测试 -->
		<dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<version>${junit.version}</version>
			<scope>test</scope>
		</dependency>
		
		<!-- json -->
		<dependency>
			<groupId>com.alibaba</groupId>
			<artifactId>fastjson</artifactId>
			<version>${fastjson.version}</version>
		</dependency>
		
		<!-- spring -->
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-core</artifactId>
			<version>${spring.version}</version>
		</dependency>

		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-beans</artifactId>
			<version>${spring.version}</version>
		</dependency>

		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-context</artifactId>
			<version>${spring.version}</version>
		</dependency>

		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-tx</artifactId>
			<version>${spring.version}</version>
		</dependency>

		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-web</artifactId>
			<version>${spring.version}</version>
		</dependency>

		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-webmvc</artifactId>
			<version>${spring.version}</version>
		</dependency>

		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-jdbc</artifactId>
			<version>${spring.version}</version>
		</dependency>

		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-test</artifactId>
			<version>${spring.version}</version>
			<scope>test</scope>
		</dependency>
		
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-aspects</artifactId>
			<version>${spring.version}</version>
		</dependency>
		
		<dependency>
			<groupId>com.fasterxml.jackson.core</groupId>
			<artifactId>jackson-annotations</artifactId>
			<version>${jackson.version}</version>
		</dependency>

		<dependency>
			<groupId>com.fasterxml.jackson.core</groupId>
			<artifactId>jackson-core</artifactId>
			<version>${jackson.version}</version>
		</dependency>

		<dependency>
			<groupId>com.fasterxml.jackson.core</groupId>
			<artifactId>jackson-databind</artifactId>
			<version>${jackson.version}</version>
		</dependency>
		
		<!-- jdbc驱动包  -->
		<dependency>
			<groupId>mysql</groupId>
			<artifactId>mysql-connector-java</artifactId>
			<version>${mysql-connector-java.version}</version>
		</dependency>
		
		<!--common 组件 -->
		<dependency>
			<groupId>commons-io</groupId>
			<artifactId>commons-io</artifactId>
			<version>${commons-io.version}</version>
		</dependency>

		<dependency>
			<groupId>commons-fileupload</groupId>
			<artifactId>commons-fileupload</artifactId>
			<version>${commons-fileupload.version}</version>
		</dependency>
		
		<dependency>
			<groupId>commons-collections</groupId>
			<artifactId>commons-collections</artifactId>
			<version>${commons-collections.version}</version>
		</dependency>
		
		<dependency>
			<groupId>org.apache.commons</groupId>
			<artifactId>commons-lang3</artifactId>
			<version>${commons-lang3.version}</version>
		</dependency>
		
		<dependency>
		    <groupId>commons-codec</groupId>
		    <artifactId>commons-codec</artifactId>
		    <version>${commons-codec.version}</version>
		</dependency>
		
		<!-- 日志处理 -->
		<dependency>
			<groupId>org.slf4j</groupId>
			<artifactId>slf4j-log4j12</artifactId>
			<version>${slf4j.version}</version>
		</dependency>
		
		<!-- servlet -->
		<!-- javax.servlet相关 -->
		<dependency>
			<groupId>javax.servlet</groupId>
			<artifactId>javax.servlet-api</artifactId>
			<version>${javax.servlet-api.version}</version>
			<scope>provided</scope>
		</dependency>

		<dependency>
			<groupId>javax.servlet</groupId>
			<artifactId>jstl</artifactId>
			<version>1.2</version>
		</dependency>
		
		<dependency>
			<groupId>com.alibaba</groupId>
			<artifactId>druid</artifactId>
			<version>${druid.version}</version>
		</dependency>
		
		<dependency>
			<groupId>org.mybatis</groupId>
			<artifactId>mybatis</artifactId>
			<version>${mybatis.version}</version>
		</dependency>
		
		<dependency>
			<groupId>org.mybatis</groupId>
			<artifactId>mybatis-spring</artifactId>
			<version>${mybatis-spring.version}</version>
		</dependency>
		
  	</dependencies>
  	
	<build>
		<finalName>ssm-demo</finalName>
		<plugins>
			
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-war-plugin</artifactId>
				<version>2.5</version>
				<configuration>
					<failOnMissingWebXml>false</failOnMissingWebXml>
				</configuration>
			</plugin>
			<plugin>
				<groupId>org.apache.tomcat.maven</groupId>
				<artifactId>tomcat7-maven-plugin</artifactId>
				<configuration>
					<port>8088</port>
					<path>/</path>
				</configuration>
			</plugin>
			
		</plugins>
	</build>
</project>
```

二、SpringMvc的配置
首先创建一个初始化类，继承 `AbstractAnnotationConfigDispatcherServletInitializer` 

```java
package com.open.ssm.config;
import org.apache.log4j.Logger;
import org.springframework.web.servlet.support.AbstractAnnotationConfigDispatcherServletInitializer;
/**
 *<p>Title: SpittrWebAppInitializer.java</p>
 *<p>Description: 前端控制器配置</p>
 *<p>CreateDate: 2017年6月12日</p>
 *@author shen
 *@version v1.0
 */
public class WebAppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {

	private final static Logger LOG = Logger.getLogger(WebAppInitializer.class);
	
	@Override
	protected Class<?>[] getRootConfigClasses() {
		LOG.info("------root配置类初始化------");
		return new Class<?>[] { RootConfig.class };
	}

	@Override
	protected Class<?>[] getServletConfigClasses() {
		LOG.info("------web配置类初始化------");
		return new Class<?>[] { WebConfig.class };
	}

	@Override
	protected String[] getServletMappings() {
		LOG.info("------映射根路径初始化------");
		return new String[]{ "/" };//请求路径映射，根路径
	}
}
```
这里需要实现三个方法，可以其中两个方法看到需要两个配置类 `RootConfig` 和 `WebConfig` , `getServletMappings` 方法处理路径映射到 “/”，表示默认的Servlet，会处理进入应用的所有请求。

其中 `WebConfig` 用于定义 `DispatcherServlet` 加载应用上下文的配置，主要包含一些web组件

```java
package com.open.ssm.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.multipart.commons.CommonsMultipartResolver;
import org.springframework.web.servlet.ViewResolver;
import org.springframework.web.servlet.config.annotation.DefaultServletHandlerConfigurer;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;
import org.springframework.web.servlet.view.InternalResourceViewResolver;

/**
 *<p>Title: WebConfig.java</p>
 *<p>Description: 配置类，用于定义DispatcherServlet上下文的bean</p>
 *<p>CreateDate: 2017年6月12日</p>
 *@author shen
 *@version v1.0
 */
@Configuration
@EnableWebMvc
@ComponentScan( "com.open.ssm.controller" )
public class WebConfig extends WebMvcConfigurerAdapter {
	
	@Bean
	public ViewResolver viewResolver(){
		InternalResourceViewResolver resolver = new InternalResourceViewResolver();
		resolver.setPrefix("/WEB-INF/view/");
		resolver.setSuffix(".jsp");
		return resolver;
	}
	
	//文件上传，bean必须写name属性且必须为multipartResolver，不然取不到文件对象，别问我为什么，我也唔知
	@Bean(name="multipartResolver")
	protected CommonsMultipartResolver MultipartResolver() {
		CommonsMultipartResolver multipartResolver = new CommonsMultipartResolver();
		//multipartResolver.setUploadTempDir(new FileSystemResource("/tmp"));//可不设置
		multipartResolver.setMaxUploadSize(2097152);//2M
		multipartResolver.setMaxInMemorySize(0);
		multipartResolver.setDefaultEncoding("UTF-8");
		return multipartResolver;
	}
	
   //静态资源的处理
   @Override
   public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
   }
}

```

而 `RootConfig` 类主要配置持久层的一些东西，包括数据库、Mybatis框架，事务之类的东西。
```java
package com.open.ssm.config;
import org.springframework.aop.framework.autoproxy.BeanNameAutoProxyCreator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

/**
 *<p>Title: RootConfig.java</p>
 *<p>Description: 配置类，用于管理ContextLoadListener创建的上下文的bean</p>
 *<p>CreateDate: 2017年6月12日</p>
 *@author shen
 *@version v1.0
 */
@Configuration
@ComponentScan(basePackages={ "com.open.ssm.config", "com.open.ssm.dao", "com.open.ssm.service" })
@Import(DruidDataSourceConfig.class)
public class RootConfig {
	
	@Bean
	public BeanNameAutoProxyCreator proxycreate(){
    	BeanNameAutoProxyCreator proxycreate = new BeanNameAutoProxyCreator();
    	proxycreate.setProxyTargetClass(true);
    	proxycreate.setBeanNames("*ServiceImpl");
    	proxycreate.setInterceptorNames("transactionInterceptor");
    	return proxycreate;
    }	
}
```

三、数据库与Mybatis相关配置
这里的数据源使用的是阿里的Druid，接上面 `RootConfig` 类，可以看到 `RootConfig` 类又 import 导入了一个配置类 `DruidDataSourceConfig`
```java
package com.open.ssm.config;

import java.io.IOException;
import java.sql.SQLException;
import java.util.Properties;

import javax.sql.DataSource;

import org.apache.log4j.Logger;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.core.io.support.ResourcePatternResolver;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.transaction.interceptor.TransactionInterceptor;

import com.alibaba.druid.pool.DruidDataSource;

/**
 *<p>Title: DruidDataSourceConfig.java</p>
 *<p>Description: 数据源属性配置</p>
 *<p>CreateDate: 2017年6月12日</p>
 *@author shen
 *@version v1.0
 */
@Configuration
@PropertySource("classpath:/jdbc.properties")
@MapperScan(basePackages="com.open.ssm.dao")
public class DruidDataSourceConfig{
	
	private final static Logger LOG = Logger.getLogger(DruidDataSourceConfig.class);
	
	@Value("${spring.datasource.url}")  
    private String dbUrl;  
      
    @Value("${spring.datasource.username}")  
    private String username;  
      
    @Value("${spring.datasource.password}")  
    private String password;  
      
    @Value("${spring.datasource.driverClassName}")  
    private String driverClassName;  
      
    @Value("${spring.datasource.initialSize}")  
    private int initialSize;  
      
    @Value("${spring.datasource.minIdle}")  
    private int minIdle;  
      
    @Value("${spring.datasource.maxActive}")  
    private int maxActive;  
      
    @Value("${spring.datasource.maxWait}")  
    private int maxWait;  
      
    @Value("${spring.datasource.timeBetweenEvictionRunsMillis}")  
    private int timeBetweenEvictionRunsMillis;  
      
    @Value("${spring.datasource.minEvictableIdleTimeMillis}")  
    private int minEvictableIdleTimeMillis;  
      
    @Value("${spring.datasource.validationQuery}")  
    private String validationQuery;  
      
    @Value("${spring.datasource.testWhileIdle}")  
    private boolean testWhileIdle;  
      
    @Value("${spring.datasource.testOnBorrow}")  
    private boolean testOnBorrow;  
      
    @Value("${spring.datasource.testOnReturn}")  
    private boolean testOnReturn;  
      
    @Value("${spring.datasource.poolPreparedStatements}")  
    private boolean poolPreparedStatements;  
      
    @Value("${spring.datasource.maxPoolPreparedStatementPerConnectionSize}")  
    private int maxPoolPreparedStatementPerConnectionSize;  
      
    @Value("${spring.datasource.filters}")  
    private String filters;  
      
    @Value("{spring.datasource.connectionProperties}")  
    private String connectionProperties;  
      
    @Bean     //声明其为Bean实例  
    public DataSource dataSource(){
    	LOG.info("Initialize the data source...");
        DruidDataSource datasource = new DruidDataSource();  
          
        datasource.setUrl(this.dbUrl);  
        datasource.setUsername(username);  
        datasource.setPassword(password);  
        datasource.setDriverClassName(driverClassName);  
          
        //configuration  
        datasource.setInitialSize(initialSize);  
        datasource.setMinIdle(minIdle);  
        datasource.setMaxActive(maxActive);  
        datasource.setMaxWait(maxWait);  
        datasource.setTimeBetweenEvictionRunsMillis(timeBetweenEvictionRunsMillis);  
        datasource.setMinEvictableIdleTimeMillis(minEvictableIdleTimeMillis);  
        datasource.setValidationQuery(validationQuery);  
        datasource.setTestWhileIdle(testWhileIdle);  
        datasource.setTestOnBorrow(testOnBorrow);  
        datasource.setTestOnReturn(testOnReturn);  
        datasource.setPoolPreparedStatements(poolPreparedStatements);  
        datasource.setMaxPoolPreparedStatementPerConnectionSize(maxPoolPreparedStatementPerConnectionSize);  
        try {  
            datasource.setFilters(filters);  
        } catch (SQLException e) {  
        	LOG.error("druid configuration initialization filter", e);  
        }  
        datasource.setConnectionProperties(connectionProperties);  
        return datasource;  
    }
    
    /*
    //JdbcTemplate的配置
    @Bean
    public JdbcTemplate jdbcTemplate(){
    	JdbcTemplate jdbcTemplate = new JdbcTemplate();
    	jdbcTemplate.setDataSource(dataSource());
    	return jdbcTemplate;
    }
    
    @Bean
    public NamedParameterJdbcTemplate namedParameterJdbcTemplate(){
    	NamedParameterJdbcTemplate namedParameterJdbcTemplate = new NamedParameterJdbcTemplate(dataSource());
    	return namedParameterJdbcTemplate;
    }*/
    
    //mybatis的配置
    @Bean
    public SqlSessionFactoryBean sqlSessionFactoryBean() throws IOException{
    	ResourcePatternResolver resourcePatternResolver = new PathMatchingResourcePatternResolver();  
        SqlSessionFactoryBean sqlSessionFactoryBean = new SqlSessionFactoryBean();  
        sqlSessionFactoryBean.setDataSource(dataSource());  
        sqlSessionFactoryBean.setMapperLocations(resourcePatternResolver.getResources("classpath*:mappers/*.xml"));
        sqlSessionFactoryBean.setTypeAliasesPackage("com.open.ssm.model");//别名，让*Mpper.xml实体类映射可以不加上具体包名
        return sqlSessionFactoryBean;
    }
    
    @Bean(name = "transactionManager")
    public DataSourceTransactionManager dataSourceTransactionManager(){
    	DataSourceTransactionManager dataSourceTransactionManager = new DataSourceTransactionManager();
    	dataSourceTransactionManager.setDataSource(dataSource());
    	return dataSourceTransactionManager;
    }
    
    @Bean(name="transactionInterceptor")
    public TransactionInterceptor interceptor(){
    	TransactionInterceptor interceptor = new TransactionInterceptor();
    	interceptor.setTransactionManager(dataSourceTransactionManager());
    	
    	Properties transactionAttributes = new Properties();
    	transactionAttributes.setProperty("save*", "PROPAGATION_REQUIRED");
    	transactionAttributes.setProperty("del*", "PROPAGATION_REQUIRED");
    	transactionAttributes.setProperty("update*", "PROPAGATION_REQUIRED");
    	transactionAttributes.setProperty("get*", "PROPAGATION_REQUIRED,readOnly");
    	transactionAttributes.setProperty("find*", "PROPAGATION_REQUIRED,readOnly");
    	transactionAttributes.setProperty("*", "PROPAGATION_REQUIRED");
    	
    	interceptor.setTransactionAttributes(transactionAttributes);
    	return interceptor;
    }
    
    /*
    //放这里会导致@value注解获取不到配置的值，移到RootConfig
    @Bean
    public BeanNameAutoProxyCreator proxycreate(){
    	BeanNameAutoProxyCreator proxycreate = new BeanNameAutoProxyCreator();
    	proxycreate.setProxyTargetClass(true);
    	proxycreate.setBeanNames("*ServiceImpl");
    	proxycreate.setInterceptorNames("transactionInterceptor");
    	return proxycreate;
    }*/
    
}
```
数据库连接信息文件 jdbc.properties 相关内容
```xml

spring.datasource.type=com.alibaba.druid.pool.DruidDataSource
spring.datasource.driverClassName=com.mysql.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/blog
spring.datasource.username=root
spring.datasource.password=root

#连接池配置
spring.datasource.initialSize=5
spring.datasource.minIdle=5
spring.datasource.maxActive=20
#连接等待超时时间
spring.datasource.maxWait=60000
#配置隔多久进行一次检测(检测可以关闭的空闲连接)
spring.datasource.timeBetweenEvictionRunsMillis=60000
#配置连接在池中的最小生存时间
spring.datasource.minEvictableIdleTimeMillis=300000
spring.datasource.validationQuery=SELECT 1 FROM DUAL
spring.datasource.testWhileIdle=true
spring.datasource.testOnBorrow=false
spring.datasource.testOnReturn=false
# 打开PSCache，并且指定每个连接上PSCache的大小
spring.datasource.poolPreparedStatements=true
spring.datasource.maxPoolPreparedStatementPerConnectionSize=20
# 配置监控统计拦截的filters，去掉后监控界面sql无法统计，'wall'用于防火墙
spring.datasource.filters=stat,wall,log4j
# 通过connectProperties属性来打开mergeSql功能；慢SQL记录
spring.datasource.connectionProperties=druid.stat.mergeSql=true;druid.stat.slowSqlMillis=5000

```

这里数据库的事务配置方式有三种：

*  第一种最简单的方式，在 `RootConfig` 加上 @EnableTransactionManagement 注解，再加上配置 DataSourceTransactionManager 的bean，就可以在service实现层使用 @Transactional 注解为方法手动加上事务，并且指定的传播属性等等，但老是要手动加 @Transactional 注解实在麻烦
*  第二种就是文中使用的方式，使用 `BeanNameAutoProxyCreator` 拦截代理方式，先创建一个 `TransactionInterceptor` bean，配置好事务传播等属性，在由 `BeanNameAutoProxyCreator` 进行事务代理。这里有个问题就是 `BeanNameAutoProxyCreator` 放在 `RootConfig` 中居然会导致 @value注解获取不到配置文件的值，而是键名字，将它直接放到 `RootConfig` 下就没事了
*  第三种是采用aop切面事务， @EnableAspectJAutoProxy 开启切面自动代理，这里写一个切面相关类 `AspectConfig` ，然后在 使用 @Import(AspectConfig.class) 导进配置就行，由于 `<tx:` 开头的这种标签实在不知如何用java方式表示，在 stackoverflow 看到一个答案讲还是只能写一个xml文件，使用 @ImportResource("classpath:/aop-config.xml") 这种方式进行配置，具体实现如下(三种方式根据需要去掉无关代码，免得出冲突)

```java
package com.open.ssm.config;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.context.annotation.ImportResource;
import org.springframework.stereotype.Component;
/**
 *<p>Title: AspectConfig.java</p>
 *<p>Description: 切面事务</p>
 *<p>CreateDate: 2017年6月12日</p>
 *@author shen
 *@version v1.0
 */
@Aspect
@Component
@ImportResource("classpath:/aop-config.xml")
public class AspectConfig {
	
	@Pointcut("execution(* com.open.ssm.service.*.*(..))")
	public void serviceAnnotatedClass() {
	}
	
}
```
四、Druid监控
Druid监控这里使用最简单的方式，就一个servlet和一个filter
servlet 继承自 StatViewServlet
```java
package com.open.ssm.web;
import javax.servlet.annotation.WebInitParam;
import javax.servlet.annotation.WebServlet;
import com.alibaba.druid.support.http.StatViewServlet;
/**
 *<p>Title: DruidServlMonitor.java</p>
 *<p>Description: Druid Servlet</p>
 *<p>CreateDate: 2017年6月14日</p>
 *@author shen
 *@version v1.0
 */
@WebServlet(name="druidMonitor", urlPatterns="/druid/*", initParams={
		@WebInitParam(name="allow", value="127.0.0.1"),
		@WebInitParam(name="loginUsername", value="admin"),
		@WebInitParam(name="loginPassword", value="123123"),
		@WebInitParam(name="resetEnable", value="false")
})
public class DruidServletMonitor extends StatViewServlet{

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
}
```

filter继承自 WebStatFilter 
```java
package com.open.ssm.web;
import javax.servlet.annotation.WebFilter;
import javax.servlet.annotation.WebInitParam;
import com.alibaba.druid.support.http.WebStatFilter;

/**
 * Servlet Filter implementation class DruidStatFilter
 */
@WebFilter(filterName="druidFilter", urlPatterns="/*", initParams={
		@WebInitParam(name="exclusions", value="*.js,*.gif,*.jpg,*.png,*.css,*.ico,/druid/*")
})
public class DruidStatFilter extends WebStatFilter {


}
```
浏览器直接输入ip+端口/druid，这里在本地是 http://localhost:8088/druid 进入登录页面，输入配置的用户名密码就可以进入监控页面了。

本文我写了一个demo，放在 https://github.com/zgshen/ssm-demo ，后续有时间会加上其他的一些东西。
