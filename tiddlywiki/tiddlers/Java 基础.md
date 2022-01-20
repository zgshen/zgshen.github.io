
## 1. 基本概念

### 1.1. JDK 和 JRE 有什么区别？

- JRE：Java Runtime Environment（ Java 运行时环境）。即 Java 程序的运行时环境，包含了 Java 虚拟机，Java 基础类库。
- JDK：Java Development Kit（Java 开发工具包）。即 Java 语言编写的程序所需的开发工具包。JDK 包含了 JRE，同时还包括 Java 源码的编译器 javac、监控工具 jconsole、分析工具 jvisualvm 等。

### 1.2. Java 语言有哪些特点

- 简单易学、有丰富的类库
- 面向对象（Java 最重要的特性，让程序耦合度更低，内聚性更高）
- 与平台无关性（JVM 是 Java 跨平台使用的根本）
- 可靠安全
- 支持多线程

## 2. 面向对象

### 2.1. 面向对象和面向过程的区别

**面向过程**：是分析解决问题的步骤，然后用函数把这些步骤一步一步地实现，最后在使用的时候一一调用则可。性能较高，在单片机、嵌入式开发等一般采用面向过程开发。

**面向对象**：是把构成问题的事务分解成各个对象，而建立对象的目的也不是为了完成一个个步骤，而是为了描述某个事物在解决整个问题的过程中所发生的行为。面向对象具有**抽象、封装、继承、多态**的特性，有易维护、易复用、易扩展的特点，可以设计出低耦合的系统。但是性能上来说，比面向过程要低。

### 2.2. 对面向对象的理解

对象有以下特点：
- 对象具有属性和行为
- 对象具有变化的状态
- 对象具有唯一性
- 对象都是某个类别的实例
- 一切皆为对象，真实世界中的所有事物都可以视为对象

面向对象的特性：
- 抽象性：抽象是将一类对象的共同特征总结出来构造类的过程，包括数据抽象和行为抽象两方面。
- 继承性：指子类拥有父类的全部特征和行为，这是类之间的一种关系。Java 只支持单继承。
- 封装性：对象是一个封装了数据以及操作这些数据的逻辑实体。封装的目的在于保护信息。
- 多态性：多态性体现在父类的属性和方法被子类继承后或接口被实现类实现后，可以具有不同的属性或表现方式。

## 3. 数据类型

### 3.1. 八种基本类型

Java 中 8 种基础的数据类型：byte、short、char、int、long、float、double、boolean  

String 类型是最常用到的引用类型。

### 3.2. 包装类型

基本类型都有对应的包装类型，基本类型与其对应的包装类型之间的赋值使用自动装箱与拆箱完成。
```Java
Integer x = 2;     // 装箱 调用了 Integer.valueOf(2)
int y = x;         // 拆箱 调用了 X.intValue()
```

### 3.3. 缓存池

基本类型对应的缓存池如下：
- boolean values true and false
- all byte values
- short values between -128 and 127
- int values between -128 and 127
- char in the range \u0000 to \u007F

在使用这些基本类型对应的包装类型时，如果该数值范围在缓冲池范围内，就可以直接使用缓冲池中的对象。

### 3.4. String 实现

String 被声明为 final，因此它不可被继承。(Integer 等包装类也不能被继承）

在 Java 8 中，String 内部使用 char 数组存储数据。
```Java
public final class String
    implements java.io.Serializable, Comparable<String>, CharSequence {
    /** The value is used for character storage. */
    private final char value[];
}
```

从 Java 9 之后，String 类的实现改用 byte 数组存储字符串，同时使用 coder 来标识使用了哪种编码。
```Java
public final class String
    implements java.io.Serializable, Comparable<String>, CharSequence {
    /** The value is used for character storage. */
    private final byte[] value;

    /** The identifier of the encoding used to encode the bytes in {@code value}. */
    private final byte coder;
}
```

value 数组被声明为 final，这意味着 value 数组初始化之后就不能再引用其它数组。并且 String 内部没有改变 value 数组的方法，因此可以保证 String 类型值不可变。

### 3.5. String, StringBuffer and StringBuilder

#### 3.5.1. 可变性

String 不可变  
StringBuffer 和 StringBuilder 可变

#### 3.5.2. 是否线程安全

String 不可变，因此是线程安全的  
StringBuilder 不是线程安全的  
StringBuffer 是线程安全的，内部使用 synchronized 进行同步

### 3.6. String Pool

字符串常量池（String Pool）保存着所有字符串字面量（literal strings），这些字面量在编译时期就确定。不仅如此，还可以使用 String 的 intern() 方法在运行过程将字符串添加到 String Pool 中。

在 Java 7 之前，String Pool 被放在运行时常量池中，它属于永久代。而在 Java 7，String Pool 被移到堆中。这是因为永久代的空间有限，在大量使用字符串的场景下可能会导致 OutOfMemoryError 错误。

### 3.7. new String("abc")

使用这种方式一共会创建两个字符串对象（前提是 String Pool 中还没有 "abc" 字符串对象）。

"abc" 属于字符串字面量，因此编译时期会在 String Pool 中创建一个字符串对象，指向这个 "abc" 字符串字面量；
而使用 new 的方式会在堆中创建一个字符串对象。

### 3.8. String s="a"+"b"+"c"+"d";创建了几个对象？

1个  
编译器会做优化，相当于直接定义一个 "abcd" 的字符串。

### 3.9. Math.round(-1.5) 等于多少？

运行结果： -1  
JDK 中的 java.lang.Math 类  
- ceil() ：向上取整，返回小数所在两整数间的较大值，返回类型是 double，如 -1.5 返回 -1.0
- floor() ：向下取整，返回小数所在两整数间的较小值，返回类型是 double，如 -1.5 返回 -2.0
- round() ：朝正无穷大方向返回参数最接近的整数，可以换算为 参数 + 0.5 向下取整，返回值是 int 或 long，如 -1.5 返回 -1


## 4. 类与对象操作

### 4.1. 抽象类

- 抽象类不能被实例化
- 抽象类可以有抽象方法，抽象方法只需申明，无需实现
- 含有抽象方法的类必须申明为抽象类
- 抽象类的子类必须实现抽象类中所有抽象方法，否则这个子类也是抽象类
- 抽象方法不能被声明为静态
- 抽象方法不能用 private 修饰
- 抽象方法不能用 final 修饰

### 4.2. 接口

接口是抽象类的延伸，在 Java8 之前，它可以看成是一个完全抽象的类，也就是说它不能有任何的方法实现。

Java8 接口可以定义默认方法和静态方法。

Java9 接口可以定义私有方法。

### 4.3. 接口和抽象类使用选择

#### 4.3.1. 使用接口的场景

- 需要让不相关的类都实现一个方法，例如不相关的类都可以实现 Comparable 接口中的 compareTo() 方法；
- 需要使用多重继承。

#### 4.3.2. 使用抽象类的场景

- 需要在几个相关的类中共享代码。
- 需要能控制继承来的成员的访问权限，而不是都为 public。
- 需要继承非静态和非常量字段。

在很多情况下，接口优先于抽象类。因为接口没有抽象类严格的类层次结构要求，可以灵活地为一个类添加行为。从 Java 8 开始，接口也可以有默认的方法实现，使得修改接口的成本也变的很低。

### 4.4. 抽象类必须要有抽象方法吗

不一定。如
```java
public abstract class TestAbstractClass {
 
	public static void notAbstractMethod() {
		System.out.println("I am not a abstract method.");
	}
	
}
```

### 4.5. 重写和重载

- 重写：在子类中将父类的成员方法的名称保留，重新编写成员方法的实现内容，更改方法的访问权限，修改返回类型为父类返回类型的子类。声明为 final、static 或 private 的方法不能被重写。

- 重载：一个类中允许同时存在一个以上的同名方法，这些方法的参数个数或者类型不同。但无法以返回值类型作为重载函数的区分标准。

### 4.6. == 和 equals 的区别是什么?

- == 是关系运算符，equals() 是方法，结果都返回布尔值
- Object 的 == 和 equals() 比较的都是地址，作用相同

### 4.7. hashCode()相同，equals()也一定为true吗？

不一定。同时反过来 equals() 为true，hashCode() 也不一定相同。

- 类的 hashCode() 方法和 equals() 方法都可以重写，返回的值完全在于自己定义。
- hashCode() 返回该对象的哈希码值；equals() 返回两个对象是否相等。

关于 hashCode() 和 equals() 方法是有一些常规约定：  

- 两个对象用 equals() 比较返回 true，那么两个对象的 hashCode() 方法必须返回相同的结果。  
- 两个对象用 equals() 比较返回 false，不要求 hashCode() 方法也一定返回不同的值，但是最好返回不同值，以提高哈希表性能。  
- 重写 equals() 方法，必须重写 hashCode() 方法，以保证 equals() 方法相等时两个对象 hashcode() 返回相同的值。

关于重写 equals() 方法必须重写 hashCode() 方法的解释例子，你和我认识的小明年龄生日和名字都一样（重写 equals()根据属性判断是不是同一个人），但很可能不是同一个人，如果他们的身份证号码相同（hashCode() 值相同），那么就可以确定我两说的是同一个小明了。hashCode() 相当于为  equals() 加一个约束，以保证两个引用的对象是相等的。

### 4.8. 深拷贝和浅拷贝区别是什么

复制一个 Java 对象

- 浅拷贝：复制基本类型的属性；引用类型的属性复制，复制栈中的变量和变量指向堆内存中的对象的指针，不复制堆内存中的对象。（复制的是全新的对象，属性都复制了，除了子类对象还是跟被复制的子类对象是同一个）

- 深拷贝：复制基本类型的属性；引用类型的属性复制，复制栈中的变量和变量指向堆内存中的对象的指针和堆内存中的对象。

浅拷贝实现：

- 实现 Cloneable 接口，重写 clone() 方法
- 不实现 Cloneable 接口，会报 CloneNotSupportedException 异常
- Object 的 clone() 方法是浅拷贝，即如果类中属性有自定义引用类型，只拷贝引用，不拷贝引用指向的对象。

深拷贝实现：

- 引用类型的变量同样要实现Cloneable 接口并重写 clone() 方法
- 使用 Apache Commons 工具类或者 Gson 序列化或 Jackson 序列化

## 5. 异常处理

### 5.1. 异常和错误

- Error：是程序无法处理的错误，表示运行应用程序中出现较严重问题。大多数错误与代码编写者执行的操作无关，而是代码运行时 JVM（Java 虚拟机）出现的问题。

- Exception
    - RuntimeException：运行时异常，编译通过了，但运行时出现的异常。
    - 非 RuntimeException：编译时（受检）异常，编译器检测到某段代码可能会发生某些问题，需要程序员提前给代码做出错误的解决方案，否则编译不通过。

### 5.2. Java 中如何进行异常处理

- 把各种不同的异常进行分类；

- 每个异常都是一个对象，是 Throwable 或其子类的实例；

- 一个方法出现异常后便抛出一个异常对象，该对象中包含有对象信息，调用对象的方法可以捕获这个异常并进行处理；

- Java 中的异常处理通过5个关键词实现：throw、throws、try、catch 和 finally。

### 5.3. throws、throw、try、catch、finally 分别如何使用

- throws：定义方法时，可以使用 throws 关键字抛出异常；
- throw：方法体内使用 throw 抛出异常；
- try：使用 try 执行一段代码，当出现异常后，停止后续代码的执行，跳至 catch 语句块；
- catch：使用 catch 来捕获指定的异常，并进行处理；
- finally：finally 语句块表示的语义是在 try、catch 语句块执行结束后，最后一定会被执行。

### 5.4. return 与 finally 的执行顺序对返回值的影响

对于 try 和 finally 至少一个语句块包含 return 语句的情况：
- finally 语句块会执行
- 当 finally 没有 return 时，finally 对 return 局部变量的重新赋值修改无效
- 当 try 和 finally 都包含 return 时，return 值会以 finally 语句块 return 值为准

## 6. 反射

### 6.1. 作用

- Java 可以通过反射获取方法名称、方法参数和返回值类型等等，但无法获取参数名称
- 使用反射对类进行动态装配，可以降低代码耦合度，但过分使用或严重消耗系统资源

JDK 中 `java.lang.Class` 类是为了实现反射提供的核心类之一。  

JVM 中一种 Class 只会被加载一次。

### 6.2. 相关类库

Class 和 `java.lang.reflect` 一起对反射提供了支持，`java.lang.reflect` 类库主要包含了以下三个类：

- Field ：可以使用 get() 和 set() 方法读取和修改 Field 对象关联的字段；
- Method ：可以使用 invoke() 方法调用与 Method 对象关联的方法；
- Constructor ：可以用 Constructor 的 newInstance() 创建新的对象。

### 6.3. 反射的优缺点

#### 6.3.1. 优点

可扩展性：应用程序可以利用全限定名创建可扩展对象的实例，来使用来自外部的用户自定义类。

类浏览器和可视化开发环境：一个类浏览器需要可以枚举类的成员。可视化开发环境（如 IDE）可以从利用反射中可用的类型信息中受益，以帮助程序员编写正确的代码。  

调试器和测试工具：调试器需要能够检查一个类里的私有成员。测试工具可以利用反射来自动地调用类里定义的可被发现的 API 定义，以确保一组测试中有较高的代码覆盖率。

#### 6.3.2. 缺点

尽管反射非常强大，但也不能滥用。如果一个功能可以不用反射完成，那么最好就不用。在我们使用反射技术时，下面几条内容应该牢记于心。

性能开销：反射涉及了动态类型的解析，所以 JVM 无法对这些代码进行优化。因此，反射操作的效率要比那些非反射操作低得多。我们应该避免在经常被执行的代码或对性能要求很高的程序中使用反射。

安全限制：使用反射技术要求程序必须在一个没有安全限制的环境中运行。如果一个程序必须在有安全限制的环境中运行，如 Applet，那么这就是个问题了。

内部暴露：由于反射允许代码执行一些在正常情况下不被允许的操作（比如访问私有的属性和方法），所以使用反射可能会导致意料之外的副作用，这可能导致代码功能失调并破坏可移植性。反射代码破坏了抽象性，因此当平台发生改变的时候，代码的行为就有可能也随着变化。

## 7. 文件IO

### 7.1. Java 中有几种类型的流

- 字节流：继承自 inputStream 和 OutputStream
- 字符流：继承自 InputSteamReader 和 OutputStreamWriter

### 7.2. 字符流和字节流有什么区别

字节流的操作不会经过缓冲区（内存）而是直接操作文本本身的，而字符流的操作会先经过缓冲区（内存）然后通过缓冲区再操作文件。  

缓冲区就是一段特殊的内存区域，很多情况下当程序需要频繁地操作一个资源（如文件或数据库）则性能会很低，所以为了提升性能就可以将一部分数据暂时读写到缓存区，以后直接从此区域中读写数据即可，这样就显著提升了性能。

 Java 对于字符流的操作都是在缓冲区操作的，如果我们想在字符流操作中主动将缓冲区刷新到文件则可以使用 flush() 方法操作。

**如何选择**

- 大多数情况下使用字节流会更好，因为大多数时候 IO 操作都是直接操作磁盘文件，这些流在传输时都是以字节的方式进行的。

- 如果对于操作需要通过 IO 在内存中频繁处理字符串的情况使用字符流会好些，因为字符流具备缓冲区，提高了性能。

### 7.3. 什么是 Java 序列化，如何实现 Java 序列化？

序列化就是一种用来处理对象流的机制，将对象的内容进行流化。可以对流化后的对象进行读写操作，流化后的对象可以在网络之间传输。序列化是为了解决在对象流读写操作时所引发的问题。  

### 7.4. 序列化的实现

将需要被序列化的类实现 Serialize 接口，没有需要实现的方法，此接口只是为了标注对象可被序列化的，然后使用一个输出流（如：FileOutputStream）来构造一个ObjectOutputStream（对象流）对象，再使用 ObjectOutputStream 对象的 write(Object obj) 方法就可以将参数 obj 的对象写出。

### 7.5. Linux 的文件描述符

Linux 中一切类型都被抽象成文件，如：普通文件、目录、字符设备、块设备、套接字等。

文件描述符是内核创建的方便管理已打开文件的索引，用来指代被打开的文件。当程序打开一个现有文件或者创建一个新文件时，内核向进程返回一个文件描述符。

所有执行 I/O 操作的系统调用都通过文件描述符（fd）。在Linux系统中，ssh 方式登录后查看 /proc下信息，可以看到系统为每一个进程默认创建0，1，2 三个 fd，0表示标准输入，1表示标准输出，2表示错误输出。$$ 表示当前进程 ID。

```bash
[root@VM-0-16-centos ~]# cd /proc/$$/fd
[root@VM-0-16-centos fd]# ll
total 0
lrwx------ 1 root root 64 Apr 24 09:01 0 -> /dev/pts/0
lrwx------ 1 root root 64 Apr 24 09:01 1 -> /dev/pts/0
lrwx------ 1 root root 64 Apr 24 09:01 2 -> /dev/pts/0
lrwx------ 1 root root 64 Apr 24 09:01 255 -> /dev/pts/0
[root@VM-0-16-centos fd]#
```

### 7.6. 内核态和用户态与 IO

为了限制不同的程序之间的访问能力, 防止他们获取别的程序的内存数据, 或者获取外围设备的数据, 并发送到网络, 内存被划分为用户态和内核态。 

内核态：CPU 可以访问内存所有数据，包括外围设备，例如硬盘、网卡等，CPU 也可以将自己从一个程序切换到另一个程序。

用户态：只能受限地访问内存，且不允许访问外围设备，必须通过系统提供的 syscall 方式调用系统函数。占用 CPU 的能力被剥夺，CPU 资源可以被其他程序获取。

举例磁盘和 socket 的 IO 操作：  
IO 对文件拷贝操作：硬盘 -->内核空间 -->用户线程空间 -->内核空间 -->硬盘  
IO 对 socket 操作: scoket -->内核空间 -->用户线程空间 -->内核空间 -->socket

![kernal-user-sapce](https://raw.githubusercontent.com/zgshen/code-note/master/doc/images/kernal-user-sapce.png)

参考 https://zhuanlan.zhihu.com/p/148673095

- Java 中通过对系统的调用来实现网络 IO；
- 实现网络 IO 不是 Java 的能力，是操作系统内核提供的能力。

### 7.7. BIO、NIO、AIO 的区别

- BIO：同步阻塞 IO 模式，数据的读取写入必须阻塞在一个线程内等待其完成
	- 先将文件内容从磁盘中拷贝到操作系统 buffer
	- 再从操作系统 buffer 拷贝到  程序应用（应用层）buffer
	- 从程序 buffer 拷贝到 socket buffer
	- 从 socket buffer 拷贝到协议引擎.
- NIO：同步非阻塞的 IO 模型
- AIO：异步非阻塞的 IO 模型

#### 7.7.1. BIO

传统的 BIO 处理多个客户端的请求或在客户端对多个服务端进行通讯，必须使用多线程来处理。每一个请求都需要分配一个线程来处理，当有大量请求时线程的上下文切换和内存占用对系统来说都是很大的负担。BIO 的阻塞体现在两个地方：
- ServerSocket # accept(); 在没有新连接时，就会阻塞;
- Socket # getInputStream() # read(byte[] bs); 在没有数据传输时，就会阻塞

#### 7.7.2. NIO

NIO 需要系统内核支持，而且在不同系统如 Linux 和 Windows 下的实现方式时不一样的。  

Java NIO 包为我们提供了一个 selector（多路复用器），然后我们把需要检查的 socket 注册到这个 selector 中，主线程堵塞在 selector 的 select 方法里面。当选择器发现某个 socket 就绪了，它就会唤醒主线程，通过 selector 获取到就绪状态的socket来进行相应的处理。  

NIO selector 调用 native 方法是调用操作系统的系统函数，即 kernel#select 函数，每次调用都涉及用户态/内核态的切换，传递的是 socket 集合，即文件描述符 fd，根据 fd 集合检查 socket 状态，就绪态直接返回，没有就堵塞直到有数据过来。

#### 7.7.3. AIO

当进行读写操作时，只须直接调用 API 的 read 或 write 方法即可，这两种方法均为异步的。

对于读操作而言，当有流可读取时，操作系统会将可读的流传入 read 方法的缓冲区，并通知应用程序。

对于写操作而言，当操作系统将 write 方法传递的流写入完毕时，操作系统主动通知应用程序。 即可以理解为，read/write 方法都是异步的，完成后会主动调用回调函数。

参考 https://blog.csdn.net/joyblur/article/details/108402364

## 8. Java8 特性

### 8.1. Lambda

Lambda 表达式（也称为闭包）允许我们将函数当成参数传递给某个方法，此类参数必定是一个函数式接口（即单抽象方法接口）。

### 8.2. JDK8中Stream接口的常用方法

中间操作：
- filter：过滤元素
- map：映射，将元素转换成其他形式或提取信息
- flatMap：扁平化流映射
- limit：截断流，使其元素不超过给定数量
- skip：跳过指定数量的元素
- sorted：排序
- distinct：去重

终端操作：
- anyMatch：检查流中是否有一个元素能匹配给定的谓词
- allMatch：检查谓词是否匹配所有元素
- noneMatch：检查是否没有任何元素与给定的谓词匹配
- findAny：返回当前流中的任意元素（用于并行的场景）
- findFirst：查找第一个元素
- collect：把流转换成其他形式，如集合 List、Map、Integer
- forEach：消费流中的每个元素并对其应用 Lambda，返回 void
- reduce：归约，如：求和、最大值、最小值
- count：返回流中元素的个数

### 8.3. Java8 以上各版本新特性

参考 https://zguishen.com/tags/NewFeatures/