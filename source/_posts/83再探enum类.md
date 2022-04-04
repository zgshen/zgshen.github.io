---
title: 再探枚举类Enum
categories: 技术
tags: 
    - 技术
    - Java
date: 2022-03-29
---

枚举类是 Java 很常见的类了，最近在推上看到一个很有意思的枚举用法，加上执行开发中碰到的枚举的一些问题，这里记录一下。


### 枚举定义和使用场景

枚举是一个被命名的整形常数的集合。在 Java 中，描述抽象的事物外面用类和接口，但有些特殊的类的属性是一组固定的常数集合，那么就可以用枚举来表示，典型的例子比如星期有周日到周一，人类的性别有男女...嗯，如果见过国外的一些网站可能会有一些跨性别或其他选项可选，不过还是一样是常数集合。

比如一个 Person 类，性别 gender 用0表示女的，1表示男的，在数据库字段也是存的0或1的tinyint类型。

```java
public class Person {
    //名字
    String name;
    //性别：0女，1男
    int gender;
    /**
     * getter/setter 省略
     * ...
     */
}
```

这种方式客户端拿到 Person 对象之后看到 gender 的值后，并不知道0或1代表什么，只能看注释或者文档。

使用 Enum 之后的写法：

```java
public class Person {
    //名字
    String name;
    //性别
    Gender gender;
    //getter/setter/toString 省略
}

//性别枚举
public enum Gender {

    Female(0),
    Male(1);

    private int gender;
    Gender(int gender) {
        this.gender = gender;
    }

    public int getVal() {
        return gender;
    }
}

//使用
public static void main(String[] args) {
    Person p = new Person();
    p.setName("nathan");
    //只能传入Gender存在的类型
    p.setGender(Gender.Male);

    System.out.println(p);
    //可以获知属性值代表什么类型
    System.out.println("gender:" + p.getGender() + "/value:" + p.getGender().getVal());
}
```

从上面可以看出，枚举类有三个好处。
- 枚举也是类，可以有属性和方法
- 类型检查和有效性检查
- 本身就带有含义，不用像常量那样需要查询文档或注释才知道值定义

### 高级用法

之前在[推上](https://twitter.com/dblevins/status/1502481447935897601)别人看到用 Enum 来简化时间解析，可以拥有类型和有效性检查的好处。用法是这样的;

```java
public enum DateUtil {

    yyyy_MM_dd("yyyy-MM-dd"),
    MMM_dd_yyyy("MMM dd, yyyy");

    private final DateTimeFormatter formatter;

    DateUtil(final String formatString) {
        formatter = DateTimeFormatter.ofPattern(formatString);
    }

    public LocalDate parse(final String string) {
        return LocalDate.parse(string, formatter);
    }

    public String format(final LocalDate date) {
        return formatter.format(date);
    }

    public Date parseDate(final String string) {
        return Date.from(parse(string).atStartOfDay()
                .atZone(ZoneId.systemDefault())
                .toInstant());
    }

    public String format(final Date date) {
        return format(date.toInstant()
                .atZone(ZoneId.systemDefault())
                .toLocalDate());
    }

    public static void main(String[] args) {
        //按照枚举定义的格式转化成LocalDate
        LocalDate parse = DateUtil.yyyy_MM_dd.parse("2022-03-31");
        System.out.println(parse);

        //把LocalDate转换成字符串
        String format = DateUtil.MMM_dd_yyyy.format(LocalDate.now());
        System.out.println(format);
    }
}
```

### 枚举的问题

看过[《阿里巴巴Java开发手册》](https://github.com/alibaba/p3c)应该注意到其中对枚举类的使用做了限制，二方库里可定义枚举类型，参数可以使用枚举类型，但是接口返回值不允许使用枚举类型或者包含枚举类型的 POLO 对象。原因是使用枚举作为返回值，若 RPC 客户端和服务端版本不一致的话，会造成反序列化异常。

以上面 Person 类为例，版本1的 Gender 属性有两个类型 Male 和 Female，将这个版本的 SDK 给客户端用。后来需求变化，版本2的 Gender 加了 Transgender，如：

```java
public enum Gender {

    Female(0),
    Male(1),
    Transgender(2);

    private int gender;
    Gender(int gender) {
        this.gender = gender;
    }

    public int getVal() {
        return gender;
    }
}
```

如果客户端还是使用旧的 SDK 的进行请求调用的话，涉及序列化就会出现错误。

以 Jackson 的序列化反序列化为例，Gender 新加类型序列化：

```java
//版本2
Person p = new Person();
p.setName("nathan");
p.setGender(Gender.Transgender);
String ps = new ObjectMapper().writeValueAsString(p);
//{"name":"nathan","gender":"Transgender"}
```

客户端反序列化：
```java
String pStr = "{\"name\":\"nathan\",\"gender\":\"Transgender\"}";
Person person = mapper.readValue(pStr, Person.class);
```

报错
```
Exception in thread "main" com.fasterxml.jackson.databind.exc.InvalidFormatException: Can not construct instance of com.review.enumtest.Gender from String value 'Transgender': value not one of declared Enum instance names: [Female, Male]
 at [Source: {"name":"nathan","gender":"Transgender"}; line: 1, column: 17] (through reference chain: com.review.enumtest.Person["gender"])
```

解决方法就是接口返回值不要用枚举，或者客户端需要自行处理不存在枚举类型，比如转换成 null 或者设置为默认值。

```java
String pStr = "{\"name\":\"nathan\",\"gender\":\"Transgender\"}";
Person person = mapper
                .configure(DeserializationFeature.READ_UNKNOWN_ENUM_VALUES_AS_NULL, true)
                .readValue(pStr, Person.class);
```

两种处理方式的分歧是在认为枚举应不应该允许变化的，使用哪种看自己业务的需求。可以看看[知乎](https://www.zhihu.com/question/52760637)上关于 Enum 反序列化问题的讨论。
