---
title: 从 Java8 到 Java11 再到 Java17 的新特性(2)
categories: 技术
tags: 
  - 技术
  - Java
date: 2021-09-22
toc: true
---

2018年9月26日，Oracle 官方宣布Java 11 正式发布，这是自 Java8 之后 Java 大版本周期变化后的第一个长期支持版本。这篇介绍的是 Java9 到 Java11 累积的一些新特性，只涉及语法和编码上的功能，其他的如工具和虚拟机改进不涉及。

源码地址：[code-note](https://github.com/zgshen/code-note/tree/master/src/com/jdk/java9to11)

### 1. 接口

接口允许有私有方法
```java
interface Enhance {

    default void defaultMethod() {
        init();
    }

    private void init() {
        staticMethod();// or Enhance.staticMethod();
    }
    static void staticMethod() {
        System.out.println("static method in interface.");
    }

}
```

### 2. try 语句

```java
@Test
public void tryTest() {
    String path = "/home/nathan/test.sh";
    //Java7 引入的 try-with-resource 机制
    try (var reader = new InputStreamReader(System.in)) {
    } catch (IOException e) {
        e.printStackTrace();
    }

    //Java9 可以在 try 中使用已初始化的资源
    var reader = new InputStreamReader(System.in);
    var writer = new OutputStreamWriter(System.out);
    try (reader; writer) {
        //reader是final的，不可再被赋值
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

### 3. I/O 流新特性

类 `java.io.InputStream` 中增加了新的方法来读取和复制 InputStream 中包含的数据。 
- readAllBytes：读取 InputStream 中的所有剩余字节。 
- readNBytes： 从 InputStream 中读取指定数量的字节到数组中。 
- transferTo：读取 InputStream 中的全部字节并写入到指定的 OutputStream 中。

```java
@Test
public void InputStreamTest() throws IOException {
    InputStream inputStream = EnhanceExample.class.getResourceAsStream("test.txt");

    byte[] arr = new byte[5];
    inputStream.readNBytes(arr, 0, 5);
    Assert.assertEquals("Java9", new String(arr));

    byte[] allBytes = inputStream.readAllBytes();
    Assert.assertEquals("Java10Java11", new String(allBytes));

    InputStream inputStream1 = EnhanceExample.class.getResourceAsStream("test.txt");;
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
    inputStream1.transferTo(outputStream);
    Assert.assertEquals("Java9Java10Java11", outputStream.toString());
}
```

### 4. 集合、Stream 和 Optional 

在集合上，Java 9 增加 了 List.of()、Set.of()、Map.of() 和 Map.ofEntries()等工厂方法来创建不可变集合

```java
@Test
public void unmodifiableCollectionTest() {
    List<Integer> integers = List.of(1, 2, 3);
    Set<String> strings = Set.of("a", "b", "c");
    Map<String, Integer> stringIntegerMap = Map.of("a", 1, "b", 2, "c", 3);
}
```

Stream 中增加了新的方法 ofNullable、dropWhile、takeWhile 和 iterate；Collectors 中增加了新的方法 filtering 和 flatMapping。
```java
@Test
public void streamTest() {
    List<Integer> list = Arrays.asList(1, 2, 4, 5, 3, 2, 8);
    //输出1，2，4，碰到5不成立停止
    list.stream().takeWhile(x -> x < 5).forEach(System.out::println);

    //丢弃1，2，碰到3不成立停止
    List<Integer> collect = Stream.of(1, 2, 3, 4, 5).dropWhile(i -> i%3!=0).collect(Collectors.toList());
    System.out.println(collect);

    //允许值为空
    Stream<Object> stream = Stream.ofNullable(null);

    //Optional 转 stream
    long count = Stream.of(
            Optional.of(1),
            Optional.empty(),
            Optional.of(2)).flatMap(Optional::stream).count();
    Assert.assertEquals(2, count);

    //空值throw
    Optional.empty().orElseThrow();
}
```

Stream 还提供一个 Predicate (判断条件)来指定什么时候结束迭代。
```java
@Test
public void iterateTest() {
    Stream.iterate(1, i -> ++i).limit(5).forEach(System.out::println);
    //可以直接在 iterate 内部判断
    Stream.iterate(1, i -> i <= 5, i -> ++i).forEach(System.out::println);
}
```


### 5. 变量类型推断

Java10 开始变量不需要写具体类型，编译器能根据右边的表达式自动推断类型
```java
@Test
public void var() {
    String str1 = "abc";
    var str2 = "abc";
    Assert.assertEquals(str1, str2);
}
```

对象引用也可以使用
```java
@Test
public void collection() {
    //相当于 Object 用
    var list = new ArrayList<>();
    list.add(123);
    list.add("abc");

    // 表示对象引用，类名很长的情况能简化代码编写
    var v = new VariableTest();
    System.out.println(v.getClass().getName());

    Runnable runnable = () -> System.out.println("interface var");
    // 无法表示接口引用，毕竟匿名类方式无法推断是哪个类的实现
    //var r = () -> System.out.println("interface var");
}
```

### 6. HTTP 客户端

Java 11 对 Java 9 中引入并在 Java 10 中进行了更新的 Http Client API 进行了标准化，Java 11 中的新 Http Client API，提供了对 HTTP/2 等业界前沿标准的支持，同时也向下兼容 HTTP/1.1，精简而又友好的 API 接口，与主流开源 API（如：Apache HttpClient、Jetty、OkHttp 等）类似甚至拥有更高的性能。

```java
import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.net.*;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class HttpClientExample {

    HttpClient client;

    @Before
    public void init() {
        client = HttpClient.newBuilder().connectTimeout(Duration.ofMillis(20000L)).build();
    }

    @Test
    public void reqTest() throws IOException, InterruptedException {
        var request = HttpRequest.newBuilder(URI.create("https://zguishen.com/")).build();
        /**
         * {@link jdk.internal.net.http.HttpRequestImpl#HttpRequestImpl(java.net.http.HttpRequest, java.net.ProxySelector)} 109
         * 没有指定协议默认是 GET
         */
        String body = client.send(request, HttpResponse.BodyHandlers.ofString()).body();
        System.out.println(body);
    }

    @Test
    public void getTest() {
        var request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.github.com/users/zgshen"))
                .header("Accept", "application/vnd.github.v3+json")
                //.header("Cookie", cookie)
                .timeout(Duration.ofSeconds(10000L))
                .GET()
                .build();
        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .whenCompleteAsync((res, exp) -> {
                    System.out.println(res.body());
                }).join();
    }

    @Test
    public void postTest() {
        var requestBody = "{'key':'val'}";
        var request = HttpRequest.newBuilder()
                .uri(URI.create("http://example.com/json"))
                .header("Contend-Type","application/json")
                .timeout(Duration.ofSeconds(10000L))
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();
        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .whenCompleteAsync((res, exp) -> {
                    System.out.println(res.body());
                }).join();
    }

    @Test
    public void Http2Test() throws URISyntaxException {
        HttpClient.newBuilder()
                .followRedirects(HttpClient.Redirect.NEVER)
                .version(HttpClient.Version.HTTP_2)
                .build()
                .sendAsync(HttpRequest.newBuilder()
                                .uri(new URI("https://zguishen.com/"))
                                .GET()
                                .build(),
                        HttpResponse.BodyHandlers.ofString())
                .whenComplete((resp, t) -> {
                    if (t != null) {
                        t.printStackTrace();
                    } else {
                        System.out.println(resp.version());
                        System.out.println(resp.statusCode());
                    }
                }).join();
    }
}
```

### 7. 参考
- [1] [A categorized list of all Java and JVM features since JDK 8 to 17](https://advancedweb.hu/a-categorized-list-of-all-java-and-jvm-features-since-jdk-8-to-17/)
- [2] [Java 全栈知识体系](https://pdai.tech/md/java/java8up/java11.html)
- [3] [Java11 HttpClient小试牛刀](https://juejin.cn/post/6844903685563088903)