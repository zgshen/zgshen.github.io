---
title: Spring Boot 过滤器、监听器和拦截器使用
categories: 技术
tags: web框架
date: 2017-06-07
---
1、过滤器和监听器
Spring Boot中对于过滤器和监听器的使用跟一般web工程中使用方式没什么不同，使用注解方式就可以快速创建，只是要使用注解方式需要在Application类加上 `@ServletComponentScan` 注解表明开启servlet的注解
创建一个监听器<!--more-->
```java
@WebListener
public class FirstListener implements ServletContextListener{

	private static Logger LOG = LoggerFactory.getLogger(FirstListener.class);
	
	@Override
	public void contextInitialized(ServletContextEvent sce) {
		LOG.info("FirstListener 初始化...");
	}

	@Override
	public void contextDestroyed(ServletContextEvent sce) {
		LOG.info("FirstListener 销毁...");
	}

}
```

创建一个过滤器，过滤test和hello下文的所有路径
```java
@WebFilter(filterName="firstFilter", urlPatterns = {
		"/test/*",
		"/hello/*"
		})
public class FirsrtFilter implements Filter{
	
	private static Logger LOG = LoggerFactory.getLogger(FirsrtFilter.class);

	@Override
	public void init(FilterConfig filterConfig) throws ServletException {
		
	}

	@Override
	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
			throws IOException, ServletException {
		HttpServletRequest req = (HttpServletRequest) request;
		String requestURI = req.getRequestURI();
		LOG.info("过滤到的请求--->"+requestURI);
	}

	@Override
	public void destroy() {
		
	}
}
```

运行 application 类可看到日志输出
`2017-06-08 17:14:55.252  INFO 7552 --- [ost-startStop-1] com.fyft.test.web.FirstListener          : FirstListener 初始化...`

写一个请求路径为 `test` 的 controller 并访问，可看到
`2017-06-08 17:15:50.799  INFO 7552 --- [nio-8003-exec-1] com.fyft.test.web.FirsrtFilter           : 过滤到的请求--->/test`

2、拦截器

实现 `HandlerInterceptor` 接口创建一个拦截器类
```java
public class MyInterceptor implements HandlerInterceptor {

	@Override
	public void afterCompletion(HttpServletRequest arg0, HttpServletResponse arg1, Object arg2, Exception arg3)
			throws Exception {
		// TODO Auto-generated method stub
		//在整个请求结束之后被调用，也就是在DispatcherServlet 渲染了对应的视图之后执行，主要是用于进行资源清理工作
	}

	@Override
	public void postHandle(HttpServletRequest arg0, HttpServletResponse arg1, Object arg2, ModelAndView arg3)
			throws Exception {
		// TODO Auto-generated method stub
		//请求处理之后进行调用，但是在视图被渲染之前，即Controller方法调用之后
	}

	@Override
	public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object object) throws Exception {
		// TODO Auto-generated method stub
		//controller方法调用之前
		return true;
	}

}
```
然后在初始化配置类中注册拦截器
```java
@Configuration
public class MyWebAppConfigurer extends WebMvcConfigurerAdapter {

	/**
	 * 添加拦截器
	 */
	@Override
	public void addInterceptors(InterceptorRegistry registry) {
		registry.addInterceptor(new MyInterceptor()).addPathPatterns("/*");
		//registry.addInterceptor(new MyInterceptor_copy()).addPathPatterns("/*");//有多个拦截器继续add进去
		super.addInterceptors(registry);
	}

}
```
这里的拦截器只有经过DispatcherServlet 的请求，才会走拦截器链，默认不拦截静态资源，Spring Boot中默认的静态资源路径有 `classpath:/META-INF/resources/，classpath:/resources/，classpath:/static/，classpath:/public/` ，在拦截器中我们可以处理一些我们需要的业务，比如防xss攻击，在调用controller前对提交内容进行过滤等等。

参考博客 `http://blog.csdn.net/catoop/article/details/50501696`