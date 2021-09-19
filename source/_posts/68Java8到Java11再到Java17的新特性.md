---
title: 从 Java8 到 Java11 再到 Java17 的新特性(1)
categories: 技术
tags: 
  - 技术
  - Java
date: 2021-09-19
---

在 2021年9月15日，Java 社区正式发布了 Java17，从 JDK8 之后，Java 的更新策略改为以时间驱动的方式。一般如果要对旧 JDK 进行升级，都会选择长期支持版，JDK11 和最近更新的 JDK17 是长期支持版本。但是，由于更新 JDK 带来的收益不大，商业项目更看重稳定性，大多数人不愿意踩坑，“又不是不能用”，干嘛要更新。因此，不少开发者都没有接触到新 JDK 的新特性，甚至有些在用 JDK8 的人连 JDK8 的新特性都用不利索或者直接旧不知道。接下来我将分三篇文章分别介绍 JDK8、JDk11 和 JDK17 常用或者有用的新功能。

先从 Java8 开始说起。

### 1. Lambda 表达式

Lambda 允许把函数作为一个方法的参数（函数作为参数传递进方法中），让匿名内部类的写法更简便。

测试类例子

```java
/**
 * 测试类
 */
public class LambdaTest {

    public LambdaTest() {
    }
    public LambdaTest(String str) {
        //use param str to do something
    }

    public static void interfaceTest(SingleFncInterface singleFunInterface) {
        singleFunInterface.doSomething("123");
    }

    public void simpleMenthod(String str) {
        System.out.println("simple method. str is:");
    }

    public static void staticMenthod(String str) {
        System.out.println("static menthod. str is:");
    }
}
/**
 * 单函数接口
 */
@FunctionalInterface
interface SingleFncInterface {
    void doSomething(String str);

    default void print() {
        System.out.println("default method.");
    }
}
```

`SingleFncInterface` 是一个典型的函数式接口，只包含一个抽象方法，可以加上 `@FunctionalInterface` 注解标记，限制只允许定义一个抽象方法。

```java
/**
 * Lambda 本质就是单函数接口
 */
@Test
public void singleFunTest() {
    //作为参数的形式
    LambdaTest.interfaceTest((String str) -> {
        System.out.println("single function interface. param:" + str);
    });

    //SingleFncInterface s = (String str) -> System.out.println(str);
		SingleFncInterface s = str -> System.out.println(str);
    s.doSomething("123");

    //简化形式，方法引用
    //LambdaTest.interfaceTest(item -> System.out.println(item));
    LambdaTest.interfaceTest(System.out::println);
}
```

lambda 表达式的语法格式如：(parameters) -> expression/statements，特殊的还有更加简化的方法引用的类型。
方法引用可分为三种，静态、实例和构造引用，使用例子如下：

```java
/**
 * 方法引用
 */
@Test
public void refTest() {
    //静态引用。意思就是用 String 的 valof() 方法来实现 Function 接口的 apply 方法
    Function<Integer, String> fun = String::valueOf;
    String apply = fun.apply(100);
    System.out.println(apply);

    //静态引用
    SingleFncInterface sfi1 = LambdaTest::staticMenthod;

    //实例引用
    LambdaTest lambdaTest = new LambdaTest();
    SingleFncInterface sfi2 = lambdaTest::simpleMenthod;

    //构造引用，带参数
    SingleFncInterface sfi3 = LambdaTest::new;

    //构造引用，不带参数
    Runnable runnable = LambdaTest::new;
    //runnable.run();//单函数 Runnable 接口 run 方法由 LambdaTest 构造实现
}
```

在 JDK 中提供了四种类型的函数式接口：

```java
/**
 * 四种类型函数式接口
 */
@Test
public void funTest() {
    /**
     * Function<T, R>
     * 调用方法 R apply(T t);
     * T：入参类型，R：出参类型
     */
    Function<Integer, Integer> function = n -> n*n;
    Integer apply = function.apply(10);
    System.out.println(apply);

    /**
     * Consumer<T>
     * 调用方法：void accept(T t);
     * T：入参类型；没有出参
     */
    Consumer<String> consumer = System.out::println;
    consumer.accept("output msg.");

    /**
     * Supplier<T>
     * 调用方法：T get();
     * T：出参类型；没有入参
     */
    Supplier<Integer> supplier = () -> 10*10;
    Integer integer = supplier.get();
    System.out.println(integer);

    /**
     * Predicate<T>
     * 调用方法：boolean test(T t);
     * T：入参类型；出参类型是Boolean
     */
    Predicate<Integer> predicate = num -> num>10;//是否大于10
    boolean test = predicate.test(20);
    System.out.println(test);
}
```

### 2. 接口默认方法

Java8 允许在接口中添加一个或者多个默认方法，在 `SingleFncInterface` 接口中 `print()` 就是一个默认方法。增加默认方法是为了给家口添加新方法的同时不影响已有的实现，不需要修改全部实现类。

```java
@FunctionalInterface
interface SingleFncInterface {
    void doSomething(String str);

    default void print() {
        System.out.println("default method.");
    }
}
```

### 3. Optional 类

在 Java8 之前，空指针异常是编码最需要注意的异常，我们往往都需要手动编码对变量进行 null 判断，对可能的空指针异常进行捕获处理。Java8 提供的 Optional 类以比较优雅的方式进行空值判断，解决空指针异常。

```java
import org.junit.Before;
import org.junit.Test;

import java.util.Optional;

public class OptionalExample {

    private Person person;
    private Car car;
    private Insurance insurance;

    @Before
    public void init() {
        insurance = new Insurance("Tesla");
        car = new Car(Optional.of(insurance));
        person = new Person(Optional.of(car));
    }

    @Test
    public void test1() {
        //允许传递为 null 的参数
        Optional<Insurance> insurance = Optional.ofNullable(this.insurance);
        Optional<String> s = insurance.map(insurance1 -> insurance1.getName());
        System.out.println(s);
    }

    @Test
    public void test2() {
        Optional<Person> person = Optional.of(this.person);
        String name = person.flatMap(Person::getCar)
                .flatMap(Car::getInsurance)//拿到封装的 Optional<Car>
                .map(Insurance::getName)//直接拿到值
                .orElse("ubknow");
        System.out.println(name);
    }

    @Test
    public void test3() {
        Optional<Car> c = Optional.empty();
        Optional<String> s = c.flatMap(Car::getInsurance)
                .map(Insurance::getName);
        System.out.println(s);
        String unknow = s.orElse("unknow");
        System.out.println(unknow);
    }

}

class Person {
    private Optional<Car> car;

    public Person(Optional<Car> car) {
        this.car = car;
    }
    public Optional<Car> getCar() {
        return car;
    }
}

class Car {
    private Optional<Insurance> insurance;

    public Car(Optional<Insurance> insurance) {
        this.insurance = insurance;
    }
    public Optional<Insurance> getInsurance() {
        return insurance;
    }
}

class Insurance {
    private String name;

    public Insurance(String name) {
        this.name = name;
    }
    public String getName() {
        return name;
    }
}
```

```java
Optional<Insurance> insurance = Optional.of(this.insurance)
// this.insurance 为 null 返回 Optional.empty
Optional<Insurance> insurance = Optional.ofNullable(this.insurance)
```
简单来说，如果想得到一个非 null 值的 Optional 使用 `Optional.of`允许 null 值的话使用 `Optional.ofNullable`;

```java
String name = person.flatMap(Person::getCar)
                .flatMap(Car::getInsurance)
                .map(Insurance::getName)
                .orElse("unknown");
```
对于返回一个 `Optional` 结果集需要使用 `flatMap`，比如 `Person::getCar` 方法和 `Car::getInsurance`，只要单一转换的使用 `map`，例如 `Insurance::getName`，如果是 empty 返回 orElse 的内容。

### 4. Stream 流处理

流 Stream 通过声明的方式来处理数据，可以在管道的节点上对数据进行排序、聚合、筛选、去重和截取等等操作。

```java
import org.junit.Test;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.IntSummaryStatistics;
import java.util.List;
import java.util.stream.Collectors;

public class StreamExample {

    List<Fruit> fruits = new ArrayList<>(Arrays.asList(
            new Fruit("apple"),
            new Fruit("banana"),
            new Fruit("orange")
    ));

    /**
     * 遍历
     */
    @Test
    public void outputTest() {
        List<Integer> integers = Arrays.asList(1, 2, 3, 4, 5);

        integers.forEach(System.out::print);
        System.out.println();
        integers.stream().forEach(System.out::print);
        System.out.println();
        //并行流底层使用Fork/Join框架实现，异步处理，输出不一定是12345
        integers.parallelStream().forEach(System.out::print);
        System.out.println();

    }

    /**
     * 映射
     */
    @Test
    public void mapTest() {
        List<Integer> integers = Arrays.asList(1, 2, 3, 4, 5);
        //映射每个元素操作，生成新的结果
        List<Integer> collect = integers.stream().map(n -> n * n).collect(Collectors.toList());
        System.out.println(collect);

        List<String> fruitList = fruits.stream().map(obj -> obj.name="I like ".concat(obj.name)).collect(Collectors.toList());
        System.out.println(fruitList);
    }

    /**
     * 排序、过滤、限制
     */
    @Test
    public void filterTest() {
        List<Integer> integers = Arrays.asList(2, 3, 1, 4, 8, 5, 9, 5);
        List<Integer> collect = integers.stream()
                //.sorted()//排序
                .sorted((x, y) -> y - x)
                .distinct()//去重
                .filter(n -> n < 6)//小于6的数
                .limit(3)//只截取3个元素
                .collect(Collectors.toList());
        System.out.println(collect);
    }

    /**
     * 聚合和统计
     */
    @Test
    public void mergeTest() {
        List<String> strings = Arrays.asList("Hello", " ", "world", "!");
        String collect = strings.stream().collect(Collectors.joining(""));
        System.out.println(collect);

        List<Integer> numbers = Arrays.asList(3, 2, 2, 3, 7, 3, 5);
        IntSummaryStatistics stats = numbers.stream().mapToInt((x) -> x).summaryStatistics();

        System.out.println("列表中最大的数 : " + stats.getMax());
        System.out.println("列表中最小的数 : " + stats.getMin());
        System.out.println("所有数之和 : " + stats.getSum());
        System.out.println("平均数 : " + stats.getAverage());
    }

}

class Fruit {
    public Fruit(String name) {
        this.name = name;
    }
    String name;

    public void setName(String name) {
        this.name = name;
    }
}
```

### 4.  Base64 工具

Java 8 内置了 Base64 编码的编码器和解码器，支持三种编解码方式。

```java
import org.junit.Test;
import java.io.UnsupportedEncodingException;
import java.util.Base64;

public class Base64Example {
    @Test
    public void test() throws UnsupportedEncodingException {
        //基本
        String s1 = Base64.getEncoder().encodeToString("base64test".getBytes("utf-8"));
        System.out.println(s1);
        System.out.println(new String(Base64.getDecoder().decode(s1), "utf-8"));

        //URL
        String s2 = Base64.getUrlEncoder().encodeToString("base64test".getBytes("utf-8"));
        System.out.println(s2);

        //Mime
        String s3 = Base64.getMimeEncoder().encodeToString("base64test".getBytes("utf-8"));
        System.out.println(s3);
    }
}
```

### 5.  新的日期和时间工具

在过去，Java 处理日期和时间我们一般是用 `java.util.Date`、`java.util.Calendar`  配合 `java.text.SimpleDateFormat` 来使用的，缺点是易用性差，线程不安全，不支持时区，新的日期和时间 API  解决了这些问题。

```java
import org.junit.Test;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

public class TimeExample {

    @Test
    public void test() {
        LocalTime localTime = LocalTime.now();
        System.out.println(localTime);

        LocalDate localDate = LocalDate.now();
        System.out.println(localDate);

        LocalDateTime localDateTime = LocalDateTime.now();
        System.out.println(localDateTime);
    }

    @Test
    public void test1() {
        LocalDateTime localDateTime = LocalDateTime.of(2021, 6, 1, 10, 30);
        System.out.println(localDateTime);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String format = localDateTime.format(formatter);
        System.out.println(format);

        LocalDateTime parse = LocalDateTime.parse("2021-01-01 12:00:00", formatter);
        System.out.println(parse);
    }
}
```

### 6. 参考
- [1] [Java Platform SE 8](https://docs.oracle.com/javase/8/docs/api/)
- [2] [Java 8  新特性 | 菜鸟教程](https://www.runoob.com/java/java8-new-features.html)
