---
title: Java 简介和开发环境
categories: 技术
tags: Java基础
date: 2016-07-01
---
一、定义与特点
定义：Java是一门面向对象编程语言，不仅吸收了C++语言的各种优点，还摒弃了C++里难以理解的多继承、指针等概念，因此Java语言具有功能强大和简单易用两个特征。Java语言作为静态面向对象编程语言的代表，极好地实现了面向对象理论，允许程序员以优雅的思维方式进行复杂的编程。[Java疯狂讲义]
特点：主要特点是面向对象和可移植等等，广泛应用于web应用程序(JavaEE相关)、嵌入式(安卓相关)，桌面程序、分布式系统等等。<!--more-->
二、开发工具和开发环境
JDK：Java开发包或Java开发工具，编写Java程序必须，已包含JRE。
JRE：Java运行环境，运行编写完毕的Java程序。
JDK的安装(Windows系统,Java8)
1、首先到oracle官网下载与计算机系统对应的Java SE的JDK即可。
2、安装、配置环境变量
配置JAVA_HOME的环境变量：
新建JAVA_HOME一个变量，路径为JDK的安装路径，指定到jdk文件夹
![这里写图片描述](http://img.blog.csdn.net/20160701013707829)
jdk的版本是1.8，在1.6版本之后的jdk都不必配置classpath环境变量了。
3、基本命令
win+r运行cmd，输入java命令，可以看到各种选项命令
![这里写图片描述](http://img.blog.csdn.net/20160703095547077)

输入java -version可以看到当前安装的jdk版本信息
![这里写图片描述](http://img.blog.csdn.net/20160701014317597)

javac命令，各种编译选项
![这里写图片描述](http://img.blog.csdn.net/20160703095933655)
三、基本数据类型
1、Java有八种基本数据类型，包括byte字节类型、int整形、short短整形、long长整形、char字符型、float浮点型(单精度)、double双精度类型、boolean布尔型。
2、基本知识
一个字节等于8位，一个字节等于256个数，就是-128到127一共256。
kB就是kBytes 
Bytes就是“字节”的意思！ 
K就是千的意思，因为计算机是通过二进制来计算，10个1正好是1024
1111111111（二进制）=1024（十进制）
1Bytes（字节）=8bit（比特）
一个英文字母或一个阿拉伯数字就是一个字符，占用一个字节
一个汉字就是两个字符，占用两个字节。
3、数据类型转换
byte->short
char->int->long
float->double
int->float
long->double
范围小的转到范围大的
范围大的转换到范围小的会失去精度