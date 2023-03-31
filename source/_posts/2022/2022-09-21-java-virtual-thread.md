---
title: 简单了解下JDK19预览版的 Virtual Threads
categories: 技术
tags:
  - 技术
  - 协程
  - Java
toc: true
date: 2022-09-21
---

最近看到JDK19发布了，拖了这么多年终于加入了虚拟线程功能，目前还是预览阶段，[OpenJDK网站](https://openjdk.org/jeps/425)上有详细的介绍，来先看看 Java 版的协程是怎么样的。

## 设计目标和解决的问题

虚拟线程是作为轻量级线程使用，以显著减少编写和维护并发程序的工作量。

### 设计目标
目标：
- 能够以简单的每个线程一个线程的风格来编写服务端应用，获得最佳的硬件利用率；
- 在已有的 `java.lang.Thread` API 做扩展修改，做到最少修改；
- 使用现有JDK工具能对虚拟线程进行故障排除、调试和分析。

非目标：
- 不是为了移除传统的线程实现，或者静默迁移现有应用程序使用虚拟线程；
- 不改变 Java 的基本并发模型；
- 不是为了在 Java 语言和库中提供一个新的数据并行结构处理工具，Stream API 仍然是并行处理大型数据集的首选方式。

### 线程池和异步线程的问题

在程序中使用线程，特别是需要创建大量的线程，每个线程有占用一定的资源（约512K～1M的空间），线程的上下文切换代价也比较大，所以使用线程池可以复用线程，限制无限使用系统的资源。

而对于需要提高系统吞吐量使用异步线程，编码将变得复杂，尤其是需要返回值编写回调函数的情况（回调地狱），而且跟踪调试困难。Java8 引入的 CompletableFuture 响应式接口在一定程度上改善了 Future 异步编程的回调问题，可组合的链式调用方式也使得编码逻辑更清晰。但是异步请求涉及多个线程和调试困难问题依旧灭解决。

针对以上的问题，再来看使用虚拟线程的优点：
- 对比线程池，由于虚拟线程非常轻量级，我们可以随意创建成千上万的虚拟线程而不耗费很多系统资源，每个虚拟线程只在本身生命周期完成单一任务，所以也完全没必要池化虚拟线程。

- 对于异步编程，虚拟线程同样具有响应式编程的特点，不会阻塞等待响应，并且降低编码和调试分析难度。

此外，我们知道各种的语言的协程不管怎么实现，实际上都是为了针对IO堵塞的场景能够有轻量高效的方法处理大量并发任务，即协程适用于IO密集型任务，对于CPU 密集型任务则无用。Java 在原本没有协程实现的时候用的是 netty 这类三方IO多路复用框架来解决问题，在系统层面上，IO多路复用单一线程就可以管理大量的 socket；在程序语言层面，创建大量的虚拟线程也同样只用到少量线程，两者解决方法的思路相似。

下面看具体的API看看虚拟线程是如何使用的。

## 相关API

先下载 JDK19，由于虚拟线程还是预览版功能，所以编译和运行程序都要带上相关参数才行，比如编译 `com.zguishen` 包下的 `VirtualThreadTest.java` 文件。

```bash
javac -d . --enable-preview -source 19 VirtualThreadTest.java
java --enable-preview com.zguishen.VirtualThreadTest
```

如果使用 IDEA，如需设置两个地方，一是 Setting-Build，Execution，Deployment-Compiler-Java Compiler 中，Project bytecode version 直接填19，Override compiler parameters per-module 添加工程，Compilation options 参数设置为`--enable-preview --source 19`；二是运行的 VM Options 也要添加参数 `--enable-preview`，嫌每个类方法运行都要添加麻烦，就直接在 Run/Debug Configuration Templates 添加。

### Thread类

- `Thread.ofVirtual()` 创建一个虚拟线程，`Thread.ofPlatform()` 创建一个平台线程；
- `isVirtual()` 函数判断是否为虚拟函数；
- `Thread.startVirtualThread()` 创建并启动虚拟线程。

```java
@Test
public void virtualVsPlatformTest() {
    Thread vt = Thread.ofVirtual().unstarted(() -> {
        System.out.println("this is a virtual thread.");
    });
    vt.start();

    Thread dv = new Thread(() -> {
        System.out.println("default platform thread.");
    });
    dv.start();
    Thread pv = Thread.ofPlatform().unstarted(() -> {
        System.out.println("this is a platform thread.");
    });
    pv.start();

    System.out.printf("is virtual?: %s %s %s %n", vt.isVirtual(), dv.isVirtual(), pv.isVirtual());
    
    Thread.startVirtualThread(() -> {
        System.out.println("this is a another virtual thread.");
    });
}
```

### Executors类

`Executors.newVirtualThreadPerTaskExecutor()` 创建任务线程。

```java
@Test
public void executorsExpTest() {
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        executor.submit(() -> {System.out.println("virtual thread test.");});
        //executor.close(); 
        //try-with-resources会隐式调用close
    }
}
```

写一个模拟任务跟传统线程池做对比。
```java
@Test
public void contrastTest() {
    long s1 = System.currentTimeMillis();
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        task(executor);
    }
    long s2 = System.currentTimeMillis();
    System.out.printf("虚拟线程耗时:%sms %n", s2-s1);

    try (var executor = Executors.newCachedThreadPool()) {
        task(executor);
    }
    long s3 = System.currentTimeMillis();
    System.out.printf("无限制线程池耗时:%sms %n", s3-s2);

    try (var executor = Executors.newFixedThreadPool(300)) {
        task(executor);
    }
    long s4 = System.currentTimeMillis();
    System.out.printf("固定线程数量线程池耗时:%sms %n", s4-s3);
}

public void task(ExecutorService executor) {
    IntStream.range(0, 10_000).forEach(i -> {
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));
            return i;
        });
    });
}
```

结果：
```
虚拟线程耗时:1291ms 
无限制线程池耗时:2698ms 
固定线程数量线程池耗时:34042ms 
```

以上是创建10000个虚拟线程同时执行任务，休眠一秒钟，在现代硬件的操作系统上只需要少量线程就可以完成，执行时间也很快。

可以看到 `Executors.newVirtualThreadPerTaskExecutor()` 比使用固定大小的线程池 `Executors.newFixedThreadPool(300)` 或者线程数无限（实际上限是 `Integer.MAX_VALUE`）的线程池 `Executors.newCachedThreadPool()` 耗时明显变短，效率大大提高。

如果你用的是 Linux 系统，可以用 `top -H -d 0.5` 观察线程数的变化，使用虚拟线程线程数基本没变化，使用没限制的线程池将会至少创建多几千个线程，内存占用也有所增加，使用固定线程池会多出几百个线程。

## 虚拟线程调度

JDK 的虚拟线程调度程序是一个 work-stealing ForkJoinPool，它以 FIFO 模式运行。调度器并行数量等于虚拟线程平台线程数，默认是CPU核心数量。虚拟线程的 ForkJoinPool 和普通的 ForkJoinPool.commonPool()不同，后者用于并行流（Stream），以 LIFO 模式运行。

JDK 的调度程序不是直接将虚拟线程分配给处理器，而是将虚拟线程分配给平台线程，即虚拟线程的 M:N 调度，大量（M）虚拟线程被调度到较少数量（N）的操作系统线程上运行。

先看一段程序：
```java
@Test
public void schedulerTest() {
    try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
        //业务代码...
        System.out.println("create virtual thread to run task.");
        for (int i = 0; i < 5; i++) {
            int finalI = i;
            Future<Integer> future = executor.submit(() -> {
                System.out.printf("i:%s, thread:%s %n", finalI, Thread.currentThread());
                Thread.sleep(Duration.ofMillis(30));
                System.out.printf("i:%s, thread:%s %n", finalI, Thread.currentThread());
                return 1;
            });
        }
    }
}
```

输出
```
create virtual thread to run task.
i=0, thread:VirtualThread[#21]/runnable@ForkJoinPool-1-worker-1 
i=3, thread:VirtualThread[#25]/runnable@ForkJoinPool-1-worker-2 
i=1, thread:VirtualThread[#23]/runnable@ForkJoinPool-1-worker-3 
i=4, thread:VirtualThread[#26]/runnable@ForkJoinPool-1-worker-4 
i=2, thread:VirtualThread[#24]/runnable@ForkJoinPool-1-worker-4 
i=0, thread:VirtualThread[#21]/runnable@ForkJoinPool-1-worker-2 
i=3, thread:VirtualThread[#25]/runnable@ForkJoinPool-1-worker-1 
i=1, thread:VirtualThread[#23]/runnable@ForkJoinPool-1-worker-2 
i=4, thread:VirtualThread[#26]/runnable@ForkJoinPool-1-worker-4 
i=2, thread:VirtualThread[#24]/runnable@ForkJoinPool-1-worker-4
```

可以看到 VirtualThread 后面的数字是虚拟线程 id，虚拟线程可以大量创建；worker 后面的的 id 数表示平台线程，不会超过 CPU 核心数。

再看 i=0 对应的信息，延时前后的虚拟线程 id 相同，但 worker 已经不同的，虚拟线程在IO堵塞时会从平台线程上卸载，保存堆栈信息，当阻塞操作完成时调度器会重新挂载，还原现场，不过重新挂载到的平台线程可能不是之前的同一个。

不过，有一些堵塞操作在堵塞期间，JDK 无法将虚拟线程从平台线程卸载的，这将严重影响性能，比如以下两种情况：
- 在 synchronized 代码块或方法中执行；
- 在本地方法和外部函数（Foreign Function，也是JDK的预览功能，允许 Java 程序与 JVM 运行时之外的代码和数据互操作）中执行。

很不幸的是，JDBC 的 API 也用到了 synchronized，但是平常业务有离不开涉及数据库的操作。对于以上情况，synchronized 可以用 ReentrantLock 来代替；修改系统参数最大平台线程数`jdk.virtualThreadScheduler.maxPoolSize`，设置超过处理器数量的平台线程数，保证有足够的平台线程可用。


## 与其他语言的协程对比

### Python

Python 对协程的支持是通过 generator 实现的，之前写过一篇[笔记](https://zguishen.com/posts/6ea62067.html)。

### Golang

最近在学 Go，Go 里面的协程用起来更加简单，只要在函数前加个 go 关键字就行，配合通道（channel）和多路复用器（select）的玩法用起来也很简便。

之前在推特上看到的一道面试题，考察的内容是典型竞态检测，涉及协程、通道和多路复用器的运用。

```go
func TestGoroutines(t *testing.T) {
    rand.Seed(time.Now().UnixNano())
    // context 设置1秒超时
    ctx, cancel := context.WithTimeout(context.Background(), time.Second)
    defer cancel()
    
    foo(ctx)
}

//只能编辑foo函数，foo函数必须调用slow函数；
//foo函数在ctx超时后必须立刻返回，如果slow结束比ctx快，也立刻返回
func foo(ctx context.Context) {
}

// slow 函数模拟任务
func slow() {
    // 随机延时[0,3)
    n := rand.Intn(3)
    fmt.Printf("sleep %ds\n", n)
    time.Sleep(time.Second * time.Duration(n))
}
```

下面是一个解法，当 slow 任务大于1秒，多路复用器会先收到 context 的超时事件，返回结束；当 slow 任务小于1秒，多路复用器会先收到数据1，正常返回结束。
```go
func foo(ctx context.Context) {
    ch := make(chan int, 1)
    // 协程异步执行slow任务，完成写通道
    go func(ctx context.Context) {
    	slow()
    	ch <- 1
    }(ctx)
    
    // 多路复用器检测通道两个事件，
    // 一个是context的超时事件，一个是数据写入事件
    select {
    case <-ctx.Done():
    	return
    case <-ch:
    	return
    }
}
```

不同编程语言的协程在实现方法和语法上有所差异，但目的不外乎都是为了能简化编码，用同步的思维写异步程序，减少线程的上下文切换和内存开销等等。

## 参考

1和3是更详细的参考文章。

- [1] [JEP 425: Virtual Threads (Preview)](https://openjdk.org/jeps/425)
- [2] [Enable "preview" features in an early-access version of Java in IntelliJ](https://stackoverflow.com/questions/72083752/enable-preview-features-in-an-early-access-version-of-java-in-intellij)
- [3] [Java19 正式 GA！看虚拟线程如何大幅提高系统吞吐量](https://developer.aliyun.com/article/1026412#slide-3)
- [4] [Golang 面试题](https://twitter.com/ezogreatagain/status/1480377334595133443?s=20&t=Y5YDWPSVcfxp6iJqhmoS2g)
