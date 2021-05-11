---
title: Java内存模型和JVM
categories: 技术
tags: 面试
date: 2020-12-21
---

对于Java开发而言，找工作面试基本上都会问道 JVM 这个知识点，其中涉及结构组成、作用原理、异常排查和参数调优等等。

<!-- more -->

<!-- TOC -->

- [1. Java 内存模型](#1-java-内存模型)
    - [1.1. 概念](#11-概念)
    - [1.2. JMM 关于同步的规定](#12-jmm-关于同步的规定)
    - [1.3. 主内存和工作内存](#13-主内存和工作内存)
    - [1.4. 并发编程三个特性](#14-并发编程三个特性)
    - [1.5. Happens-Before规则](#15-happens-before规则)
    - [1.6. Java 8种关于主内存和工作内存的交互协议操作](#16-java-8种关于主内存和工作内存的交互协议操作)
    - [1.7. volatile 禁止指令重排序，保证变量对所有线程的可见性](#17-volatile-禁止指令重排序保证变量对所有线程的可见性)
- [2. JVM](#2-jvm)
    - [2.1. JVM 内存模型](#21-jvm-内存模型)
    - [2.2. 运行时数据区](#22-运行时数据区)
        - [2.2.1. 虚拟机栈](#221-虚拟机栈)
        - [2.2.2. 本地方法栈](#222-本地方法栈)
        - [2.2.3. 程序计数器](#223-程序计数器)
        - [2.2.4. 堆](#224-堆)
        - [2.2.5. 方法区](#225-方法区)
    - [2.3. 三种常量池](#23-三种常量池)
        - [2.3.1. 常量池](#231-常量池)
        - [2.3.2. 运行时常量池](#232-运行时常量池)
        - [2.3.3. 字符串常量池](#233-字符串常量池)
- [3. 类加载机制](#3-类加载机制)
    - [3.1. 类加载过程](#31-类加载过程)
    - [3.2. 类加载器](#32-类加载器)
    - [3.3. 双亲委派机制](#33-双亲委派机制)
    - [3.4. 双亲委派机制如何打破](#34-双亲委派机制如何打破)
    - [3.5. 类初始化顺序](#35-类初始化顺序)
    - [3.6. Java的对象结构](#36-java的对象结构)
- [4. 内存分配与垃圾回收](#4-内存分配与垃圾回收)
    - [4.1. 内存分配策略](#41-内存分配策略)
    - [4.2. 垃圾回收判断](#42-垃圾回收判断)
    - [4.3. 垃圾回收算法](#43-垃圾回收算法)
    - [4.4. 垃圾回收器](#44-垃圾回收器)
    - [4.5. GC 回收机制](#45-gc-回收机制)
        - [4.5.1. 详细说明](#451-详细说明)
        - [4.5.2. 为什么有两个 Survivor 区](#452-为什么有两个-survivor-区)
        - [4.5.3. 相关参数](#453-相关参数)
    - [4.6. Minor GC 和 Full GC](#46-minor-gc-和-full-gc)
    - [4.7. Full GC 触发条件](#47-full-gc-触发条件)
- [5. JVM 问题和调优](#5-jvm-问题和调优)
    - [5.1. 内存泄漏和内存溢出的区别](#51-内存泄漏和内存溢出的区别)
    - [5.2. OOM相关](#52-oom相关)
            - [5.2.1. 堆溢出](#521-堆溢出)
            - [5.2.2. 栈内存溢出（-Xss）](#522-栈内存溢出-xss)
            - [5.2.3. 方法区和运行时常量池溢出（-XX:PermSize -XX:MaxPermSize）](#523-方法区和运行时常量池溢出-xxpermsize--xxmaxpermsize)
            - [5.2.4. 本机直接内存溢出（-MaxDirectMemorySize）](#524-本机直接内存溢出-maxdirectmemorysize)
    - [5.3. OOM 常见原因](#53-oom-常见原因)
    - [5.4. 各类 OOM 和解决方法](#54-各类-oom-和解决方法)
    - [5.5. JVM 调优](#55-jvm-调优)
    - [5.6. 调优命令](#56-调优命令)
    - [5.7. 调优工具](#57-调优工具)

<!-- /TOC -->

## 1. Java 内存模型
### 1.1. 概念
Java 内存模型(即 Java Memory Model，简称 JMM )本身是一种抽象的概念，并不真实存在，它描述的是一组规则或规范，通过这组规范定义了程序中各个变量（包括实例字段，静态字段和构成数组对象的元素）的访问方式。

### 1.2. JMM 关于同步的规定
1. 线程解锁前，必须把共享变量的值刷新回主内存；
2. 线程加锁前，必须读取主内存的最新值到自己的工作内存；
3. 加锁解锁为同一把锁。

### 1.3. 主内存和工作内存
- Java 内存模型规定了所有的变量都存储在主内存中，每条线程还有自己的工作内存，线程的工作内存中保存了该线程使用到的变量的主内存副本拷贝。
- 线程对变量的所有操作（读取、赋值）都必须在工作内存中进行，而不能直接读写主内存中的变量。  
- 不同线程之间无法直接访问对方工作内存中的变量，线程间变量值的传递均需要在主内存来完成。

### 1.4. 并发编程三个特性
- 原子性：一个操作中 cpu 不能中断，要么不执行，要么执行完成
- 可见性：多线程访问变量，一个线程修改了变量，其他线程能够立即看到修改值
- 有序性：按照代码顺序执行

### 1.5. Happens-Before规则
- 程序顺序规则：一个线程中的每一个操作，happens-before 于该线程中的任意后续操作。
- 监视器规则：对一个锁的解锁，happens-before 于随后对这个锁的加锁。
- volatile 规则：对一个 volatile 变量的写，happens-before 于任意后续对一个 volatile 变量的读。
- 传递性：如果 A happens-before B，B happens-before C，那么 A happens-before C。
- 线程启动规则：Thread 对象的 start() 方法，happens-before 于这个线程的任意后续操作。
- 线程终止规则：线程中的任意操作，happens-before 于该线程的终止监测。我们可以通过 Thread.join() 方法结束、Thread.isAlive() 的返回值等手段检测到线程已经终止执行。
- 线程中断操作：对线程 interrupt() 方法的调用，happens-before 于被中断线程的代码检测到中断事件的发生，可以通过 Thread.interrupted() 方法检测到线程是否有中断发生。
- 对象终结规则：一个对象的初始化完成，happens-before 于这个对象的 finalize() 方法的开始。

### 1.6. Java 8种关于主内存和工作内存的交互协议操作
lock：作用于主内存，锁住主内存主变量。

unlock：作用于主内存，解锁主内存主变量。

read：作用主内存，主内存传递到工作内存。

load：作用于工作内存，主内存传递来的值赋给工作内存工作变量。

use：作用工作内存，工作内存工作变量值传给执行引擎。

assign：作用工作内存，引擎的结果值赋值给工作内存工作变量。

store：作用于工作内存的变量，工作内存工作变量传送到主内存中。

write：作用于主内存的变量，工作内存传来工作变量赋值给主内存主变量。

read and load 从主存复制变量到当前工作内存；  
use and assign  执行代码，改变共享变量值；  
store and write 用工作内存数据刷新主存相关内容。

其中use and assign 可以多次出现。  
但是这一些操作并不是原子性，也就是 在read load之后，如果主内存count变量发生修改之后，线程工作内存中的值由于已经加载，不会产生对应的变化，所以计算出来的结果会和预期不一样。

对于volatile修饰的变量，jvm虚拟机只是保证从主内存加载到线程工作内存的值是最新的。

### 1.7. volatile 禁止指令重排序，保证变量对所有线程的可见性
一旦一个共享变量（类的成员变量、类的静态成员变量）被 volatile 修饰之后，那么就具备了两层语义：  
1）保证了不同线程对这个变量进行操作时的可见性，即一个线程修改了某个变量的值，这新值对其他线程来说是立即可见的，volatile 关键字会强制将修改的值立即写入主存。  
2）禁止进行指令重排序。  
volatile 不是原子性操作，只保证可见性和有序性，不保证原子性。  
使用 volatile 一般用于**状态标记量**和**单例模式的双检锁。**

```Java
public class ThreadTest extends Thread {

    private volatile boolean flag = false;

    @Override
    public void run() {
        try {
            Thread.sleep(1000L);//延迟一下让主线程循环跑起来
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        flag = true;
    }

    public static void main(String[] args) {
        ThreadTest threadTest = new ThreadTest();
        threadTest.start();

        System.out.println(threadTest.flag);
        while (true) {
            if (threadTest.flag) {//主程读取
                break;
            }
        }
        System.out.println("do something.");
    }

}
```
多核 CPU 下如果 flag 变量不加 volatile 关键字，主程读取 flag 变量这里可能一直读到的是 false，volatile 关键字会强制子线程将修改的值立即写入主存，并将其他线程下的缓存行失效，强制其他线程再访问此变量时从主内存中获取，达到可见性的效果。

```Java
public class Singleton {
    private static Singleton instance;

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();//创建对象并不是一个原子操作
                }
            }
        }
        return instance;
    }
}
```
单例模式用到，new 对象不是原子操作，分三步：
- 分配内存空间
- 初始化对象
- 对象引用指向分配的地址  

由于 CPU 可能的优化排序，第三步可能会先与第二步执行，这时其他线程读到就会由问题，可用 volatile 禁止指令重排序避免此问题。

volatile 关键字使用的是 Lock 指令，volatile 的作用取决于 Lock 指令。CAS 不是保证原子的更新，而是使用死循环保证更新成功时候只有一个线程更新，不包括主工作内存的同步。 CAS 配合 volatile 既保证了只有一个线程更新又保证了多个线程更新获得的是最新的值互不影响。

## 2. JVM
### 2.1. JVM 内存模型
- 类加载器子系统
- 运行时数据区
- 执行引擎

![img](https://raw.githubusercontent.com/zgshen/code-note/master/doc/images/jvm-struct.png)

### 2.2. 运行时数据区
#### 2.2.1. 虚拟机栈
栈是线程私有，用来存放局部变量、对象引用和常量池引用。方法执行的时候会创建一个栈帧，存储了**局部变量表、操作数栈、动态链接和方法出口信息**。每个方法从调用到执行完毕，对应一个栈帧在虚拟机中的入栈和出栈。  
Java 虚拟机栈会出现两种异常：  
**StackOverFlowError** ：若 Java 虚拟机栈的内存大小不允许动态扩展，那么当线程请求栈的深度超过当前 Java 虚拟机栈的最大深度的时候，就抛出 StackOverFlowError 错误。  
**OutOfMemoryError** ： 若 Java 虚拟机栈的内存允许动态扩展，并且当线程请求栈时内存用完了，无法再动态扩展了，就会抛出 OutOfMemoryError 异常。

#### 2.2.2. 本地方法栈
线程私有，和虚拟机栈类似，主要为虚拟机使用到的 Native 方法服务，也会抛出 `StackOverFlowError ` 和 `OutOfMemoryError` 错误。

#### 2.2.3. 程序计数器
线程私有，是当前线程锁执行字节码的行号治时期，每条线程都有一个独立的程序计数器，这类内存也称为“线程私有”的内存。正在执行 Java 方法的话，计数器记录的是虚拟机字节码指令的地址（当前指令的地址）。如果是 Native 方法，则为空。

#### 2.2.4. 堆
线程共享，在虚拟机启动的时候创建，用于存放对象实例。通过-Xmx 和-Xms 来控制大小。  
堆区域可分为新生代、老年代。（方法区中的永久代在 JDK 1.8及之后已经移除，实现为元空间）。  
新生代可分为 Eden 空间、From Survivor 和 To Survivor 空间等。  
堆容易出现的错误是 `OutOfMemoryError` 错误，表现有几种：
- `OutOfMemoryError: GC Overhead Limit Exceeded` ：当JVM花太多时间执行垃圾回收并且只能回收很少的堆空间时，就会发生此错误。
- `java.lang.OutOfMemoryError: Java heap space` ：假如在创建新的对象时, 堆内存中的空间不足以存放新创建的对象, 就会引发这个错误(和本机物理内存无关，和你配置的堆内存大小有关)。

#### 2.2.5. 方法区
线程共享，用于存储已被 JVM 加载的类信息、静态变量、常量、属性和方法信息。  
永久代和元空间都是方法区的一种实现，JDK1.8 之前永久代还没被彻底移除的时候通常通过下面这些参数来调节方法区大小：
```
-XX:PermSize=N //方法区 (永久代) 初始大小
-XX:MaxPermSize=N //方法区 (永久代) 最大大小,超过这个值将会抛出 OutOfMemoryError 异常 `java.lang.OutOfMemoryError: PermGen`
```
JDK 1.8及之后永久代被彻底移除了，取代的是元空间，元空间使用的是直接内存，常用设置参数：
```
-XX:MetaspaceSize=N //设置 Metaspace 的初始（和最小大小）
-XX:MaxMetaspaceSize=N //设置 Metaspace 的最大大小
```
永久代 (PermGen) 替换为元空间 (MetaSpace) 的原因是永久代有一个 JVM 本身设置固定大小上限，无法进行调整，而元空间使用的是直接内存，只受本机可用内存的限制。元空间也会溢出，但比原来出现的几率小。  

### 2.3. 三种常量池

#### 2.3.1. 常量池
常量池，即 class 文件常量池，是 class 文件的一部分，用于保存编译时确定的数据；
![常量池](https://raw.githubusercontent.com/zgshen/code-note/master/doc/images/constant.png)

#### 2.3.2. 运行时常量池
类加载后，常量池信息就会放入运行时常量池，并将常量池内符号引用替换成直接引用。运行时常量池是动态的，程序运行期间也可能产生新的常量，这些常量被放到运行时常量池中。  

运行时常量池也是方法区的一部分。

#### 2.3.3. 字符串常量池
字符串常量池是由 StringTable 实现的，其实就是一个 HashTable，存储在堆区。
字符串常量池保存着所有字符串字面量（literal strings），这些字面量在编译时期就确定。不仅如此，还可以使用 String 的 intern() 方法在运行过程将字符串添加到 String Pool 中。

```Java
String a = "123";
String b = "123";

String c = new String("123");
String d = new String("123");

String e = "12";
String f = "3";
String g = e + f;
g.intern();//池化后没返回

System.out.println(a == b);//true  a 和 b 都指向同一引用对象
System.out.println(c == d);//false 在堆中是两个不同对象
System.out.println(a == c);//false a 在 String Pool 中，c 在堆中，不同对象
System.out.println(a == g);//false + 号是使用 StringBuilder 实现拼接的
g = g.intern();
System.out.println(a == g);//true g 池化后返回给 g，跟 a 指向同一对象
```
对以上各种 String 对象创建的解释：  
`String a = "123";` 在堆中创建对象，这个 String 对象包含了各种指针类型的成员对象，其内部实现 value 则是指向了存储在字符串常量池的字符串“123”；  

`String c = new String("123");`  如果字符串常量池中不存在“123”字符串，直接在堆中创建对象然后返回给变量；如果字符串常量池中存在“123”字符串，会先在堆中创建一个 c 变量的对象引用，再将引用指向已经存在的常量对象，其实就是上面的 a 指向的对象；

`g = g.intern()` 如果当前字符串内容存在于字符串常量池，那直接返回此字符串在常量池的引用；如果之前不在字符串常量池中，那么在常量池创建一个引用并且指向堆中已存在的字符串，然后返回常量池中的地址。

**存储位置及区别区别**  
字符串常量池和运行时常量池是两个独立不同的东西。  
JDK1.7 之前的运行时常量池，字符串常量池存放在方法区，JDK1.7 开始把字符串常量池方法区拿到了堆中，运行时常量池还在方法区。  
到 JDK1.8 使用元空间替代永久区来实现方法区，此时运行时常量池在元空间，字符串常量池在堆。  

## 3. 类加载机制
### 3.1. 类加载过程
![类加载过程](https://raw.githubusercontent.com/zgshen/code-note/master/doc/images/classinit.png)

其中验证，准备，解析一般合称链接。

- 加载：
	- 获取类的二进制字节流
	- 将字节流代表的静态存储结构转化为方法区运行时数据结构
	- 在堆中生成class字节码对象
- 验证：连接过程的第一步，确保 class 文件的字节流中的信息符合当前 JVM 的要求，不会危害 JVM 的安全
- 准备：为类的静态变量分配内存并将其初始化为默认值（不包含 final 修饰的静态变量，因为 final 变量在编译时分配）
- 解析：JVM 将常量池内符号引用替换成直接引用的过程。直接引用为直接指向目标指针或者相对偏移量等
- 初始化：完成静态块执行以及静态变量的赋值，先初始化父类，再初始化子类。只有对类主动使用才会初始化。  
触发条件包括：创建类实例时，访问类静态变量和静态方法时，使用 Class.forName 反射类时或者某个子类初始化时。

### 3.2. 类加载器
![类加载器](https://raw.githubusercontent.com/zgshen/code-note/master/doc/images/classload.png)
-  启动类加载器 BootstrapClassLoad  rt.jar
-  扩展类加载器 ExtClassLoad  ext 目录下扩展 jar
-  应用程序类加载器 AppClassLoad  claddpath 上的类

Java 自带的加载器的类，在虚拟机的生命周期中是不会被卸载的，只有用户自定义的加载器加载的类才可以被卸载。

### 3.3. 双亲委派机制
一个类加载器首先将类加载请求转发到父类加载器，只有当父类加载器无法完成时才尝试自己加载。  
优点：  
- 避免类的重复加载；
- 避免 Java 的核心 API 被篡改。

### 3.4. 双亲委派机制如何打破
- 自定义类加载器实现，重写自定义加载器的 loadClass()，JDk 不推荐。一般都只是重写 findClass()，这样可以保持双亲委派机制。而 loadClass 方法加载规则由自己定义，就可以随心所欲的加载类了。
- JDBC驱动例子，DriverManager 在 jre/lib/rt.jar 中，加载器是 BootstrapClassLoader，但其实现则在各厂商 SPI 实现的 jar 包中。  
根据类加载机制，若A类调用B类，则B类由A类的加载器加载。也就是启动类加载器需要加载实现类，这就出现问题，实现类不在 rt.jar 里而是在开发工程目录下。此时 SPI 是通过线程上下文类加载器 `Thread.currentThread().getContextClassLoader()` 来加载实现类。线程上下文类加载器就是当前线程的 CurrentClassloader。

### 3.5. 类初始化顺序
- 静态变量/静态代码块，普通代码块，构造器
- 父类静态变量/静态代码块→子类静态变量/静态代码块→父类普通代码块→父类构造器→子类普通代码块→子类构造器
- 子类的静态变量和静态初始化块的初始化是在父类的变量、初始化块和构造器初始化之前就完成了；（父类静态-子类静态-父类普通初始化块-子类普通初始化块。跟上面其实重复）
- 静态变量、静态初始化块顺序取决于它们在类中出现的先后顺序
- 变量、初始化块初始化顺序取决于它们在类中出现的先后顺序

### 3.6. Java的对象结构
Java 对象由三个部分组成：对象头、实例数据、对齐填充。
- 对象头：由两部分组成，第一部分存储对象自身的运行时数据：哈希码、GC 分代年龄、锁标识状态、线程持有的锁、偏向线程 ID（一般占32/64 bit）。第二部分是指针类型，指向对象的类元数据类型（即对象代表哪个类）。如果是数组对象，则对象头中还有一部分用来记录数组长度。
- 实例数据：用来存储对象真正的有效信息（包括父类继承下来的和自己定义的）。
- 对齐填充：JVM 要求对象起始地址必须是8字节的整数倍（8字节对齐）。


## 4. 内存分配与垃圾回收
### 4.1. 内存分配策略
- **对象优先分配在 Eden 区**，如果 Eden 区没有足够的空间时，虚拟机执行一次 Minor GC。
- **大对象直接进入老年代**（大对象是指需要大量连续内存空间的对象）。这样做的目的是避免在 Eden 区和两个 Survivor 区之间发生大量的内存拷贝（新生代采用复制算法收集内存）。
- **长期存活的对象进入老年代**。虚拟机为每个对象定义了一个年龄计数器，如果对象经过了1次 Minor GC 那么对象会进入 Survivor 区，之后每经过一次 Minor GC 那么对象的年龄加1，知道达到阀值对象进入老年区。
- **动态对象年龄判定**。如果 Survivor 区中相同年龄的所有对象大小的总和大于 Survivor 空间的一半，年龄大于或等于该年龄的对象可以直接进入老年代。
- **空间分配担保**。每次进行 Minor GC 时，JVM 会计算 Survivor 区移至老年区的对象的平均大小，如果这个值大于老年区的剩余值大小则进行一次 Full GC，如果小于检查 HandlePromotionFailure 设置，如果 true 则只进行 Monitor GC,如果 false 则进行 Full GC。

### 4.2. 垃圾回收判断
- 引用计数算法：引用数为0的对象回收，难以解决对象循环引用问题
- 根搜索法（可达性分析）：从 GC Root 对象开始向下搜索，可达的对象都是存活的，不可达的对象无法被回收

### 4.3. 垃圾回收算法
判断对象已死去的方法有引用计数法（已淘汰）和根搜索法（可达性分析算法）
- 标记-清除算法：先标记需要清除对象，遍历清除，容易产生内存碎片
- 复制算法：分两块内存，把存活对象复制到另一块内存上，再把第一块内存所有对象清除
- 标记-整理算法：将标记的存活对象都像一端移动，清理端边界以外的内存（老年代）
- 增量算法
- 分代收集算法：不同的代采用不同是算法。
	- 年轻代采用复制算法，因为大部分对象都是朝生夕死；
	- Eden 区和 From Survivor 回收后存活对象复制到 To Survivor
	- 默认15次没被回收的对象会被复制到 Old 区
	- Old 区也被填满时，进行 Full GC，对 Old 区进行垃圾回收

### 4.4. 垃圾回收器
- Serial 收集器
- ParNew 收集器
- Parallel Scavenge 收集器
- Serial Old 收集器
- Parallel Old 收集器
- CMS 收集器
- G1 收集器

### 4.5. GC 回收机制
#### 4.5.1. 详细说明
![img](https://raw.githubusercontent.com/zgshen/code-note/master/doc/images/jvm-gc.webp)

年轻代分为 Eden 区和 Survivor 区（两块分别为 From Survivor  和 To Survivor 交替使用，哪个被回收了就由 From 变成 To），且 Eden:From:To = 8:1:1。  
1. 新产生的对象优先分配在 Eden 区（除非配置了`-XX:PretenureSizeThreshold`，大于该值的对象会直接进入年老代）; 
2. 当 Eden 区满了或放不下了，这时候其中存活的对象会复制到 From 区（如果存活下来的对象 From 区都放不下，则这些存活下来的对象全部进入年老代，即依赖老年代空间担保。之后 Eden 区的内存全部回收掉）；
3. 之后产生的对象继续分配在 Eden 区，当 Eden 区又满了或放不下了，这时候将会把 Eden 区和 From 区存活下来的对象复制到 To 区（同理，如果存活下来的对象 To 区都放不下，则这些存活下来的对象全部进入年老代），之后回收掉 Eden 区和 From 区的所有内存；
4. 如上这样，会有很多对象会被复制很多次（每复制一次，对象的年龄就+1），默认情况下，当对象被复制了15次，就会进入年老代了；
5. 当年老代满了或者存放不下将要进入年老代的存活对象的时候，就会发生一次 Full GC（这个是我们最需要减少的，因为耗时很严重）。

#### 4.5.2. 为什么有两个 Survivor 区
因为新生代内存区域我们使用了复制算法，而使用复制算法的目的，也是为了消除内存碎片。  

新建的对象放到 Eden 中，一旦 Eden 满了，触发 Minor GC，Eden 中的存活对象就会被移动到Survivor 区。下一次 Eden 满了的时候，再进行Minor GC，Eden 和 Survivor 各有一些存活对象，如果只有一个 Survivor，Eden 第二次的 GC 的存活对象也是放在唯一的一个 Survivor 区域中。但此时把 Eden 区的存活对象硬放到 Survivor 区，很明显这两部分对象所占有的内存是不连续的，也就导致了内存碎片化。

#### 4.5.3. 相关参数
```Java
-Xms20m  设置堆最小内存20MB
-Xmx20M  设置堆最大内存20MB
当-Xms和-Xmx值相同表示不允许堆内存进行扩展

-Xmn5m  表示新生代内存为5MB
-XX:NewRatio=3  表示新生代占堆内存1/3
-XX:SurvivorRatio=8  表示Eden:2个Survivor = 8:2
```

### 4.6. Minor GC 和 Full GC
- Minor GC（MGC 也叫 YGC）：回收新生代，因为新生代对象存活时间很短，因此会频繁执行，速度较快
- Full GC（也叫 Major GC ，FGC）：回收老年代和新生代，老年代对象存活时间长，因此 Full GC 很少执行，
执行速度会比 Minor GC 慢很多

### 4.7. Full GC 触发条件
- 调用 System.gc()
- 空间分配担保失败
- JDK1.7 以前的永久代空间不足


## 5. JVM 问题和调优
### 5.1. 内存泄漏和内存溢出的区别
- 内存溢出(out of memory)：指程序在申请内存时，没有足够的内存空间供其使用，出现 out of memory。
- 内存泄露(memory leak)：指程序在申请内存后，无法释放已申请的内存空间，内存泄露堆积会导致内存被占光。(静态集合类、各类数据库和网络连接用完不关闭、内部类持有外部类、改变哈希值)
- memory leak 最终会导致 out of memory。

### 5.2. OOM相关
##### 5.2.1. 堆溢出
- 1)内存泄漏（Memory Leak）：使用工具查看泄漏对象到 GC ROOTS 的引用链，找到泄漏对象是通过怎么样的路径与 GC Roots 相关联并导致垃圾收集器无法自动回收他们，准确地定位出泄漏代码的位置。
- 2)内存溢出(Memory overflow)：如果不是内存泄漏，换句话说，就是内存中的对象确实都还必须活着，那就应当检查虚拟机的堆参数（-Xmx 与 -Xms），与机器物理内存对比看是否还可以调大，从代码上检查是否存在某些对象生命周期过长、持有状态时间过长的情况，尝试减少程序运行期的内存消耗。
##### 5.2.2. 栈内存溢出（-Xss）
- 1)如果线程请求的深度大于虚拟机所允许的最大深度，将抛出 StackOverflowError 异常。如果栈的深度小或者栈针的容量比较大、用递归时，都可能引起。
- 2)如果是虚拟机在扩展时无法申请到足够的内存空间，则抛出 OutOfMemoryError 异常。当使用多线程的时候，需要注意。
##### 5.2.3. 方法区和运行时常量池溢出（-XX:PermSize -XX:MaxPermSize）
- 1)常量池中存放大量的 String 对象，并保持对这些对象的引用，避免 Full GC 回收常量池，就会产生 OutOfMemoryError 异常，后面跟的提示信息是“PermGen space”,说明运行时常量池属于方法区。
- 2)方法区用于存放 Class 的相关信息，如类名、访问修饰符、常量池、字段描述、方法描述等。当产生大量的类去填充满方法区，就会溢出
- 3)Jdk1.8之后方法区由元空间替代，字符串常量池和类静态变量都放到堆中了，因为不好指定大小和容易内存溢出，增加GC复杂度，回事效率低
##### 5.2.4. 本机直接内存溢出（-MaxDirectMemorySize）
DirectMemory 容量可通过 MaxDirectMemorySize 指定，如果不指定，则默认与 Java 堆最大值一样。虽然 DirectMemory 内存溢出时也会抛出内存溢出异常，但它抛出的异常时并没有真正向操作系统申请内存分配，于是手动抛出异常。一个明显的特征是在 Heap Dump 文件中不会看见明显的异常，如果发现 OOM 之后 Dump 文件很小，而且程序中又直接或者间接使用了 NIO，那就可以考虑检查一下是不是这方面的原因。

### 5.3. OOM 常见原因
- 内存加载的数据量太大，一次性从数据库获取太多数据
- 集合类中有对对象的引用，使用后未清空， GC 不能回收
- 代码存在循环产生过多的重复对象
- 启动参数堆内存太小

### 5.4. 各类 OOM 和解决方法
- Java堆空间
	- 原因：无法在 Java 堆中分配对象；应用程序无意中保存了对象引用，对象无法被 GC 回收；应用程序过度使用 finalizer。finalizer 对象不能被 GC 立刻回收。finalizer 由结束队列服务的守护线程调用，有时 finalizer 线程的处理能力无法跟上结束队列的增长
	- 解决：使用 -Xmx 增加堆大小；修复应用程序中的内存泄漏
- GC 开销超过限制
	- 原因：Java 进程98%的时间在进行垃圾回收，恢复了不到2%的堆空间，最后连续5个（编译时常量）垃圾回收一直如此。
	- 解决：使用 -Xmx 增加堆大小;使用 -XX:-UseGCOverheadLimit 取消 GC 开销限制;修复应用程序中的内存泄漏
- Requested array size exceeds VM limit 应用程序试图分配一个大于堆大小的数组
	- 原因：应用程序试图分配一个超过堆大小的数组
	- 解决：使用 -Xmx 增加堆大小;修复应用程序中分配巨大数组的 bug
- Perm gen 空间
	- 原因：当 Perm gen 空间用尽时，将抛出异常。Perm gen 空间包含：类的名字、字段、方法；与类相关的对象数组和类型数组；JIT 编译器优化
	- 解决：使用 -XX: MaxPermSize 增加 Permgen 大小；不重启应用部署应用程序可能会导致此问题。重启 JVM 解决
- Metaspace 元空间
	- 原因：从 Java 8 开始 Perm gen 改成了 Metaspace，在本机内存中分配 class 元数据（称为 metaspace）。如果 metaspace 耗尽，则抛出异常
	- 解决：通过命令行设置 -XX: MaxMetaSpaceSize 增加 metaspace 大小；取消 -XX: maxmetsspacedize；减小 Java 堆大小,为 MetaSpace 提供更多的可用空间；为服务器分配更多的内存；修复bug
- unable to create new native thread 无法新建本机线程
	- 原因：内存不足，无法创建新线程。由于线程在本机内存中创建，报告这个错误表明本机内存空间不足
	- 解决：将 heap 及 perm 的最大值下调，并将线程栈内存 -Xss 调小；修复应用程序中的线程泄漏；增加操作系统级别的限制
`ulimit -a`；用户进程数增大 (-u) 1800；使用 -Xss 减小线程堆栈大小
- 杀死进程或子进程
	- 原因：内核任务在可用内存极低的情况下会杀死进程
	- 解决：将进程迁移到不同的机器上；给机器增加更多内存；与其他 OOM 错误不同，这是由操作系统而非 JVM 触发的
- 发生 stack_trace_with_native_method
	- 原因：本机方法（native method）分配失败；打印的堆栈跟踪信息，最顶层的帧是本机方法
	- 解决：使用操作系统本地工具进行诊断

### 5.5. JVM 调优
JVM调优是比较高深的学问，包括设置合理的内存参数，选择合理垃圾回收器甚至修改 JVM 代码等等。在一般项目中很少会去做具体调优。比较常用简单的优化：
- 堆设置合理的-Xmx 和-Xms大小，一般两个值设为一样，避免每次 GC 后调整堆的大小；
- XX:NewSize：新生代大小
- XX:NewRatio 设置新生代和老年代比例；
- 开启 GC 日志，查看 GC 情况，排查解决 Full GC 频繁原因；
- 使用  Jconsole 监控工具监控线程和堆空间分配。

### 5.6. 调优命令
Sun JDK监控和故障处理命令有 jps jstat jmap jhat jstack jinfo
- jps，JVM Process Status Tool，显示指定系统内所有的 HotSpot 虚拟机进程；
- jstat，JVM statistics Monitoring，用于监视虚拟机运行时状态信息的命令，它可以显示出虚拟机进程中的类装载、内存、垃圾收集、JIT 编译等运行数据；
- jmap，JVM Memory Map 命令用于生成 heap dump 文件；
- jhat，JVM Heap Analysis Tool 命令是与 jmap 搭配使用，用来分析 jmap 生成的 dump 文件，jhat 内置了一个微型的 HTTP/HTML 服务器，生成 dump 的分析结果后，可以在浏览器中查看；
- jstack，用于生成java虚拟机当前时刻的线程快照；
- jinfo，JVM Configuration info 这个命令作用是实时查看和调整虚拟机运行参数。

### 5.7. 调优工具
常用调优工具分为两类，JDK 自带监控工具：jconsole 和 jvisualvm，第三方有：MAT(Memory Analyzer Tool)、GChisto。
- jconsole，Java Monitoring and Management Console 是从 Java5 开始，在 JDK 中自带的 Java 监控和管理控制台，用于对JVM中内存，线程和类等的监控;
- jvisualvm，JDK 自带全能工具，可以分析内存快照、线程快照；监控内存变化、GC 变化等;
- MAT，Memory Analyzer Tool，一个基于Eclipse的内存分析工具，是一个快速、功能丰富的Java heap分析工具，它可以帮助我们查找内存泄漏和减少内存消耗;
- GChisto，一款专业分析gc日志的工具。