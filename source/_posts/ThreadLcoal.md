---
title: ThreadLcoal
categories: 技术
tags: Java基础
date: 2017-07-01
---
ThreadLcoal不是线程，而是一个创建线程的局部变量的类，主要用于存储多线程下类的某些变量，ThreadLocal为每个使用该变量的线程提供独立的变量副本，当前线程的ThreadLocal的变量只能被该线程访问，而其他线程访问不到。
<!--more-->
__使用__
类定义，支持泛型
`public class ThreadLocal<T>`
初始化值
`private T setInitialValue()`
set方法
`public void set(T value)`
get方法
`public T get()`

__例子__
```java
public class Test04 {
    
    private ThreadLocal<Integer> local = new ThreadLocal<>();
    int i=0;
    
    class localTread implements Runnable{
        public void setNum(){
            local.set(i++);
        }
        public Integer getNum(){
            return local.get();
        }
        @Override
        public void run() {
            if(local.get() == null){
                setNum();
                System.out.println("set threadlocal num...");
            }
            System.out.print("the object is: ");
            System.out.println(local);
            System.out.println(local.get());
        }
    }
    
    public static void main(String[] args) {
        try {
            localTread t = new Test04().new localTread();
            
            Thread t1 = new Thread(t);
            Thread t2 = new Thread(t);
            Thread t3 = new Thread(t);
            
            t1.start();
            Thread.sleep(1000);
            t2.start();
            Thread.sleep(1000);
            t3.start();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
    }
}
```
输出
```
set threadlocal num...
the object is: java.lang.ThreadLocal@6b2ce86d
0
set threadlocal num...
the object is: java.lang.ThreadLocal@6b2ce86d
1
set threadlocal num...
the object is: java.lang.ThreadLocal@6b2ce86d
2
```

可以看到三个线程访问的都是同一个ThreadLocal，但只能访问当前线程存储的各自的变量。
看源码set方法的实现
```java
public void set(T value) {
	Thread t = Thread.currentThread();
	ThreadLocalMap map = getMap(t);
	if (map != null)
		map.set(this, value);
	else
		createMap(t, value);
}
```
通过获取当前线程，再ThreadL中，ThreadLocalMap用弱引用实现
get方法实现
```java
public T get() {
	Thread t = Thread.currentThread();
	ThreadLocalMap map = getMap(t);
	if (map != null) {
		ThreadLocalMap.Entry e = map.getEntry(this);
		if (e != null) {
			@SuppressWarnings("unchecked")
			T result = (T)e.value;
			return result;
		}
	}
	return setInitialValue();
}
```

同样是为了解决多线程中变量冲突的问题，线程同步机制实现在某个时间点只有一个线程能访问变量，而ThreadLcoal是通过存储每个线程自己变量，以隔离多线程访问数据的冲突，一个损耗时间，一个损耗空间。


